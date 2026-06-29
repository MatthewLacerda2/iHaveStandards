"""Async database engine, session factory, and bootstrap routine.

`init_db()` is the only place outside `repositories/` that issues SQL, and it
does so purely as an application-bootstrap step (table creation, admin seed).
Schema upgrades beyond additive `create_all` should go through Alembic; this
skeleton intentionally ships no migrations. SQLite's limited `ALTER TABLE`
makes that upgrade matter sooner than it would on a server database.
"""

from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import get_settings
from models.base import Base


def normalize_database_url(url: str) -> str:
    """Coerce a driverless SQLite URL to the async aiosqlite form.

    Accepts a plain `sqlite://` URL and rewrites it to `sqlite+aiosqlite://`.
    URLs that already name a driver are returned unchanged.
    """
    if url.startswith("sqlite+"):
        return url
    if url.startswith("sqlite://"):
        return "sqlite+aiosqlite://" + url[len("sqlite://") :]
    return url


def configure_sqlite(async_engine: AsyncEngine) -> None:
    """Make SQLite behave correctly for this app. No-op for other dialects.

    Two adjustments, both applied per connection:

    * **Enforce foreign keys.** SQLite ignores constraints (and `ON DELETE`
      cascades) unless `PRAGMA foreign_keys=ON` is set on every connection.
    * **Take over transaction control.** The pysqlite/aiosqlite driver otherwise
      emits its own `COMMIT` around `SAVEPOINT`s, which breaks nested savepoints
      and the test's rollback-per-test recipe. Disabling the driver's implicit
      transactions and emitting `BEGIN` ourselves is SQLAlchemy's documented fix.
    """
    if async_engine.dialect.name != "sqlite":
        return

    sync_engine = async_engine.sync_engine

    @event.listens_for(sync_engine, "connect")
    def _setup_connection(dbapi_connection: object, _record: object) -> None:
        # Hand transaction control to SQLAlchemy (disable the driver's autobegin).
        dbapi_connection.isolation_level = None
        # Enforce foreign keys; runs in autocommit since we control BEGIN.
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @event.listens_for(sync_engine, "begin")
    def _emit_begin(conn: object) -> None:
        conn.exec_driver_sql("BEGIN")


_settings = get_settings()
DATABASE_URL = normalize_database_url(_settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL, future=True)
configure_sqlite(engine)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Bootstrap the database: tables, default admin."""
    # Import models so their tables are registered on `Base.metadata`.
    import models  # noqa: F401

    async with engine.begin() as conn:
        # Additive only. Alembic is the upgrade path for non-additive changes.
        await conn.run_sync(Base.metadata.create_all)

    await _seed_default_admin()


async def _seed_default_admin() -> None:
    """Create the default admin user if no user exists yet."""
    from models.user import User
    from utils.security import hash_password

    settings = get_settings()
    async with SessionLocal() as session:
        existing = await session.scalar(select(User).limit(1))
        if existing is not None:
            return
        admin = User(
            email=settings.DEFAULT_ADMIN_EMAIL,
            password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
            is_active=True,
        )
        session.add(admin)
        await session.commit()
