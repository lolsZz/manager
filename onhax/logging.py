"""Logging configuration for OnHax."""
import logging
import logging.config
import os
from pathlib import Path
from typing import Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Configure logging for the application.
    
    Args:
        log_level: The logging level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to a log file. If not provided, logs only go to console.
    """
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": log_level,
            },
            "onhax": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    
    if log_file:
        # Create log directory if it doesn't exist
        log_path = Path(log_file).parent
        if not log_path.exists():
            log_path.mkdir(parents=True)
            
        config["handlers"]["file"] = {
            "class": "logging.FileHandler",
            "level": log_level,
            "formatter": "standard",
            "filename": log_file,
            "mode": "a",
        }
        config["loggers"][""]["handlers"].append("file")
        config["loggers"]["onhax"]["handlers"].append("file")
    
    logging.config.dictConfig(config)

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name.
    
    Args:
        name: The name for the logger, typically __name__.
        
    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)