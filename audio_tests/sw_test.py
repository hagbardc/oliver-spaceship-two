import swmixer
import time

swmixer.init(samplerate=44100, chunksize=1024, stereo=False)
swmixer.start()
snd = swmixer.Sound("sounds/piano2.wav")
snd.play()
time.sleep(10.0) #don't quit before we hear the sound!
