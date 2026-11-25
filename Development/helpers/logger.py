import logging
import sys
from logging.handlers import RotatingFileHandler

# Initializa logging
logFormat = '%(asctime)s | %(levelname)s | %(message)s'
#Rotate log files when specific size is reached
#specify size limit foe each log file
handler_ = RotatingFileHandler('output_log.log', maxBytes=5000000, backupCount=3)
std_out_handler = logging.StreamHandler(sys.stdout)
handlers = [handler_, std_out_handler]
logging.basicConfig(format= logFormat, level= logging.DEBUG, handlers=handlers)
logger = logging.getLogger()