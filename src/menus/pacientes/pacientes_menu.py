from ...ui.input import pausar
from ...ui.layout import menu_opciones
from ...ui.mensajes import error
from .pacientes_vistas import (
    buscar_paciente,
    crear_paciente,
    editar_paciente,
    eliminar_paciente,
    listar_pacientes,
)


def menu_pacientes():
    OPCIONES = [
        ("1", "📋", "Listar todos los pacientes"),
        ("2", "🔍", "Buscar paciente"),
        ("3", "➕", "Registrar nuevo paciente"),
        ("4", "✏️ ", "Editar paciente"),
        ("5", "🗑️ ", "Eliminar paciente"),
        ("0", "🔙", "Volver al menú principal"),
    ]

    while True:
        opcion = menu_opciones("Gestión de Pacientes", OPCIONES)

        if opcion == "1":
            listar_pacientes()
        elif opcion == "2":
            buscar_paciente()
        elif opcion == "3":
            crear_paciente()
        elif opcion == "4":
            editar_paciente()
        elif opcion == "5":
            eliminar_paciente()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
