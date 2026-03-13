from .migration import migrate
from .models import db

DB_PATH = "data/clinica.db"


def connect_db():
    db.init(DB_PATH, pragmas={"foreign_keys": 1, "journal_mode": "wal"})
    db.connect()
    migrate(db)
