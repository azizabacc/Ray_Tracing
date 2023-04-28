import math
from math import sqrt, pi
from transmitter import Transmitter
from line import Line

class Wall(Line):
    relativ_permittivity=0
    conductivity=0
    omega = 2*pi*Transmitter.frequency
    mu0 = Transmitter.mu0
    epsilon0=Transmitter.epsilon0
    def __init__(self, thickness, point_list, material):
        if material == "brick" :
            self.conductivity = 0.02
            self.relativ_permittivity =4.6
        elif material == "concrete" :
            self.conductivity = 0.014
            self.relativ_permittivity = 5
        self.epsilon = self.relativ_permittivity*self.epsilon0
        self.thickness = thickness
        self.material=material
        self.point_list=point_list
        super().__init__(point_list[0],point_list[1])
        #propagation constantes 
        self.alpha=self.omega*sqrt(self.mu0*self.epsilon/2)\
                    *sqrt(sqrt(1+(self.conductivity/(self.omega*self.epsilon))**2)-1)
        self.beta=self.omega*sqrt(self.mu0*self.epsilon/2)\
                   *sqrt(sqrt(1+(self.conductivity/(self.omega*self.epsilon))**2)+1)
        self.little_gamma =complex(self.alpha,self.beta)
        #medium impedancy
        self.a=(sqrt(self.mu0)/(2*sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
                *sqrt(4-(3*self.epsilon)/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.b=(sqrt(self.mu0)/(sqrt(2)*(self.epsilon**2+self.conductivity**2/self.omega**2)**0.25))\
                *sqrt(1-self.epsilon/(sqrt(self.epsilon**2+self.conductivity**2/self.omega**2)))
        self.intrinsic_impedance=complex(self.a,self.b)

    def point_in_Line_outof_wall(self,point):
# returns True if the point is out of the wall (but in the Line containing the wall) 
        x1=point[0]
        y1=point[1]
        v_x=self.direction_vector[0]
        point_outof_wall =True
        if v_x ==0:
            for i in range(len(self.point_list)//2) :
                if self.point_list[2*i][1] <= y1 < self.point_list[2*i+1][1] :
                    point_outof_wall = False
                    break
        else:
            for i in range(len(self.point_list)//2) :
                if self.point_list[2*i][0] <= x1 < self.point_list[2*i+1][0] :
                    point_outof_wall = False
                    break
        return point_outof_wall


