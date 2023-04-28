import math
from transmitter import Transmitter


class Receiver:
    def __init__(self, position, type):
        self.position = position
        self.received_mean_power = 0
        self.received_local_power = 0
        self.received_bit_rate = 0
        if type == "half_wave":
            # Height above average terrain
            # that we will use squared => therefore no concept of sign
            self.he = Transmitter.wavelength / math.pi
        else:
            pass
