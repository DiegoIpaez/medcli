DB      = clinica.db
PYTHON  = poetry run python
RUFF    = poetry run ruff

help:
	@echo ""
	@echo "  Comandos disponibles:"
	@echo ""
	@echo "  make install   Instala dependencias y hooks de pre-commit"
	@echo "  make run       Ejecuta la aplicación"
	@echo "  make lint      Analiza el código con Ruff"
	@echo "  make format    Formatea el código con Ruff"
	@echo "  make fix       Corrige problemas automáticamente"
	@echo "  make check     Ejecuta lint + format check"
	@echo "  make hooks     Instala los hooks de pre-commit"
	@echo ""

install:
	poetry install
	poetry run pre-commit install

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

hooks:
	poetry run pre-commit install
