from ...ui.input import pausar
from ...ui.layout import menu_opciones
from ...ui.mensajes import error
from .especialidades_vistas import (
    crear_especialidad,
    editar_especialidad,
    eliminar_especialidad,
    listar_especialidades,
)


def menu_especialidades():
    OPCIONES = [
        ("1", "📋", "Listar todas las especialidades"),
        ("2", "➕", "Registrar nueva especialidad"),
        ("3", "✏️ ", "Editar especialidad"),
        ("4", "🗑️ ", "Eliminar especialidad"),
        ("0", "🔙", "Volver al menú principal"),
    ]

    while True:
        opcion = menu_opciones("Gestión de Especialidades", OPCIONES)

        if opcion == "1":
            listar_especialidades()
        elif opcion == "2":
            crear_especialidad()
        elif opcion == "3":
            editar_especialidad()
        elif opcion == "4":
            eliminar_especialidad()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
