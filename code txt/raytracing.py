from view import create_wall, plot_wall, plott, power_graphical_display, ray_graphical_display
from ray import Ray
from line import Line
import copy
import math
import cmath
import numpy as np


def between(point1, point2, point3):
    """ point1 belongs to the line containing the segment [point2,point3]
        This function verifies if point1 belongs to the segment [point2,point3] and returns True if it is the case"""
    result = False
    if point2[0] == point3[0]:
        if (point2[1] <= point1[1] <= point3[1]) or (point2[1] >= point1[1] >= point3[1]):
            result = True
    else:
        if (point2[0] <= point1[0] <= point3[0]) or (point2[0] >= point1[0] >= point3[0]):
            result = True
    return result


def end_calculated_localpower(receiver):
    """finalisation of the calculation of the mean power """
    receiver.received_local_power = (abs(receiver.received_local_power)) ** 2
    return 0


def calculate_mean_power(ray_list, receiver, transmitter):
    mean_power = 0
    for ray in ray_list:
        attenuation = 1
        for coeff_ref in ray.reflection_coef:
            attenuation = attenuation * abs(coeff_ref)
        for coeff_tran in ray.transmission_coef:
            attenuation = attenuation * abs(coeff_tran)
        if ray.distance == 0:
            continue
        E = attenuation * math.sqrt(60 * transmitter.gain * transmitter.power) / ray.distance
        hE = receiver.he * E
        mean_power = mean_power + hE ** 2
    mean_power = mean_power / (8 * transmitter.resistance)
    return mean_power


def bit_rate_power(power):
    # converts le power to bit rate
    if power == 0:
        bit_rate = 0
    else:
        sensibility = 10 * math.log10(power / 10 ** -3)  # todo c'est juste ??
        if sensibility < -82:
            bit_rate = 0
        elif sensibility == -82:
            bit_rate = 40
        elif sensibility > -73:
            bit_rate = 320
        else:
            # considering the relation sensibility-bit_rate linear in this interval
            # bit_rate = 35.55 * sensibility + 2915.1
            bit_rate = 31.11111111 * sensibility + 2591.111111

    return bit_rate


def transmission_coeff_calc(wall, ray, ray_line):
    coeff = ray.transmission_coef_calculator(wall, ray_line)
    ray.transmission_coef.append(coeff)
    return 0


def reflection_coeff_calc(wall, ray, ray_line):
    coeff = ray.reflection_coef_calculator(wall, ray_line)
    ray.reflection_coef.append(coeff)
    return 0


def dist(point1, point2):
    eucli_distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return eucli_distance


def image(original_point, line):
    """returns the original point image by orthogonal symmetry with respect to the line"""

    x1 = original_point[0]
    y1 = original_point[1]
    x2 = line.point[0]
    y2 = line.point[1]
    v_x = line.direction_vector[0]
    v_y = line.direction_vector[1]
    d = (y2 - y1) * v_x - (x2 - x1) * v_y
    v_perp = (-v_y * d, v_x * d)
    image_point = tuple(map(sum, zip(original_point, v_perp, v_perp)))
    return image_point


def verif_transmission(ray, wall_list, sub_wall_list):
    """ fills the list of transmission coefficients of ray """
    T = len(sub_wall_list)
    for i in range(len(ray.point_list) - 1):
        ray_line = Line(ray.point_list[i], ray.point_list[i + 1])
        reflection_wall = []  # for each ray segment, a list containing the walls on which the ray is reflected
        # there is no transmission on these walls
        if i == 0:
            if sub_wall_list:
                reflection_wall.append(sub_wall_list[T - 1])
        elif i == len(ray.point_list) - 2:
            reflection_wall.append(sub_wall_list[0])
        else:
            reflection_wall.append(sub_wall_list[T - i])
            reflection_wall.append(sub_wall_list[T - i - 1])
        for j in wall_list:
            if j in reflection_wall:
                # no transmission
                continue
            intersection = ray_line.intersection(j)  # intersection of the ray segment and the wall line
            if not j.point_in_Line_outof_wall(intersection):
                # reflection on corner => ray not counted
                if (intersection == ray.point_list[i]) or (intersection == ray.point_list[i + 1]):
                    ray.point_list = []
                    return 0
                if between(intersection, ray.point_list[i], ray.point_list[i + 1]):
                    """ if the intersection with the wall j takes place => transmission coefficient calculation """
                    transmission_coeff_calc(j, ray, ray_line)
    return 0


def calculate_local_power(ray_list, receiver, transmitter):
    # calculates the local power taking into account all the connecting rays between the receiver and transmitter
    power = 0
    for ray in ray_list:
        attenuation = 1
        for coeff_ref in ray.reflection_coef:
            attenuation = attenuation * coeff_ref
        for coeff_tran in ray.transmission_coef:
            attenuation = attenuation * coeff_tran
        if ray.distance == 0:
            continue
        E = attenuation * math.sqrt(60 * transmitter.gain * transmitter.power) * cmath.exp(
            -1j * ray.beta_air * ray.distance) / ray.distance
        hE = receiver.he * E
        power += hE

    power /= math.sqrt(8) * math.sqrt(transmitter.resistance)
    return power


class Raytracing:
    def __init__(self):
        self.wall_list = []
        self.transmitter_list = []
        self.receiver_list = []
        self.direct_ray_calculated = False

    def ray_power_distribution(self, receiver_position, max_number_reflection, graphical_display):
        """arguments :
-receiver_position
-max_number_reflection : maximum number of s allowed
-graphical_display : ( string ) local, mean, rays"""
        # text files containing the bit rate value of each receiver in their positions
        f1 = open("local_bit_rate.txt", "w")
        f2 = open("mean_bit_rate.txt", "w")
        for receiver in self.receiver_list:
            for transmitter in self.transmitter_list:
                self.direct_ray_calculated = False
                ray_list = []

                # call of the recursive function of ray tracing
                self.ray_tracing([], max_number_reflection, transmitter, receiver, self.wall_list, ray_list)
                if "mean" in graphical_display:
                    receiver.received_mean_power += calculate_mean_power(ray_list, receiver, transmitter)
                if "local" in graphical_display:
                    receiver.received_local_power += calculate_local_power(ray_list, receiver, transmitter)
                if ("ray" in graphical_display) and (receiver.position == receiver_position) and (
                        transmitter == self.transmitter_list[0]):
                    ray_graphical_display(receiver, transmitter, self.wall_list, ray_list)
            if "local" in graphical_display:
                # finalization of the calculation of the local power
                end_calculated_localpower(receiver)
                # convertion of the local power to bit rate
                receiver.received_bit_rate = bit_rate_power(receiver.received_local_power)  # todo
                # receiver.received_bit_rate = receiver.received_local_power
                f1.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.received_bit_rate) + "\n")
            if "mean" in graphical_display:
                # convertion of the mean power to bit rate
                receiver.received_bit_rate = bit_rate_power(receiver.received_mean_power)  # todo
                # receiver.received_bit_rate = receiver.received_mean_power
                f2.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.received_bit_rate) + "\n")

        f1.close()
        f2.close()
        # self.ray_graphical_display(receiver,transmitter,ray_list)#todo
        if "local" in graphical_display:
            power_graphical_display("local_bit_rate.txt", self.wall_list, self.transmitter_list)
        if "mean" in graphical_display:
            power_graphical_display("mean_bit_rate.txt", self.wall_list, self.transmitter_list)

    def ray_tracing(self, saved_list, max_number_reflection, transmitter, receiver, wall_list, ray_list):
        """ recursive function of ray tracing : on each call of the function, max_number_reflection is decremented by one unit
parameters:
- saved_list :list which allows the saving of a list from one iteration to another
- max_number_reflection : maximum number of s allowed
- wall_list : list of walls in the room
- ray_list : list of the rays
- transmitter
- receiver
"""
        if max_number_reflection == 0:
            # case where we do not admit a direct ray
            sub_wall_list = []
            if self.direct_ray_calculated is False:
                # direct ray creation
                ray = self.ray_creation(sub_wall_list, transmitter, receiver)
                ray_list.append(ray)
                self.direct_ray_calculated = True
        elif max_number_reflection != 1:
            # condition to continue the recursivity ( max_number_reflection > 1 : decrementation allowed)
            max_number_reflection = max_number_reflection - 1
            for j in range(len(wall_list)):
                if len(saved_list) == 0:
                    pass
                elif j == saved_list[len(saved_list) - 1]:  # can not add 2 identical walls to the list
                    continue
                saved_list_copy = copy.deepcopy(
                    saved_list)  # saved_list_copy is a deepcopy of saved_list, which allows the saving of saved_list in each iteration
                saved_list_copy.append(j)  # saved_list_copy and saved_list : lists of walls index used in ray_creation
                sub_wall_list = []
                for k in saved_list_copy:
                    sub_wall_list.append(wall_list[k])  # unique wall list per iteration
                ray = self.ray_creation(sub_wall_list, transmitter, receiver)  # ray creation direct
                if len(ray.point_list) != 0:
                    ray_list.append(ray)
                # recursive call
                self.ray_tracing(saved_list_copy, max_number_reflection, transmitter, receiver, wall_list, ray_list)
        elif max_number_reflection == 1:
            # last recursion step
            sub_wall_list = []
            if self.direct_ray_calculated is False:
                ray = self.ray_creation(sub_wall_list, transmitter, receiver)  # ray creation direct
                ray_list.append(ray)
                self.direct_ray_calculated = True
            for j in range(len(wall_list)):
                if not saved_list:
                    pass
                elif j == saved_list[len(saved_list) - 1]:
                    continue
                saved_list_copy = copy.deepcopy(saved_list)
                saved_list_copy.append(j)
                sub_wall_list = []
                for k in saved_list_copy:
                    sub_wall_list.append(wall_list[k])
                ray = self.ray_creation(sub_wall_list, transmitter, receiver)
                if ray.point_list:
                    ray_list.append(ray)

    def ray_creation(self, sub_wall_list, transmitter, receiver):
        """  creates the set of rays going through the sub_wall_list and connecting the transmitter to the receiver """
        point = transmitter.position
        image_list = []
        ray = Ray([])
        for wall in sub_wall_list:
            # images creation
            image_point = image(point, wall)
            image_list.append(image_point)
            point = image_point
        ray.point_list.append(receiver.position)
        ray_point = receiver.position  # starting point of ray tracing
        if len(sub_wall_list) != 0:
            ray.distance = dist(receiver.position, image_list[
                len(image_list) - 1])  # used in the reflection and transmission coefficient calculation
        else:  # direct ray case
            ray.distance = dist(receiver.position, transmitter.position)
        for j in range(len(image_list)):
            # creation of all the rays
            ray_line = Line(ray_point, image_list[len(image_list) - 1 - j])
            intersection_point = ray_line.intersection(
                sub_wall_list[len(image_list) - 1 - j])  # intersection point wall / ray
            if sub_wall_list[len(image_list) - 1 - j].point_in_Line_outof_wall(intersection_point):
                ray.point_list = []  # no intersection with the wall, ray not counted
                break
            if between(intersection_point, ray_point, image_list[len(image_list) - 1 - j]):
                # verifies if the intersection point belongs to the segment [image, receiver]
                ray_point = intersection_point
                ray.point_list.append(ray_point)
            else:  # do not belong
                ray.point_list = []  # ray not counted
                break
            # calculation of each reflection coefficient of the ray
            reflection_coeff_calc(sub_wall_list[len(image_list) - 1 - j], ray, ray_line)
        # end point of ray tracing
        if len(ray.point_list) != 0:
            ray.point_list.append(transmitter.position)
        # calculation of each transmission coefficient of the ray
        if len(ray.point_list) != 0:
            verif_transmission(ray, self.wall_list, sub_wall_list)

        return ray

    def ray_bit_rate_distribution(self, max_number_reflection=0, graphical_display='mean'):
        """arguments :
-receiver_position
-max_number_reflection : maximum number of s allowed
-graphical_display : ( string ) local, mean, rays"""
        # text files containing the bit rate value of each receiver in their positions
        f1 = open("local_bit_rate.txt", "w")
        f2 = open("mean_bit_rate.txt", "w")
        for receiver in self.receiver_list:
            for transmitter in self.transmitter_list:
                self.direct_ray_calculated = False
                ray_list = []

                # call of the recursive function of ray tracing
                self.ray_tracing([], max_number_reflection, transmitter, receiver, self.wall_list, ray_list)
                if "mean" in graphical_display:
                    receiver.received_mean_power += calculate_mean_power(ray_list, receiver, transmitter)
                if "local" in graphical_display:
                    receiver.received_local_power += calculate_local_power(ray_list, receiver, transmitter)
            if "local" in graphical_display:
                # finalization of the calculation of the local power
                end_calculated_localpower(receiver)
                # convertion of the local power to bit rate
                receiver.received_bit_rate = bit_rate_power(receiver.received_local_power)  # todo
                # receiver.received_bit_rate = receiver.received_local_power
                f1.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.received_bit_rate) + "\n")
            if "mean" in graphical_display:
                # convertion of the mean power to bit rate
                receiver.received_bit_rate = bit_rate_power(receiver.received_mean_power)  # todo
                # receiver.received_bit_rate = receiver.received_mean_power
                f2.write(str(receiver.position[0]) + " " + str(receiver.position[1]) + " " + str(
                    receiver.received_bit_rate) + "\n")

        f1.close()
        f2.close()
        # self.ray_graphical_display(receiver,transmitter,ray_list)#todo
        if "local" in graphical_display:
            x, y, br = np.loadtxt("local_bit_rate.txt").T
            x= x.tolist()
            y= y.tolist()
            br= br.tolist()
            return [x, y, br]
        if "mean" in graphical_display:
            x, y, br = np.loadtxt("mean_bit_rate.txt").T
            x= x.tolist()
            y= y.tolist()
            br= br.tolist()
            return [x, y, br]
