"""Converts the messages from the microcontroller(s) to messages intended for the audiocontroller
"""

import logging
from panelstate import PanelState, PanelActiveStatus


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

        self.panelState = PanelState(logger, log_level)


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

        self.panelState.processEventMessage(event_message)
        self._logger.debug(self.panelState)

        if not self.panelState.controllersAreReady():
            self._logger.debug('Controllers are not ready!')
            return None

        if event_message['action'] == 'stateread':
            return None
        
        component = event_message['component']
        self._logger.debug('Calling method for event [%s]' % event_message)

        if component not in self.__eventMap:
            self._logger.warning('Component %s not registered. Check _configureEventMap' % component)
            return None

        audio_message = self.__eventMap[component](event_message)
        if not audio_message:
            return None
            
        if 'name' not in audio_message:
            self._logger.warning('Sound lookup failed for event [%s]' % event_message)
        return audio_message
        

    def _configureEventMap(self):
        """Populates __eventMap with mappings of component names to methods that should be called when that component sends a message
        """

        # We will only get one of these when the system is ready
        self.__eventMap['controller01'] = self._controllerEvent
        self.__eventMap['controller02'] = self._controllerEvent

        # The key event is a special one, since we want to have differing behavior 
        # based on the panelActiveState
        self.__eventMap['key'] = self._keyEvent


        self.__eventMap['switch-32'] = self._simpleEvent


        self.__eventMap['switch-07'] = self._blueButtonEvent

        self.__eventMap['redToggle'] = self._toggleEvent
        self.__eventMap['greenToggle'] = self._toggleEvent
        self.__eventMap['blueToggle'] = self._toggleEvent

        self.__eventMap['switch-22'] = self._switchEvent
        self.__eventMap['switch-23'] = self._switchEvent
        self.__eventMap['switch-24'] = self._switchEvent
        self.__eventMap['switch-25'] = self._switchEvent
        self.__eventMap['switch-26'] = self._switchEvent
        self.__eventMap['switch-27'] = self._switchEvent
        self.__eventMap['switch-28'] = self._switchEvent
        self.__eventMap['switch-29'] = self._switchEvent
        self.__eventMap['switch-30'] = self._switchEvent
        self.__eventMap['switch-31'] = self._switchEvent
        self.__eventMap['switch-33'] = self._switchEvent
        self.__eventMap['switch-34'] = self._switchEvent
        self.__eventMap['switch-35'] = self._switchEvent
        self.__eventMap['switch-36'] = self._switchEvent
        self.__eventMap['switch-37'] = self._switchEvent
        self.__eventMap['switch-38'] = self._switchEvent
        self.__eventMap['switch-39'] = self._switchEvent
        self.__eventMap['switch-40'] = self._switchEvent
        self.__eventMap['switch-41'] = self._switchEvent

        self.__eventMap['switch-42-43'] = self._switchEvent
        self.__eventMap['switch-50-52'] = self._switchEvent
        self.__eventMap['switch-51-53'] = self._switchEvent


    def _controllerEvent(self, event_message):
        """Transforms a incoming microcontroller event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """
        audiocontroller_message = {'action': 'play', 'loop': False}
        if event_message['component'] == 'controller01' or event_message['component'] == 'controller02':
            audiocontroller_message['name'] = 'systems_nominal'

        return audiocontroller_message

    def _toggleEvent(self, event_message):
        """Transforms a incoming microcontroller event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """
        audiocontroller_message = {'action': 'play', 'loop': False}

        if event_message['action'] != 'statechange':
            return None

        if event_message['value'] == 'PROCESSING:1':
            audiocontroller_message['name'] = 'blip_low'
        if event_message['value'] == 'PROCESSING:2':
            audiocontroller_message['name'] = 'blip_medium'


        if event_message['component'] == 'redToggle':
            if event_message['value'] == 'WAITING:0':
                audiocontroller_message['name'] = 'artemis_offline'
            if event_message['value'] == 'ACTIVE:3':
                audiocontroller_message['name'] = 'artemis_online'
        elif event_message['component'] == 'greenToggle':
            if event_message['value'] == 'WAITING:0':
                audiocontroller_message['name'] = 'sensors_offline'
            if event_message['value'] == 'ACTIVE:3':
                audiocontroller_message['name'] = 'sensors_online'
        elif event_message['component'] == 'blueToggle':
            if event_message['value'] == 'WAITING:0':
                audiocontroller_message['name'] = 'targeting_computer_offline'
            if event_message['value'] == 'ACTIVE:3':
                audiocontroller_message['name'] = 'targeting_computer_online'
        return audiocontroller_message



    def _blueButtonEvent(self, event_message):
        """Transforms a incoming microcontroller event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """
        audiocontroller_message = {'name': 'heat_warning', 'loop': True}

        if self.panelState.panelActiveStatus != PanelActiveStatus.ON:
            return {'action': 'play', 'loop': False, 'name': 'systems_offline'}


        if event_message['action'] != 'switch':
            return None

        if event_message['value'] == str(0):
            audiocontroller_message['action'] = 'play'
        elif event_message['value'] == str(1):
            audiocontroller_message['action'] = 'stop'

        return audiocontroller_message
        

    def _keyEvent(self, event_message):
        """Transforms a incoming key event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """
        audiocontroller_message = {'action': 'play', 'loop': False}
        if event_message['component'] != 'key':
            self._logger.error("Component [%s] is not expected 'key'" % event_message['component'])
            return None # This should never happen
            
        if self.panelState.panelActiveStatus ==  PanelActiveStatus.INVALID:
            if event_message['value'] == str(0):
                audiocontroller_message['name'] = 'power_restored'
            if event_message['value'] == str(1):
                audiocontroller_message['name'] = 'shutdown_sequence' # this should not be able to happen
        
        # This part looks backwards because we update the panel state before we play the sound
        elif self.panelState.panelActiveStatus ==  PanelActiveStatus.OFF:
            if event_message['value'] == str(1):
                audiocontroller_message['name'] = 'shutdown_sequence'
        elif self.panelState.panelActiveStatus ==  PanelActiveStatus.ON: 
            if event_message['value'] == str(0):
                audiocontroller_message['name'] = 'power_restored'

        self._logger.debug("Returning key audio message: %s" % audiocontroller_message)
        return audiocontroller_message


    def _loopedEvent(self, event_message):
        """Transforms a incoming switch event to the relevant audiocontroller message
        Assumes that 
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """

    def _switchEvent(self, event_message):
        """Transforms a incoming switch event to the relevant audiocontroller message
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message

        Returns:
            {dict} -- Dictionary of {'action': <str>, 'name': <str>, 'loop': <bool>} which can be passed to audiocontroller
        """

        audiocontroller_message = {'action': 'play', 'loop': False}
        if self.panelState.panelActiveStatus != PanelActiveStatus.ON:
            audiocontroller_message['name'] = 'systems_offline'
            return audiocontroller_message

        if event_message['component'] == 'switch-50-52' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'reactor_online'
        elif event_message['component'] == 'switch-50-52' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'reactor_offline'
        if event_message['component'] == 'switch-28' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'beagle_engaged'
        elif event_message['component'] == 'switch-28' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'beagle_shutdown'
        if event_message['component'] == 'switch-27' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'c3_online'
        elif event_message['component'] == 'switch-27' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'c3_shutdown'
            
        elif event_message['component'] == 'switch-30' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'data_transfer_initiated'
        elif event_message['component'] == 'switch-30' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'data_transfer_complete'
        elif event_message['component'] == 'switch-31' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'satellite_established'
        elif event_message['component'] == 'switch-31' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'satellite_shutdown'
        elif event_message['component'] == 'switch-51-53' and event_message['value'] == str(2):
            audiocontroller_message['name'] = 'linked_fire'
        elif event_message['component'] == 'switch-51-53' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'single_fire'
        elif event_message['component'] == 'switch-51-53' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'group_fire'
        elif event_message['component'] == 'switch-42-43' and event_message['value'] == str(2):
            audiocontroller_message['name'] = 'light_amp_maximum'
        elif event_message['component'] == 'switch-42-43' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'light_amp_moderate'
        elif event_message['component'] == 'switch-42-43' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'light_amp_nominal'
        elif event_message['component'] == 'switch-22' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'camera_engaged'
        elif event_message['component'] == 'switch-22' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'camera_offline'
        elif event_message['component'] == 'switch-23' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'shield_generator_active'
        elif event_message['component'] == 'switch-23' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'shield_generator_shutdown'
        elif event_message['component'] == 'switch-24' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'arm_extended'
        elif event_message['component'] == 'switch-24' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'arm_retracted'
        elif event_message['component'] == 'switch-25' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'ams_engaged'
        elif event_message['component'] == 'switch-25' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'ams_offline'
        elif event_message['component'] == 'switch-26' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'ecm_online'
        elif event_message['component'] == 'switch-26' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'ecm_offline'
        elif event_message['component'] == 'switch-29' and event_message['value'] == str(1):
            audiocontroller_message['name'] = 'power_converter_online'
        elif event_message['component'] == 'switch-29' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'power_converter_offline'
        elif event_message['component'] == 'switch-33' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'missile_launch_01'
        elif event_message['component'] == 'switch-34' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'attacking_machinegun'
        elif event_message['component'] == 'switch-35' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'flamethrower'
        elif event_message['component'] == 'switch-36' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'ac10_gun'
        elif event_message['component'] == 'switch-37' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'srm4_launch'
        elif event_message['component'] == 'switch-38' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'laser_large'
        elif event_message['component'] == 'switch-39' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'lbx_10'
        elif event_message['component'] == 'switch-40' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'xpulse_large'
        elif event_message['component'] == 'switch-41' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'laser_small'




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
        if self.panelState.panelActiveStatus != PanelActiveStatus.ON:
            audiocontroller_message['name'] = 'systems_offline'
            return audiocontroller_message

        audiocontroller_message = {'action': 'play', 'loop': False}
        if event_message['component'] == 'switch-32' and event_message['value'] == str(0):
            audiocontroller_message['name'] = 'gauss_rifle'
        

        self._logger.debug('Audiocontroller Message is [%s]' % audiocontroller_message)
        return audiocontroller_message


        
if __name__ == '__main__':
    logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                        level=logging.DEBUG)
    
    m = MessageMapper(log_level=logging.DEBUG)
    e = {'action': 'switch', 'component': 'switch-42-49', 'value': 1, 'element': 'n/a'}
    print(m.getAudiocontrollerMessageForEvent(e))
