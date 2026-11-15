import csv

from registro import log
from tickets import ESTADOS, PRIORIDADES, horas_abierto, sla_vencido

ARCHIVO_REPORTE = "reporte_tickets.csv"
COLUMNAS = [
    "id",
    "titulo",
    "descripcion",
    "prioridad",
    "estado",
    "categoria",
    "tecnico",
    "fecha_creacion",
    "horas_abierto",
    "sla_vencido",
]


def contar_por_campo(tickets, campo, valores):
    conteo = {valor: 0 for valor in valores}
    for ticket in tickets:
        valor = ticket.get(campo)
        if valor in conteo:
            conteo[valor] += 1
    return conteo


def generar_resumen(tickets):
    return {
        "total": len(tickets),
        "por_estado": contar_por_campo(tickets, "estado", ESTADOS),
        "por_prioridad": contar_por_campo(tickets, "prioridad", PRIORIDADES),
    }


def fila_reporte(ticket):
    fila = {columna: ticket.get(columna, "") for columna in COLUMNAS}
    horas = horas_abierto(ticket)
    fila["horas_abierto"] = "" if horas is None else horas
    fila["sla_vencido"] = "si" if sla_vencido(ticket) else "no"
    return fila


def exportar_csv(tickets, ruta=ARCHIVO_REPORTE):
    try:
        with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=COLUMNAS, delimiter=";"
            )
            escritor.writeheader()
            for ticket in tickets:
                escritor.writerow(fila_reporte(ticket))
    except OSError as error:
        mensaje = f"No se pudo crear el reporte {ruta}: {error}"
        raise OSError(mensaje) from error
    log.info(f"Reporte exportado a {ruta} ({len(tickets)} tickets)")
    return ruta
