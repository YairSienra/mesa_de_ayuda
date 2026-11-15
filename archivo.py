"""Lectura y guardado de los tickets en el archivo JSON."""

import json
import os

ARCHIVO_TICKETS = "tickets.json"


def crear_archivo_si_no_existe(ruta=ARCHIVO_TICKETS):
    """Crea el archivo de tickets vacío si todavía no existe.

    Args:
        ruta: Ruta del archivo JSON de tickets.
    """
    if not os.path.exists(ruta):
        guardar_tickets([], ruta)


def cargar_tickets(ruta=ARCHIVO_TICKETS):
    """Carga la lista de tickets desde el archivo JSON.

    Si el archivo no existe se crea vacío. Si está dañado o no se
    puede leer, se devuelve una lista vacía.

    Args:
        ruta: Ruta del archivo JSON de tickets.

    Returns:
        Lista de diccionarios con los tickets.
    """
    crear_archivo_si_no_existe(ruta)
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except json.JSONDecodeError:
        print(f"El archivo {ruta} está dañado. Se inicia con una lista vacía.")
        return []
    except OSError as error:
        print(f"No se pudo leer {ruta}: {error}")
        return []
    if not isinstance(datos, list):
        return []
    return datos


def guardar_tickets(tickets, ruta=ARCHIVO_TICKETS):
    """Guarda la lista de tickets en el archivo JSON.

    Args:
        tickets: Lista de tickets a guardar.
        ruta: Ruta del archivo JSON de tickets.

    Returns:
        True si se guardó correctamente, False si hubo un error.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(tickets, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        print(f"No se pudo guardar {ruta}: {error}")
        return False
