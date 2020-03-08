# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:59:48 2020
@author: Andrea
"""

'''
This is meant to incorporate toxins according to source (see below)
parameters are all pretty made up but the functions are real

source: https://www.researchgate.net/publication/237183674_Controls_on_Domoic_Acid_Production_by_the_Diatom_Nitzschia_pungens_f_multiseries_in_Culture_Nutrients_and_Irradance

Things  to do:
    double check units
    figure out parameters that make sense biologically
        ToxOut -how fast DA leaves the cell
        SiOut - how much silicate is needed for growth (1 cell dividing into 2)
        NOut - how much nitrate is needed for growth (1 cell dividing into 2); how much nitrate is required to make toxins
        NIn - how fast is nitrate added through river input etc
        SiIn - how fast is silicate added through river input etc     
'''

import matplotlib.pyplot as plt

#parameters
a = 7 #for the s-shaped ToxIn function
b = 2 #for the s-shaped ToxIn function
c = 5 #for the s-shaped ToxIn function

ToxOut = .5 #how fast the toxin leaves the cell
SiIn = 200 #rate of silicate input
SiOut = 1 #rate of use for growth
NIn = 8000 #rate of nitrate input
NOut = 4 #rate of use for growth or toxin. if both at once, multiply by 2 or something
PhytoDeath = .35 #percent of phyto that die each timstep via grazing; citation: https://www.researchgate.net/publication/231424278_Intrinsic_growth_and_microzooplankton_grazing_on_toxigenic_Pseudo-nitzschia_spp_diatoms_from_the_coastal_northeast_Pacific

#initial conditions
Tox = 0 #starting total toxicity
ToxCell = 0 #starting cellular toxins
Phyto = 100 #starting num phyto
N = NIn #starting amt nitrate
Si = SiIn #starting amt silicate
NutRatio = N/Si
Condition = 0

#euler stuff
time = 0 #starting step
deltat = .01 
n = 10000 #num steps

#initialize lists
time_list = []
iteration_list = []
N_list = []
Si_list = []
NutRatio_list = []
Phyto_list = []
Tox_list = []
ToxCell_list = []
Condition_list = []

time_list.append(time) 
iteration_list.append(0)
N_list.append(N)
Si_list.append(Si)
NutRatio_list.append(NutRatio) 
Phyto_list.append(Phyto)
Tox_list.append(Tox)
ToxCell_list.append(ToxCell)
Condition_list.append(Condition) 

#define functions
def ToxIn(x): 
    return(a*(b**x)/((b**x)+c)) # x axis = current toxin level; y axis = toxin added 
    #return(7) 

def PhytoGrowth(x): 
    minN = x*NOut*deltat
    minSi = x*SiOut*deltat
    #r = .45 #average irradiance conditions; time step is 1 day
    r = .64 #high irradiance; time step is 1 day
    #r = .35 #low irradiance; time step is 1 day
    if N >= minN:
        if Si >= minSi: #if there is enough Si and N to do all the growing
            print("\t growth not limited")
            return(x*(r))
        if Si <= minSi:  # enough N but not enough Si to do all the growing, grows until Si is 0
            print("\t not enough silicate to grow to full potential")
            return(x*(((Si/minSi)*r))) 
    if N < minN:
        if Si < minSi:
            return(x*r*(Si/minSi)*(N/minN))
        if Si >= minSi:
            print("\t not enough nitrate to grow to full potential")
            return(x*(((N/minN)*r))) 

#loop through each timestep
for i in range(n):
    
    print("iteration number " + str(i) +":")
    
    #change values depending on nutrient conditions
    if N == 0: #no growth and no toxin production
        dN = NIn*deltat
        dSi = SiIn*deltat
        dPhyto = -PhytoDeath*Phyto*deltat
        dToxCell = -ToxCell*ToxOut*deltat
        dTox = -Tox*ToxOut*deltat
        Condition = 1
        print("\t first if statement ran")     
    if Si == .00001 and N>0: #limiting condition, no silicate means no growth but can still produce DA because of nitrate
        dN = (NIn -(NOut*Phyto))*deltat
        dSi = SiIn*deltat
        dPhyto = -PhytoDeath*Phyto*deltat
        dToxCell = (-(ToxCell*ToxOut) + ToxIn(ToxCell))*deltat
        dTox = ((-Tox*ToxOut) + ToxIn(ToxCell)*(dPhyto +Phyto))*deltat #(dPhyto+Phyto) term is here because i want it to multiply by the current num phyto instead of the previous one
        Condition = 2
        print("\t second if statement ran")
    if NutRatio > 7.999 and Si > .00001 and N !=0: #growth and DA at this threshold    
        dN = (NIn -(2*NOut*Phyto))*deltat #NOut mutiplied by 2 because it is being used for growth and DA production at same time
        dSi = (SiIn -(SiOut*Phyto))*deltat
        dPhyto = (PhytoGrowth(Phyto) -(PhytoDeath*Phyto))*deltat
        dToxCell = (-(ToxCell*ToxOut) + ToxIn(ToxCell))*deltat
        dTox = ((-Tox*ToxOut) + (ToxIn(ToxCell)*(dPhyto+Phyto)))*deltat #(dPhyto+Phyto) term is here because i want it to multiply by the current num phyto instead of the previous one
        Condition = 3
        print("\t third if statement ran")
    if NutRatio <= 7.999 and Si > .00001 and N != 0: #growth but no DA below this threshold
        dN = (NIn -(NOut*Phyto))*deltat
        dSi = (SiIn - (SiOut*Phyto))*deltat
        dPhyto = (PhytoGrowth(Phyto) - (PhytoDeath*Phyto))*deltat
        dToxCell = -ToxCell*ToxOut*deltat
        dTox = -Tox*ToxOut*deltat
        Condition = 4
        print("\t fourth if statement ran")
    
    #add the change value to each
    time = time+deltat
    N = N + dN
    Si = Si + dSi
    NutRatio = N/Si
    Phyto = Phyto + dPhyto
    ToxCell = ToxCell +dToxCell
    Tox = Tox + dTox
    
    #safeguards in case anything tries to go negative
    if Si <= .00001: 
        Si = .00001
        print("\t Si safeguard triggered")
    if N < 0:
        N = 0
        print("\t N safeguard triggered")
    if Phyto <= 0:
        Phyto = 1
        print("\t Phyto min safeguard triggered")
    if Tox < 0:
        Tox = 0
        print("\t Tox safeguard triggered")
    if ToxCell < 0:
        ToxCell = 0
        print("\t ToxCell safeguard triggered")
    
    #append new values to lists
    time_list.append(time) 
    iteration_list.append(i+1) #since python starts stuff at 0 and we already did 0 up top
    N_list.append(N)
    Si_list.append(Si)
    NutRatio_list.append(NutRatio) 
    Phyto_list.append(Phyto)
    Tox_list.append(Tox)
    ToxCell_list.append(ToxCell)
    Condition_list.append(Condition) 
    
'''   
#plot on one graph
plt.figure(figsize=(9,9))
plt.plot(iteration_list,N_list,label="Nitrate", color = 'navy')
plt.plot(iteration_list,Si_list,label="Silicate", color = 'orange')
plt.plot(iteration_list,Phyto_list,label="Harmful Algae", color = 'green')
plt.plot(iteration_list,Tox_list, label = "Total Cellular Toxins", color = 'red')
#plt.plot(iteration_list, ToxCell_list, label = 'Cellular Toxins', color = 'purple')
#plt.plot(iteration_list, NutRatio_list, label = 'Nutrient Ratio', color = 'black')
plt.ylabel("Amount")
plt.xlabel("Time (days)")
plt.legend(loc="best")
plt.show()
'''

title = "Nitrate Input = " + str(NIn) +"; Silicate Input = " + str(SiIn)
#plot in separate facets
f2, axarr = plt.subplots(6, sharex=True, figsize=(9,9))
f2.suptitle(title, fontsize=16)
axarr[0].plot(time_list, N_list, color = 'navy')
axarr[0].set_title('Nitrate')
axarr[1].plot(time_list, Si_list, color = 'orange')
axarr[1].set_title('Silicate')
axarr[2].plot(time_list, Phyto_list,color = 'green')
axarr[2].set_title('Harmful Algae')
axarr[3].plot(time_list, Tox_list, color = 'red')
axarr[3].set_title('Total Cellular Toxins')
axarr[4].plot(time_list, ToxCell_list, color = 'purple')
axarr[4].set_title('Cellular Toxins')
#axarr[5].plot(iteration_list, NutRatio_list, color = 'black')
#axarr[5].set_title('Nutrient Ratio')
axarr[5].plot(time_list, Condition_list, color = 'skyblue')
axarr[5].set_title('Condition')
f2.tight_layout()
f2.subplots_adjust(top=0.88)
plt.xlabel("Time (days)")
plt.show()
