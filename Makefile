# Single task runner. CI invokes these exact targets so local and CI never drift.
# PYTHON auto-uses backend/.venv when present (after `make back-install`), so local
# runs need no flag. CI overrides it explicitly: make backend PYTHON=python

PYTHON ?= $(shell [ -x backend/.venv/bin/python ] && echo .venv/bin/python || echo python3.12)
BUN    ?= bun

.DEFAULT_GOAL := check

# ---------------------------------------------------------------------------
# Aggregate gates
# ---------------------------------------------------------------------------
.PHONY: check backend frontend
check: backend frontend

backend: back-lint back-build back-test
frontend: front-lint front-build front-test

# ---------------------------------------------------------------------------
# Run the app locally (backend + frontend together; Ctrl-C stops both)
# ---------------------------------------------------------------------------
.PHONY: dev
dev:
	@[ -x backend/.venv/bin/python ] || { echo "Backend not installed — run 'make back-install' first."; exit 1; }
	@[ -d frontend/node_modules ] || { echo "Frontend not installed — run 'make front-install' first."; exit 1; }
	@echo "Backend  -> http://localhost:8000"
	@echo "Frontend -> http://localhost:5173   (Ctrl-C stops both)"
	@trap 'kill 0' INT TERM EXIT; \
	( cd backend && $(PYTHON) -m uvicorn main:app --reload ) & \
	( cd frontend && $(BUN) run dev ) & \
	wait

# ---------------------------------------------------------------------------
# Backend gates  (run from backend/, driven by $(PYTHON))
# ---------------------------------------------------------------------------
.PHONY: back-lint back-build back-test back-install
back-lint:
	cd backend && $(PYTHON) -m ruff check .
	cd backend && $(PYTHON) -m ruff format --check .
	cd backend && $(PYTHON) tools/house_lint.py

back-build:
	cd backend && $(PYTHON) -c "import main"

back-test:
	cd backend && $(PYTHON) -m pytest

back-install:
	cd backend && python3.12 -m venv .venv
	cd backend && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt

# ---------------------------------------------------------------------------
# Frontend gates  (run from frontend/, driven by $(BUN))
# ---------------------------------------------------------------------------
.PHONY: front-lint front-build front-test front-install
front-lint:
	cd frontend && $(BUN) run check

front-build:
	cd frontend && $(BUN) run build

front-test:
	cd frontend && $(BUN) run test

front-install:
	cd frontend && $(BUN) install
