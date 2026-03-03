DB      = clinica.db
PYTHON  = poetry run python

help:
	@echo ""
	@echo "  Comandos disponibles:"
	@echo ""
	@echo "  make install   Instala dependencias con Poetry"
	@echo "  make run       Muestra todos los datos"
	
	@echo ""

install:
	poetry install

run:
	$(PYTHON) -m src.main