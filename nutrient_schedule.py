import random 
from collections import defaultdict
from mesa.time import RandomActivation 
import numpy as np

class NutrientRandomActivation(RandomActivation):
    agents_by_breed = defaultdict(list)

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_breed = defaultdict(list)


    def add(self, agent):
        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_by_breed[agent_class].append(agent)

    def remove(self, agent):

        while agent in self.agents:
            self.agents.remove(agent)
        
        agent_class = type(agent)
        while agent in self.agents_by_breed[agent_class]:
            self.agents_by_breed[agent_class].remove(agent)

    def step(self, by_breed = True):
        if by_breed:
            for agent_class in self.agents_by_breed:
                self.step_breed(agent_class)
        else:
            super().step()
        
        self.steps += 1
        self.time += 1

    def step_breed(self, breed):
        agents = self.agents_by_breed[breed]
        for agent in agents:
            agent.step()

    def get_breed_count(self, breed_class):
        if len(self.agents_by_breed[breed_class]) == 1:
            agent_pos = self.agents_by_breed[breed_class][0].pos
            return agent_pos
        else:
            len_ = len(self.agents_by_breed[breed_class])
            nutrient_ = np.zeros((int(np.sqrt(len_)), int(np.sqrt(len_))))
            for i in range(len_):
                if self.agents_by_breed[breed_class][i].nutrient_level != 0:
                    x, y= self.agents_by_breed[breed_class][i].pos
                    nutrient_[x,y] = self.agents_by_breed[breed_class][i].nutrient_level
            return nutrient_
            
