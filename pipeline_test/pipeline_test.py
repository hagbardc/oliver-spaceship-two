from audiocontroller.audiocontroller import audio_queue
from audiocontroller.audiocontroller import audio_controller_worker
from serialprocessor.serialprocessor import SerialProcessor
import threading
import time
import logging

logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)
#  serial_config = {'port_paths': ['/dev/ttyUSB1', '/dev/ttyACM1']}
#serial_config = {'port_paths': ['/dev/ttyACM0', '/dev/ttyUSB0']}
#serial_config = {'port_paths': ['/dev/ttyUSB0']}
serial_config = {'port_paths': ['/dev/ttyACM0', '/dev/ttyACM1']}


audio_config = [
            {'name': 'reactor_online', 'sound': 'audio_files/reactor_online.wav',
             'loopable': False},
            {'name': 'reactor_offline', 'sound': 'audio_files/reactor_offline.wav',
             'loopable': False},
            {'name': 'switch_flipped', 'sound': 'audio_files/mathbutton_yellow.wav',
             'loopable': False},
            {'name': 'button_pressed', 'sound': 'audio_files/mathbutton_green.wav',
             'loopable': False},
            {'name': 'system_activated', 'sound': 'audio_files/missile_phase_1.wav',
             'loopable': False}
            ]

audio_thread = threading.Thread(target=audio_controller_worker,
                                args=[audio_config])
audio_thread.start()

sp = SerialProcessor(config=serial_config,
                     audio_controller_queue=audio_queue,
                     log_level=logging.DEBUG)

sp.startSerialListening()

try:
    while(True):
        pass
except (KeyboardInterrupt, SystemExit):
    sp.killall()
    time.sleep(1)
    audio_queue.put({'action': 'end_thread'})
