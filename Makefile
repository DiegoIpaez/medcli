DB      = clinica.db
PYTHON  = poetry run python
RUFF    = poetry run ruff

help:
	@echo ""
	@echo "  Comandos disponibles:"
	@echo ""
	@echo "  make install   Instala dependencias con Poetry"
	@echo "  make run       Ejecuta la aplicación"
	@echo "  make lint      Analiza el código con Ruff"
	@echo "  make format    Formatea el código con Ruff"
	@echo "  make fix       Corrige problemas automáticamente"
	@echo "  make check     Ejecuta lint + format check"
	@echo ""

install:
	poetry install

run:
	$(PYTHON) -m src.main

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

fix:
	$(RUFF) check . --fix

check:
	$(RUFF) check .
	$(RUFF) format . --check