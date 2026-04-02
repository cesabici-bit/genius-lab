# Makefile — NuclearMind
# Target principale: `make check-all` esegue TUTTI i controlli in sequenza.
# Se uno fallisce, i successivi NON vengono eseguiti.

.PHONY: check-all types lint test smoke deps clean

## check-all: Esegue tutti i controlli (deps, types, lint, test, smoke)
check-all: deps types lint test smoke
	@echo ""
	@echo "=== ALL CHECKS PASSED ==="
	@echo ""

# ============================================================
# Python targets
# ============================================================

## types: Type checking con mypy
types:
	@echo "--- Type checking (mypy) ---"
	mypy src/nuclearmind/ --ignore-missing-imports

## lint: Linting con ruff
lint:
	@echo "--- Linting (ruff) ---"
	ruff check src/ tests/

## test: Unit + integration tests
test:
	@echo "--- Tests (pytest) ---"
	pytest tests/ -v --ignore=tests/test_smoke.py -m "not openmc"

## smoke: Smoke test E2E (M3)
smoke:
	@echo "--- Smoke test E2E ---"
	pytest tests/test_smoke.py -v -s

# ============================================================
# Dependency verification (M1)
# ============================================================

## deps: Verifica che verified-deps.toml esista e non sia vuoto
deps:
	@echo "--- Checking verified-deps.toml ---"
	@test -f verified-deps.toml || (echo "ERROR: verified-deps.toml not found" && exit 1)
	@grep -c '^\[\[dependency\]\]' verified-deps.toml > /dev/null || (echo "ERROR: no dependencies in verified-deps.toml" && exit 1)
	@echo "verified-deps.toml found with $$(grep -c '^\[\[dependency\]\]' verified-deps.toml) dependencies"

# ============================================================
# OpenMC-specific targets (richiede OpenMC installato)
# ============================================================

## test-openmc: Test che richiedono OpenMC
test-openmc:
	@echo "--- OpenMC tests ---"
	pytest tests/ -v -m "openmc"

## generate-data: Genera dataset con OpenMC
generate-data:
	@echo "--- Generating dataset ---"
	python scripts/generate_dataset.py

# ============================================================
# Utility
# ============================================================

## clean: Rimuovi artefatti
clean:
	@echo "Cleaning build artifacts..."
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	rm -rf src/nuclearmind/__pycache__ src/nuclearmind/**/__pycache__
	rm -rf dist/ build/ *.egg-info
	find . -name "*.pyc" -delete 2>/dev/null || true

## help: Mostra i target disponibili
help:
	@grep -E '^## ' Makefile | sed 's/## //'
