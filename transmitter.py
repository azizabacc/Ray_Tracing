import math


class Transmitter:
    frequency = 27 * 10 ** 9
    epsilon0 = 8.854 * 10 ** -12
    mu0 = 4 * math.pi * 10 ** -7
    wavelength = 1 / (math.sqrt(mu0 * epsilon0) * frequency)

    def __init__(self, position, type):
        self.position = position
        if type == "half_wave":
            self.resistance = 73
            self.gain = 1.63
            self.power = 0.1
            """ 0.1 Watt = 20dBm """
        else:
            pass
