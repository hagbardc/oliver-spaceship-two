from multiprocessing import Process, Queue
from serialprocessor.serialprocessor import serial_processor_worker
from audiocontroller.audiocontroller import audio_controller_worker, AudioController
from serialprocessor.messagemapper import MessageMapper

import sys
import logging
import argparse


logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

audio_config = [
            {'name': 'systems_nominal',         'sound': 'audio_files/systems_nominal.wav', 'loopable': False},
            {'name': 'power_restored',          'sound': 'audio_files/power_restored.wav', 'loopable': False},
            {'name': 'systems_offline',         'sound': 'audio_files/systems_offline.wav', 'loopable': False},
            {'name': 'blip_low',                'sound': 'audio_files/blip_low.wav', 'loopable': False},
            {'name': 'blip_medium',             'sound': 'audio_files/blip_medium.wav', 'loopable': False},
            {'name': 'blip_high',               'sound': 'audio_files/blip_high.wav', 'loopable': False},
            {'name': 'artemis_online',          'sound': 'audio_files/artemis_online.wav', 'loopable': False},
            {'name': 'artemis_offline',         'sound': 'audio_files/artemis_offline.wav', 'loopable': False},
            {'name': 'sensors_online',          'sound': 'audio_files/sensors_online.wav', 'loopable': False},
            {'name': 'sensors_offline',         'sound': 'audio_files/sensors_offline.wav', 'loopable': False},
            {'name': 'targeting_computer_online','sound': 'audio_files/targeting_computer_online.wav', 'loopable': False},
            {'name': 'targeting_computer_offline','sound': 'audio_files/targeting_computer_offline.wav', 'loopable': False},
            {'name': 'single_fire',             'sound': 'audio_files/single_fire_engaged.wav', 'loopable': False},
            {'name': 'linked_fire',             'sound': 'audio_files/linked_fire_engaged.wav', 'loopable': False},
            {'name': 'group_fire',              'sound': 'audio_files/group_fire_engaged.wav', 'loopable': False},
            {'name': 'reactor_online',          'sound': 'audio_files/reactor_online.wav', 'loopable': False},
            {'name': 'reactor_offline',         'sound': 'audio_files/reactor_offline.wav', 'loopable': False},
            {'name': 'power_converter_online',  'sound': 'audio_files/power_converter_online.wav', 'loopable': False},
            {'name': 'power_converter_offline', 'sound': 'audio_files/power_converter_offline.wav', 'loopable': False},
            {'name': 'switch_flipped',          'sound': 'audio_files/mathbutton_yellow.wav', 'loopable': False}, 
            {'name': 'button_pressed',          'sound': 'audio_files/mathbutton_green.wav', 'loopable': False},
            {'name': 'warning',                 'sound': 'audio_files/warning_tone.wav', 'loopable': True},
            {'name': 'flamethrower',            'sound': 'audio_files/flamethrower.wav', 'loopable': False},
            {'name': 'gauss_rifle',             'sound': 'audio_files/gauss_rifle.wav', 'loopable': False},
            {'name': 'missile_launch_01',       'sound': 'audio_files/missile_launch_01.wav', 'loopable': False},
            {'name': 'attacking_machinegun',    'sound': 'audio_files/attacking_machinegun.wav', 'loopable': False},
            {'name': 'ac10_gun',                'sound': 'audio_files/ac10_gun.wav', 'loopable': False},
            {'name': 'ams_engaged',             'sound': 'audio_files/ams_engaged.wav', 'loopable': False},
            {'name': 'ams_offline',             'sound': 'audio_files/ams_offline.wav', 'loopable': False},
            {'name': 'initialization_sequence', 'sound': 'audio_files/initialization_sequence.wav', 'loopable': False},
            {'name': 'heat_warning',            'sound': 'audio_files/heat_warning.wav', 'loopable': True},
            {'name': 'shutdown_sequence',       'sound': 'audio_files/shutdown_sequence.wav', 'loopable': False},
            {'name': 'satellite_established',   'sound': 'audio_files/satellite_link_established.wav', 'loopable': False},
            {'name': 'satellite_shutdown',      'sound': 'audio_files/satellite_link_shutdown.wav', 'loopable': False},
            {'name': 'initiating_scan',         'sound': 'audio_files/scan_initiated.wav', 'loopable': False},
            {'name': 'scan_completed',          'sound': 'audio_files/scan_completed.wav', 'loopable': False},
            {'name': 'shield_generator_active', 'sound': 'audio_files/shield_generator_active.wav', 'loopable': False},
            {'name': 'shield_generator_shutdown','sound': 'audio_files/shield_generator_shutdown.wav', 'loopable': False}
            ]


def parse_arguments(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log", dest="log_level", 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        default='INFO', help="Set the logging level")

    return parser.parse_args(argv)



if __name__ == '__main__':
    print("Starting multiprocess app")

    args = parse_arguments(sys.argv[1:])
    log_level = args.log_level

    q1 = Queue()
    q2 = Queue()
    q3 = Queue()

    message_mapper = MessageMapper(log_level=log_level)
    
    audio_process = Process( target=audio_controller_worker, args=(audio_config, [q3],))
    audio_process.start()

    serial_process_01 = Process( target = serial_processor_worker, args=('/dev/ttyACM1', q1,))
    serial_process_01.start()

    serial_process_02 = Process( target = serial_processor_worker, args=('/dev/ttyACM0', q2,))
    serial_process_02.start()


    while True:
        for q in [q1, q2]:
            if not q.empty():
                event_message = q.get(block=False, timeout=0.01)
                if not event_message:
                    continue
                
                logging.debug("event_message is: %s" % event_message)
                audio_command = message_mapper.getAudiocontrollerMessageForEvent(event_message)
                logging.debug("audio_command is: %s" % audio_command)

                # If the message mapper didn't return a message for the audio controller, continue loop
                if not audio_command:
                    continue

                if not AudioController.isValidAudioCommand(audio_command):
                    logging.error("Audio command [%s] invalid" % audio_command)
                    continue

                q3.put(audio_command)
    

    audio_process.join()
    serial_process_01.join()
    serial_process_02.join()
