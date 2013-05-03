from matplotlib.mlab import find
import itertools
import math
import numpy
import time
import pprint
import pyaudio
import pygame
import random
import serial
import struct
import wave

from serial.tools.list_ports import comports
from random import randrange

BAUD_RATE = 115200
SIZE = 4

ser = None
cube = [[[]]]

def get_port():
    ports = comports()
    for i, (name, desc, _) in enumerate(ports):
        print('{i}: {name}'.format(i=i, name=name))
    port = raw_input('which port? ')
    try:
        return ports[int(port)][0]
    except (ValueError, IndexError):
        pass
    return port

def fill(n=0):
    global cube
    cube = [[[n for i in range(SIZE)] for i in range(SIZE)] for i in range(SIZE)]

def write():
    global cube, ser
    for layer in cube:
        # flatten 4x4 integer array into binary representation of number
        flattened = ''.join(str(x) for x in itertools.chain(*layer))
        num = int(flattened, 2)
        binary = struct.pack('>H', num)
        pprint.pprint(binary)
        ser.write(binary)

def effect_random():
    print "EFFECT RANDOM"
    global cube
    for i in range(200):
        fill(0)
        for j in range(4):
            cube[randrange(SIZE)][randrange(SIZE)][randrange(SIZE)] = 1
        tick(60)

def effect_steady():
    print "EFFECT STEADY"
    fill(1)
    tick(5000)
        

def effect_blink():
    print "EFFECT BLINK"
    for i in range(5):
        fill(1)
        tick(20)
        fill(0)
        tick(20)

def effect_loadbar(delay=50):
    fill(0)
    for z in range(4):
        for y in range(4):
            for x in range(4):
                cube[z][y][x] = 1
        tick(delay)
    tick(delay*3)
    for z in reversed(range(4)):
        for y in range(4):
            for x in range(4):
                cube[z][y][x] = 0
        tick(delay)

def effect_random_onoff():
    def effect(delay, state):
        loop = 0
        while loop < 63:
            x = random.randint(0,3)
            y = random.randint(0,3)
            z = random.randint(0,3)
            if ((state == 0 and cube[z][y][x] == 1) or (state == 1 and cube[z][y][x] == 0)):

                cube[z][y][x] = (cube[z][y][x] + 1) % 2
                tick(max(int(math.log((loop + 1)) * delay), 30))
                loop += 1
    fill(0)
    effect(20, 1)
    tick(1000)
    effect(20, 0)

def effect_plane():
    effect_sendplaneto_z(0, 3)

def effect_sendplaneto_z(oldZ, newZ):
    fill(0)
    setPlane(oldZ)
    loop = 16
    while loop>0:
        x = random.randint(0,3)
        y = random.randint(0,3)
        if(cube[oldZ][y][x] == 1):
            sendVoxelZ(x,y,oldZ,newZ)
            loop -= 1
            tick(200)

def sendVoxelZ(x,y,currentZ,newZ):
    if currentZ > newZ:
        for i in range(currentZ-newZ):
            tick(50)
            cube[currentZ+i][y][x] = 0
            cube[currentZ-i+1][y][x] = 1
    elif newZ > currentZ:
        for i in range(newZ-currentZ):
                tick(50)
                cube[currentZ+i][y][x] = 0
                cube[currentZ+i+1][y][x] = 1

def setPlane(z):
    for y in range(4):
        for x in range(4):
            cube[z][y][x] = 1

def tick(ms):
    received_data = ser.readline()
    write()
    pygame.time.delay(ms)

def main():
    global cube, ser
    pygame.init()
    fill()
    clock = pygame.time.Clock()
    ser = serial.Serial(get_port(), BAUD_RATE, timeout=0)
    effects = [music]
    while True:
        random.choice(effects)()
    ser.close()

class SimpleBeatDetection:
    """
    Simple beat detection algorithm from
    http://archive.gamedev.net/archive/reference/programming/features/beatdetection/index.html
    """
    def __init__(self, history = 43):
        self.local_energy = numpy.zeros(history) # a simple ring buffer
        self.local_energy_index = 0 # the index of the oldest element

    def detect_beat(self, signal):

        samples = signal.astype(numpy.int) # make room for squares
        # optimized sum of squares, i.e faster version of (samples**2).sum()
        instant_energy = numpy.dot(samples, samples) / float(0xffffffff) # normalize

        local_energy_average = self.local_energy.mean()
        local_energy_variance = self.local_energy.var()

        beat_sensibility = (-0.0025714 * local_energy_variance) + 1.15142857
        beat = instant_energy > beat_sensibility * local_energy_average

        self.local_energy[self.local_energy_index] = instant_energy
        self.local_energy_index -= 1
        if self.local_energy_index < 0:
            self.local_energy_index = len(self.local_energy) - 1

        return beat


def music():
    global cube
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    while True:
        data = stream.read(CHUNK)
        signal = numpy.fromstring(data, 'Int16')
        fft = numpy.fft.rfft(signal, 34)
        coeffs = numpy.absolute(fft)[1:17]
        fill(0)
        for i, coeff in enumerate(coeffs):
            print min(4, int(coeff/100))
            level = int(min(4, coeff / 100))
            print coeff
            for j in range(level):
                cube[j][i / 4][i % 4] = 1
        tick(0)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()



if __name__ == '__main__':
    main()