import logging
import pygame
import Queue


audio_queue = Queue.Queue()

def audio_controller_worker(config):
    """
    config is an array of dict objects:

    [ {'name': 'piano', 'sound': 'piano2.wav', 'loopable': False } ]

    """
    ac = AudioController(config)
    
    while True:
        soundInfo = audio_queue.get(block=True)
        logging.debug("audioQueue.get pulled [%s]" % str(soundInfo) )

        if dict is not type(soundInfo):
            logging.warn("audioQueue.get pulled an object that was not a dict")
            continue
        
        try:
            if soundInfo['action'] == 'play':
                ac.playSound(soundInfo['name'], soundInfo['loop'])
            elif soundInfo['action'] == 'stop':
                ac.stopSound(soundInfo['name'])
            elif soundInfo['action'] == 'end_thread':
                return # special message to end the thread
        except KeyError:
            logging.error("KeyError - soundInfo %s improperly structured" %
                            soundInfo)
            


class AudioController:
    def __init__(self, config):
        pygame.init()
        pygame.mixer.init()

        self._audio_registry = {}
        for item in config:
            self.__register(item['name'], item['sound'], item['loopable'])


    
    def __register(self, registry_name, file_path, loopable=False):
        self._audio_registry[registry_name] = {
            'sound': pygame.mixer.Sound(file_path),
            'loopable': loopable
            }

    def playSound(self, registry_name, loop=False):
        """ Play a sound previously registered (via the pygame linkage)

        Keyword arguments:
        registry_name -- the string used to refer to a registered audio clip
        loop -- Whether or not to loop the audio clip (default False)
        """
        num_times = 0
        if loop:
            num_times = -1
        self._audio_registry[registry_name]['sound'].play(loops=num_times)

    def stopSound(self, registry_name):
        """ Stop a sound previously registered (via the pygame linkage)

        Keyword arguments:
        registry_name -- the string used to refer to a registered audio clip
        """
        self._audio_registry[registry_name]['sound'].stop()


if __name__ == '__main__':
    print "huge"
