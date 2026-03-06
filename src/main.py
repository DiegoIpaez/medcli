import os

from .database.connection import connect_db, db
from .menus.app.app_menu import menu_principal
from .ui.mensajes import error, info


def main():
    try:
        os.makedirs("data", exist_ok=True)
        connect_db()
        menu_principal()
    except KeyboardInterrupt:
        info("Saliendo de la aplicación...")
    except Exception as err:
        error(f"Ocurrió un error inesperado: {err}")
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()
