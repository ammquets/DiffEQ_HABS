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
    figure out what to do with ToxIn: 
        should it be s-shaped or 7
        probably need to make up a new s-shaped function
    figure out units
    figure out parameters that make sense biologically
        ToxOut -how fast DA leaves the cell
        SiOut - how much silicate is needed for growth (1 cell dividing into 2)
        NOut - how much nitrate is needed for growth (1 cell dividing into 2); how much nitrate is required to make toxins
        PhytoDeath - how fast do phyto die or get eaten
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
NIn = 2000 #rate of nitrate input
NOut = 4 #rate of use for growth or toxin. if both at once, multiply by 2 or something
PhytoDeath = .5 #percent of phyto that die of natural causes each timstep

#initial conditions
Tox = 0 #starting total toxicity
ToxCell = 0 #starting cellular toxins
Phyto = 150 #starting num phyto
N = 1000 #starting amt nitrate
Si = 200 #starting amt silicate
NutRatio = N/Si

#euler's stuff
timestep = 0 #starting step
deltat = 0.01
n = 50 #num steps

#initialize some lists
time_list = []
iteration_list = []
N_list = []
Si_list = []
NutRatio_list = []
Phyto_list = []
Tox_list = []
ToxCell_list = []

def ToxIn(x): #how fast the toxin is produced could replace with function r*((k^x)/((k^x)+l)) -> where k = 2; r = 7; l = ? but somewhere between 10,000 and 100,000 
    return(a*(b**x)/((b**x)+c)) #x and y axis
    #return(7)

def PhytoGrowth(x): 
    minN = Phyto*NOut
    minSi = Phyto*SiOut
    if N >= minN:
        if Si >= minSi:
            r = 2
            return(Phyto*r)
        if Si < minSi:
            return(Phyto*((Si/minSi)+1)) 
    if N < minN:
        if Si < minSi:
            UsableSi = Si/minSi
            UsableN = N/minN
            if UsableSi < UsableN:
                return(Phyto*((Si/minSi)+1))
            if UsableN <= UsableSi: #using a <= because if they are equally limiting, it doesn't matter which one i apply as the limiting one
                return(Phyto*((N/minN)+1))
        if Si >= minSi:
            return(Phyto*((N/minN)+1)) 
'''
def PhytoGrowth(x): 
    minN = Phyto*NOut
    minSi = Phyto*SiOut
    if N >= minN:
        if Si >= minSi:
            r = 2
            return(Phyto*r)
        else:
            return(0)  # this really shouldn't be 0 because at least some growth should happen even if not max possible
    else:
        return(0) # this really shouldn't be 0 because at least some growth should happen even if not max possible
    #r = 2
    #r = (N*Si)/4 #redfield make sure that silicate time 16 is close to nitrate
    #K = 200
    #return(r*x*(1-(x/K)))
    #return(Phyto*r)
'''
for i in range(n):
    print("iteration number " + str(i) +":")
    if Si <= 0: #these are safeguards in case anything tries to go negative
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
      
    if N == 0:
        dN = NIn
        dSi = SiIn
        dPhyto = -PhytoDeath*Phyto
        dTox = -Tox*ToxOut
        dToxCell = -ToxCell*ToxOut
        NutRatio = N/Si #trying to reset this for each new iteration because this shouldn't really be a DiffEQ
        temp_results = [dN, dSi, NutRatio, dPhyto, dTox, dToxCell]
        print("\t first if statement ran")     
    if Si == .00001:
        if N>0: #limiting condition, no silicate means no growth but can still produce DA because of nitrate
            dN = NIn -NOut*Phyto
            dSi = SiIn
            dPhyto = -PhytoDeath*Phyto
            dTox = -Tox*ToxOut + 2*ToxIn(ToxCell)*Phyto #ToxIn multiplied by 2 because energy isn't going to growth
            dToxCell = -ToxCell*ToxOut + 2*ToxIn(ToxCell)
            NutRatio = N/Si #trying to reset this for each new iteration
            temp_results = [dN, dSi, NutRatio, dPhyto, dTox, dToxCell]
            print("\t second if statement ran")
        else:
            pass
    if NutRatio >= 8:
        if Si > .00001: #growth and DA at this threshold    
            dN = NIn -2*NOut*Phyto #NOut mutiplied by 2 because it is being used for growth and DA production at same time
            dSi = SiIn -SiOut*Phyto
            dPhyto = PhytoGrowth(Phyto) -PhytoDeath*Phyto
            dTox = -Tox*ToxOut + ToxIn(ToxCell)*Phyto
            dToxCell = -ToxCell*ToxOut + ToxIn(ToxCell)
            NutRatio = N/Si #trying to reset this for each new iteration
            temp_results = [dN, dSi, NutRatio, dPhyto, dTox, dToxCell]
            print("\t third if statement ran")
        else:
            pass
    if NutRatio < 8:
        if Si > .00001 and N != 0: #growth but no DA below this threshold
            dN = NIn -NOut*Phyto
            dSi = SiIn -SiOut*Phyto
            dPhyto = PhytoGrowth(Phyto) -PhytoDeath*Phyto
            dTox = -Tox*ToxOut
            dToxCell = -ToxCell*ToxOut
            NutRatio = N/Si #trying to reset this for each new iteration
            temp_results = [dN, dSi, NutRatio, dPhyto, dTox, dToxCell]
            print("\t fourth if statement ran")
        else:
            pass
    
    dN = temp_results[0]
    dSi = temp_results[1] 
    NutRatio = temp_results[2]
    dPhyto = temp_results[3]
    dTox = temp_results[4]
    dToxCell = temp_results[5]

    time_list.append(timestep) #add previous to list
    iteration_list.append(i)
    N_list.append(N)
    Si_list.append(Si)
    NutRatio_list.append(NutRatio)
    Phyto_list.append(Phyto)
    Tox_list.append(Tox)
    ToxCell_list.append(ToxCell)
    timestep = timestep+deltat
    N = N + dN
    Si = Si + dSi
    #NutRatio = NutRatio #check this out
    Phyto = Phyto + dPhyto
    Tox = Tox + dTox
    ToxCell = ToxCell +dToxCell
    

plt.figure()
plt.plot(iteration_list,N_list,label="Nitrate", color = 'navy')
plt.plot(iteration_list,Si_list,label="Silicate", color = 'orange')
plt.plot(iteration_list,Phyto_list,label="Harmful Algae", color = 'green')
plt.plot(iteration_list,Tox_list, label = "Total Cellular Toxins", color = 'red')
plt.plot(iteration_list, ToxCell_list, label = 'Cellular Toxins', color = 'purple')
#plt.plot(iteration_list, NutRatio_list, label = 'Nutrient Ratio', color = 'black')
plt.ylabel("Amount")
plt.xlabel("Time t")
plt.legend(loc="best")
plt.show()

f2, axarr = plt.subplots(6, sharex=True)
axarr[0].plot(iteration_list, N_list, color = 'navy')
axarr[0].set_title('Nitrate')
axarr[1].plot(iteration_list, Si_list, color = 'orange')
axarr[1].set_title('Silicate')
axarr[2].plot(iteration_list, Phyto_list,color = 'green')
axarr[2].set_title('Harmful Algae')
axarr[3].plot(iteration_list, Tox_list, color = 'red')
axarr[3].set_title('Total Cellular Toxins')
axarr[4].plot(iteration_list, ToxCell_list, color = 'purple')
axarr[4].set_title('Cellular Toxins')
axarr[5].plot(iteration_list, NutRatio_list, color = 'black')
axarr[5].set_title('Nutrient Ratio')
f2.tight_layout(pad=1.0)
plt.xlabel("Time t")
plt.show()
