#  This class represents the state of the control panel or panels
#  Receives JSON messages declaring state changes in named components
#  Applies those state changes to an internal model, and determines which
#  resultant messages should be sent to the various named controllers
#  Currently this only really means the audiocontroller, but could be expanded
#  to other elements not managed by the microcontroller

#  import json
import logging
#  import Queue


#  These components are responsible only for state maintenance, maybe?
class ComponentBase(object):
    def __init__(self, name):
        self._logger = logging.getLogger()
        self.name = name

    def processAction(self, action):
        logging.getLogger().warn('No action processor registered')

    def __str__(self):
        return self.name


class Button(ComponentBase):
    def __init__(self, name):
        super(Button, self).__init__(name)
        self.is_pressed = False

    def processAction(self, action):
        if action == 'pressed':
            self.is_pressed = True
        elif action == 'unpressed':
            self.is_pressed = False
        else:
            self.is_pressed = False

    def __str__(self):
        state = 'pressed' if self.is_pressed else 'unpressed'
        return '%s: %s' % (self.name, state)


class MissileController(ComponentBase):
    def __init__(
            self, name,
            number_of_switches=3,
            leds_per_switch=3
            ):
        super(MissileController, self).__init__(name)
        self.__switches = []
        self.__leds = []
        for i in range(number_of_switches):
            self.__switches.append(False)

            led_state = []
            for l in range(leds_per_switch):
                led_state.append(False)

            self.__leds.append(led_state)


class SystemState:

    @staticmethod
    def getComponentInterface(component_type):
        if component_type == 'button':
            return Button
        elif component_type == 'switch':
            return Button
        elif component_type == 'missile_controller':
            return MissileController

        return Button

    def __init__(self, system_config, log_level=logging.WARNING):
        '''
        @brief Accepts a configuration file and maintains a model
        @param system_config: list of tuples: [ (name, component_type)]
        '''
        self._logger = logging.getLogger()
        self._logger.setLevel(log_level)
        self._logger.debug('Inside SystemState constructor')

        if type(system_config) is not list:
            self._logger.warn('Configuration is not a tuple')
            raise TypeError('Systemstate configuration is not a tuple')

        self._componentMap = {}
        for component in system_config:
            component_name = component[0]
            self._logger.debug('Registering component name [%s]' %
                               component_name)
            component_type = SystemState.getComponentInterface(component[1])
            self._componentMap[component_name] = component_type(component_name)

    def applyComponentStateChange(self, component_name, action):
        '''
        @brief Apply a state change to one of the components, and determine
        '''
        if component_name not in self._componentMap:
            self._logger.error('No component [%s]. Action [%s] not applied' %
                               (component_name, action))
            return

        self._logger.debug('Passing action [%s] to component [%s]' %
                           (component_name, action))
        self._componentMap[component_name].processAction(action)

    def determineAudioAction(self, component_name, action):
        '''
        @brief  Given a component action (and current state of system)
                return an audio action tuple (audio name and behavior)
                E.g. ('button01', 'play') or ('siren01', 'loop')
        '''

    def printState(self):
        for component in self._componentMap:
            print self._componentMap[component]
