"""Configuración del registro de eventos en helpdesk.log."""

import logging

ARCHIVO_LOG = "helpdesk.log"


def configurar_logs(ruta=ARCHIVO_LOG):
    """Configura el logger que escribe en el archivo de logs.

    Args:
        ruta: Ruta del archivo de logs.

    Returns:
        El logger configurado.
    """
    logger = logging.getLogger("helpdesk")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    manejador = logging.FileHandler(ruta, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger


log = configurar_logs()
