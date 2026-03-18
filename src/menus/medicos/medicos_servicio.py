from ...database.models import Especialidad, Medico


def crear_medico(nombre: str, matricula: str, especialidad: Especialidad):
    if Medico.select().where(Medico.matricula == matricula).exists():
        raise ValueError("Ya existe un médico con esa matrícula.")

    return Medico.create(
        nombre=nombre.upper(),
        especialidad=especialidad,
        matricula=matricula,
        activo=True,
    )


def listar_especialidades():
    return list(Especialidad.select().order_by(Especialidad.nombre))


def listar_medicos(solo_activos: bool = False):
    query = Medico.select().order_by(Medico.nombre)

    if solo_activos:
        query = query.where(Medico.activo == 1)

    return list(query)


def buscar_medicos(termino: str):
    return list(
        Medico.select()
        .join(Especialidad)
        .where((Medico.nombre.contains(termino)) | (Especialidad.nombre.contains(termino)) | (Medico.matricula.contains(termino)))
        .order_by(Medico.nombre)
    )


def obtener_medico_por_id(medico_id: int):
    try:
        return Medico.get_by_id(medico_id)
    except Exception:
        return None


def actualizar_medico(medico, nombre, matricula, especialidad, activo):
    medico.nombre = nombre.upper()
    medico.matricula = matricula
    medico.especialidad = especialidad
    medico.activo = activo
    medico.save()

    return medico


def eliminar_medico(medico):
    medico.delete_instance(recursive=True)
