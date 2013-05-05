import serial

from serial.tools.list_ports import comports


class Communicator(object):
    BAUD_RATE = 115200
    TIMEOUT = 0

    def __init__(self):
        port = self._get_port()
        self.ser = serial.Serial(port, self.BAUD_RATE, timeout=self.TIMEOUT)

    def _get_port(self):
        ports = comports()
        for i, (name, desc, _) in enumerate(ports):
            print('{i}: {name}'.format(i=i, name=name))
        port = raw_input('which serial port? ')
        try:
            index = int(port)
            return ports[index][0]
        except (ValueError, IndexError):
            pass
        return port

    def write(self, cube):
        self.ser.readline() # necessary for syncing
        self.ser.write(cube.to_bytes())