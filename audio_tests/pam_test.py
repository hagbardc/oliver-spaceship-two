import PyAudioMixer as pam
import time
mixer = pam.Mixer()
mixer.start()
snd = pam.Sound("sounds/piano2.wav")
snd.play()
time.sleep(2)
