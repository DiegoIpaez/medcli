from .models import db

TURNOS_SPECIFIC_TRIGGERS = [
    """
    CREATE TRIGGER IF NOT EXISTS trg_turnos_duracion_entre_turno
    AFTER INSERT ON turnos WHEN NEW.entre_turno = 1
    BEGIN UPDATE turnos SET duracion_min = 5 WHERE id = NEW.id; END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS trg_turnos_conflicto_medico_insert
    BEFORE INSERT ON turnos
    WHEN NEW.entre_turno = 0 AND EXISTS (
        SELECT 1 FROM turnos WHERE medico_id = NEW.medico_id 
        AND fecha = NEW.fecha AND horario = NEW.horario 
        AND estado != 'CANCELADO' AND entre_turno = 0)
    BEGIN SELECT RAISE(ABORT, 'Médico ocupado'); END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS trg_turnos_conflicto_paciente_insert
    BEFORE INSERT ON turnos
    WHEN NEW.entre_turno = 0 AND EXISTS (
        SELECT 1 FROM turnos WHERE paciente_id = NEW.paciente_id 
        AND fecha = NEW.fecha AND horario = NEW.horario 
        AND estado != 'CANCELADO' AND entre_turno = 0)
    BEGIN SELECT RAISE(ABORT, 'Paciente ocupado'); END;
    """,
]


def crear_timestamp_triggers(tables):
    """Crea triggers genéricos de created_at/updated_at para múltiples tablas"""
    created_sql = """
    CREATE TRIGGER IF NOT EXISTS trg_{table}_created_at
    BEFORE INSERT ON {table}
    WHEN NEW.created_at IS NULL OR NEW.created_at = ''
    BEGIN
        UPDATE {table} SET created_at = datetime('now', 'localtime') 
        WHERE rowid = NEW.rowid;
    END;
    """

    updated_sql = """
    CREATE TRIGGER IF NOT EXISTS trg_{table}_updated_at
    AFTER UPDATE ON {table}
    WHEN NEW.updated_at = OLD.updated_at OR NEW.updated_at IS NULL
    BEGIN
        UPDATE {table} SET updated_at = datetime('now', 'localtime') 
        WHERE id = NEW.id;
    END;
    """

    for table in tables:
        db.execute_sql(created_sql.format(table=table))
        db.execute_sql(updated_sql.format(table=table))


def crear_turnos_triggers():
    """Crea triggers específicos de negocio para turnos"""
    for trigger_sql in TURNOS_SPECIFIC_TRIGGERS:
        db.execute_sql(trigger_sql)
