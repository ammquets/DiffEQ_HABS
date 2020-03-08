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
num_steps = 600000
deltat = 0.001 #this is delta t


# Stuff to change **************

 #rate of death aside from nutrient limitation and grazing - like what?b

N = 0.25 #amount of nutrients 
P = 0.05 #amount pf plankton
C = 0.01 #number of copepods

# ******************************
A = .01 #growth rate of nutrients 
a1 = 0.2 #half saturation 1
a2 = 0.2 #half saturation 2 
a3 = 0.4 #half saturastion 3
d = .01 #rate of nutrient loss
d1 = 0.21 #phyto death
d2 = 0.1 #zoo death
d3 = .1 #nutrient recycling phyto
d4 = .06 #nutrient recycling zoo
rPhyto = 0.14
rZoo = 0.05
m1 = 0.6
m2 = 0.6
theta = .6 #make a function? Limiting conidition around .6


#def fP1(P): #not used right now!
 #   return(P/(half_saturation + P))
    
def fN(X, N, P, C):
    #N = X[0]
    dN = (A - (d * N) - ((m1*N*P)/(a1 + N)) + (d3 * P) + (d4 * C))
    return(dN)

def fP(X, N, P, C):
    #P = X[0]
    dP = (((rPhyto*P)+(m1*N*P)/(a1 + N)) - (d1 * P) - ((m2*P*C)/(a2 + P)))
    return(dP)
    
def fC(X, N, P, C):
   # C = X[0]
    dC = ((rZoo * C) + (m2 * P * C)/(a2 + P) - (d2 * C) - ((theta*P*C)/(a3 + P)))
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
