import threading
from audiocontroller import audio_queue, audio_controller_worker
from audiocontroller import AudioController as ac
import time


config = [ {'name': 'piano', 'sound': 'piano2.wav', 'loopable': False } ]
cmd = {'name': 'piano', 'action': 'play', 'loop': False}

t = threading.Thread(target=audio_controller_worker, args=[config])
t.start()


time.sleep(1)
audio_queue.put(cmd)
time.sleep(5)

end_thread = { 'action': 'end_thread' }
audio_queue.put(end_thread)
