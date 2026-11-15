"""Lógica para crear, buscar, modificar y eliminar tickets."""

from datetime import datetime

from registro import log

PRIORIDADES = ["alta", "media", "baja"]
ESTADOS = ["abierto", "en_curso", "resuelto"]
SIGUIENTE_ESTADO = {"abierto": "en_curso", "en_curso": "resuelto"}
FORMATO_FECHA = "%Y-%m-%d %H:%M"
SIN_TECNICO = "sin asignar"
HORAS_SLA_ALTA = 8
CATEGORIAS = ["Hardware", "Redes", "Software", "Impresoras"]


def generar_id(tickets):
    """Calcula el próximo ID disponible.

    Args:
        tickets: Lista de tickets.

    Returns:
        El ID más alto más uno, o 1 si no hay tickets.
    """
    if not tickets:
        return 1
    return max(ticket["id"] for ticket in tickets) + 1


def crear_ticket(tickets, titulo, descripcion, prioridad, categoria):
    """Crea un ticket nuevo y lo agrega a la lista.

    Args:
        tickets: Lista de tickets.
        titulo: Título del ticket, no puede estar vacío.
        descripcion: Descripción del problema.
        prioridad: alta, media o baja.
        categoria: Una de las categorías de CATEGORIAS.

    Returns:
        El ticket creado.

    Raises:
        ValueError: Si el título está vacío o algún valor es inválido.
    """
    titulo = titulo.strip()
    prioridad = prioridad.strip().lower()
    if not titulo:
        raise ValueError("El título no puede estar vacío.")
    if prioridad not in PRIORIDADES:
        raise ValueError("La prioridad debe ser alta, media o baja.")
    if categoria not in CATEGORIAS:
        validas = ", ".join(CATEGORIAS)
        raise ValueError(f"La categoría debe ser una de: {validas}.")
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
    """Busca un ticket por su ID.

    Args:
        tickets: Lista de tickets.
        id_ticket: ID del ticket a buscar.

    Returns:
        El ticket encontrado, o None si no existe.
    """
    for ticket in tickets:
        if ticket["id"] == id_ticket:
            return ticket
    return None


def cambiar_estado(tickets, id_ticket):
    """Avanza el ticket de abierto a en_curso o a resuelto.

    Args:
        tickets: Lista de tickets.
        id_ticket: ID del ticket.

    Returns:
        El ticket modificado.

    Raises:
        LookupError: Si no existe el ticket.
        ValueError: Si el ticket ya está resuelto.
    """
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
    """Asigna un técnico a un ticket.

    Args:
        tickets: Lista de tickets.
        id_ticket: ID del ticket.
        tecnico: Nombre del técnico.

    Returns:
        El ticket modificado.

    Raises:
        ValueError: Si el nombre está vacío.
        LookupError: Si no existe el ticket.
    """
    tecnico = tecnico.strip()
    if not tecnico:
        raise ValueError("El nombre del técnico no puede estar vacío.")
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    ticket["tecnico"] = tecnico
    log.info(f"Ticket #{id_ticket} asignado a {tecnico}")
    return ticket


def editar_ticket(tickets, id_ticket, titulo="", descripcion="", prioridad=""):
    """Modifica título, descripción o prioridad de un ticket.

    Los campos que llegan vacíos no se modifican.

    Args:
        tickets: Lista de tickets.
        id_ticket: ID del ticket.
        titulo: Nuevo título.
        descripcion: Nueva descripción.
        prioridad: Nueva prioridad.

    Returns:
        Lista con los nombres de los campos modificados.

    Raises:
        LookupError: Si no existe el ticket.
        ValueError: Si la prioridad es inválida.
    """
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    prioridad = prioridad.strip().lower()
    if prioridad and prioridad not in PRIORIDADES:
        raise ValueError("La prioridad debe ser alta, media o baja.")
    cambios = []
    if titulo.strip():
        ticket["titulo"] = titulo.strip()
        cambios.append("titulo")
    if descripcion.strip():
        ticket["descripcion"] = descripcion.strip()
        cambios.append("descripcion")
    if prioridad:
        ticket["prioridad"] = prioridad
        cambios.append("prioridad")
    if cambios:
        log.info(f"Ticket #{id_ticket} editado ({', '.join(cambios)})")
    return cambios


def horas_abierto(ticket, ahora=None):
    """Calcula las horas que pasaron desde que se creó el ticket.

    Args:
        ticket: Ticket a evaluar.
        ahora: Fecha y hora de referencia; por defecto, la actual.

    Returns:
        Horas completas transcurridas, o None si la fecha es inválida.
    """
    if ahora is None:
        ahora = datetime.now()
    try:
        creado = datetime.strptime(ticket["fecha_creacion"], FORMATO_FECHA)
    except (KeyError, ValueError):
        return None
    return int((ahora - creado).total_seconds() // 3600)


def sla_vencido(ticket, ahora=None):
    """Indica si un ticket de prioridad alta superó el SLA.

    Args:
        ticket: Ticket a evaluar.
        ahora: Fecha y hora de referencia; por defecto, la actual.

    Returns:
        True si es alta, no está resuelto y supera HORAS_SLA_ALTA.
    """
    if ticket["prioridad"] != "alta" or ticket["estado"] == "resuelto":
        return False
    horas = horas_abierto(ticket, ahora)
    return horas is not None and horas > HORAS_SLA_ALTA


def tickets_vencidos(tickets):
    """Devuelve los tickets que tienen el SLA vencido.

    Args:
        tickets: Lista de tickets.

    Returns:
        Lista con los tickets vencidos.
    """
    return [ticket for ticket in tickets if sla_vencido(ticket)]


def filtrar_tickets(tickets, campo, valor):
    """Devuelve los tickets cuyo campo tiene el valor indicado.

    Args:
        tickets: Lista de tickets.
        campo: Nombre del campo a comparar.
        valor: Valor buscado.

    Returns:
        Lista con los tickets que coinciden.
    """
    return [ticket for ticket in tickets if ticket.get(campo) == valor]


def buscar_por_palabra(tickets, palabra):
    """Busca una palabra en el título o la descripción.

    La búsqueda no distingue mayúsculas de minúsculas.

    Args:
        tickets: Lista de tickets.
        palabra: Texto a buscar.

    Returns:
        Lista con los tickets que contienen la palabra.
    """
    palabra = palabra.strip().lower()
    return [
        ticket
        for ticket in tickets
        if palabra in ticket["titulo"].lower()
        or palabra in ticket["descripcion"].lower()
    ]


def ordenar_por_prioridad(tickets):
    """Ordena los tickets de prioridad alta a baja.

    Args:
        tickets: Lista de tickets.

    Returns:
        Nueva lista ordenada.
    """
    return sorted(
        tickets, key=lambda ticket: PRIORIDADES.index(ticket["prioridad"])
    )


def eliminar_ticket(tickets, id_ticket):
    """Elimina un ticket de la lista.

    Args:
        tickets: Lista de tickets.
        id_ticket: ID del ticket a eliminar.

    Returns:
        El ticket eliminado.

    Raises:
        LookupError: Si no existe el ticket.
    """
    ticket = buscar_ticket(tickets, id_ticket)
    if ticket is None:
        raise LookupError(f"No existe el ticket #{id_ticket}.")
    tickets.remove(ticket)
    log.info(f"Ticket #{id_ticket} eliminado")
    return ticket
