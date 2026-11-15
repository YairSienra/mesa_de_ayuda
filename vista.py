from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

init(autoreset=True)
consola = Console()

COLORES_PRIORIDAD = {"alta": "red", "media": "yellow", "baja": "green"}


def colorear_prioridad(prioridad):
    color = COLORES_PRIORIDAD.get(prioridad, "white")
    return f"[{color}]{prioridad}[/{color}]"


def mensaje_ok(texto):
    print(Fore.GREEN + texto)


def mensaje_error(texto):
    print(Fore.RED + texto)


def mensaje_info(texto):
    print(Fore.CYAN + texto)


def mostrar_titulo(texto):
    print(Style.BRIGHT + Fore.CYAN + f"\n=== {texto} ===")


def mostrar_tabla(tickets):
    if not tickets:
        mensaje_info("No hay tickets para mostrar.")
        return
    tabla = Table(title="Tickets")
    tabla.add_column("ID", justify="right")
    tabla.add_column("Título")
    tabla.add_column("Prioridad")
    tabla.add_column("Estado")
    tabla.add_column("Categoría")
    tabla.add_column("Técnico")
    tabla.add_column("Creado")
    for ticket in tickets:
        tabla.add_row(
            str(ticket["id"]),
            ticket["titulo"],
            colorear_prioridad(ticket["prioridad"]),
            ticket["estado"],
            ticket.get("categoria", "-"),
            ticket.get("tecnico", "sin asignar"),
            ticket["fecha_creacion"],
        )
    consola.print(tabla)


def mostrar_detalle(ticket):
    tabla = Table(title=f"Ticket #{ticket['id']}", show_header=False)
    tabla.add_column("Campo", style="bold")
    tabla.add_column("Valor")
    for campo, valor in ticket.items():
        tabla.add_row(campo, str(valor))
    consola.print(tabla)
