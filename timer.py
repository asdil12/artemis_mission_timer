#!/usr/bin/python3

import serial
import Pyro4
import json
import time

warserver = "PYRONAME:warserver"
serial_interface = "/dev/ttyS0"


ser = serial.Serial(serial_interface, 9600)
print("Using serial device: %s" % ser.name)

game = Pyro4.Proxy(warserver)
assert game.ping(), "Could not find warserver"
print("Found Warserver %s at %s" % (warserver, game.get_ip()))

ser.write(b'\x8E')

ob = bytes()

while True:
    turn_info = json.loads(game.get("turn"))
    print(turn_info)

    b = bytes()

    if turn_info['interlude']:
        b += b'\x89\x82Interlude Time  '
    else:
        b += b'\x89\x80Mission Time    '

    b += b'\x8A\x87'
    t = time.strftime("%M:%S", time.gmtime(int(turn_info['remaining'])))
    b += t.encode("ASCII")

    b += b'\x85      '
    b += str("%02i" % turn_info['turn_number']).encode("ASCII")
    b += b'/'
    b += str("%02i" % turn_info['max_turns']).encode("ASCII")

    if ob != b:
        ser.write(b)
        ob = b

    time.sleep(0.1)


ser.close()  
