import datetime

from ...database.models import Medico, Paciente, Turno, TurnoEstado


def obtener_medicos_activos():
    return Medico.select().where(Medico.activo == 1).order_by(Medico.nombre)


def obtener_turnos_por_paciente(paciente):
    return Turno.select().where(Turno.paciente == paciente).order_by(Turno.fecha.desc(), Turno.horario.desc())


def obtener_turnos_por_medico_y_fecha(medico, fecha):
    return Turno.select().where((Turno.medico == medico) & (Turno.fecha == fecha)).order_by(Turno.horario)


def obtener_turno_por_id(id):
    return Turno.get_by_id(id)


def obtener_turnos_pendientes():
    return Turno.select().join(TurnoEstado).where(TurnoEstado.nombre == "RESERVADO").order_by(Turno.fecha, Turno.horario)


def buscar_pacientes(termino):
    return Paciente.select().where((Paciente.nombre.contains(termino)) | (Paciente.cuit.contains(termino)))


def verificar_conflicto(medico_id, fecha, horario, excluir_id=None):
    t_nuevo = datetime.datetime.strptime(horario, "%H:%M")
    query = Turno.select().join(TurnoEstado).where((Turno.medico == medico_id) & (Turno.fecha == fecha) & (TurnoEstado.nombre != "CANCELADO"))
    if excluir_id:
        query = query.where(Turno.id != excluir_id)
    for t in query:
        t_exist = datetime.datetime.strptime(t.horario, "%H:%M")
        diff = abs((t_nuevo - t_exist).total_seconds()) / 60
        if diff < 30:
            return True
    return False


def crear_turno(paciente, medico, fecha, horario, entre_turno, notas):
    return Turno.create(
        paciente=paciente,
        medico=medico,
        fecha=fecha,
        horario=horario,
        estado=obtener_estado_por_nombre("RESERVADO"),
        entre_turno=entre_turno,
        duracion_min=30,
        duracion_real=None,
        notas=notas or None,
    )


def actualizar_estado(turno, nuevo_estado):
    turno.estado = nuevo_estado
    turno.save()
    return turno


def registrar_duracion_real(turno, duracion):
    turno.duracion_real = duracion
    turno.estado = obtener_estado_por_nombre("ATENDIDO")
    turno.save()
    return turno


def obtener_estados_turno():
    return TurnoEstado.select().order_by(TurnoEstado.id)


def obtener_estado_por_nombre(nombre):
    return TurnoEstado.get(TurnoEstado.nombre == nombre)
