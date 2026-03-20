from ...database.models import Paciente
from ..obras_sociales.obras_sociales_servicio import (
    obtener_all_obras_sociales as listar_obras_sociales,
)


def obtener_all_obras_sociales():
    return listar_obras_sociales()


def cuil_existe(cuil):
    return Paciente.select().where(Paciente.cuil == cuil).exists()


def crear_paciente(nombre, cuil, fecha_nac, obra_social):
    return Paciente.create(
        nombre=nombre.upper(),
        cuil=cuil,
        fecha_nacimiento=fecha_nac,
        obra_social=obra_social,
    )


def obtener_todos_los_pacientes():
    return Paciente.select().order_by(Paciente.nombre)


def buscar_pacientes(termino):
    return Paciente.select().where((Paciente.nombre.contains(termino)) | (Paciente.cuil.contains(termino))).order_by(Paciente.nombre)


def obtener_paciente_por_id(id):
    try:
        return Paciente.get_by_id(id)
    except Exception:
        return None


def actualizar_paciente(paciente, nombre, cuil, fecha_nac, obra_social):
    paciente.nombre = nombre.upper()
    paciente.cuil = cuil
    paciente.fecha_nacimiento = fecha_nac
    paciente.obra_social = obra_social
    paciente.save()
    return paciente


def contar_turnos(paciente):
    return paciente.turnos.count()


def eliminar_paciente(paciente):
    paciente.delete_instance(recursive=True)
