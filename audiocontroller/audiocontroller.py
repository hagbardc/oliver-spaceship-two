import logging
import pygame
import Queue


# This is the queue into which we publish sound request events
audio_queue = Queue.Queue()


def audio_controller_worker(config, queue_list):
    """
    config is an array of dict objects:

    [ {'name': 'piano', 'sound': 'piano2.wav', 'loopable': False } ]

    """
    ac = AudioController(config, queue_list)
    ac.consumeMessages()


class AudioController:


    @staticmethod
    def isValidAudioCommand(audio_message):
        """Returns true if the passed in audio message dict is a properly structured audio message
        Does not care if the given message is registered properly, just checks the dictionary 
        for the proper keys
        
        Arguments:
            audio_message {keys} -- Audio message suitable for playing
        """
        if not audio_message:
            logging.error('None type passed to isValidAudioCommand')
            return False

        if type(audio_message) is not dict:
            logging.error('type of passed in audio_message is %s' % type(audio_message))
            return False

        if  'name' not in audio_message or \
            'action' not in audio_message or \
            'loop' not in audio_message:
            return False

        return True

    @staticmethod
    def isConfigValid(config):
        """Takes in a configuration dictionary, and states whether it's valid for an AudioController

        Checks that each element in the list has the proper keys, and that the 
        'sound' element actually exists in the file system 
        
        Arguments:
            config {dict} -- AudioController config (dictionary of various relevant keys)

        Returns True if the configuration is valid, False else
        """
        return False

    def __init__(self, config, message_queue_list):
        pygame.init()
        pygame.mixer.init()

        self._audio_registry = {}

        # The expected path for audio files, used if no path is provided in the 
        # list of configured sounds
        self._default_audio_path = None  
        if 'default_audio_path' in config:
            self._default_audio_path = config['default_audio_path']


        # If there was a default audio path provided, we don't require
        # a 'sound' key:  Just the name, which we use to build the path
        # and file name
        for item in config['audio_file_list']:
            if self._default_audio_path:
                sound = "%s/%s.wav" % (self._default_audio_path, item['name'])
            else:
                sound = item['sound']
            self.__register(item['name'], sound, item['loopable'])

        # This is a list of messages queues from which we should be consuming messagess
        self._queue_list = message_queue_list

    def __register(self, registry_name, file_path, loopable=False):
        self._audio_registry[registry_name] = {
            'sound': pygame.mixer.Sound(file_path),
            'loopable': loopable
            }

    def consumeMessages(self):
        while True:
            for q in self._queue_list:
                if not q.empty():
                    soundInfo = q.get(block=False, timeout=0.01)
                    if not soundInfo:
                        continue

                    logging.debug("audioQueue.get pulled [%s]" % str(soundInfo))
                    if dict is not type(soundInfo):
                        logging.warn("audioQueue.get pulled an object that was not a dict")
                        logging.warn("type is %s" % type(soundInfo))
                        continue

                    try:
                        if soundInfo['action'] == 'play':
                            self.playSound(soundInfo['name'], soundInfo['loop'])
                        elif soundInfo['action'] == 'stop':
                            self.stopSound(soundInfo['name'])
                        elif soundInfo['action'] == 'end_thread':
                            logging.debug("Received end_thread message.")
                            return  # special message to end the thread
                    except KeyError:
                        logging.error("KeyError - soundInfo %s improperly structured" %
                                    soundInfo)



    def playSound(self, registry_name, loop=False):
        """ Play a sound previously registered (via the pygame linkage)

        Keyword arguments:
        registry_name -- the string used to refer to a registered audio clip
        loop -- Whether or not to loop the audio clip (default False)
        """
        num_times = 0
        if loop:
            num_times = -1


        if registry_name not in self._audio_registry:
            logging.error('Could not found [%s] in sound registry. No action taken' % registry_name)
            return

        logging.debug("Playing sound registered as %s" % registry_name)
        self._audio_registry[registry_name]['sound'].play(loops=num_times)

    def stopSound(self, registry_name):
        """ Stop a sound previously registered (via the pygame linkage)

        Keyword arguments:
        registry_name -- the string used to refer to a registered audio clip
        """
        if registry_name not in self._audio_registry:
            logging.error('Could not found [%s] in sound registry. No action taken' % registry_name)
            return
        self._audio_registry[registry_name]['sound'].stop()


if __name__ == '__main__':
    print("huge")
