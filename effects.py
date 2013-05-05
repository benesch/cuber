import audio
import datetime
import collections
import numpy
import random
import utils
from cuber import tick

def get_effects():
    return Effect.__subclasses__()

class Effect(object):
    DEFAULT_SPEED = 30
    DEFAULT_LENGTH = 200

    def __init__(self, tick, cube, speed=None, length=None):
        self.tick = tick
        self.cube = cube
        self.speed = self.DEFAULT_SPEED if speed is None else speed
        self.length = self.DEFAULT_LENGTH if length is None else length
        self.setup()

    def setup(self):
        pass

    def _run(self):
        raise NotImplementedError

    def _randidx(self):
        return random.randrange(0, self.cube.size)

    def run(self):
        for i in range(self.length):
            self._run()
            self.tick(self.speed)

    def __repr__(self):
        print "Base Effect"

class RandomEffect(Effect):
    name = "Random"

    DEFAULT_SPEED = 60

    def _run(self):
        self.cube.off()
        for j in range(4):
             self.cube[self._randidx()][self._randidx()][self._randidx()] = 1

        self.speed -= 1

class SteadyEffect(Effect):
    name = "Steady"

    DEFAULT_LENGTH = 100

    def _run(self):
        self.cube.on()
        
class BlinkEffect(Effect):
    name = "Blink"
    state = False

    DEFAULT_SPEED = 100
    DEFAULT_LENGTH = 100

    def _run(self):
        self.cube.fill(self.state)
        self.state = not self.state

class MusicEffect(Effect):
    name = "Music"
    ADJUST = 80
    DEFAULT_SPEED = 0
    DEFAULT_LENGTH = 2000

    def setup(self):
        self.stream = audio.open()

    def _run(self):
        data = self.stream.read(audio.CHUNK)
        signal = numpy.fromstring(data, 'Int16')
        fft = numpy.fft.rfft(signal, 34)
        coeffs = numpy.absolute(fft)[1:17] / self.ADJUST
        self.cube.off()
        for i, coeff in enumerate(coeffs):
            level = int(min(4, coeff / 100))
            for j in range(level):
                self.cube[j][i / 4][i % 4] = 1

class BeatEffect(Effect):
    name = "Beat"
    ADJUST = 80
    DEFAULT_SPEED = 0
    DEFAULT_LENGTH = 2000

    def setup(self):
        self.stream = audio.open()

    def _run(self):
        data = self.stream.read(audio.CHUNK)
        signal = numpy.fromstring(data, 'Int16')
        fft = numpy.fft.rfft(signal, 34)
        coeff = numpy.absolute(fft)[0] / self.ADJUST
        if coeff > 500:
            self.cube.on()
        else:
            self.cube.off()
        

class SnakeEffect(Effect):
    name = "Snake"
    directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
                  (0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    DEFAULT_LENGTH = 500

    def setup(self):
        self.snake_length = 3
        self.pos = collections.deque()
        self.pos.append((self._randidx(), self._randidx(), self._randidx()))
        self.direction = random.choice(self.directions)
        self.cube.off()

    def _run(self):
        valid_directions = [d for d in self.directions if d != self.direction and d != utils.tuple_invert(self.direction)]
        pos = utils.tuple_sum(self.pos[-1], self.direction)
        valid = self.cube.valid_position(pos)
        while not valid:
            self.direction = random.choice(valid_directions)
            pos = utils.tuple_sum(self.pos[-1], self.direction)
            valid = self.cube.valid_position(pos)
        self.pos.append(pos)
        if len(self.pos) > self.snake_length:
            self.pos.popleft()
        self.cube.off()
        self.cube.on(*self.pos)

class LoadbarEffect(Effect):
    name = "Loading Bar"
    DEFAULT_SPEED = 200
    DEFAULT_LENGTH = 20

    def setup(self):
        self.z = 0
        self.direction = -1

    def _run(self):
        if self.z == 0 or self.z == self.cube.size - 1:
            self.direction *= -1
            self.cube.off()
        self.z += self.direction

        for y in range(self.cube.size):
            for x in range(self.cube.size):
                self.cube.on((self.z, y, x)) 