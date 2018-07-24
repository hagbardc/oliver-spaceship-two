import logging
import json
import Queue
import serial
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def serial_processor_worker(serial_name, serial_port, audio_controller_queue,
                            logger=logging.getLogger()):

    while not SerialProcessor.terminateFlag():
        line = serial_port.readline()
        if not line:
            break

        try:
            logger.debug("Message recived on %s: %s"
                         % (serial_name, line))
            event_message = SerialProcessor.processJson(serial_name, line)
            logger.debug("Post processing on %s: [%s]"
                         % (serial_name, event_message))

            if audio_controller_queue:
                logger.debug("Publishing message onto audio_controller_queue")
                audio_controller_queue.put(event_message)

        except KeyError:
            logger.error("KeyError - serialInfo %s improperly structured"
                         % line)
        except TypeError:
            pass


class SerialProcessor:

    _terminate = False
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)

    # Config is dict:  { 'port_paths': []}
    def __init__(self, config, audio_controller_queue,
                 controller_baud=19200,
                 log_level=logging.WARNING):

        self._logger = SerialProcessor._logger
        self._logger.setLevel(log_level)

        self._logger.debug('Inside SerialProcessor constructor')
        self._controller_baud = controller_baud
        self._audio_controller_queue = audio_controller_queue

        # Paths to serial ports
        self._port_paths = config['port_paths']
        self._serial_ports = []
        for p in self._port_paths:
            self._logger.info('Connecting serial port at %s' % p)
            port = serial.Serial(p, self._controller_baud)
            self._serial_ports.append((p, port))

        self._threads = []

    def startSerialListening(self):
        for p in self._serial_ports:
            self._logger.info("Creating thread for %s" % (p[0]))
            t = threading.Thread(target=serial_processor_worker,
                                 args=[p[0], p[1],
                                       self._audio_controller_queue,
                                       self._logger])
            self._threads.append(t)
            self._logger.info("Starting thread for %s" % (p[0]))
            t.start()

    @staticmethod
    def terminateFlag():
        return SerialProcessor._terminate

    @staticmethod
    def killall():
        SerialProcessor._terminate = True

    @staticmethod
    def processJson(serial_name, msg_json):

        SerialProcessor._logger.debug("processJson:%s: %s"
                                      % (serial_name, msg_json))
        try:
            SerialProcessor._logger.debug("Type of json_message is %s"
                                          % type(msg_json))
            event_message = json.loads(msg_json.decode("utf-8"))
            SerialProcessor._logger.info("Message: %s: %s"
                                         % (event_message['name'],
                                            event_message['action']))

            audio_command = {'action': 'play', 'loop': False}
            if event_message['name'] == 'arduino_1' and event_message['action'] == 'button_down':
                audio_command['name'] = 'ard_1_down'
            if event_message['name'] == 'arduino_1' and event_message['action'] == 'button_up':
                audio_command['name'] = 'ard_1_up'
            if event_message['name'] == 'arduino_2'and event_message['action'] == 'button_down':
                audio_command['name'] = 'ard_2_down'
            if event_message['name'] == 'arduino_2' and event_message['action'] == 'button_up':
                audio_command['name'] = 'ard_2_up'

            return audio_command
        except ValueError:
            SerialProcessor._logger.error("Invalid JSON message on %s: %s"
                                          % (serial_name, msg_json))
        except Exception as err:
            SerialProcessor._logger.error("Some other error hit: %s" % err)

        return None
