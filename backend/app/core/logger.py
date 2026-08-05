import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logger():
    logger = logging.getLogger("nimbus")
    logger.setLevel(logging.INFO)
    
    # Avoid duplicate logs if already configured
    if logger.handlers:
        return logger

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger

logger = setup_logger()
