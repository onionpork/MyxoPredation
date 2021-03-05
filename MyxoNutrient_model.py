import random 
import numpy as np
from mesa import Model
from mesa.space import ContinuousSpace, MultiGrid
from MyxoNutrient_agent import Myxo, Nutrient
from mesa.datacollection import DataCollector
from nutrient_schedule import NutrientRandomActivation

class MyxoModel(Model):

    def __init__(self, x, y, N, width, height, v_mu, v_std, angleLow, angleHigh, \
                white_angle_mu, white_angle_std, reversal, clock, dt, initx, inity, nutrient_range, OPTION):

        pos = np.array((x, y))
        self.N = N
        self.v_mu = v_mu
        self.v_std = v_std
        self.angleLow = angleLow
        self.angleHigh = angleHigh
        self.white_angle_mu = white_angle_mu
        self.white_angle_std = white_angle_std
        self.reversal = reversal
        self.dt = dt
        self.clock = clock
        self.schedule = NutrientRandomActivation(self)
        self.space = ContinuousSpace(width, height, True, 0, 0)
        self.grid = MultiGrid(width, height, torus=True)
        self.OPTION = OPTION
        self.nutrientx = initx
        self.nutrienty = inity
        self.nutrientrange = nutrient_range

        self.datacollector = DataCollector({"Position": \
                                            lambda x: x.schedule.get_breed_count(Myxo), 
                                            "Nutrient":\
                                                lambda x:x.schedule.get_breed_count(Nutrient)})
        
        for i in range(self.N):
            myxo = Myxo(i, self, pos, self.v_mu, self.v_std, self.angleLow, self.angleHigh, \
                        self.white_angle_mu, self.white_angle_std, self.reversal, self.clock, self.dt, self.OPTION)
            self.space.place_agent(myxo, pos)
            self.schedule.add(myxo)

        for agent, x, y in self.grid.coord_iter():
            if x in range(self.nutrientx - self.nutrientrange, self.nutrientx + self.nutrientrange)\
                and y in range(self.nutrienty - self.nutrientrange, self.nutrienty + self.nutrientrange):
                nutrient = Nutrient((x, y), self, myxo, nutrient_level = 1)

            else:
                nutrient = Nutrient((x, y), self, myxo)
            
            self.grid.place_agent(nutrient, (x, y))
            self.schedule.add(nutrient)

        self.running = True
        self.datacollector.collect(self)

    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)