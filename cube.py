import itertools
import struct

class Cube(object):
    def __init__(self, size):
        self.size = size
        self.fill(False)

    def fill(self, state):
        s = self.size
        self.cube = (
            [[[state for i in range(s)] for i in range(s)] for i in range(s)]
        )

    def _toggle(self, state, *args):
        if args:
            for pos in args: self.set_pos(pos, state)
        else:
            self.fill(state)        

    def on(self, *args):
        self._toggle(True, *args)

    def off(self, *args):
        self._toggle(False, *args)

    def set_pos(self,   pos, state):
        z, y, x = pos
        self.cube[z][y][x] = state

    def valid_position(self, position):
        return all(0 <= p < self.size for p in position)

    def to_bytes(self):
        def bool_to_bit(bit):
            return '1' if bit else '0'
        
        bytes = ''
        for layer in self.cube:
            flattened = ''.join(bool_to_bit(x) for x in itertools.chain(*layer))
            num = int(flattened, 2)
            bytes += struct.pack('>H', num)
        return bytes

    def __getitem__(self, index):
        return self.cube[index]