from serialprocessor import SerialProcessor
import logging

logging.info("instantiating serial processor")
logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

serial_config = {'port_paths': ['/dev/ttyUSB0', '/dev/ttyACM0']}
audio_controller_queue = None

logging.debug('serial_config is %s' % serial_config)
sp = SerialProcessor(config=serial_config,
                     audio_controller_queue=audio_controller_queue,
                     log_level=logging.INFO)

sp.startSerialListening()

try:
    while(True):
        pass
except (KeyboardInterrupt, SystemExit):
    sp.killall()
