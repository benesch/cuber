import random
import effects

from cube import Cube
from communicator import Communicator
from pygame.time import delay

__all__ = ['tick']

com = None

def main():
    global cube, com
    cube = Cube(4)
    com = Communicator()

    effs = effects.get_effects()
    e = random.choice(effs)(tick, cube)
    while True:
        try:
            print e.name
            e.run()
            e = random.choice(effs)(tick, cube)
        except KeyboardInterrupt:
            print "available effects: "
            e = prompt(effs)(tick, cube)

def tick(ms):
    global com
    com.write(cube)
    delay(ms)

def prompt(choices):
    while True:
        for i, choice in enumerate(choices):
            print('{i}: {name}'.format(i=i, name=choice.name))

        selection = raw_input("which? ")
        try:
            return choices[int(selection)]
        except (ValueError, IndexError):
            print "try again!"

if __name__ == '__main__':
    main()