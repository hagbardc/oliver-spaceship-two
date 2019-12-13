"""Stores the current state of the control panel
"""
import logging
from enum import Enum

class PanelActiveStatus(Enum):
    ON = 1      # The key is ON
    OFF = 2     # The key is OFF
    INVALID = 3 # The key is in the ON position, but came up like that on system wakeup


class PanelState(object):

    _logger = logging.getLogger()
    _logger.setLevel(logging.WARNING)

    def __init__(self, logger=_logger, log_level=logging.WARNING):
        self._logger = PanelState._logger
        self._logger.setLevel(log_level)

        self.panelActiveStatus = PanelActiveStatus.INVALID

        # These will be False until the two microcontroller components report a ready state
        self._controller01Ready = False
        self._controller02Ready = False

    def __str__(self):
        return "Controllers: [%s/%s] PanelActive: %s" % (self._controller01Ready, self._controller02Ready, self.panelActiveStatus)

    def controllersAreReady(self):
        return self._controller01Ready and self._controller02Ready

    # {u'action': u'setup_complete', u'component': u'controller01', u'value': u'n/a', u'element': u'n/a'}
    def _processControllerEventMessage(self, event_message):
        """For handling panel state
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message
        """
        if event_message['component'] == 'controller01' and event_message['action'] == 'setup_complete':
            self._logger.debug("Setting controller01Ready to True")
            self._controller01Ready = True
        elif event_message['component'] == 'controller02' and event_message['action'] == 'setup_complete':
            self._logger.debug("Setting controller02Ready to True")
            self._controller02Ready = True


    def _processKeyEventMessage(self, event_message):
        
        # We don't want to process any key event messages unless the controllers are set up
        try:
            if event_message['action'] == 'stateread' and event_message['value'] == str(0):
                return
            elif event_message['action'] == 'stateread' and event_message['value'] == str(1):
                self.panelActiveStatus = PanelActiveStatus.OFF
            elif event_message['action'] == 'switch' and event_message['value'] == str(0):
                self.panelActiveStatus = PanelActiveStatus.ON
            elif event_message['action'] == 'switch' and event_message['value'] == str(1):
                self.panelActiveStatus = PanelActiveStatus.OFF
        except KeyError:
            self._logger.error("Received improperly formed event message: %s" % event_message)
            return

    def processEventMessage(self, event_message):
        """Takes in an event message dictionary and updates the state of the panel accordingly
        
        Arguments:
            event_message {dict} -- Message dictionary as extracted from json payload of arduino message
        """
        try:
            if event_message['component'] == 'controller01' or event_message['component'] == 'controller02':
                self._processControllerEventMessage(event_message)
            elif event_message['component'] == 'key':
                self._processKeyEventMessage(event_message)


        
        except KeyError:
            self._logger.error("Received event message without 'component' key: %s" % event_message)
            return

