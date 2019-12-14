from multiprocessing import Process, Queue

from audiocontroller import audio_controller_worker
from audiocontroller import AudioController as ac
import time


config = [{'name': 'button', 'sound': 'button.wav', 'loopable': True}]
cmdStart = {'name': 'button', 'action': 'play', 'loop': True}
cmdStop = {'name': 'button', 'action': 'stop', 'loop': True}

q = Queue()
audio_process = Process( target=audio_controller_worker, args=(config, [q],))
audio_process.start()


time.sleep(1)
q.put(cmdStart)
time.sleep(2)
q.put(cmdStop)
time.sleep(2)


end_thread = {'action': 'end_thread'}
q.put(end_thread)
