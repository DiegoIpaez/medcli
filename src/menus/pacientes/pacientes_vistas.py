import datetime

from ...ui.colores import (
    CYAN,
    DIM,
    GREEN,
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
from ...utils.cuit import validar_cuit
from ...utils.decorators import vista
from . import pacientes_servicio


def _mostrar_obras_sociales(obras):
    print(f"\n  {CYAN}Obras Sociales disponibles:{RESET}")
    print(f"  {DIM}  [0] Sin obra social{RESET}")
    for i, o in enumerate(obras, 1):
        print(f"  {GREEN}  [{i}]{RESET} {o.nombre}")


def _seleccionar_obra_social(obras, prompt, fallback=None):
    os_input = input(f"\n  {YELLOW}  {prompt}: {RESET}").strip()
    if os_input == "0":
        return None
    if os_input.isdigit() and 1 <= int(os_input) <= len(obras):
        return obras[int(os_input) - 1]
    return fallback


def _pedir_fecha(prompt, default=None):
    while True:
        valor = pedir(
            prompt,
            requerido=default is None,
            default=default if default is not None else "",
        )
        try:
            return datetime.datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            error("Formato inválido. Usá DD/MM/AAAA.")


def _filas_pacientes(pacientes):
    return [
        [
            p.id,
            p.nombre,
            p.cuit,
            p.fecha_nacimiento.strftime("%d/%m/%Y"),
            p.obra_social.nombre if p.obra_social else "—",
        ]
        for p in pacientes
    ]


@vista("Registrar Nuevo Paciente")
def crear_paciente():
    nombre = pedir("Nombre completo")
    while True:
        cuit = pedir("CUIT")
        if not validar_cuit(cuit):
            error("CUIT inválido. Debe tener 11 dígitos y dígito verificador correcto.")
            continue
        if pacientes_servicio.cuit_existe(cuit):
            error(f"Ya existe un paciente con este CUIT '{cuit}'.")
            continue
        break

    fecha_nac = _pedir_fecha("Fecha de nacimiento (DD/MM/AAAA)")

    obras = pacientes_servicio.obtener_all_obras_sociales()
    _mostrar_obras_sociales(obras)
    obra_social = _seleccionar_obra_social(obras, "Elegí obra social (número)")

    pacientes_servicio.crear_paciente(nombre, cuit, fecha_nac, obra_social)
    exito(f"Paciente '{nombre.upper()}' registrado exitosamente.")
    pausar()


def _mostrar_pacientes(pacientes):
    tabla(
        _filas_pacientes(pacientes),
        ["ID", "Nombre", "CUIT", "Nacimiento", "Obra Social"],
    )


@vista("Listado de Pacientes")
def listar_pacientes():
    pacientes = pacientes_servicio.obtener_todos_los_pacientes()

    if not pacientes:
        advertencia("No hay pacientes registrados.")
        pausar()
        return

    _mostrar_pacientes(pacientes)
    pausar()


@vista("Buscar Paciente")
def buscar_paciente():
    pacientes = pacientes_servicio.obtener_todos_los_pacientes()
    if not pacientes:
        advertencia("No hay pacientes registrados.")
        pausar()
        return

    termino = pedir("Nombre o CUIT a buscar")
    resultados = pacientes_servicio.buscar_pacientes(termino)

    if not resultados:
        advertencia("No se encontraron resultados.")
        pausar()
        return

    tabla(
        _filas_pacientes(resultados),
        ["ID", "Nombre", "CUIT", "Nacimiento", "Obra Social"],
    )
    pausar()


@vista("Editar Paciente")
def editar_paciente():
    pacientes = pacientes_servicio.obtener_todos_los_pacientes()

    if not pacientes:
        advertencia("No hay pacientes registrados.")
        pausar()
        return

    _mostrar_pacientes(pacientes)
    id_str = pedir("ID del paciente a editar")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    paciente = pacientes_servicio.obtener_paciente_por_id(int(id_str))
    if not paciente:
        error("Paciente no encontrado.")
        pausar()
        return

    os_actual = paciente.obra_social.nombre if paciente.obra_social else "Sin obra social"
    info(f"Editando: {paciente.nombre} | {paciente.cuit} | {os_actual}")
    print(f"  {DIM}(Dejá vacío para mantener el valor actual){RESET}\n")

    nombre = pedir("Nombre completo", requerido=False, default=paciente.nombre)
    while True:
        cuit = pedir("CUIT", requerido=False, default=paciente.cuit)
        if not validar_cuit(cuit):
            error("CUIT inválido. Debe tener 11 dígitos y dígito verificador correcto.")
            continue

        if cuit != paciente.cuit and pacientes_servicio.cuit_existe(cuit):
            error(f"Ya existe un paciente con CUIT '{cuit}'.")
            continue
        break
    fecha_nac = _pedir_fecha(
        "Fecha de nacimiento (DD/MM/AAAA)",
        default=paciente.fecha_nacimiento.strftime("%d/%m/%Y"),
    )

    obras = pacientes_servicio.obtener_all_obras_sociales()
    _mostrar_obras_sociales(obras)
    obra_social = _seleccionar_obra_social(
        obras,
        "Elegí obra social (número, Enter para mantener)",
        fallback=paciente.obra_social,
    )

    pacientes_servicio.actualizar_paciente(paciente, nombre, cuit, fecha_nac, obra_social)
    exito(f"Paciente '{nombre.upper()}' actualizado.")
    pausar()


@vista("Eliminar Paciente")
def eliminar_paciente():
    pacientes = pacientes_servicio.obtener_todos_los_pacientes()

    if not pacientes:
        advertencia("No hay pacientes registrados.")
        pausar()
        return

    _mostrar_pacientes(pacientes)
    id_str = pedir("ID del paciente a eliminar")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    paciente = pacientes_servicio.obtener_paciente_por_id(int(id_str))
    if not paciente:
        error("Paciente no encontrado.")
        pausar()
        return

    turnos_count = pacientes_servicio.contar_turnos(paciente)
    advertencia(f"'{paciente.nombre}' tiene {turnos_count} turno(s) asociado(s).")

    if not confirmar(f"¿Eliminar a '{paciente.nombre}'? Esta acción no se puede deshacer"):
        info("Operación cancelada.")
        pausar()
        return

    pacientes_servicio.eliminar_paciente(paciente)
    exito(f"Paciente '{paciente.nombre}' eliminado correctamente.")
    pausar()
