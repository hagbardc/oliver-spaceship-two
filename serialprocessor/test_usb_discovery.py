import logging
from serialprocessor import SerialProcessor as SP

logging.info("Running usb discovery test")
logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

try:
    sp = SP({}, None)
except RuntimeError as rte:
    print rte.message
