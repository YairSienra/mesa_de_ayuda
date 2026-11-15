from datetime import datetime

from registro import log

PRIORIDADES = ["alta", "media", "baja"]
ESTADOS = ["abierto", "en_curso", "resuelto"]
SIGUIENTE_ESTADO = {"abierto": "en_curso", "en_curso": "resuelto"}
FORMATO_FECHA = "%Y-%m-%d %H:%M"
SIN_TECNICO = "sin asignar"
CATEGORIAS = ["Hardware", "Redes", "Software", "Impresoras"]


def generar_id(tickets):
    if not tickets:
        return 1
    return max(ticket["id"] for ticket in tickets) + 1


def crear_ticket(tickets, titulo, descripcion, prioridad, categoria):
    titulo = titulo.strip()
    prioridad = prioridad.strip().lower()
    if not titulo:
        raise ValueError("El título no puede estar vacío.")
    if prioridad not in PRIORIDADES:
        raise ValueError("La prioridad debe ser alta, media o baja.")
    if categoria not in CATEGORIAS:
        raise ValueError(f"La categoría debe ser una de: {', '.join(CATEGORIAS)}.")
    ticket = {
        "id": generar_id(tickets),
        "titulo": titulo,
        "descripcion": descripcion.strip(),
        "prioridad": prioridad,
        "estado": "abierto",
        "fecha_creacion": datetime.now().strftime(FORMATO_FECHA),
        "tecnico": SIN_TECNICO,
        "categoria": categoria,
    }
    tickets.append(ticket)
    log.info(f"Ticket #{ticket['id']} creado (prioridad {prioridad})")
    return ticket


def buscar_ticket(tickets, id_ticket):
    for ticket in tickets:
        if ticket["id"] == id_ticket:
            return ticket
    return None


def cambiar_estado(tickets, id_ticket):
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    estado_actual = ticket["estado"]
    if estado_actual not in SIGUIENTE_ESTADO:
        raise ValueError(f"El ticket #{id_ticket} ya está resuelto.")
    ticket["estado"] = SIGUIENTE_ESTADO[estado_actual]
    log.info(f"Ticket #{id_ticket} cambió a {ticket['estado']}")
    return ticket


def asignar_tecnico(tickets, id_ticket, tecnico):
    tecnico = tecnico.strip()
    if not tecnico:
        raise ValueError("El nombre del técnico no puede estar vacío.")
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    ticket["tecnico"] = tecnico
    log.info(f"Ticket #{id_ticket} asignado a {tecnico}")
    return ticket


def filtrar_tickets(tickets, campo, valor):
    return [ticket for ticket in tickets if ticket.get(campo) == valor]


def ordenar_por_prioridad(tickets):
    return sorted(tickets, key=lambda ticket: PRIORIDADES.index(ticket["prioridad"]))


def eliminar_ticket(tickets, id_ticket):
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    tickets.remove(ticket)
    log.info(f"Ticket #{id_ticket} eliminado")
    return ticket
