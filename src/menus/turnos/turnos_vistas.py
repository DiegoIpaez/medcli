import datetime

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
    pedir_opcion,
)
from ...ui.layout import encabezado, limpiar, tabla
from ...ui.mensajes import (
    advertencia,
    error,
    exito,
    info,
)
from ...utils.constantes import HORARIO_APERTURA, HORARIO_CIERRE
from ...utils.decorators import vista
from . import turnos_service


def _color_estado(estado):
    nombre = estado.nombre if hasattr(estado, "nombre") else estado
    colores = {
        "RESERVADO": CYAN,
        "ATENDIDO": GREEN,
        "CANCELADO": RED,
        "AUSENTE": YELLOW,
    }
    c = colores.get(nombre, RESET)
    return f"{c}{nombre}{RESET}"


def _pedir_fecha(prompt, default=None):
    hoy = datetime.date.today()

    while True:
        if default is not None:
            valor = pedir(prompt, requerido=False, default=default)
        else:
            valor = pedir(prompt, requerido=True)

        try:
            fecha = datetime.datetime.strptime(valor, "%d/%m/%Y").date()
            hora_actual = datetime.datetime.now().hour

            if fecha < hoy:
                error(f"La fecha no puede ser anterior a hoy ({hoy.strftime('%d/%m/%Y')}).")
                continue
            if fecha == hoy:
                if hora_actual >= HORARIO_CIERRE:
                    error("Ya pasó el horario de cierre para hoy. Elegí otra fecha.")
                    continue

            return fecha
        except ValueError:
            error("Formato inválido. Usá DD/MM/AAAA.")


def _pedir_horario(prompt, fecha):
    while True:
        horario = pedir(prompt)
        try:
            dt = datetime.datetime.strptime(horario, "%H:%M")
            if not (HORARIO_APERTURA <= dt.hour <= HORARIO_CIERRE):
                error(f"El horario debe estar entre {HORARIO_APERTURA:02d}:00 y {HORARIO_CIERRE:02d}:00.")
                continue

            if fecha == datetime.date.today():
                ahora = datetime.datetime.now().time().replace(second=0, microsecond=0)
                if dt.time() <= ahora:
                    msg_err = f"El horario debe ser posterior a {ahora.strftime('%H:%M')}."
                    error(msg_err)
                    continue

            return horario
        except ValueError:
            error("Formato inválido. Usá HH:MM.")


def _seleccionar_medico():
    medicos = turnos_service.obtener_medicos_activos()
    if not medicos:
        advertencia("No hay médicos activos registrados.")
        return None
    opciones = [f"{m.nombre} — {m.especialidad}" for m in medicos]
    seleccion = pedir_opcion("Elegí médico", opciones)
    return medicos[opciones.index(seleccion)]


def _seleccionar_paciente():
    termino = pedir("Buscar paciente (nombre o CUIT)")
    pacientes = turnos_service.buscar_pacientes(termino)
    if not pacientes:
        advertencia("No se encontraron pacientes.")
        return None
    opciones = [f"{paciente.nombre} — DNI: {paciente.cuit}" for paciente in pacientes]
    seleccion = pedir_opcion("Elegí paciente", opciones)
    return pacientes[opciones.index(seleccion)]


def _formato_duracion(turno):
    return f"{turno.duracion_real}'" if turno.duracion_real else f"{turno.duracion_min}' (est.)"


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
    horario = _pedir_horario("Horario (HH:MM)", fecha)

    entre_turno = False
    if turnos_service.verificar_conflicto(medico.id, fecha, horario):
        advertencia(f"El Dr/a. {medico.nombre} ya tiene un turno dentro de los 30 min de ese horario.")
        if not confirmar("¿Registrar igual como entre-turno?"):
            info("Turno no creado.")
            pausar()
            return
        entre_turno = True

    notas = pedir("Notas (opcional)", requerido=False)
    turnos_service.crear_turno(paciente, medico, fecha, horario, entre_turno, notas)
    fecha_str = fecha.strftime("%d/%m/%Y")
    exito(f"Turno creado: {paciente.nombre} con {medico.nombre} el {fecha_str} a las {horario}.")
    pausar()


@vista("Agenda Diaria por Médico")
def agenda_diaria():
    medico = _seleccionar_medico()
    if not medico:
        pausar()
        return

    fecha = _pedir_fecha("Ingrese Fecha ", default=datetime.date.today().strftime("%d/%m/%Y"))
    turnos = turnos_service.obtener_turnos_por_medico_y_fecha(medico, fecha)

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

    tabla(filas, ["Hora", "Paciente", "CUIT", "Estado", "Duración", "ET", "Notas"])
    pausar()


@vista("Cambiar Estado de Turno")
def cambiar_estado():
    id_str = pedir("ID del turno")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    turno = turnos_service.obtener_turno_por_id(int(id_str))
    if not turno:
        error("Turno no encontrado.")
        pausar()
        return

    fecha = turno.fecha.strftime("%d/%m/%Y")
    info(f"Turno #{turno.id}: {turno.paciente.nombre} con {turno.medico.nombre}")
    info(f"Fecha: {fecha} {turno.horario} — Estado actual: {turno.estado.nombre}")

    estados = list(turnos_service.obtener_estados_turno())
    opciones = [estado.nombre for estado in estados]
    seleccion = pedir_opcion("Elegí nuevo estado", opciones)
    nuevo_estado = estados[opciones.index(seleccion)]
    turnos_service.actualizar_estado(turno, nuevo_estado)
    exito(f"Estado actualizado a '{nuevo_estado.nombre}'.")
    pausar()


def _mostrar_turnos_pendientes(turnos_pendientes):
    columnas = ["ID", "Fecha", "Hora", "Médico", "Especialidad", "Estado", "Duración"]
    filas = [
        [
            turno_pendiente.id,
            turno_pendiente.fecha.strftime("%d/%m/%Y"),
            turno_pendiente.horario,
            turno_pendiente.medico.nombre,
            turno_pendiente.medico.especialidad,
            _color_estado(turno_pendiente.estado),
            _formato_duracion(turno_pendiente),
        ]
        for turno_pendiente in turnos_pendientes
    ]
    tabla(filas, columnas)


@vista("Registrar Duración Real de Consulta")
def registrar_duracion():
    turnos_pendientes = turnos_service.obtener_turnos_pendientes()
    if not turnos_pendientes:
        advertencia("No hay turnos pendientes para registrar duración.")
        pausar()
        return

    _mostrar_turnos_pendientes(turnos_pendientes)

    id_str = pedir("ID del turno")
    if not id_str.isdigit():
        error("ID inválido.")
        pausar()
        return

    turno = turnos_service.obtener_turno_por_id(int(id_str))
    if not turno:
        error("Turno no encontrado.")
        pausar()
        return

    if turno.estado.nombre != "ATENDIDO":
        advertencia(f"El turno tiene estado '{turno.estado.nombre}'. Marcarlo como ATENDIDO primero.")
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

    turnos = turnos_service.obtener_turnos_por_paciente(paciente)

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
