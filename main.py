"""Menú principal de la Mesa de Ayuda por consola."""

import archivo
import reportes
import tickets as gestor
import vista


def pedir_texto(mensaje, obligatorio=False):
    """Pide un texto al usuario.

    Args:
        mensaje: Texto que se muestra al pedir el dato.
        obligatorio: Si es True, vuelve a pedir mientras esté vacío.

    Returns:
        El texto ingresado, sin espacios al principio ni al final.
    """
    while True:
        texto = input(mensaje).strip()
        if texto or not obligatorio:
            return texto
        vista.mensaje_error("Este campo no puede estar vacío.")


def pedir_opcion(mensaje, opciones):
    """Pide al usuario que elija un valor de una lista.

    Args:
        mensaje: Texto que se muestra al pedir el dato.
        opciones: Lista de valores válidos.

    Returns:
        El valor elegido, en minúsculas.
    """
    while True:
        valor = input(f"{mensaje} ({'/'.join(opciones)}): ").strip().lower()
        if valor in opciones:
            return valor
        validas = ", ".join(opciones)
        vista.mensaje_error(f"Opción inválida. Elegí entre: {validas}.")


def pedir_categoria():
    """Muestra las categorías numeradas y pide elegir una.

    Returns:
        El nombre de la categoría elegida.
    """
    for numero, categoria in enumerate(gestor.CATEGORIAS, start=1):
        print(f"  {numero}. {categoria}")
    while True:
        try:
            numero = int(input("Categoría (número): "))
        except ValueError:
            vista.mensaje_error("Ingresá un número.")
            continue
        if 1 <= numero <= len(gestor.CATEGORIAS):
            return gestor.CATEGORIAS[numero - 1]
        vista.mensaje_error("Número fuera de rango.")


def pedir_id():
    """Pide el ID de un ticket y lo convierte a entero.

    Returns:
        El ID como entero, o None si no es un número válido.
    """
    try:
        return int(input("ID del ticket: "))
    except ValueError:
        vista.mensaje_error("El ID debe ser un número entero.")
        return None


def opcion_crear(lista):
    """Pide los datos de un ticket nuevo y lo agrega a la lista.

    Args:
        lista: Lista de tickets.
    """
    titulo = pedir_texto("Título: ", obligatorio=True)
    descripcion = pedir_texto("Descripción: ")
    prioridad = pedir_opcion("Prioridad", gestor.PRIORIDADES)
    categoria = pedir_categoria()
    try:
        ticket = gestor.crear_ticket(
            lista, titulo, descripcion, prioridad, categoria
        )
    except ValueError as error:
        vista.mensaje_error(str(error))
        return
    archivo.guardar_tickets(lista)
    vista.mensaje_ok(f"Ticket #{ticket['id']} creado.")


def opcion_listar(lista):
    """Muestra todos los tickets en una tabla.

    Args:
        lista: Lista de tickets.
    """
    vista.mostrar_tabla(lista)


def opcion_buscar(lista):
    """Pide un ID y muestra todos los datos de ese ticket.

    Args:
        lista: Lista de tickets.
    """
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    ticket = gestor.buscar_ticket(lista, id_ticket)
    if ticket is None:
        vista.mensaje_error(f"No existe el ticket #{id_ticket}.")
        return
    vista.mostrar_detalle(ticket)


def opcion_cambiar_estado(lista):
    """Pide un ID y avanza el ticket al siguiente estado.

    Args:
        lista: Lista de tickets.
    """
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    try:
        ticket = gestor.cambiar_estado(lista, id_ticket)
    except (LookupError, ValueError) as error:
        vista.mensaje_error(str(error))
        return
    archivo.guardar_tickets(lista)
    vista.mensaje_ok(f"Ticket #{id_ticket} ahora está {ticket['estado']}.")


def opcion_eliminar(lista):
    """Pide un ID y elimina el ticket previa confirmación.

    Args:
        lista: Lista de tickets.
    """
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    ticket = gestor.buscar_ticket(lista, id_ticket)
    if ticket is None:
        vista.mensaje_error(f"No existe el ticket #{id_ticket}.")
        return
    confirmacion = pedir_opcion(
        f"¿Eliminar el ticket #{id_ticket} '{ticket['titulo']}'?", ["s", "n"]
    )
    if confirmacion != "s":
        vista.mensaje_info("Eliminación cancelada.")
        return
    gestor.eliminar_ticket(lista, id_ticket)
    archivo.guardar_tickets(lista)
    vista.mensaje_ok(f"Ticket #{id_ticket} eliminado.")


def opcion_filtrar(lista):
    """Muestra los tickets de una prioridad, estado o categoría.

    Args:
        lista: Lista de tickets.
    """
    campo = pedir_opcion("Filtrar por", ["prioridad", "estado", "categoria"])
    if campo == "categoria":
        valor = pedir_categoria()
    else:
        if campo == "prioridad":
            valores = gestor.PRIORIDADES
        else:
            valores = gestor.ESTADOS
        valor = pedir_opcion(campo.capitalize(), valores)
    vista.mostrar_tabla(gestor.filtrar_tickets(lista, campo, valor))


def opcion_ordenar(lista):
    """Muestra los tickets ordenados de prioridad alta a baja.

    Args:
        lista: Lista de tickets.
    """
    vista.mostrar_tabla(gestor.ordenar_por_prioridad(lista))


def opcion_asignar_tecnico(lista):
    """Pide un ID y el nombre del técnico a asignar.

    Args:
        lista: Lista de tickets.
    """
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    tecnico = pedir_texto("Nombre del técnico: ", obligatorio=True)
    try:
        gestor.asignar_tecnico(lista, id_ticket, tecnico)
    except (LookupError, ValueError) as error:
        vista.mensaje_error(str(error))
        return
    archivo.guardar_tickets(lista)
    vista.mensaje_ok(f"Ticket #{id_ticket} asignado a {tecnico}.")


def opcion_editar(lista):
    """Permite modificar título, descripción o prioridad.

    Args:
        lista: Lista de tickets.
    """
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    ticket = gestor.buscar_ticket(lista, id_ticket)
    if ticket is None:
        vista.mensaje_error(f"No existe el ticket #{id_ticket}.")
        return
    vista.mensaje_info("Dejá vacío el campo que no quieras cambiar.")
    titulo = pedir_texto(f"Título [{ticket['titulo']}]: ")
    descripcion = pedir_texto(f"Descripción [{ticket['descripcion']}]: ")
    prioridad = pedir_texto(f"Prioridad [{ticket['prioridad']}]: ")
    try:
        cambios = gestor.editar_ticket(
            lista, id_ticket, titulo, descripcion, prioridad
        )
    except (LookupError, ValueError) as error:
        vista.mensaje_error(str(error))
        return
    if not cambios:
        vista.mensaje_info("No se realizaron cambios.")
        return
    archivo.guardar_tickets(lista)
    vista.mensaje_ok(f"Ticket #{id_ticket} actualizado.")


def opcion_buscar_palabra(lista):
    """Muestra los tickets que contienen una palabra.

    Args:
        lista: Lista de tickets.
    """
    palabra = pedir_texto("Palabra a buscar: ", obligatorio=True)
    vista.mostrar_tabla(gestor.buscar_por_palabra(lista, palabra))


def opcion_vencidos(lista):
    """Muestra los tickets con el SLA vencido.

    Args:
        lista: Lista de tickets.
    """
    vencidos = gestor.tickets_vencidos(lista)
    if not vencidos:
        vista.mensaje_ok("No hay tickets con SLA vencido.")
        return
    vista.mensaje_error(f"Hay {len(vencidos)} ticket(s) con SLA vencido.")
    vista.mostrar_tabla(vencidos)


def opcion_resumen(lista):
    """Muestra la cantidad de tickets por estado y prioridad.

    Args:
        lista: Lista de tickets.
    """
    vista.mostrar_resumen(reportes.generar_resumen(lista))


def opcion_exportar(lista):
    """Exporta todos los tickets a un archivo CSV.

    Args:
        lista: Lista de tickets.
    """
    if not lista:
        vista.mensaje_info("No hay tickets para exportar.")
        return
    try:
        ruta = reportes.exportar_csv(lista)
    except OSError as error:
        vista.mensaje_error(str(error))
        return
    vista.mensaje_ok(f"Reporte generado en {ruta}.")


OPCIONES = [
    ("Crear ticket", opcion_crear),
    ("Listar tickets", opcion_listar),
    ("Buscar ticket por ID", opcion_buscar),
    ("Cambiar estado", opcion_cambiar_estado),
    ("Eliminar ticket", opcion_eliminar),
    ("Filtrar por prioridad, estado o categoría", opcion_filtrar),
    ("Listar ordenados por prioridad", opcion_ordenar),
    ("Asignar técnico", opcion_asignar_tecnico),
    ("Ver resumen", opcion_resumen),
    ("Editar ticket", opcion_editar),
    ("Buscar por palabra", opcion_buscar_palabra),
    ("Ver tickets con SLA vencido", opcion_vencidos),
    ("Exportar reporte CSV", opcion_exportar),
]


def mostrar_menu():
    """Muestra las opciones del menú principal."""
    vista.mostrar_titulo("Mesa de Ayuda")
    for numero, (texto, _) in enumerate(OPCIONES, start=1):
        print(f"{numero}. {texto}")
    print(f"{len(OPCIONES) + 1}. Salir")


def elegir_accion(opcion):
    """Devuelve la función asociada a la opción elegida.

    Args:
        opcion: Texto ingresado por el usuario.

    Returns:
        La función de la opción, o None si la opción no es válida.
    """
    try:
        numero = int(opcion)
    except ValueError:
        return None
    if 1 <= numero <= len(OPCIONES):
        return OPCIONES[numero - 1][1]
    return None


def main():
    """Carga los tickets y repite el menú hasta elegir Salir."""
    lista = archivo.cargar_tickets()
    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()
        if opcion == str(len(OPCIONES) + 1):
            archivo.guardar_tickets(lista)
            vista.mensaje_ok("Tickets guardados. ¡Hasta luego!")
            break
        accion = elegir_accion(opcion)
        if accion is None:
            vista.mensaje_error("Opción inválida.")
            continue
        accion(lista)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido.")
