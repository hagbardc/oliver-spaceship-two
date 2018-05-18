import logging
import pygame
import Queue


class AudioController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self._audio_registry = {}

    def register(self, registry_name, file_path, loopable=False):
        # TODO: Check for collision here
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
