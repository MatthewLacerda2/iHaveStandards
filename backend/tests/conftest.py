"""Root test fixtures: per-worktree SQLite test DB + rollback-per-test sessions.

The test database is a SQLite file whose name is derived from the worktree path
(under the system temp dir) so parallel git worktrees never collide. The schema
is created once per process; each test runs inside an outer transaction that is
rolled back on teardown, so nothing persists between tests.
"""

import hashlib
import os
import subprocess
import tempfile

import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from core.database import configure_sqlite
from models.base import Base

# One-time guard so schema creation happens once per process even though the
# engine fixture is function-scoped (each test runs on its own event loop).
_DB_READY = False


def _repo_root() -> str:
    """Return the worktree root path used to derive the test DB name."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return os.getcwd()


def _test_db_path() -> str:
    """Derive a stable per-worktree SQLite file path in the temp dir."""
    digest = hashlib.sha1(_repo_root().encode()).hexdigest()[:12]
    return os.path.join(tempfile.gettempdir(), f"test_gs_{digest}.db")


@pytest_asyncio.fixture
async def engine():
    """Function-scoped engine bound to the per-worktree SQLite test database.

    aiosqlite connections are bound to the event loop that created them, so the
    engine is created per test (each test runs on its own loop). NullPool avoids
    reusing connections across loops. The schema is dropped and recreated once
    per process, guarded by ``_DB_READY``, so every run starts clean.
    """
    global _DB_READY
    url = f"sqlite+aiosqlite:///{_test_db_path()}"
    test_engine = create_async_engine(url, future=True, poolclass=NullPool)
    configure_sqlite(test_engine)
    if not _DB_READY:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        _DB_READY = True
    yield test_engine
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncSession:
    """Session joined to an outer transaction; rolled back after each test.

    Uses the SQLAlchemy "join an external transaction" recipe: a SAVEPOINT is
    restarted whenever the application code commits, so handler ``commit()``
    calls are isolated and the outer transaction's rollback discards everything.
    """
    connection = await engine.connect()
    transaction = await connection.begin()
    maker = async_sessionmaker(bind=connection, expire_on_commit=False, class_=AsyncSession)
    session = maker()
    await session.begin_nested()

    sync_session = session.sync_session

    @event.listens_for(sync_session, "after_transaction_end")
    def _restart_savepoint(sess, trans) -> None:
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    try:
        yield session
    finally:
        event.remove(sync_session, "after_transaction_end", _restart_savepoint)
        await session.close()
        if transaction.is_active:
            await transaction.rollback()
        await connection.close()
