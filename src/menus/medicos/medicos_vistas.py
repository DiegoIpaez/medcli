from ...database.models import ESPECIALIDADES
from ...ui.colores import (
    CYAN,
    DIM,
    GREEN,
    RED,
    RESET,
    YELLOW,
)
from ...ui.input import (
    confirmar,
    pausar,
    pedir,
)
from ...ui.layout import tabla
from ...ui.mensajes import (
    advertencia,
    error,
    exito,
    info,
)
from ...utils.decorators import vista
from . import medicos_servicio


def _mostrar_especialidades():
    print(f"\n  {CYAN}Especialidades disponibles:{RESET}")
    for i, esp in enumerate(ESPECIALIDADES, 1):
        print(f"  {GREEN}  [{i:>2}]{RESET} {esp}")


@vista("Registrar Nuevo Médico")
def alta_medico():
    nombre = pedir("Nombre completo")
    matricula = pedir("Matrícula")

    _mostrar_especialidades()
    while True:
        esp_input = input(f"\n  {YELLOW}  Elegí especialidad (número): {RESET}").strip()
        if esp_input.isdigit() and 1 <= int(esp_input) <= len(ESPECIALIDADES):
            especialidad = ESPECIALIDADES[int(esp_input) - 1]
            break
        error("Número inválido.")

    try:
        medicos_servicio.crear_medico(nombre, matricula, especialidad)
        exito(f"Médico '{nombre.upper()}' registrado exitosamente.")
    except ValueError as e:
        error(str(e))

    pausar()


def _mostrar_tabla_medicos(medicos):
    filas = []
    for medico in medicos:
        estado = f"{GREEN}Activo{RESET}" if medico.activo else f"{RED}Inactivo{RESET}"
        filas.append(
            [medico.id, medico.nombre, medico.especialidad, medico.matricula, estado]
        )

    tabla(filas, ["ID", "Nombre", "Especialidad", "Matrícula", "Estado"])


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
    id_str = pedir("ID del médico a editar")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    medico = medicos_servicio.obtener_medico_por_id(int(id_str))
    if not medico:
        error("Médico no encontrado.")
        pausar()
        return

    info(f"Editando: {medico.nombre} | {medico.especialidad} | Mat: {medico.matricula}")
    print(f"  {DIM}(Dejá vacío para mantener el valor actual){RESET}\n")

    nombre = pedir("Nombre completo", requerido=False, default=medico.nombre)
    matricula = pedir("Matrícula", requerido=False, default=medico.matricula)

    _mostrar_especialidades()
    esp_actual_idx = (
        ESPECIALIDADES.index(medico.especialidad) + 1
        if medico.especialidad in ESPECIALIDADES
        else 1
    )

    titulo_esp = (
        f"Especialidad [{esp_actual_idx} - {medico.especialidad}] (Enter para mantener)"
    )
    esp_input = input(f"\n  {YELLOW}  {titulo_esp}: {RESET}").strip()

    especialidad = medico.especialidad
    if esp_input.isdigit() and 1 <= int(esp_input) <= len(ESPECIALIDADES):
        especialidad = ESPECIALIDADES[int(esp_input) - 1]

    activo_actual = "s" if medico.activo else "n"
    activo_str = (
        input(f"  {YELLOW}  ¿Activo? [s/n] (actual: {activo_actual}): {RESET}")
        .strip()
        .lower()
    )

    activo = medico.activo
    if activo_str in ("s", "si"):
        activo = True
    elif activo_str in ("n", "no"):
        activo = False

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
    id_str = pedir("ID del médico a eliminar")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    medico = medicos_servicio.obtener_medico_por_id(int(id_str))
    if not medico:
        error("Médico no encontrado.")
        pausar()
        return

    advertencia(f"'{medico.nombre}' será eliminado permanentemente.")

    if not confirmar(f"¿Eliminar a '{medico.nombre}'? Esta acción no se puede deshacer"):
        info("Operación cancelada.")
        pausar()
        return

    medicos_servicio.eliminar_medico(medico)

    exito(f"Médico '{medico.nombre}' eliminado correctamente.")
    pausar()
