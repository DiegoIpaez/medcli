from ...ui.input import pausar
from ...ui.layout import menu_opciones
from ...ui.mensajes import error
from .medicos_vistas import (
    alta_medico,
    buscar_medico,
    editar_medico,
    eliminar_medico,
    mostrar_medicos,
)


def menu_medicos():
    OPCIONES = [
        ("1", "📋", "Listar todos los médicos"),
        ("2", "🟢", "Listar médicos activos"),
        ("3", "🔍", "Buscar médico"),
        ("4", "➕", "Registrar nuevo médico"),
        ("5", "✏️ ", "Editar médico"),
        ("6", "🗑️ ", "Eliminar médico"),
        ("0", "🔙", "Volver al menú principal"),
    ]

    while True:
        opcion = menu_opciones("Gestión de Médicos", OPCIONES)

        if opcion == "1":
            mostrar_medicos(False)
        elif opcion == "2":
            mostrar_medicos(True)
        elif opcion == "3":
            buscar_medico()
        elif opcion == "4":
            alta_medico()
        elif opcion == "5":
            editar_medico()
        elif opcion == "6":
            eliminar_medico()
        elif opcion == "0":
            break
        else:
            error("Opción inválida.")
            pausar()
