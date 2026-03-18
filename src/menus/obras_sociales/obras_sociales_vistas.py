from ...ui.input import confirmar, pausar, pedir
from ...ui.layout import tabla
from ...ui.mensajes import advertencia, error, exito, info
from ...utils.decorators import vista
from . import obras_sociales_servicio


def _mostrar_obras_sociales(obras):
    filas = [[o.id, o.nombre] for o in obras]
    tabla(filas, ["ID", "Nombre"])


def _pedir_id(accion):
    id_str = pedir(f"ID de la obra social a {accion}")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return None
    obra = obras_sociales_servicio.obtener_obra_social_por_id(int(id_str))
    if not obra:
        error("Obra social no encontrada.")
        pausar()
        return None
    return obra


@vista("Registrar Nueva Obra Social")
def crear_obra_social():
    nombre = pedir("Nombre de la obra social")
    try:
        obras_sociales_servicio.crear_obra_social(nombre)
    except ValueError as err:
        error(str(err))
        pausar()
        return
    exito(f"Obra social '{nombre}' registrada exitosamente.")
    pausar()


@vista("Listado de Obras Sociales")
def listar_obras_sociales():
    obras = obras_sociales_servicio.listar_obras_sociales()
    if not obras:
        advertencia("No hay obras sociales registradas.")
        pausar()
        return
    _mostrar_obras_sociales(obras)
    pausar()


@vista("Editar Obra Social")
def editar_obra_social():
    obras = obras_sociales_servicio.listar_obras_sociales()
    if not obras:
        advertencia("No hay obras sociales registradas.")
        pausar()
        return
    _mostrar_obras_sociales(obras)
    obra = _pedir_id("editar")
    if not obra:
        return
    info(f"Editando: {obra.nombre}")
    nombre = pedir("Nombre de la obra social", requerido=False, default=obra.nombre)
    try:
        obras_sociales_servicio.actualizar_obra_social(obra, nombre)
    except ValueError as err:
        error(str(err))
        pausar()
        return
    exito(f"Obra social '{obra.nombre}' actualizada.")
    pausar()


@vista("Eliminar Obra Social")
def eliminar_obra_social():
    obras = obras_sociales_servicio.listar_obras_sociales()
    if not obras:
        advertencia("No hay obras sociales registradas.")
        pausar()
        return
    _mostrar_obras_sociales(obras)
    obra = _pedir_id("eliminar")
    if not obra:
        return
    pacientes_count = obras_sociales_servicio.contar_pacientes_asociados(obra)
    if pacientes_count:
        advertencia(f"La obra social '{obra.nombre}' tiene {pacientes_count} paciente(s) asociado(s).")
        error("No se puede eliminar mientras tenga pacientes asociados.")
        pausar()
        return
    advertencia(f"'{obra.nombre}' será eliminado permanentemente.")
    if not confirmar(f"¿Eliminar '{obra.nombre}'? Esta acción no se puede deshacer"):
        info("Operación cancelada.")
        pausar()
        return
    obras_sociales_servicio.eliminar_obra_social(obra)
    exito(f"Obra social '{obra.nombre}' eliminada correctamente.")
    pausar()
