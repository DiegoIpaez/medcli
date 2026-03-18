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
        AND estado_id != (SELECT id FROM turno_estados WHERE nombre = 'CANCELADO') 
        AND entre_turno = 0)
    BEGIN SELECT RAISE(ABORT, 'Médico ocupado'); END;
    """,
    """
    CREATE TRIGGER IF NOT EXISTS trg_turnos_conflicto_paciente_insert
    BEFORE INSERT ON turnos
    WHEN NEW.entre_turno = 0 AND EXISTS (
        SELECT 1 FROM turnos WHERE paciente_id = NEW.paciente_id 
        AND fecha = NEW.fecha AND horario = NEW.horario 
        AND estado_id != (SELECT id FROM turno_estados WHERE nombre = 'CANCELADO') 
        AND entre_turno = 0)
    BEGIN SELECT RAISE(ABORT, 'Paciente ocupado'); END;
    """,
]


def crear_timestamp_triggers(tables):
    """Crea triggers genéricos de creado_el/actualizado_el para múltiples tablas"""
    created_sql = """
    CREATE TRIGGER IF NOT EXISTS trg_{table}_creado_el
    BEFORE INSERT ON {table}
    WHEN NEW.creado_el IS NULL OR NEW.creado_el = ''
    BEGIN
        UPDATE {table} SET creado_el = datetime('now', 'localtime') 
        WHERE rowid = NEW.rowid;
    END;
    """

    updated_sql = """
    CREATE TRIGGER IF NOT EXISTS trg_{table}_actualizado_el
    AFTER UPDATE ON {table}
    WHEN NEW.actualizado_el = OLD.actualizado_el OR NEW.actualizado_el IS NULL
    BEGIN
        UPDATE {table} SET actualizado_el = datetime('now', 'localtime') 
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
