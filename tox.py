# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:59:48 2020

@author: Andrea
"""

'''
This is meant to incorporate toxins according to source (see below)
parameters are all pretty made up but the functions are real
except that we made up the function that represents ToxIn
It's a good approximation though. except that we don't have a clue what c (aka l) is. 

source: https://www.researchgate.net/publication/237183674_Controls_on_Domoic_Acid_Production_by_the_Diatom_Nitzschia_pungens_f_multiseries_in_Culture_Nutrients_and_Irradance
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint #odeint = ordinary diffEq integrater 


# Stuff to change **************
a = 7
b = 2
c = 50000
'''
ToxIn = 7 #how fast the toxin is produced could replace with function r*((k^x)/((k^x)+l)) -> where k = 2; r = 7; l = ? but somewhere between 10,000 and 100,000
''' 
ToxOut = .5 #how fast the toxin leaves the cell
SiIn = 50 #rate of silicate input
SiOut = 1 #rate of use for growth
NIn = 400 #rate of nitrate input
NOut = 4 #rate of use for growth or toxin. if both at once, multiply by 2 or something
r = 2
K = 200
EndTime = 20 #how far to run for
Tox0 = 1 #starting toxicity
Phyto0 = 50 #starting num phyto
N0 = 400 #starting amt nitrogen
Si0 = 100 #starting amt silicate
NutRatio0 = N0/Si0
NumPoints = 1000

N = []
Si = []
NutRatio = []
Phyto = []
Tox = []


def f(X, t):
    N = X[0]
    Si = X[1] 
    NutRatio = X[2]
    Phyto = X[3]
    Tox = X[4]
    ''' 
    if Si < 0: #these are safeguards in case anything tries to go negative
        Si = 1
    if N < 0:
        N = 0
    if Phyto < 0:
        Phyto = 0
    if Tox < 0:
        Tox = 0
     '''  
    if N == 0: #limiting condition, no nitrate means no growth and no DA
        dN = NIn
        dSi = SiIn
        dPhyto = 0
        dTox = -Tox*ToxOut*Phyto
        dNutRatio = -NutRatio + N/Si #trying to reset this for each new iteration because this shouldn't really be a DiffEQ
    if Si == 0: #limiting condition, no silicate means no growth but can still produce DA because of nitrate
        dN = NIn -NOut*Phyto
        dSi = SiIn
        dPhyto = 0
        dTox = -Tox*ToxOut*Phyto +2*a*((b**Tox)/((b**Tox)+c))*Phyto #ToxIn multiplied by 2 because energy isn't going to growth
        dNutRatio = -NutRatio + N/Si #trying to reset this for each new iteration
    if NutRatio >= 8: #growth and DA at this threshold
        dN = NIn -2*NOut*Phyto #NOut mutiplied by 2 because it is being used for growth and DA production at same time
        dSi = SiIn -SiOut*Phyto
        dPhyto = r*Phyto*(1-(Phyto/K))
        dTox = -Tox*ToxOut*Phyto +a*((b**Tox)/((b**Tox)+c))*Phyto
        dNutRatio = -NutRatio + N/Si #trying to reset this for each new iteration
    if NutRatio < 8: #growth byt no DA below this threshold
        dN = NIn -NOut*Phyto
        dSi = SiIn -SiOut*Phyto
        dPhyto = r*Phyto*(1-(Phyto/K))
        dTox = -Tox*ToxOut*Phyto
        dNutRatio = -NutRatio + N/Si #trying to reset this for each new iteration
    return( [dN, dSi, dNutRatio, dPhyto, dTox] )


T = np.linspace(0,EndTime,NumPoints)


InitialCondition = [N0, Si0, NutRatio0, Phyto0, Tox0]

TOX_solution = odeint(f, InitialCondition, T)


N = [i[0] for i in TOX_solution] 
Si = [i[1] for i in TOX_solution]
NutRatio = [i[2] for i in TOX_solution]
Phyto = [i[3] for i in TOX_solution]
Tox = [i[4] for i in TOX_solution]



plt.figure(1)
plt.plot(T,N,label="Nitrate", color = 'navy')
plt.plot(T,Si,label="Silicate", color = 'orange')
plt.plot(T,Phyto,label="Harmful Algae", color = 'green')
plt.plot(T, Tox, label = "Cellular Toxins", color = 'red')
plt.ylabel("Amount")
plt.xlabel("Time t")
plt.legend(loc=7)
plt.show()
