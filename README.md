# Mesa de Ayuda

Sistema de tickets de soporte técnico (Helpdesk) por consola, hecho en Python.

Permite que el equipo de soporte registre los problemas que reportan los usuarios
(la impresora no imprime, no hay acceso a la VPN, una PC no enciende) como tickets,
con una prioridad (alta, media o baja) y un estado que cambia a medida que se
trabaja (abierto → en_curso → resuelto).

## Requisitos

- Python 3.10 o superior
- Librerías externas (en `requirements.txt`):
  - [rich](https://pypi.org/project/rich/): tablas y colores en la consola
  - [colorama](https://pypi.org/project/colorama/): colores en los mensajes

## Instalación

```bash
git clone <url-del-repositorio>
cd mesa_de_ayuda
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

Al iniciar se cargan los tickets desde `tickets.json`. Si el archivo no existe,
se crea vacío. Cada acción importante queda registrada en `helpdesk.log`.

## Menú

### Versión básica

| Opción | Descripción |
|---|---|
| Crear ticket | Pide título, descripción, prioridad y categoría. El ID, el estado `abierto` y la fecha se asignan solos. |
| Listar tickets | Muestra todos los tickets en una tabla. |
| Buscar ticket por ID | Muestra todos los datos de un ticket. |
| Cambiar estado | Pasa un ticket de `abierto` a `en_curso`, o de `en_curso` a `resuelto`. |
| Eliminar ticket | Pide confirmación antes de borrar. |
| Salir | Guarda los tickets y termina el programa. |

### Mejoras opcionales implementadas

| Mejora | Descripción |
|---|---|
| Filtrar | Lista solo los tickets de una prioridad, un estado o una categoría. |
| Ordenar | Muestra primero los tickets de prioridad alta. |
| Colores | Prioridad alta en rojo, media en amarillo y baja en verde. |
| Técnico asignado | Nuevo campo `tecnico` y opción para asignarlo. |
| Categorías | Nuevo campo `categoria` (Hardware, Redes, Software, Impresoras). |
| Resumen | Cantidad de tickets por estado y por prioridad. |
| Editar ticket | Modifica título, descripción o prioridad. |
| Buscar por palabra | Busca texto en el título o la descripción. |
| Tiempo abierto | Muestra hace cuántas horas está abierto cada ticket. |
| SLA | Marca como vencidos los tickets de prioridad alta con más de 8 horas abiertos. |
| Exportar | Genera `reporte_tickets.csv` (separado por `;`) para abrir en Excel. |

## Estructura del proyecto

```
mesa_de_ayuda/
├── .gitignore         # Archivos ignorados por git
├── main.py            # Menú y entrada del usuario
├── tickets.py         # Lógica de los tickets
├── archivo.py         # Leer y guardar tickets.json
├── registro.py        # Configuración de logs (helpdesk.log)
├── reportes.py        # Resumen y exportación a CSV
├── vista.py           # Tablas y mensajes en consola
├── requirements.txt   # Librerías externas
└── README.md          # Documentación
```

Los archivos `tickets.json`, `helpdesk.log` y `reporte_tickets.csv` se generan
al usar el programa.

## Estructura de un ticket

```json
{
    "id": 1,
    "titulo": "No hay acceso a la VPN",
    "descripcion": "Error de autenticación desde las 9 hs",
    "prioridad": "alta",
    "estado": "abierto",
    "fecha_creacion": "2026-11-03 09:15",
    "tecnico": "sin asignar",
    "categoria": "Redes"
}
```

## Ejemplo de log

```
2026-11-03 09:40:12 | INFO | Ticket #1 creado (prioridad alta)
2026-11-03 10:05:30 | INFO | Ticket #1 cambió a en_curso
```

## Manejo de errores

- IDs no numéricos al buscar, cambiar estado, editar o eliminar.
- Títulos vacíos, prioridades y categorías inválidas.
- Opciones de menú inexistentes.
- `tickets.json` inexistente (se crea) o dañado (se inicia vacío).
- Errores al leer o escribir archivos.
- Interrupción con Ctrl+C.
