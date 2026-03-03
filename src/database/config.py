from .models import db
from .migration import migrate

DB_PATH = "data/clinica.db"


def init_db():
    """Inicialización inteligente y persistente"""
    db.init(DB_PATH, pragmas={"foreign_keys": 1, "journal_mode": "wal"})
    db.connect()

    try:
        migrate(db)
    except Exception as error:
        print(f"Error durante migración: {error}")
    finally:
        db.close()
