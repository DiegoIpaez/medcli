import datetime

from ...database.models import ESTADOS
from ...ui.colores import (
    CYAN,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    YELLOW,
)
from ...ui.input import (
    confirmar,
    pausar,
    pedir,
)
from ...ui.layout import encabezado, limpiar, tabla
from ...ui.mensajes import (
    advertencia,
    error,
    exito,
    info,
)
from ...utils.decorators import vista
from . import turnos_service


def _color_estado(estado):
    colores = {
        "RESERVADO": CYAN,
        "ATENDIDO": GREEN,
        "CANCELADO": RED,
        "AUSENTE": YELLOW,
    }
    c = colores.get(estado, RESET)
    return f"{c}{estado}{RESET}"


def _pedir_fecha(prompt, default=None):
    while True:
        if default is not None:
            valor = pedir(prompt, requerido=False, default=default)
        else:
            valor = pedir(prompt, requerido=True)
        try:
            return datetime.datetime.strptime(valor, "%d/%m/%Y").date()
        except ValueError:
            error("Formato inválido. Usá DD/MM/AAAA.")


def _pedir_horario(prompt):
    while True:
        horario = pedir(prompt)
        try:
            datetime.datetime.strptime(horario, "%H:%M")
            return horario
        except ValueError:
            error("Formato inválido. Usá HH:MM.")


def _seleccionar_de_lista(items, prompt):
    while True:
        idx = input(f"\n  {YELLOW}  {prompt}: {RESET}").strip()
        if idx.isdigit() and 1 <= int(idx) <= len(items):
            return items[int(idx) - 1]
        error("Número inválido.")


def _seleccionar_medico():
    medicos = turnos_service.get_medicos_activos()
    if not medicos:
        advertencia("No hay médicos activos registrados.")
        return None
    print(f"\n  {CYAN}Médicos disponibles:{RESET}")
    for i, m in enumerate(medicos, 1):
        print(f"  {GREEN}  [{i}]{RESET} {m.nombre} — {m.especialidad}")
    return _seleccionar_de_lista(medicos, "Elegí médico (número)")


def _seleccionar_paciente():
    termino = pedir("Buscar paciente (nombre o CUIT/DNI)")
    resultados = turnos_service.buscar_pacientes(termino)
    if not resultados:
        advertencia("No se encontraron pacientes.")
        return None
    print(f"\n  {CYAN}Resultados:{RESET}")
    for i, p in enumerate(resultados, 1):
        print(f"  {GREEN}  [{i}]{RESET} {p.nombre} — DNI: {p.cuit}")
    return _seleccionar_de_lista(resultados, "Elegí paciente (número)")


def _formato_duracion(turno):
    return (
        f"{turno.duracion_real}'" if turno.duracion_real else f"{turno.duracion_min}' (est.)"
    )


@vista("Crear Nuevo Turno")
def crear_turno():
    paciente = _seleccionar_paciente()
    if not paciente:
        pausar()
        return

    medico = _seleccionar_medico()
    if not medico:
        pausar()
        return

    fecha = _pedir_fecha("Fecha del turno (DD/MM/AAAA)")
    horario = _pedir_horario("Horario (HH:MM)")

    entre_turno = False
    if turnos_service.verificar_conflicto(medico.id, fecha, horario):
        advertencia(
            f"El Dr/a. {medico.nombre} ya tiene un turno dentro de los 30 min de ese horario."
        )
        if not confirmar("¿Registrar igual como entre-turno?"):
            info("Turno no creado.")
            pausar()
            return
        entre_turno = True

    notas = pedir("Notas (opcional)", requerido=False)
    turnos_service.crear_turno(paciente, medico, fecha, horario, entre_turno, notas)
    fecha_str = fecha.strftime("%d/%m/%Y")
    exito(
        f"Turno creado: {paciente.nombre} con {medico.nombre} el {fecha_str} a las {horario}."
    )
    pausar()


@vista("Agenda Diaria por Médico")
def agenda_diaria():
    medico = _seleccionar_medico()
    if not medico:
        pausar()
        return

    fecha = _pedir_fecha(
        "Fecha (DD/MM/AAAA)", default=datetime.date.today().strftime("%d/%m/%Y")
    )
    turnos = turnos_service.get_turnos_por_medico_y_fecha(medico, fecha)

    limpiar()
    encabezado(f"Agenda — {medico.nombre} — {fecha.strftime('%d/%m/%Y')}")
    info(f"Especialidad: {medico.especialidad}")

    if not turnos:
        advertencia("No hay turnos para esta fecha.")
        pausar()
        return

    filas = [
        [
            t.horario,
            t.paciente.nombre,
            t.paciente.cuit,
            _color_estado(t.estado),
            _formato_duracion(t),
            f"{MAGENTA}*ET{RESET}" if t.entre_turno else "",
            t.notas or "—",
        ]
        for t in turnos
    ]

    tabla(filas, ["Hora", "Paciente", "CUIT/DNI", "Estado", "Duración", "ET", "Notas"])
    pausar()


@vista("Cambiar Estado de Turno")
def cambiar_estado():
    id_str = pedir("ID del turno")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    turno = turnos_service.get_turno_por_id(int(id_str))
    if not turno:
        error("Turno no encontrado.")
        pausar()
        return

    fecha = turno.fecha.strftime("%d/%m/%Y")
    info(f"Turno #{turno.id}: {turno.paciente.nombre} con {turno.medico.nombre}")
    info(f"Fecha: {fecha} {turno.horario} — Estado actual: {turno.estado}")

    print(f"\n  {CYAN}Nuevos estados disponibles:{RESET}")
    for i, e in enumerate(ESTADOS, 1):
        print(f"  {GREEN}  [{i}]{RESET} {e}")

    nuevo_estado = _seleccionar_de_lista(ESTADOS, "Elegí nuevo estado (número)")
    turnos_service.actualizar_estado(turno, nuevo_estado)
    exito(f"Estado actualizado a '{nuevo_estado}'.")
    pausar()


@vista("Registrar Duración Real de Consulta")
def registrar_duracion():
    id_str = pedir("ID del turno")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    turno = turnos_service.get_turno_por_id(int(id_str))
    if not turno:
        error("Turno no encontrado.")
        pausar()
        return

    if turno.estado != "ATENDIDO":
        advertencia(
            f"El turno tiene estado '{turno.estado}'. Marcarlo como ATENDIDO primero."
        )
    fecha = turno.fecha.strftime("%d/%m/%Y")
    info(f"Turno #{turno.id}: {turno.paciente.nombre} — {fecha} {turno.horario}")
    info(f"Duración estimada: {turno.duracion_min} minutos")
    info(f"Duración real actual: {turno.duracion_real or 'no registrada'}")

    while True:
        dur_str = pedir("Duración real (en minutos)")
        if dur_str.isdigit() and int(dur_str) > 0:
            break
        error("Ingresá un número entero positivo.")

    turnos_service.registrar_duracion_real(turno, int(dur_str))
    exito(f"Duración registrada: {dur_str} minutos. Estado actualizado a ATENDIDO.")
    pausar()


@vista("Turnos por Paciente")
def turnos_por_paciente():
    paciente = _seleccionar_paciente()
    if not paciente:
        pausar()
        return

    turnos = turnos_service.get_turnos_por_paciente(paciente)

    limpiar()
    encabezado(f"Turnos de: {paciente.nombre}")

    if not turnos:
        advertencia("Este paciente no tiene turnos registrados.")
        pausar()
        return

    filas = [
        [
            t.id,
            t.fecha.strftime("%d/%m/%Y"),
            t.horario,
            t.medico.nombre,
            t.medico.especialidad,
            _color_estado(t.estado),
            _formato_duracion(t),
        ]
        for t in turnos
    ]

    tabla(filas, ["ID", "Fecha", "Hora", "Médico", "Especialidad", "Estado", "Duración"])
    pausar()
