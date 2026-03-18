from peewee import fn

from ...database.models import Especialidad, Medico


def obtener_all_especialidades():
    return Especialidad.select().order_by(Especialidad.nombre)


def listar_especialidades():
    return list(obtener_all_especialidades())


def buscar_especialidades(termino: str):
    termino = termino.strip()
    if not termino:
        return list(obtener_all_especialidades())
    return list(Especialidad.select().where(Especialidad.nombre.contains(termino)).order_by(Especialidad.nombre))


def _nombre_existe(nombre: str, excluir_id: int | None = None):
    query = Especialidad.select().where(fn.Lower(Especialidad.nombre) == nombre.lower())
    if excluir_id is not None:
        query = query.where(Especialidad.id != excluir_id)
    return query.exists()


def crear_especialidad(nombre: str):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if _nombre_existe(nombre):
        raise ValueError("Ya existe una especialidad con ese nombre.")
    return Especialidad.create(nombre=nombre)


def obtener_especialidad_por_id(especialidad_id: int):
    try:
        return Especialidad.get_by_id(especialidad_id)
    except Exception:
        return None


def actualizar_especialidad(especialidad, nombre: str):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if _nombre_existe(nombre, excluir_id=especialidad.id):
        raise ValueError("Ya existe una especialidad con ese nombre.")
    especialidad.nombre = nombre
    especialidad.save()
    return especialidad


def contar_medicos_asociados(especialidad):
    return Medico.select().where(Medico.especialidad == especialidad).count()


def eliminar_especialidad(especialidad):
    especialidad.delete_instance()
