import Queue
from audiocontroller import AudioController

audioQueue = Queue.Queue()

"""
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()       # block until all tasks are done
"""


"""
soundInfo = { 'name': <registry_name>,
              'action': <play|stop>,
              'loop': <True|False>
            }
"""


def audio_worker():
    ac = AudioController()
    ac.register(registry_name='piano', file_path='piano2.wav')

    while True:
        soundInfo = None
        try:
            soundInfo = audioQueue.get()
        except Queue.Empty:
            pass

        if soundInfo:
            print soundInfo
            if soundInfo['action'] == 'play':
                ac.playSound(soundInfo['name'], soundInfo['loop'])
            elif soundInfo['action'] == 'stop':
                ac.stopSound(soundInfo['name'])
