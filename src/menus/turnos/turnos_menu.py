from ...ui.input import (
    pausar,
)
from ...ui.layout import menu_opciones
from ...ui.mensajes import (
    error,
)
from .turnos_vistas import (
    crear_turno,
    agenda_diaria,
    cambiar_estado,
    registrar_duracion,
    turnos_por_paciente,
)


def menu_turnos():
    OPCIONES = [
        ("1", "➕", "Crear nuevo turno"),
        ("2", "📅", "Ver agenda diaria por médico"),
        ("3", "🔄", "Cambiar estado de un turno"),
        ("4", "⏱️ ", "Registrar duración real de consulta"),
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
            cambiar_estado()
        elif opcion == "4":
            registrar_duracion()
        elif opcion == "5":
            turnos_por_paciente()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
