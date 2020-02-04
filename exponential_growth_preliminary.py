# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 15:27:41 2020

@author: Andrea
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

Initial_Pop = 2 #g carbon
photosynth = 1.8 #g*cal per cm squared per hour, we only sort of trust this number
resp = 0.1 #we made this number up but it seems reasonable, also it needs to depend on temp
graze = 0.05 # g carbon
endtime = 5  #hours

time = np.linspace(0,endtime,50)

def f(X,time):
    Pop = X[0]
    dPop = Pop*(photosynth-resp-graze)
    return([dPop])

Initial_condition = 20 #g carbon

hab_solution = odeint(f, Initial_Pop, time)
EndPop = [vector[0] for vector in hab_solution]

plt.figure()
plt.plot(time,EndPop)
plt.xlabel("time (hours)")
plt.ylabel("Number of cells")
plt.title("Exponential HAB growth")
