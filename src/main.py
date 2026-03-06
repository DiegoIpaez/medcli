import os

from .database.connection import connect_db, db
from .menus.app.app_menu import menu_principal


def main():
    os.makedirs("data", exist_ok=True)
    connect_db()
    try:
        menu_principal()
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()
