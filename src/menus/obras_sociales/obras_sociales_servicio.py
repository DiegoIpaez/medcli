from peewee import fn

from ...database.models import ObraSocial, Paciente


def obtener_all_obras_sociales():
    return ObraSocial.select().order_by(ObraSocial.nombre)


def listar_obras_sociales():
    return list(obtener_all_obras_sociales())


def buscar_obras_sociales(termino: str):
    termino = termino.strip()
    if not termino:
        return list(obtener_all_obras_sociales())
    return list(ObraSocial.select().where(ObraSocial.nombre.contains(termino)).order_by(ObraSocial.nombre))


def _nombre_existe(nombre: str, excluir_id: int | None = None):
    query = ObraSocial.select().where(fn.Lower(ObraSocial.nombre) == nombre.lower())
    if excluir_id is not None:
        query = query.where(ObraSocial.id != excluir_id)
    return query.exists()


def crear_obra_social(nombre: str):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if _nombre_existe(nombre):
        raise ValueError("Ya existe una obra social con ese nombre.")
    return ObraSocial.create(nombre=nombre)


def obtener_obra_social_por_id(obra_social_id: int):
    try:
        return ObraSocial.get_by_id(obra_social_id)
    except Exception:
        return None


def actualizar_obra_social(obra_social, nombre: str):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre es obligatorio.")
    if _nombre_existe(nombre, excluir_id=obra_social.id):
        raise ValueError("Ya existe una obra social con ese nombre.")
    obra_social.nombre = nombre
    obra_social.save()
    return obra_social


def contar_pacientes_asociados(obra_social):
    return Paciente.select().where(Paciente.obra_social == obra_social).count()


def eliminar_obra_social(obra_social):
    obra_social.delete_instance()
