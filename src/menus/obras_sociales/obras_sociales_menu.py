from ...ui.input import pausar
from ...ui.layout import menu_opciones
from ...ui.mensajes import error
from .obras_sociales_vistas import (
    crear_obra_social,
    editar_obra_social,
    eliminar_obra_social,
    listar_obras_sociales,
)


def menu_obras_sociales():
    OPCIONES = [
        ("1", "📋", "Listar todas las obras sociales"),
        ("2", "➕", "Registrar nueva obra social"),
        ("3", "✏️ ", "Editar obra social"),
        ("4", "🗑️ ", "Eliminar obra social"),
        ("0", "🔙", "Volver al menú principal"),
    ]

    while True:
        opcion = menu_opciones("Gestión de Obras Sociales", OPCIONES)

        if opcion == "1":
            listar_obras_sociales()
        elif opcion == "2":
            crear_obra_social()
        elif opcion == "3":
            editar_obra_social()
        elif opcion == "4":
            eliminar_obra_social()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
