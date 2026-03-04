import datetime
from ...database.models import Turno, Medico, Paciente


def get_medicos_activos():
    return Medico.select().where(Medico.activo == True).order_by(Medico.nombre)


def buscar_pacientes(termino):
    return Paciente.select().where(
        (Paciente.nombre.contains(termino)) | (Paciente.cuit.contains(termino))
    )


def verificar_conflicto(medico_id, fecha, horario, excluir_id=None):
    t_nuevo = datetime.datetime.strptime(horario, "%H:%M")
    query = Turno.select().where(
        (Turno.medico == medico_id)
        & (Turno.fecha == fecha)
        & (Turno.estado != "CANCELADO")
    )
    if excluir_id:
        query = query.where(Turno.id != excluir_id)
    for t in query:
        t_exist = datetime.datetime.strptime(t.horario, "%H:%M")
        diff = abs((t_nuevo - t_exist).total_seconds()) / 60
        if diff < 30:
            return True
    return False


def crear_turno(paciente, medico, fecha, horario, entre_turno, notas):
    ahora = datetime.datetime.now()
    return Turno.create(
        paciente=paciente,
        medico=medico,
        fecha=fecha,
        horario=horario,
        estado="RESERVADO",
        entre_turno=entre_turno,
        duracion_min=30,
        duracion_real=None,
        notas=notas or None,
        created_at=ahora,
        updated_at=ahora,
    )


def get_turnos_por_medico_y_fecha(medico, fecha):
    return (
        Turno.select()
        .where((Turno.medico == medico) & (Turno.fecha == fecha))
        .order_by(Turno.horario)
    )


def get_turno_por_id(id):
    return Turno.get_by_id(id)


def actualizar_estado(turno, nuevo_estado):
    turno.estado = nuevo_estado
    turno.updated_at = datetime.datetime.now()
    turno.save()
    return turno


def registrar_duracion_real(turno, duracion):
    turno.duracion_real = duracion
    turno.estado = "ATENDIDO"
    turno.updated_at = datetime.datetime.now()
    turno.save()
    return turno


def get_turnos_por_paciente(paciente):
    return (
        Turno.select()
        .where(Turno.paciente == paciente)
        .order_by(Turno.fecha.desc(), Turno.horario.desc())
    )
