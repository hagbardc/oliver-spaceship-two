import subprocess
import pygame
import time
import os


print "Setting display environment variable"
os.environ['DISPLAY'] = ':0'

print "Starting pulseaudio"
subprocess.call(['/usr/bin/pulseaudio', '-D'])
print "sleep 1"
time.sleep(1)
#print "Starting jackd"
#subprocess.call(['/usr/bin/jackd', '-d', 'alsa', '&'])
#print "sleep 1"
#time.sleep(1)

print "initing pygame"
pygame.init()
pygame.mixer.init()


snd1 = pygame.mixer.Sound("sounds/piano2.wav")
snd2 = pygame.mixer.Sound("sounds/piano2.wav")

print "Playing sound 1"
c1 = snd1.play()
time.sleep(2)
print "playing sound 2"
c2 = snd2.play()
time.sleep(2)
c1.stop()
time.sleep(5)
