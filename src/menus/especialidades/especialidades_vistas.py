from ...ui.input import confirmar, pausar, pedir
from ...ui.layout import tabla
from ...ui.mensajes import advertencia, error, exito, info
from ...utils.decorators import vista
from . import especialidades_servicio


def _mostrar_especialidades(especialidades):
    filas = [[e.id, e.nombre] for e in especialidades]
    tabla(filas, ["ID", "Nombre"])


def _pedir_id(accion):
    id_str = pedir(f"ID de la especialidad a {accion}")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return None
    especialidad = especialidades_servicio.obtener_especialidad_por_id(int(id_str))
    if not especialidad:
        error("Especialidad no encontrada.")
        pausar()
        return None
    return especialidad


@vista("Registrar Nueva Especialidad")
def crear_especialidad():
    nombre = pedir("Nombre de la especialidad")
    try:
        especialidades_servicio.crear_especialidad(nombre)
    except ValueError as err:
        error(str(err))
        pausar()
        return
    exito(f"Especialidad '{nombre}' registrada exitosamente.")
    pausar()


@vista("Listado de Especialidades")
def listar_especialidades():
    especialidades = especialidades_servicio.listar_especialidades()
    if not especialidades:
        advertencia("No hay especialidades registradas.")
        pausar()
        return
    _mostrar_especialidades(especialidades)
    pausar()


@vista("Editar Especialidad")
def editar_especialidad():
    especialidades = especialidades_servicio.listar_especialidades()
    if not especialidades:
        advertencia("No hay especialidades registradas.")
        pausar()
        return
    _mostrar_especialidades(especialidades)
    especialidad = _pedir_id("editar")
    if not especialidad:
        return
    info(f"Editando: {especialidad.nombre}")
    nombre = pedir("Nombre de la especialidad", requerido=False, default=especialidad.nombre)
    try:
        especialidades_servicio.actualizar_especialidad(especialidad, nombre)
    except ValueError as err:
        error(str(err))
        pausar()
        return
    exito(f"Especialidad '{especialidad.nombre}' actualizada.")
    pausar()


@vista("Eliminar Especialidad")
def eliminar_especialidad():
    especialidades = especialidades_servicio.listar_especialidades()
    if not especialidades:
        advertencia("No hay especialidades registradas.")
        pausar()
        return
    _mostrar_especialidades(especialidades)
    especialidad = _pedir_id("eliminar")
    if not especialidad:
        return
    medicos_count = especialidades_servicio.contar_medicos_asociados(especialidad)
    if medicos_count:
        advertencia(f"La especialidad '{especialidad.nombre}' tiene {medicos_count} médico(s) asociado(s).")
        error("No se puede eliminar mientras tenga médicos asociados.")
        pausar()
        return
    advertencia(f"'{especialidad.nombre}' será eliminada permanentemente.")
    if not confirmar(f"¿Eliminar '{especialidad.nombre}'? Esta acción no se puede deshacer"):
        info("Operación cancelada.")
        pausar()
        return
    especialidades_servicio.eliminar_especialidad(especialidad)
    exito(f"Especialidad '{especialidad.nombre}' eliminada correctamente.")
    pausar()
