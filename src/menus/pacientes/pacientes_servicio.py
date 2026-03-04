import datetime

from ...database.models import ObraSocial, Paciente


def get_all_obras_sociales():
    return ObraSocial.select()


def cuit_existe(cuit):
    return Paciente.select().where(Paciente.cuit == cuit).exists()


def crear_paciente(nombre, cuit, fecha_nac, obra_social):
    ahora = datetime.datetime.now()
    return Paciente.create(
        nombre=nombre.upper(),
        cuit=cuit,
        fecha_nacimiento=fecha_nac,
        obra_social=obra_social,
        created_at=ahora,
        updated_at=ahora,
    )


def get_todos_los_pacientes():
    return Paciente.select().order_by(Paciente.nombre)


def buscar_pacientes(termino):
    return (
        Paciente.select()
        .where((Paciente.nombre.contains(termino)) | (Paciente.cuit.contains(termino)))
        .order_by(Paciente.nombre)
    )


def get_paciente_por_id(id):
    return Paciente.get_by_id(id)


def actualizar_paciente(paciente, nombre, cuit, fecha_nac, obra_social):
    paciente.nombre = nombre.upper()
    paciente.cuit = cuit
    paciente.fecha_nacimiento = fecha_nac
    paciente.obra_social = obra_social
    paciente.updated_at = datetime.datetime.now()
    paciente.save()
    return paciente


def contar_turnos(paciente):
    return paciente.turnos.count()


def eliminar_paciente(paciente):
    paciente.delete_instance(recursive=True)
