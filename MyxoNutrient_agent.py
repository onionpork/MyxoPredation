import numpy as np
from mesa import Agent, Model
from math import sin, cos
import math

class Myxo(Agent):
    """
    Myxo Agent 
    The agent follows several properties to move:
        - speed : v_mu, v_std
        - rad: deviation angle calculated by angleLow, angleHigh and white noise; rad changes the heading direction
        - deviation angle: angleLow, angleHigh
        - white noise for deviation angle: white_angle_mu, white_angle_std
        - reversal: clock - record the timestamp to reverses; reversal - reversal period; sign - the moving direction
        - OPTION: the angle deviates only during the reversal (Not None); deviates all the time (None)

    """

    def __init__(self, unique_id, model, pos, v_mu, v_std, 
                angleLow, angleHigh, white_angle_mu, white_angle_std, 
                reversal, clock, dt, OPTION):
        super().__init__(unique_id, model)
        self.name = "Myxo"
        self.pos = np.array(pos)
        self.v_mu = v_mu
        self.v_std = v_std
        self.white_angle_mu = white_angle_mu
        self.white_angle_std = white_angle_std
        self.clock = clock
        self.angleHigh = angleHigh
        self.angleLow = angleLow
        self.speed = 0 
        self.sign = 1
        self.rad = 0 
        self.reversal = reversal
        self.dt = dt
        self.OPTION = OPTION

    
    def step(self):
        self.clock += 1
        d_phi = np.random.uniform(low=self.angleLow, high=self.angleHigh)

        reversal_time = np.random.choice(self.reversal, 1)
        if self.clock > reversal_time/ self.dt:
            self.clock = 0
            self.sign *= -1

        self.speed = np.random.normal(self.v_mu, self.v_std, 1)


        if self.OPTION is not None:
            if self.sign == -1:
                self.rad += \
                            np.random.normal(self.white_angle_mu, self.white_angle_std, 1)* np.sqrt(2*d_phi)*self.dt
        else:
            self.rad += \
                        np.random.normal(self.white_angle_mu, self.white_angle_std, 1)* np.sqrt(2*d_phi)*self.dt

        self.heading = np.array([cos(self.rad), sin(self.rad)])
        self.heading /= np.linalg.norm(self.heading)

        new_pos = np.array(self.pos) + self.heading * self.speed* self.dt
        self.model.space.move_agent(self, new_pos)


class Nutrient(Agent):

    def __init__(self, pos, model, myxo, nutrient_level=0):
        super().__init__(pos, model)
        self.name = "Nutrient"
        self.nutrient_level = nutrient_level
        self.myxo = myxo

    def step(self):
        self.cellx = math.floor(self.myxo.pos[0])
        self.celly = math.floor(self.myxo.pos[1])
        
        if self.pos == (self.cellx, self.celly) and self.nutrient_level > 0:
            self.nutrient_level -= 0.1
            if self.nutrient_level <= 0:
                self.model.grid.remove_agent(self)



