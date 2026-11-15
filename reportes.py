"""Resumen de tickets y exportación de reportes a CSV."""

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
    """Cuenta cuántos tickets hay para cada valor de un campo.

    Args:
        tickets: Lista de tickets.
        campo: Nombre del campo a contar.
        valores: Valores posibles del campo.

    Returns:
        Diccionario con cada valor y su cantidad.
    """
    conteo = {valor: 0 for valor in valores}
    for ticket in tickets:
        valor = ticket.get(campo)
        if valor in conteo:
            conteo[valor] += 1
    return conteo


def generar_resumen(tickets):
    """Genera el resumen de tickets por estado y prioridad.

    Args:
        tickets: Lista de tickets.

    Returns:
        Diccionario con el total y los conteos por estado y prioridad.
    """
    return {
        "total": len(tickets),
        "por_estado": contar_por_campo(tickets, "estado", ESTADOS),
        "por_prioridad": contar_por_campo(tickets, "prioridad", PRIORIDADES),
    }


def fila_reporte(ticket):
    """Arma la fila del reporte CSV para un ticket.

    Args:
        ticket: Ticket a convertir.

    Returns:
        Diccionario con una clave por cada columna del reporte.
    """
    fila = {columna: ticket.get(columna, "") for columna in COLUMNAS}
    horas = horas_abierto(ticket)
    fila["horas_abierto"] = "" if horas is None else horas
    fila["sla_vencido"] = "si" if sla_vencido(ticket) else "no"
    return fila


def exportar_csv(tickets, ruta=ARCHIVO_REPORTE):
    """Exporta los tickets a un archivo CSV para abrir en Excel.

    Args:
        tickets: Lista de tickets.
        ruta: Ruta del archivo CSV a generar.

    Returns:
        La ruta del archivo generado.

    Raises:
        OSError: Si no se puede escribir el archivo.
    """
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
