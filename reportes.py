from tickets import ESTADOS, PRIORIDADES


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
