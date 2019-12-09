"""Converts the messages from the microcontroller(s) to messages intended for the audiocontroller
"""

import logging


class MessageMapper(object):
    """Configures and transforms microcontroller events to audio events

    This is also responsible for keeping track of any state that needs to be kept track of, 
    since a given event might need to be different dependant on state of the panel
    """
    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)

    def __init__(self, logger=_logger, log_level=logging.WARNING):
        """Initializes message mapper.  
        
        Arguments:
            object {MessageMapper} -- This object
        """
        self._logger = MessageMapper._logger
        self._logger.setLevel(log_level)

        self._logger.debug('Inside MessageMapper constructor')

        # Dictionary of component names and methods to call when that component triggers an event
        self.__eventMap = {}
        self._configureEventMap()


    def getAudiocontrollerMessageForEvent(self, event_message):
        """Given a microcontroller event, return the relevant message for the audiocontroller
        
        Arguments:
            event_message {dict} -- Event message dictionary

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """
        if 'component' not in event_message:
            self._logger.error('Event message passed without "component": [%s]' % event_message)
            return None
        
        component = event_message['component']
        self._logger.debug('Calling method for event [%s]' % event_message)
        return self.__eventMap[component](event_message)
        

    def _configureEventMap(self):
        """Populates __eventMap with mappings of component names to methods that should be called when that component sends a message
        """

        self.__eventMap['switch-32'] = self._simpleEvent



        self.__eventMap['switch-42-49'] = self._switchEvent
        self.__eventMap['switch-50-52'] = self._switchEvent
        self.__eventMap['key'] = self._simpleEvent


    def _switchEvent(self, event_message):
        """Transforms a incoming switch event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """

        audiocontroller_message = {'action': 'play', 'loop': False}
        if event_message['component'] == 'switch-50-52' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'reactor_online'
        if event_message['component'] == 'switch-50-52' and event_message['value'] == str(2):
            audiocontroller_message['name'] = 'reactor_offline'

        self._logger.debug('Audiocontroller Message is [%s]' % audiocontroller_message)
        return audiocontroller_message



    # Associates the simple events:  Single component name to audio event connection
    def _simpleEvent(self, event_message):
        """Transforms the incoming event_message to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """

        audiocontroller_message = {'action': 'play', 'loop': False}
        if event_message['component'] == 'key' and event_message['value'] == 1:
            audiocontroller_message['name'] = 'system_activated'
        if event_message['component'] == 'switch-32' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'button_pressed'
        

        self._logger.debug('Audiocontroller Message is [%s]' % audiocontroller_message)
        return audiocontroller_message


        
if __name__ == '__main__':
    logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    
    m = MessageMapper(log_level=logging.DEBUG)
    e = {'action': 'switch', 'component': 'switch-42-49', 'value': 1, 'element': 'n/a'}
    print(m.getAudiocontrollerMessageForEvent(e))
