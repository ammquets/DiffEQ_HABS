# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:46:14 2020

@author: Andrea
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

alpha = .9 #specific pedation rate
beta = .4 #ratio of biomass consumed per zoo for growth
mu = 1.2 #zoo mortality rate
theta = .9 #rate of toxin production per phyto
gamma = .4 #half saturation constant, we made this value up
r = 2
K = 50
#nu = 0.06
endtime = 40

t = np.linspace(0,endtime,200)

def f(X,time):
    P = X[0]
    Z = X[1]
    dP = (r*P*(1-(P/K)))-(alpha*P*Z)
    dZ = (beta*P*Z)-(mu*Z)-(((theta*P)/(gamma+P))*Z)
    return([dP,dZ])


P0 = 50
Z0 = 2
Initial_Pop = [P0, Z0] #we made this up

hab_solution = odeint(f, Initial_Pop, t)
P = [vector[0] for vector in hab_solution]
Z = [vector[1] for vector in hab_solution]

plt.figure()
plt.plot(t,P,label="phyto")
plt.plot(t,Z,label="zoo")
plt.legend(loc=7)
plt.show()