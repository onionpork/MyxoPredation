# %%
from MyxoNutrient_agent import Myxo, Nutrient
from MyxoNutrient_model import MyxoModel
from matplotlib import pyplot as plt
import numpy as np 
from os import path 
import cv2
import pandas as pd

# %%
x_ini, y_ini = 50, 50
N = 1
dt = 0.1
width = 100
height = 100
v_mu, v_std = 2.3, 0
angleLow, angleHigh = 0.5, 0.5 
white_angle_mu, white_angle_std = 0, 0.4
reversal = [8.6]

# %%
model = MyxoModel(x=x_ini, y=y_ini, N=N, width=width, height=height, v_mu=v_mu, 
                    v_std=v_std, angleLow=angleLow, angleHigh=angleHigh, white_angle_mu=white_angle_mu, 
                    white_angle_std=white_angle_std, reversal = reversal, clock=0, dt=dt, initx=50,
                    inity=50, nutrient_range =10, OPTION =1)

for i in range(6000):
    model.step()

# %% 
agent_pos = model.datacollector.get_model_vars_dataframe()
agent_pos.head()
# %%
from matplotlib import pyplot as plt
agent_counts = agent_pos.iloc[-1]['Nutrient']
fig = plt.imshow(agent_counts, interpolation = 'nearest')
plt.colorbar()
# %%
