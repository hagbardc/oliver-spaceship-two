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

from messagemapper import MessageMapper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def serial_processor_worker(serial_name, audio_controller_queue,
                            logger=logging.getLogger()):
    """ Generates a SerialProcessor and sets it to start monitoring the port
    
    Arguments:
        serial_name {str} -- Name associated with the serial port in `serial_port`
        audio_controller_queue {queue.Queue} -- Queue onto which to publish the messages from the serial line
    
    Keyword Arguments:
        logger {logging.Logger} -- Logging object (default: {logging.getLogger()})
    """
 
    serialProcessor = SerialProcessor( config = {'port_path': serial_name}, audio_controller_queue = audio_controller_queue)
    serialProcessor.startSerialListening()




class SerialProcessor:
    """Opens up connections to specified serial ports, and passes on those on to a specified queue
    """

    _terminate = False
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)

    _message_mapper = MessageMapper(logger=_logger)

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
        serial_config = {'port_path': '/dev/ttyUSB0'}

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
        self._port_path = config['port_path']

        
        # self._serial_port <serial.Serial> object>
        self._logger.info('Connecting serial port at %s' % self._port_path)
        self._serial_port = serial.Serial(self._port_path, self._controller_baud, timeout=None)

    def startSerialListening(self):
        """This is a blocking call that will just start listening on the port specified by the item in port_path
        """
        while True:
            line = self._serial_port.readline()
            if not line:
                continue

            try:
                logger.debug("Message recived on %s: %s" % (self._port_path, line))
                event_message = SerialProcessor.processJson(self._port_path, line)
                logger.debug("Post processing on %s: [%s]"  % (self._port_path, event_message))

                if self._audio_controller_queue:
                    logger.debug("Publishing message onto audio_controller_queue")
                    self._audio_controller_queue.put(event_message)

            except KeyError as ke:
                logger.error("KeyError - serialInfo %s improperly structured"
                            % line)
                logger.error("%s" % ke)
            except TypeError as err:
                logger.error("Got type error: %s" % err)
                pass


    @staticmethod
    def terminateFlag():
        pass # TODO: Change this so that we end the process that this class is running in


    @staticmethod
    def processJson(serial_name, msg_json):
        """This actually converts the json messages from the arduino to the audio control messages

        The way this is constructed now, if we want to maintain state for the panel, we will need
        to check the state in here and make an assessment of what sound should play given the 
        arduino json message, and the current system state
        
        Arguments:
            serial_name {str} -- Name of the serial connection over which the json messages were recieved (only used for logging)
            msg_json {str} -- The json object sent in over the specified serial connection
        
        Returns:
            [dict] -- Message to be passed to the audio controller.  Has keys 'name', 'action', and 'loop'
        """

        SerialProcessor._logger.debug("processJson:%s: %s"
                                      % (serial_name, msg_json))
        try:
            SerialProcessor._logger.debug("Type of json_message is %s"
                                          % type(msg_json))
            event_message = json.loads(msg_json.decode('utf-8'))
            SerialProcessor._logger.info("Message: %s" % event_message)

            audio_command = SerialProcessor._message_mapper.getAudiocontrollerMessageForEvent(event_message)

            SerialProcessor._logger.debug("audio_command [%s]" % audio_command)
            return audio_command
        except ValueError:
            SerialProcessor._logger.error("Invalid JSON message on %s: %s"
                                          % (serial_name, msg_json))
        except Exception as err:
            SerialProcessor._logger.error("Some other error was hit: %s" % err)

        return None


if __name__ == '__main__':

    logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                        level=logging.DEBUG)


    serial_config = {'port_path': '/dev/ttyACM1'}
    s = SerialProcessor(config=serial_config, audio_controller_queue=None, log_level=logging.DEBUG)
    s.startSerialListening()