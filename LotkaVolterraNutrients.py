#Source: https://www.jstor.org/stable/pdf
#/3219158.pdf?refreqid=excelsior%3A36072dba14bfd2da176dff9e046ff7dc

#This assumes that phytoplankton respond the same way to all nutrients regardless of ratio, 
#which is not true in the real world. You also have to manually make sure they reach 100%.
#Does not take diltution into account.  

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint #odeint = ordinary diffEq integrater 

# Stuff to change **************
nut_growth = 0.1*(random.randint(2, 8)) #growth rate of nutrients - how do we add a delay?
phyto_uptake = 0.7 #rate of plankton nutrient uptake, needs to be larger than nutrient accumulation
## (pctNut*P)/TotalNutrients this is a calculation which probably gives a changing nutrient uptake rate depending on 
# the amount of phytoplankton. pctNut is a number like .25 which means that each phyto needs .25 nutrient units during the timestep
phyto_growth = 0.8 #propogation rate of phytopkankton when there are nutrients
phyto_death = 0.8 #rate of death aside from nutrient limitation and grazing - like what?b
zoo_predation = 0.5 #predation by copepods
zoo_death = 0.7 #natural death rate of copepods regardless of phyto
zoo_birth = 0.6 #propogation rate of copepods
EndTime = 20 #how far to run for
N0 = 5 #amount of nutrients (bottom prey)
P0 = 6 #amount pf plankton
C0 = 2 #number of copepods
NumPoints = 200

#NEW IN DRAFT 2 - needs to add to 1
nitrogen0 = 1
phos0 = 0
silicate0 = 0

# ******************************
n2 = nitrogen0/16
s2 = silicate0/15
p2 = phos0/1

nutrient_coefficient = min(n2, s2, p2)


def f(X, t):
    if t % 2 == 0: #weather? What scale is this on? 
        nut_growth = .1
    else:
        nut_growth = .8
    N = X[0]
    P = X[1]
    C = X[2]
    Nitro = X[3]
    Phos = X[4]
    Sil = X[5]
    dN = nut_growth - (phyto_uptake * N * P) 
    dNitrogen = nitrogen0*nut_growth * N - (phyto_uptake * N * P)*nitrogen0
    dPhos = phos0*nut_growth * N - (phyto_uptake * N * P)*phos0
    dSilicate = silicate0*nut_growth * N - (phyto_uptake * N * P)*silicate0
    dP = (-1 * P * phyto_death) + (phyto_growth * N * P) - (zoo_predation * P * C) #fix caps names
    dC = -1 * C * zoo_death + (zoo_birth * P * C)
 
    return( [dN, dP, dC, dNitrogen, dPhos, dSilicate] )


T = np.linspace(0,EndTime,NumPoints)


InitialCondition = [N0, P0, C0, (nitrogen0*N0), (phos0*N0), (silicate0*N0)]

LV_solution = odeint(f, InitialCondition, T)


N = [i[0] for i in LV_solution] 
P = [i[1] for i in LV_solution]
C = [i[2] for i in LV_solution]
Nit = [i[3] for i in LV_solution]
Ph = [i[4] for i in LV_solution]
Si = [i[5] for i in LV_solution]



plt.figure(1)
plt.plot(T,N,label="Nutrients", color = 'navy')
#plt.plot(T,Nit,label="Nitrogen", color = 'teal')
#plt.plot(T,Ph,label="Phosphorus", color = 'blue')
#plt.plot(T,Si,label="Silicate", color = 'aqua')
plt.plot(T,P,label="Phytoplankton", color = 'orange')
plt.plot(T,C,label="Grazers", color = 'red')
#plt.hlines(xmin= 0, xmax = 50, y=0)
plt.ylabel("Population")
plt.xlabel("Time t")
plt.legend(loc=7)
plt.show()

