from .database.models import ObraSocial, Paciente, Medico, Turno
from .database.connection import connect_db, db

SEP = "─" * 80


def tabla(titulo: str):
    print(f"\n{'═' * 80}")
    print(f"  {titulo}")
    print("═" * 80)


def show_obras_sociales():
    tabla("OBRAS SOCIALES")
    print(f"{'ID':<5} {'Nombre'}")
    print(SEP)
    for o in ObraSocial.select().order_by(ObraSocial.id):
        print(f"{o.id:<5} {o.nombre}")
    print(f"\nTotal: {ObraSocial.select().count()} registros")


def show_medicos():
    tabla("MÉDICOS")
    print(f"{'ID':<5} {'Nombre':<28} {'Especialidad':<25} {'Matrícula':<12} {'Activo'}")
    print(SEP)
    for m in Medico.select().order_by(Medico.id):
        activo = "✅" if m.activo else "❌"
        print(
            f"{m.id:<5} {m.nombre:<28} {m.especialidad:<25} {m.matricula:<12} {activo}"
        )
    print(f"\nTotal: {Medico.select().count()} registros")


def show_pacientes():
    tabla("PACIENTES")
    print(f"{'ID':<5} {'Nombre':<28} {'CUIT':<16} {'Nacimiento':<12} {'Obra Social'}")
    print(SEP)

    query = Paciente.select(Paciente, ObraSocial).join(ObraSocial).order_by(Paciente.id)
    for p in query:
        print(
            f"{p.id:<5} {p.nombre:<28} {p.cuit:<16} "
            f"{p.fecha_nacimiento:<12} {p.obra_social.nombre}"
        )
    print(f"\nTotal: {Paciente.select().count()} registros")


def show_turnos():
    tabla("TURNOS")
    print(
        f"{'ID':<5} {'Fecha':<12} {'Hora':<7} {'Estado':<12} "
        f"{'ET':<4} {'Dur.':<6} {'Dur.R':<6} {'Médico':<25} {'Paciente':<25} {'Notas'}"
    )
    print(SEP)

    query = (
        Turno.select(Turno, Medico, Paciente)
        .join(Medico)
        .switch(Turno)
        .join(Paciente)
        .order_by(Turno.fecha, Turno.horario)
    )

    count = 0
    for t in query:
        et = "SI" if t.entre_turno else "NO"
        dur_real = str(t.duracion_real) if t.duracion_real else "-"
        medico = t.medico.nombre
        paciente = t.paciente.nombre
        notas = (t.notas or "")[:30]
        print(
            f"{t.id:<5} {t.fecha:<12} {t.horario:<7} {t.estado:<12} "
            f"{et:<4} {t.duracion_min:<6} {dur_real:<6} {medico:<25} {paciente:<25} {notas}"
        )
        count += 1

    print(f"\nTotal: {count} registros")

    # resumen por estado
    print("\n  Resumen por estado:")
    for estado in ["RESERVADO", "ATENDIDO", "CANCELADO", "AUSENTE"]:
        n = Turno.select().where(Turno.estado == estado).count()
        print(f"    {estado:<12}: {n}")


def main():
    connect_db()

    show_obras_sociales()
    show_medicos()
    show_pacientes()
    show_turnos()

    db.close()
    print(f"\n{'═' * 80}\n")


main()
