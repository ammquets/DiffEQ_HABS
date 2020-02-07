#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 11:19:01 2020

@author: hallie
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:46:34 2020
@author: Andrea
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

Initial_Pop = [2, 20, 45] #g carbon
photosynth = 1.8 #g*cal per cm squared per hour, we only sort of trust this number
resp = 0.1 #we made this number up but it seems reasonable, also it needs to depend on temp
graze = 0.05 # g carbon
endtime = 5  #hours

time = np.linspace(0,endtime,50)
plt.figure()

for i in Initial_Pop:
    def f(X,time):
        Pop = X[0]
        dZooGraze = graze*Pop
        dPop = Pop*(photosynth-resp-dZooGraze) #Riley, Gordon A. "Factors controlling phytoplankton populations on Georges Bank." J. mar. Res 6.1 (1946): 54-73.
        return([dPop])


    hab_solution = odeint(f, i, time)
    EndPop = [vector[0] for vector in hab_solution]


    plt.plot(time,EndPop)
    plt.xlabel("time (hours)")
    plt.ylabel("Phytoplankton (Grams of Carbon)")
    plt.title("HAB growth mediated by strong predation")
