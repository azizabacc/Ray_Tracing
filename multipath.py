import cmath
from math import pi, cos, sin, sqrt
from transmitter import Transmitter
from line import Line

class MultiPath(Line):
    omega = 2 * pi * Transmitter.frequency
    epsilon0 = 8.854 * 10 ** (-12)
    mu0 = 4 * pi * 10 ** (-7)
    beta_air = 2 * pi / Transmitter.wavelength

    def __init__(self, point_list):
        self.point_list = point_list
        self.distance = 0
        self.reflection_coef = []
        self.transmission_coef = []

    def reflection_coef_calculator(self, wall, ray_line):
        """ parameters:
            - wall : wall where the reflection takes place
            - ray_line : incident line segment of the ray
            return :
            reflexion coefficient of the wall """
        theta_i = wall.theta_i_calculator(ray_line)
        theta_t = wall.theta_t_calculator(wall, theta_i)
        epsilon_tilde = self.epsilon0
        Z_0 = sqrt(self.mu0 / epsilon_tilde)
        Z_m = wall.intrinsic_impedance
        gamma_perp = (Z_m * cos(theta_i) - Z_0 * cos(theta_t)) / (Z_m * cos(theta_i) + Z_0 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        gamma_wall = gamma_perp + (1 - gamma_perp ** 2) * (
                    gamma_perp * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
                1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t))) / (
                                 1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
                             1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        return gamma_wall

    def transmission_coef_calculator(self, wall, ray_line):
        """ parameters:
            - wall : wall where the transmission takes place
            - ray_line : incident line segment of the ray
            return :
            reflexion coefficient of the wall """

        theta_i = wall.theta_i_calculator(ray_line)
        theta_t = wall.theta_t_calculator(wall, theta_i)
        epsilon_tilde = self.epsilon0
        Z_0 = sqrt(self.mu0 / epsilon_tilde)
        Z_m = wall.intrinsic_impedance
        gamma_perp = (Z_m * cos(theta_i) - Z_0 * cos(theta_t)) / (Z_m * cos(theta_i) + Z_0 * cos(theta_t))
        s = wall.thickness / cos(theta_t)
        little_gamma_wall = wall.little_gamma
        tau_wall = (1 - gamma_perp ** 2) * cmath.exp(-little_gamma_wall * s) / (
                    1 - (gamma_perp ** 2) * cmath.exp(-2 * little_gamma_wall * s) * cmath.exp(
                1j * self.beta_air * 2 * s * sin(theta_i) * sin(theta_t)))
        return tau_wall
