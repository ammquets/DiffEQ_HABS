#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 10:04:26 2020

@author: hallie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:52:19 2020

@author: hallie
"""

#Source: https://www.jstor.org/stable/pdf
#/3219158.pdf?refreqid=excelsior%3A36072dba14bfd2da176dff9e046ff7dc

#This assumes that phytoplankton respond the same way to all nutrients regardless of ratio, 
#which is not true in the real world. You also have to manually make sure they reach 100%.
#Does not take diltution into account.  

import numpy as np
import matplotlib.pyplot as plt
import random



time_list = []
temp_listN = []
temp_listP = []
temp_listC = []

step = 0 #this is starting time
num_steps = 70000
deltat = 0.001 #this is delta t


# Stuff to change **************
nut_growth = .2 #growth rate of nutrients 
phyto_death = 0.3 #rate of death aside from nutrient limitation and grazing - like what?b
zoo_predation = 0.1 #predation by copepods
zoo_death = 0.7 #natural death rate of copepods regardless of phyto
zoo_birth = 0.6 #propogation rate of copepods
N = 50 #amount of nutrients 
P = 30 #amount pf plankton
C = 20 #number of copepods
m1 = 0.001
m_2 = 0.01
nut_recycling = .001
nut_recyclingZoo = .01
dilution_loss = .02 #rate of nutrient loss


# ******************************
half_saturation = .5
half_sat2 = .7
theta = .45 #make a function
fp1 = 0.419 #just testing - should be the function below


def fP1(P): #not used right now!
    return(P/(half_saturation + P))
    
def fN(X, N, P, C):
    #N = X[0]
    dN = (nut_growth - (dilution_loss * N) - ((m1*N*P)/(half_saturation + N)) + (nut_recycling * P) + (nut_recyclingZoo * C))

    return(dN)

def fP(X, N, P, C):
    #P = X[0]
    dP = (((m1*N*P)/(half_saturation + N)) - phyto_death * P - (half_saturation * P * C)/(half_sat2 + P))

    return(dP)
    
def fC(X, N, P, C):
   # C = X[0]
    dC = ((m_2 * P * C)/(half_sat2 + P) - (zoo_death * C) - (C * fP1(P)*theta))
 
    return(dC)


for i in range(num_steps): 
    temp_listP.append(P) #add previous temp to list
    temp_listN.append(N)
    temp_listC.append(C)
    time_list.append(step) #add previous time to list
    P = P + (fP(P, N, P, C) * deltat) #find new temp
    N = N + (fN(N, N, P, C) * deltat) 
    C = C + (fC(C, N, P, C) * deltat)
    step = step + deltat #find new time



fig1, ax1  = plt.subplots()

ax1.set_xlabel('Time')
ax1.set_ylabel('Population')
ax1.plot(time_list, temp_listN, 'b-o', linewidth = 1, markersize = 2)
ax1.plot(time_list, temp_listP, 'g-o', linewidth = 1, markersize = 2)
ax1.plot(time_list, temp_listC, 'r-o', linewidth = 1, markersize = 2)



plt.show()
