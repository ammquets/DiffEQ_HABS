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

Things  to do:
    code an eulers method, this is good because each euler step should really be equal to the next because of assumptions in the functions
    figure out what to do with ToxIn:
        should it be s-shaped or 7
        is x supposed to be Tox or Phyto
        should it still be mulitplied by Phyto
    figure out units
    this doesn't take predation into account, unless we assume it is included in carrying capacity. which it very well may be. but this really doesn't have anything cyclic about it unlike the lotka volterra stuff that we had before
'''

import matplotlib.pyplot as plt

#parameters
a = 7 #for the s-shaped ToxIn function
b = 2 #for the s-shaped ToxIn function
c = 50000 #for the s-shaped ToxIn function

ToxOut = .5 #how fast the toxin leaves the cell
SiIn = 90 #rate of silicate input
SiOut = 1 #rate of use for growth
NIn = 1000 #rate of nitrate input
NOut = 4 #rate of use for growth or toxin. if both at once, multiply by 2 or something
PhytoDeath = .7 #percent of phyto that die of natural causes each timstep

#initial conditions
Tox = 0 #starting toxicity
Phyto = 150 #starting num phyto
N = 1000 #starting amt nitrate
Si = 200 #starting amt silicate
NutRatio = N/Si

#euler's stuff
timestep = 0 #starting step
deltat = 0.01
n = 75 #num steps

#initialize some lists
time_list = []
N_list = []
Si_list = []
NutRatio_list = []
Phyto_list = []
Tox_list = []

def ToxIn(x): #how fast the toxin is produced could replace with function r*((k^x)/((k^x)+l)) -> where k = 2; r = 7; l = ? but somewhere between 10,000 and 100,000 
    return(a*(b**x)/((b**x)+c))
    #return(7)

def PhytoGrowth(x):
    #r = 2
    r = (N*Si)/4
    #K = 200
    #return(r*x*(1-(x/K)))
    return(Phyto*r)

for i in range(n):
    
    if Si <= 0: #these are safeguards in case anything tries to go negative
        Si = .00001
        print("Si safeguard triggered")
    if N < 0:
        N = 0
        print("N safeguard triggered")
    if Phyto <= 0:
        Phyto = 1
        print("Phyto min safeguard triggered")
        Phyto = 100000000
        print("Phyto max safeguard triggered")
    if Tox < 0:
        Tox = 0
        print("Tox safeguard triggered")
      
    if N == 0: #limiting condition, no nitrate means no growth and no DA
        dN = NIn
        dSi = SiIn
        dPhyto = -PhytoDeath*Phyto
        dTox = -Tox*ToxOut
        NutRatio = N/Si #trying to reset this for each new iteration because this shouldn't really be a DiffEQ
        temp_results = [dN, dSi, NutRatio, dPhyto, dTox]
        print("first if statement ran")
    if Si == .00001: #limiting condition, no silicate means no growth but can still produce DA because of nitrate
        dN = NIn -NOut*Phyto
        dSi = SiIn
        dPhyto = -PhytoDeath*Phyto
        dTox = -Tox*ToxOut + 2*ToxIn(Tox)*Phyto #ToxIn multiplied by 2 because energy isn't going to growth
        NutRatio = N/Si #trying to reset this for each new iteration
        temp_results = [dN, dSi, NutRatio, dPhyto, dTox]
        print("second if statement ran")
    if NutRatio >= 8: #growth and DA at this threshold    
        dN = NIn -2*NOut*Phyto #NOut mutiplied by 2 because it is being used for growth and DA production at same time
        dSi = SiIn -SiOut*Phyto
        dPhyto = PhytoGrowth(Phyto) -PhytoDeath*Phyto
        dTox = -Tox*ToxOut +ToxIn(Tox)*Phyto
        NutRatio = N/Si #trying to reset this for each new iteration
        temp_results = [dN, dSi, NutRatio, dPhyto, dTox]
        print("third if statement ran")
    if NutRatio < 8: #growth but no DA below this threshold
        dN = NIn -NOut*Phyto
        dSi = SiIn -SiOut*Phyto
        dPhyto = PhytoGrowth(Phyto) -PhytoDeath*Phyto
        dTox = -Tox*ToxOut
        NutRatio = N/Si #trying to reset this for each new iteration
        temp_results = [dN, dSi, NutRatio, dPhyto, dTox]
        print("fourth if statement ran")
    
    dN = temp_results[0]
    dSi = temp_results[1] 
    NutRatio = temp_results[2]
    dPhyto = temp_results[3]
    dTox = temp_results[4]

    time_list.append(timestep) #add previous time to list
    N_list.append(N)
    Si_list.append(Si)
    NutRatio_list.append(NutRatio)
    Phyto_list.append(Phyto)
    Tox_list.append(Tox)
    timestep = timestep+deltat
    N = N + dN
    Si = Si + dSi
    #NutRatio = NutRatio #check this out
    Phyto = Phyto + dPhyto
    Tox = Tox + dTox
    print("iteration number " + str(i) +" completed")

plt.figure()
plt.plot(time_list,N_list,label="Nitrate", color = 'navy')
plt.plot(time_list,Si_list,label="Silicate", color = 'orange')
plt.plot(time_list,Phyto_list,label="Harmful Algae", color = 'green')
plt.plot(time_list,Tox_list, label = "Cellular Toxins", color = 'red')
plt.ylabel("Amount")
plt.xlabel("Time t")
plt.legend(loc="best")
plt.show()

f2, axarr = plt.subplots(5, sharex=True)
axarr[0].plot(time_list, N_list, color = 'navy')
axarr[0].set_title('Nitrate')
axarr[1].plot(time_list, Si_list, color = 'orange')
axarr[1].set_title('Silicate')
axarr[2].plot(time_list, Phyto_list,color = 'green')
axarr[2].set_title('Harmful Algae')
axarr[3].plot(time_list, Tox_list, color = 'red')
axarr[3].set_title('Cellular Toxins')
axarr[4].plot(time_list, NutRatio_list, color = 'black')
axarr[4].set_title('Nutrient Ratio')
f2.tight_layout(pad=1.0)
plt.ylabel("Amount")
plt.xlabel("Time t")
plt.show()
