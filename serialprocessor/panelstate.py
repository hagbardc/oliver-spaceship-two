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


    def _processKeyEventMessage(self, event_message):
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
            if event_message['component'] == 'key':
                self._processKeyEventMessage(event_message)
        
        except KeyError:
            self._logger.error("Received event message without 'component' key: %s" % event_message)
            return

