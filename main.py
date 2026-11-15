import archivo
import reportes
import tickets as gestor
import vista


def pedir_texto(mensaje, obligatorio=False):
    while True:
        texto = input(mensaje).strip()
        if texto or not obligatorio:
            return texto
        vista.mensaje_error("Este campo no puede estar vacío.")


def pedir_opcion(mensaje, opciones):
    while True:
        valor = input(f"{mensaje} ({'/'.join(opciones)}): ").strip().lower()
        if valor in opciones:
            return valor
        vista.mensaje_error(f"Opción inválida. Elegí entre: {', '.join(opciones)}.")


def pedir_categoria():
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
    try:
        return int(input("ID del ticket: "))
    except ValueError:
        vista.mensaje_error("El ID debe ser un número entero.")
        return None


def opcion_crear(lista):
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
    vista.mostrar_tabla(lista)


def opcion_buscar(lista):
    id_ticket = pedir_id()
    if id_ticket is None:
        return
    ticket = gestor.buscar_ticket(lista, id_ticket)
    if ticket is None:
        vista.mensaje_error(f"No existe el ticket #{id_ticket}.")
        return
    vista.mostrar_detalle(ticket)


def opcion_cambiar_estado(lista):
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
    campo = pedir_opcion("Filtrar por", ["prioridad", "estado", "categoria"])
    if campo == "categoria":
        valor = pedir_categoria()
    else:
        valores = gestor.PRIORIDADES if campo == "prioridad" else gestor.ESTADOS
        valor = pedir_opcion(campo.capitalize(), valores)
    vista.mostrar_tabla(gestor.filtrar_tickets(lista, campo, valor))


def opcion_ordenar(lista):
    vista.mostrar_tabla(gestor.ordenar_por_prioridad(lista))


def opcion_asignar_tecnico(lista):
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


def opcion_resumen(lista):
    vista.mostrar_resumen(reportes.generar_resumen(lista))


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
]


def mostrar_menu():
    vista.mostrar_titulo("Mesa de Ayuda")
    for numero, (texto, _) in enumerate(OPCIONES, start=1):
        print(f"{numero}. {texto}")
    print(f"{len(OPCIONES) + 1}. Salir")


def elegir_accion(opcion):
    try:
        numero = int(opcion)
    except ValueError:
        return None
    if 1 <= numero <= len(OPCIONES):
        return OPCIONES[numero - 1][1]
    return None


def main():
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
