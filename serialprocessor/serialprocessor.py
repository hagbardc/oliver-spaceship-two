"""
Contains components to handle consumption of messages from a serial connection, 
and publication of those messages to a queue.  Ideally, that queue is consumed
by another application which pulls those messages off the queue and does something.
Like play a sound
"""



import logging
import json
import os
import Queue
import serial
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def serial_processor_worker(serial_name, serial_port, audio_controller_queue,
                            logger=logging.getLogger()):
    """ Worker function to publish data coming in from a serial port to a queue
    
    Arguments:
        serial_name {str} -- Name associated with the serial port in `serial_port`
        serial_port {serial.Serial} -- Serial port from which to read data for publishing to the audio queue
        audio_controller_queue {queue.Queue} -- Queue onto which to publish the messages from the serial line
    
    Keyword Arguments:
        logger {logging.Logger} -- Logging object (default: {logging.getLogger()})
    """

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
    """Opens up connections to specified serial ports, and passes on those on to a specified queue
    """

    _terminate = False
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)

    # Config is dict:  { 'port_paths': []}
    def __init__(self, config, audio_controller_queue,
                 controller_baud=19200,
                 log_level=logging.WARNING):
        """Initialize the SerialProcessor object
        
        Arguments:
            config {dict} -- Configuration dictionary for the object
            audio_controller_queue {queue.Queue} -- Queue onto which messages from the serial line will be passed
        
        Keyword Arguments:
            controller_baud {int} -- Connection speed for the serial ports (default: {19200})
            log_level {logging.LogLevel} -- Log level (default: {logging.WARNING})
        
        example usage:

        q = queue.Queue()
        serial_config = {'port_paths': ['/dev/ttyUSB0', '/dev/ttyACM0']}

        sp = SerialProcessor(config=serial_config,
                            audio_controller_queue=q,
                            log_level=logging.INFO)
        """


        self._logger = SerialProcessor._logger
        self._logger.setLevel(log_level)

        self._logger.debug('Inside SerialProcessor constructor')
        self._controller_baud = controller_baud
        self._audio_controller_queue = audio_controller_queue

        # Paths to serial ports
        # TODO:  Check for existence of paths, and exit if not found
        # TODO: Auto discover USB and ACM paths
        if 'port_paths' not in config:
            self.autoAssignUSBSerialPorts()
        else:
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

    # Does an ls -1 /dev/ and picks up any ttyUSB or ttyACM ports
    def autoAssignUSBSerialPorts(self):
        files = os.listdir('/dev/')
        for name in files:
            print(name)

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
