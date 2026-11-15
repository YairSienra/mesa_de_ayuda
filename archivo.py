import json
import os

ARCHIVO_TICKETS = "tickets.json"


def crear_archivo_si_no_existe(ruta=ARCHIVO_TICKETS):
    if not os.path.exists(ruta):
        guardar_tickets([], ruta)


def cargar_tickets(ruta=ARCHIVO_TICKETS):
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
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(tickets, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError as error:
        print(f"No se pudo guardar {ruta}: {error}")
        return False
