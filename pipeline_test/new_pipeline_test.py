from multiprocessing import Process, Queue
from serialprocessor.serialprocessor import serial_processor_worker
from audiocontroller.audiocontroller import audio_controller_worker, AudioController
from serialprocessor.messagemapper import MessageMapper

import sys
import logging
import argparse


logging.basicConfig(format='%(filename)s.%(lineno)d:%(levelname)s:%(message)s',
                    level=logging.DEBUG)

audio_file_list = [
            {'name': 'systems_nominal',         'loopable': False},
            {'name': 'power_restored',          'loopable': False},
            {'name': 'systems_offline',         'loopable': False},
            {'name': 'blip_low',                'loopable': False},
            {'name': 'blip_medium',             'loopable': False},
            {'name': 'blip_high',               'loopable': False},
            {'name': 'artemis_online',          'loopable': False},
            {'name': 'artemis_offline',         'loopable': False},
            {'name': 'sensors_online',          'loopable': False},
            {'name': 'sensors_offline',         'loopable': False},
            {'name': 'targeting_computer_online','loopable': False},
            {'name': 'targeting_computer_offline','loopable': False},
            {'name': 'light_amp_moderate',      'loopable': False},
            {'name': 'light_amp_maximum',       'loopable': False},
            {'name': 'light_amp_nominal',       'loopable': False},
            {'name': 'single_fire',             'loopable': False},
            {'name': 'linked_fire',             'loopable': False},
            {'name': 'group_fire',              'loopable': False},
            {'name': 'arm_retracted',           'loopable': False},
            {'name': 'arm_extended',            'loopable': False},
            {'name': 'data_transfer_initiated', 'loopable': False},
            {'name': 'data_transfer_complete',  'loopable': False},
            {'name': 'reactor_online',          'loopable': False},
            {'name': 'reactor_offline',         'loopable': False},
            {'name': 'camera_engaged',          'loopable': False},
            {'name': 'camera_offline',          'loopable': False},
            {'name': 'power_converter_online',  'loopable': False},
            {'name': 'power_converter_offline', 'loopable': False},
            {'name': 'ecm_online',              'loopable': False},
            {'name': 'ecm_offline',             'loopable': False},
            {'name': 'beagle_engaged',          'loopable': False},
            {'name': 'beagle_shutdown',         'loopable': False},
            {'name': 'c3_online',               'loopable': False},
            {'name': 'c3_shutdown',             'loopable': False},
            {'name': 'switch_flipped',          'loopable': False}, 
            {'name': 'button_pressed',          'loopable': False},
            {'name': 'warning',                 'loopable': True},
            {'name': 'flamethrower',            'loopable': False},
            {'name': 'lbx_10',                  'loopable': False},
            {'name': 'srm4_launch',             'loopable': False},
            {'name': 'xpulse_large',            'loopable': False},
            {'name': 'laser_small',             'loopable': False},
            {'name': 'laser_large',             'loopable': False},
            {'name': 'gauss_rifle',             'loopable': False},
            {'name': 'missile_launch_01',       'loopable': False},
            {'name': 'attacking_machinegun',    'loopable': False},
            {'name': 'ac10_gun',                'loopable': False},
            {'name': 'ams_engaged',             'loopable': False},
            {'name': 'ams_offline',             'loopable': False},
            {'name': 'initialization_sequence', 'loopable': False},
            {'name': 'heat_warning',            'loopable': True},
            {'name': 'shutdown_sequence',       'loopable': False},
            {'name': 'satellite_established',   'loopable': False},
            {'name': 'satellite_shutdown',      'loopable': False},
            {'name': 'initiating_scan',         'loopable': False},
            {'name': 'scan_completed',          'loopable': False},
            {'name': 'shield_generator_active', 'loopable': False},
            {'name': 'shield_generator_shutdown','loopable': False}
            ]

audio_config = { 
    'audio_file_list': audio_file_list,
    'default_audio_path': 'audio_files'
 }

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
