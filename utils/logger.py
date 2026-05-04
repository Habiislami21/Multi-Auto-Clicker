import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    logger = logging.getLogger("MultiAutoClicker")
    logger.setLevel(logging.DEBUG)
    
    # File handler untuk menyimpan log ke dalam file dengan ukuran max 5MB, backup 2
    fh = RotatingFileHandler('logs/app.log', maxBytes=5*1024*1024, backupCount=2)
    fh.setLevel(logging.DEBUG)
    
    # Console handler untuk menampilkan log di terminal
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = setup_logger()
