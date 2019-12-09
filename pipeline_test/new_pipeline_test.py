from multiprocessing import Process, Queue
from serialprocessor.serialprocessor import serial_processor_worker
from audiocontroller.audiocontroller import audio_controller_worker

import time
import logging

logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

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



if __name__ == '__main__':
    print("Starting multiprocess app")

    q1 = Queue()
    q2 = Queue()
    audio_process = Process( target=audio_controller_worker, args=(audio_config, [q1, q2],))
    audio_process.start()

    serial_process_01 = Process( target = serial_processor_worker, args=('/dev/ttyACM1', q1,))
    serial_process_01.start()

    serial_process_02 = Process( target = serial_processor_worker, args=('/dev/ttyACM0', q2,))
    serial_process_02.start()


    while True:
        continue
    
    audio_process.join()
    serial_process_01.join()
    serial_process_02.join()
