import logging
import json
from pythonjsonlogger import jsonlogger
from config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """Set up structured JSON logging."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger