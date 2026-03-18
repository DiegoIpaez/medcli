from ...database.models import Medico, Turno, TurnoEstado


def obtener_tasa_ausentismo():
    estado_cancelado = _estado_por_nombre("CANCELADO")
    estado_ausente = _estado_por_nombre("AUSENTE")
    total = Turno.select().where(Turno.estado != estado_cancelado).count()
    ausentes = Turno.select().where(Turno.estado == estado_ausente).count()
    tasa = (ausentes / total * 100) if total else 0
    return {"total": total, "ausentes": ausentes, "tasa": round(tasa, 2)}


def obtener_promedio_duracion_por_medico():
    medicos = Medico.select().order_by(Medico.nombre)
    resultado = []
    for m in medicos:
        turnos = Turno.select().where((Turno.medico == m) & (Turno.duracion_real.is_null(False)))
        if turnos:
            promedio = sum(t.duracion_real for t in turnos) / len(turnos)
            resultado.append(
                {
                    "medico": m.nombre,
                    "promedio": round(promedio, 1),
                    "cantidad": len(turnos),
                }
            )
    return resultado


def obtener_medico_por_turnos_atentidos():
    medicos = Medico.select()
    if not medicos:
        return None
    estado_atendido = _estado_por_nombre("ATENDIDO")
    mejor = max(
        medicos,
        key=lambda m: Turno.select().where((Turno.medico == m) & (Turno.estado == estado_atendido)).count(),
    )
    cantidad = Turno.select().where((Turno.medico == mejor) & (Turno.estado == estado_atendido)).count()
    return {
        "medico": mejor.nombre,
        "especialidad": mejor.especialidad,
        "cantidad": cantidad,
    }


def obtener_turnos_por_mes():
    turnos = Turno.select()
    conteo = {}
    for t in turnos:
        clave = t.fecha.strftime("%Y-%m")
        conteo[clave] = conteo.get(clave, 0) + 1
    return [{"mes": k, "cantidad": v} for k, v in sorted(conteo.items())]


def obtener_medicos():
    medicos = Medico.select().order_by(Medico.nombre)
    filas = []
    estado_atendido = _estado_por_nombre("ATENDIDO")
    estado_ausente = _estado_por_nombre("AUSENTE")
    estado_cancelado = _estado_por_nombre("CANCELADO")
    for m in medicos:
        total = Turno.select().where(Turno.medico == m).count()
        atendidos = Turno.select().where((Turno.medico == m) & (Turno.estado == estado_atendido)).count()
        ausentes = Turno.select().where((Turno.medico == m) & (Turno.estado == estado_ausente)).count()
        cancelados = Turno.select().where((Turno.medico == m) & (Turno.estado == estado_cancelado)).count()
        filas.append(
            {
                "nombre": m.nombre,
                "especialidad": m.especialidad,
                "total": total,
                "atendidos": atendidos,
                "ausentes": ausentes,
                "cancelados": cancelados,
            }
        )
    return sorted(filas, key=lambda x: x["total"], reverse=True)


def _estado_por_nombre(nombre):
    return TurnoEstado.get(TurnoEstado.nombre == nombre)
