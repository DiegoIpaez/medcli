from ...database.models import ESPECIALIDADES
from ...ui.colores import DIM, GREEN, RED, RESET
from ...ui.input import confirmar, pausar, pedir, pedir_opcion, pedir_validado
from ...ui.layout import tabla
from ...ui.mensajes import advertencia, error, exito, info
from ...utils.decorators import vista
from ...utils.matricula import validar_matricula
from . import medicos_servicio


def _mostrar_tabla_medicos(medicos):
    filas = []
    for medico in medicos:
        estado = f"{GREEN}Activo{RESET}" if medico.activo else f"{RED}Inactivo{RESET}"
        filas.append(
            [medico.id, medico.nombre, medico.especialidad, medico.matricula, estado]
        )
    tabla(filas, ["ID", "Nombre", "Especialidad", "Matrícula", "Estado"])


def _pedir_id(accion):
    id_str = pedir(f"ID del médico a {accion}")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return None

    medico = medicos_servicio.obtener_medico_por_id(int(id_str))
    if not medico:
        error("Médico no encontrado.")
        pausar()
        return None

    return medico


def _pedir_activo(actual: bool) -> bool:
    actual_str = "s" if actual else "n"
    respuesta = pedir(campo="¿Activo? [s/n]", requerido=False, default=actual_str).lower()
    if respuesta in ("s", "si"):
        return True
    if respuesta in ("n", "no"):
        return False
    return actual


@vista("Registrar Nuevo Médico")
def alta_medico():
    nombre = pedir("Nombre completo")
    matricula = pedir_validado(
        prompt="Matrícula (ej: MN 123456)",
        validador=validar_matricula,
        msg_error="Formato inválido.",
    ).upper()
    especialidad = pedir_opcion(prompt="Especialidad", opciones=ESPECIALIDADES)

    medicos_servicio.crear_medico(nombre, matricula, especialidad)
    exito(f"Médico '{nombre.upper()}' registrado exitosamente.")
    pausar()


@vista("Listado de Médicos")
def mostrar_medicos(solo_activos: bool = False):
    medicos = medicos_servicio.listar_medicos(solo_activos)

    if not medicos:
        advertencia("No hay médicos registrados.")
        pausar()
        return

    _mostrar_tabla_medicos(medicos)
    pausar()


@vista("Buscar Médico")
def buscar_medico():
    medicos = medicos_servicio.listar_medicos()

    if not medicos:
        advertencia("No hay médicos registrados.")
        pausar()
        return

    termino = pedir("Nombre, especialidad o matrícula")
    resultados = medicos_servicio.buscar_medicos(termino)

    if not resultados:
        advertencia("No se encontraron resultados.")
        pausar()
        return

    _mostrar_tabla_medicos(resultados)
    pausar()


@vista("Editar Médico")
def editar_medico():
    medicos = medicos_servicio.listar_medicos()

    if not medicos:
        advertencia("No hay médicos registrados.")
        pausar()
        return

    _mostrar_tabla_medicos(medicos)
    medico = _pedir_id("editar")
    if not medico:
        return

    info(f"Editando: {medico.nombre} | {medico.especialidad} | Mat: {medico.matricula}")
    print(f"  {DIM}(Dejá vacío para mantener el valor actual){RESET}\n")

    nombre = pedir("Nombre completo", requerido=False, default=medico.nombre)
    matricula = pedir_validado(
        prompt="Matrícula",
        validador=validar_matricula,
        msg_error="Formato inválido.",
        requerido=False,
        default=medico.matricula,
    ).upper()
    especialidad = pedir_opcion(
        prompt="Especialidad", opciones=ESPECIALIDADES, default=medico.especialidad
    )
    activo = _pedir_activo(medico.activo)

    medicos_servicio.actualizar_medico(medico, nombre, matricula, especialidad, activo)
    exito(f"Médico '{nombre.upper()}' actualizado.")
    pausar()


@vista("Eliminar Médico")
def eliminar_medico():
    medicos = medicos_servicio.listar_medicos()

    if not medicos:
        advertencia("No hay médicos registrados.")
        pausar()
        return

    _mostrar_tabla_medicos(medicos)
    medico = _pedir_id("eliminar")
    if not medico:
        return

    advertencia(f"'{medico.nombre}' será eliminado permanentemente.")

    if not confirmar(f"¿Eliminar a '{medico.nombre}'? Esta acción no se puede deshacer"):
        info("Operación cancelada.")
        pausar()
        return

    medicos_servicio.eliminar_medico(medico)
    exito(f"Médico '{medico.nombre}' eliminado correctamente.")
    pausar()
