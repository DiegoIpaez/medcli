import datetime

from ...ui.colores import (
    DIM,
    RESET,
)
from ...ui.input import (
    confirmar,
    pausar,
    pedir,
    pedir_opcion,
    pedir_validado,
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


def _opciones_obras_sociales(obras):
    return ["Sin obra social"] + [obra.nombre for obra in obras]


def _seleccionar_obra_social(obras, prompt, fallback=None):
    opciones = _opciones_obras_sociales(obras)
    default = fallback.nombre if fallback else "Sin obra social"
    seleccion = pedir_opcion(prompt, opciones, default=default)
    if seleccion == "Sin obra social":
        return None
    return next((obra for obra in obras if obra.nombre == seleccion), fallback)


def _pedir_fecha(prompt, default=None):
    def validador(valor):
        try:
            datetime.datetime.strptime(valor, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    valor = pedir_validado(
        prompt,
        validador,
        "Formato inválido. Usá DD/MM/AAAA.",
        requerido=default is None,
        default=default or "",
    )
    return datetime.datetime.strptime(valor, "%d/%m/%Y").date()


def _pedir_cuit(cuit_actual=None):
    def validador(valor):
        return validar_cuit(valor)

    while True:
        cuit = pedir_validado(
            "CUIT",
            validador,
            "CUIT inválido. Debe tener 11 dígitos y dígito verificador correcto.",
            requerido=cuit_actual is None,
            default=cuit_actual or "",
        )
        if cuit != cuit_actual and pacientes_servicio.cuit_existe(cuit):
            error(f"Ya existe un paciente con CUIT '{cuit}'.")
            continue
        return cuit


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


def _mostrar_pacientes(pacientes):
    tabla(
        _filas_pacientes(pacientes),
        ["ID", "Nombre", "CUIT", "Nacimiento", "Obra Social"],
    )


@vista("Registrar Nuevo Paciente")
def crear_paciente():
    nombre = pedir("Nombre completo")
    cuit = _pedir_cuit()
    fecha_nac = _pedir_fecha("Fecha de nacimiento (DD/MM/AAAA)")

    obras = pacientes_servicio.obtener_all_obras_sociales()
    obra_social = _seleccionar_obra_social(obras, "Elegí obra social")

    pacientes_servicio.crear_paciente(nombre, cuit, fecha_nac, obra_social)
    exito(f"Paciente '{nombre.upper()}' registrado exitosamente.")
    pausar()


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
    cuit = _pedir_cuit(cuit_actual=paciente.cuit)
    fecha_nac = _pedir_fecha(
        "Fecha de nacimiento (DD/MM/AAAA)",
        default=paciente.fecha_nacimiento.strftime("%d/%m/%Y"),
    )

    obras = pacientes_servicio.obtener_all_obras_sociales()
    obra_social = _seleccionar_obra_social(
        obras,
        "Elegí obra social",
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
