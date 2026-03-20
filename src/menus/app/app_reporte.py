import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

AZUL_OSCURO = colors.HexColor("#1a3a5c")
AZUL_MEDIO = colors.HexColor("#2563a8")
AZUL_CLARO = colors.HexColor("#dbeafe")
GRIS_HEADER = colors.HexColor("#f1f5f9")
GRIS_LINEA = colors.HexColor("#cbd5e1")
VERDE = colors.HexColor("#16a34a")
ROJO = colors.HexColor("#dc2626")
BLANCO = colors.white


styles = getSampleStyleSheet()

estilo_titulo = ParagraphStyle(
    "titulo",
    parent=styles["Normal"],
    fontSize=22,
    textColor=BLANCO,
    fontName="Helvetica-Bold",
    spaceAfter=4,
)

estilo_subtitulo = ParagraphStyle(
    "subtitulo",
    parent=styles["Normal"],
    fontSize=10,
    textColor=colors.HexColor("#bfdbfe"),
    fontName="Helvetica",
)

estilo_seccion = ParagraphStyle(
    "seccion",
    parent=styles["Normal"],
    fontSize=12,
    textColor=AZUL_OSCURO,
    fontName="Helvetica-Bold",
    spaceBefore=14,
    spaceAfter=6,
)

estilo_normal = ParagraphStyle(
    "normal_custom",
    parent=styles["Normal"],
    fontSize=9,
    textColor=colors.HexColor("#334155"),
    fontName="Helvetica",
    leading=14,
)

estilo_destacado = ParagraphStyle(
    "destacado",
    parent=styles["Normal"],
    fontSize=11,
    textColor=AZUL_OSCURO,
    fontName="Helvetica-Bold",
)


def _separador():
    return HRFlowable(width="100%", thickness=1, color=GRIS_LINEA, spaceAfter=6, spaceBefore=2)


def _tabla_estilo_base(headers=True):
    base = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_HEADER]),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIS_LINEA),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if headers:
        base += [
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_MEDIO),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLANCO),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
        ]
    return base


def _kpi_tabla(items):
    """items: lista de (label, valor, color_valor, font_size_val)"""
    ancho = (A4[0] - 4 * cm) / len(items)
    celdas = []
    for label, valor, color_val, font_size_val in items:
        valueStyle = ParagraphStyle(
            "kv",
            fontSize=font_size_val,
            textColor=color_val,
            fontName="Helvetica-Bold",
            alignment=1,
        )
        valueParagraph = Paragraph(f"<b>{valor}</b>", valueStyle)
        labelStyle = ParagraphStyle(
            "kl",
            fontSize=8,
            textColor=colors.HexColor("#64748b"),
            fontName="Helvetica",
            alignment=1,
        )
        labelParagraph = Paragraph(label, labelStyle)

        celdaStyle = [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 0), (-1, -1), GRIS_HEADER),
            ("BOX", (0, 0), (-1, -1), 1, GRIS_LINEA),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ]
        celdas.append(
            Table(
                [[valueParagraph], [labelParagraph]],
                colWidths=[ancho - 0.4 * cm],
                style=TableStyle(celdaStyle),
            )
        )

    pdfTable = Table([celdas], colWidths=[ancho] * len(items))
    pdfStyles = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    pdfTable.setStyle(TableStyle(pdfStyles))
    return pdfTable


def _on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    canvas.setFillColor(AZUL_OSCURO)
    canvas.rect(0, h - 3.2 * cm, w, 3.2 * cm, fill=1, stroke=0)

    canvas.setFillColor(BLANCO)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(2 * cm, h - 1.6 * cm, "MedCLI — Reporte de Gestión Clínica")
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#bfdbfe"))
    canvas.drawString(
        2 * cm,
        h - 2.2 * cm,
        f"Generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
    )

    # Footer
    canvas.setFillColor(GRIS_HEADER)
    canvas.rect(0, 0, w, 1.2 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(2 * cm, 0.45 * cm, "MedCLI — Uso interno")
    canvas.drawRightString(w - 2 * cm, 0.45 * cm, f"Página {doc.page}")

    canvas.restoreState()


def generar_reporte(ruta_salida, ausentismo, promedios, top_medico, turnos_por_mes, tabla_medicos):
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        topMargin=3.8 * cm,
        bottomMargin=1.8 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    story = []
    ancho = A4[0] - 4 * cm

    story.append(Paragraph("Indicadores Generales", estilo_seccion))
    story.append(_separador())

    color_tasa = ROJO if ausentismo["tasa"] > 20 else VERDE
    kpis = [
        ("Total turnos (no cancelados)", str(ausentismo["total"]), AZUL_MEDIO, 20),
        ("Ausentes", str(ausentismo["ausentes"]), ROJO, 20),
        ("Tasa de ausentismo", f"{ausentismo['tasa']}%", color_tasa, 20),
    ]
    story.append(_kpi_tabla(kpis))
    story.append(Spacer(1, 0.5 * cm))

    if top_medico:
        story.append(Paragraph("Médico con Mayor Cantidad de Turnos Atendidos", estilo_seccion))
        story.append(_separador())
        story.append(
            _kpi_tabla(
                [
                    ("Nombre", top_medico["medico"], AZUL_OSCURO, 10),
                    ("Especialidad", top_medico["especialidad"], AZUL_MEDIO, 10),
                    ("Turnos atendidos", str(top_medico["cantidad"]), VERDE, 20),
                ]
            )
        )
        story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Turnos por Mes", estilo_seccion))
    story.append(_separador())

    if turnos_por_mes:
        data_mes = [["Mes", "Cantidad"]]
        for row in turnos_por_mes:
            anio, mes = row["mes"].split("-")
            meses = [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre",
            ]
            label = f"{meses[int(mes) - 1]} {anio}"
            data_mes.append([label, str(row["cantidad"])])

        t_mes = Table(data_mes, colWidths=[ancho * 0.7, ancho * 0.3])
        t_mes.setStyle(
            TableStyle(
                _tabla_estilo_base()
                + [
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                ]
            )
        )
        story.append(t_mes)
    else:
        story.append(Paragraph("Sin datos registrados.", estilo_normal))

    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Promedio de Duración de Consultas por Médico", estilo_seccion))
    story.append(_separador())

    if promedios:
        data_prom = [["Médico", "Consultas con duración real", "Promedio (min)"]]
        for row in promedios:
            data_prom.append([row["medico"], str(row["cantidad"]), str(row["promedio"])])

        t_prom = Table(data_prom, colWidths=[ancho * 0.5, ancho * 0.3, ancho * 0.2])
        t_prom.setStyle(
            TableStyle(
                _tabla_estilo_base()
                + [
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        story.append(t_prom)
    else:
        story.append(Paragraph("Sin consultas con duración real registrada.", estilo_normal))

    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("Resumen por Médico", estilo_seccion))
    story.append(_separador())

    if tabla_medicos:
        data_med = [["Médico", "Especialidad", "Total", "Atendidos", "Ausentes", "Cancelados"]]
        for row in tabla_medicos:
            data_med.append(
                [
                    row["nombre"],
                    row["especialidad"],
                    str(row["total"]),
                    str(row["atendidos"]),
                    str(row["ausentes"]),
                    str(row["cancelados"]),
                ]
            )

        col_w = [
            ancho * 0.25,
            ancho * 0.27,
            ancho * 0.12,
            ancho * 0.12,
            ancho * 0.12,
            ancho * 0.12,
        ]
        t_med = Table(data_med, colWidths=col_w)
        t_med.setStyle(
            TableStyle(
                _tabla_estilo_base()
                + [
                    ("ALIGN", (2, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        story.append(t_med)
    else:
        story.append(Paragraph("Sin médicos registrados.", estilo_normal))

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
