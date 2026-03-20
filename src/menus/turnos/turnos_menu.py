from ...ui.input import (
    pausar,
)
from ...ui.layout import menu_opciones
from ...ui.mensajes import (
    error,
)
from .turnos_vistas import (
    actualizar_turnos,
    agenda_diaria,
    crear_turno,
    turnos_por_fecha,
    turnos_por_paciente,
)


def menu_turnos():
    OPCIONES = [
        ("1", "➕", "Crear nuevo turno"),
        ("2", "📅", "Ver agenda diaria por médico"),
        ("3", "📅", "Ver turnos por fecha"),
        ("4", "📝", "Actualizar turnos"),
        ("5", "👤", "Ver turnos de un paciente"),
        ("0", "🔙", "Volver al menú principal"),
    ]

    while True:
        opcion = menu_opciones("Gestión de Turnos", OPCIONES)

        if opcion == "1":
            crear_turno()
        elif opcion == "2":
            agenda_diaria()
        elif opcion == "3":
            turnos_por_fecha()
        elif opcion == "4":
            actualizar_turnos()
        elif opcion == "5":
            turnos_por_paciente()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
