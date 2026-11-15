"""Funciones para mostrar tablas y mensajes en la consola."""

from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table

from tickets import horas_abierto, sla_vencido

init(autoreset=True)
consola = Console()

COLORES_PRIORIDAD = {"alta": "red", "media": "yellow", "baja": "green"}


def colorear_prioridad(prioridad):
    """Devuelve la prioridad con el color que le corresponde.

    Args:
        prioridad: alta, media o baja.

    Returns:
        Texto con formato de color de rich.
    """
    color = COLORES_PRIORIDAD.get(prioridad, "white")
    return f"[{color}]{prioridad}[/{color}]"


def mensaje_ok(texto):
    """Muestra un mensaje de éxito en verde.

    Args:
        texto: Mensaje a mostrar.
    """
    print(Fore.GREEN + texto)


def mensaje_error(texto):
    """Muestra un mensaje de error en rojo.

    Args:
        texto: Mensaje a mostrar.
    """
    print(Fore.RED + texto)


def mensaje_info(texto):
    """Muestra un mensaje informativo en celeste.

    Args:
        texto: Mensaje a mostrar.
    """
    print(Fore.CYAN + texto)


def mostrar_titulo(texto):
    """Muestra un título destacado.

    Args:
        texto: Título a mostrar.
    """
    print(Style.BRIGHT + Fore.CYAN + f"\n=== {texto} ===")


def formatear_tiempo(ticket):
    """Arma el texto de horas abierto y marca el SLA vencido.

    Args:
        ticket: Ticket a evaluar.

    Returns:
        Texto con las horas, "-" si está resuelto o "?" si no se sabe.
    """
    if ticket["estado"] == "resuelto":
        return "-"
    horas = horas_abierto(ticket)
    if horas is None:
        return "?"
    if sla_vencido(ticket):
        return f"[bold red]{horas} h VENCIDO[/bold red]"
    return f"{horas} h"


def mostrar_tabla(tickets):
    """Muestra una lista de tickets en una tabla.

    Args:
        tickets: Lista de tickets a mostrar.
    """
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
    tabla.add_column("Abierto hace", justify="right")
    for ticket in tickets:
        tabla.add_row(
            str(ticket["id"]),
            ticket["titulo"],
            colorear_prioridad(ticket["prioridad"]),
            ticket["estado"],
            ticket.get("categoria", "-"),
            ticket.get("tecnico", "sin asignar"),
            ticket["fecha_creacion"],
            formatear_tiempo(ticket),
        )
    consola.print(tabla)


def mostrar_conteo(titulo, conteo):
    """Muestra una tabla con cantidades por valor.

    Args:
        titulo: Título de la tabla.
        conteo: Diccionario con cada valor y su cantidad.
    """
    tabla = Table(title=titulo)
    tabla.add_column(titulo.split()[-1].capitalize())
    tabla.add_column("Cantidad", justify="right")
    for clave, cantidad in conteo.items():
        tabla.add_row(clave, str(cantidad))
    consola.print(tabla)


def mostrar_resumen(resumen):
    """Muestra el resumen de tickets por estado y prioridad.

    Args:
        resumen: Diccionario generado por reportes.generar_resumen.
    """
    mostrar_titulo(f"Resumen: {resumen['total']} tickets")
    mostrar_conteo("Tickets por estado", resumen["por_estado"])
    mostrar_conteo("Tickets por prioridad", resumen["por_prioridad"])


def mostrar_detalle(ticket):
    """Muestra todos los campos de un ticket.

    Args:
        ticket: Ticket a mostrar.
    """
    tabla = Table(title=f"Ticket #{ticket['id']}", show_header=False)
    tabla.add_column("Campo", style="bold")
    tabla.add_column("Valor")
    for campo, valor in ticket.items():
        tabla.add_row(campo, str(valor))
    consola.print(tabla)
