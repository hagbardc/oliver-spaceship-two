import serial
import threading


def child(port):
    while True:
        line = port.readline()
        if not line:
            break
        print('child(): read line: {!r}'.format(line))


baud = 19200
port_locations = ['/dev/ttyUSB0', '/dev/ttyACM0']
ports = []

for p in port_locations:
    port = serial.Serial(p, baud)
    ports.append(port)


threads = []
for p in ports:
    print("Creating thread")
    t = threading.Thread(target=child, args=[p])
    threads.append(t)
    print("Starting thread")
    t.start()

while(True):
    pass
