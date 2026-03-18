from ..ui.mensajes import info
from .models import ESTADOS_TURNO, ObraSocial, TurnoEstado


def seed_obras_sociales(db):
    if ObraSocial.select().exists():
        return

    obras = [
        "OSDE",
        "Swiss Medical",
        "Galeno",
        "Medicus",
        "Omint",
        "Hospital Italiano",
        "PAMI",
        "IOMA",
        "OSDEPYM",
        "Jerárquicos Salud",
    ]

    data = [{"nombre": nombre} for nombre in obras]

    with db.atomic():
        ObraSocial.insert_many(data).execute()

    info("Obras sociales iniciales cargadas", prefijo="🌱")


def seed_estados_turno(db):
    if TurnoEstado.select().exists():
        return

    data = [{"nombre": nombre} for nombre in ESTADOS_TURNO]

    with db.atomic():
        TurnoEstado.insert_many(data).execute()

    info("Estados de turno iniciales cargados", prefijo="🌱")
