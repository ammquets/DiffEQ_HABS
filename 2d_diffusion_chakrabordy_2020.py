# This program solves the 2D heat equation.  It is based on an example
# from pp. 373-375 of MEJ Newman's book, Computational Physics.
# http://www-personal.umich.edu/~mejn/cp/

# Works w/ a vmin of 0, vmax of 1100, numplot 20 for 100 t, initial condition = 1000

import numpy as np
import matplotlib.pylab as plt
import random as rand
import math

# Set system parameters
#L = 0.01 # length of system
D = 0.00001 # diffusivity


InitialNitrogen= 0.25


# Set algorithm parameters
Num = 25 # Number of elements in grid
# a = L/N We'll effectively take a = 1
DeltaT= 1e-4 # Time step
EndTime = 100
Steps = EndTime/DeltaT
NumPlots = 25 # This is the number of plots that will be saved.  Be careful!
Directory = "TempFigs" # Name of Directory where plots will be saved.
# If this directory doesn't already exist you might need to create it.

# Set Initial conditions.  Susceptibles, uniformly on grid
# Infectives at random with probability ProbSick
N = np.empty((Num+1,Num+1),float)
P = np.empty((Num+1,Num+1),float)
R = np.empty((Num+1,Num+1),float)

for i in range(1,Num):
    for j in range(1,Num):
        N[i,j] = InitialNitrogen + InitialNitrogen*rand.random() - InitialNitrogen
        P[i,j] = 0.05
        R[i,j] = .010
   
N_New = np.empty((Num+1,Num+1),float)
P_New = np.empty((Num+1,Num+1),float)
R_New = np.empty((Num+1,Num+1),float)

#N = 0.25 #initial amount of nutrients 
#P = 0.05 #initial amount pf plankton
#R = 0.01 #initial number of copepods

# ******************************
A = .003 #growth rate of nutrients 
a1 = 0.2 #half saturation 1
a2 = 0.2 #half saturation 2 
a3 = 0.4 #half saturastion 3
d = .01 #rate of nutrient loss
d1 = 0.21 #phyto death
d2 = 0.1 #zoo death
d3 = .1 #nutrient recycling phyto
d4 = .06 #nutrient recycling zoo
rPhyto = 0.0 #could change if it was a dino
rZoo = 0.05
m1 = 0.6
m2 = 0.6
theta = .6 #make a function? Limiting conidition around .6

# This function applies no-flux boundary conditions.  See discussion on
# the bottom of p. 236 of Guckeheimer and Ellner. I want the boundaries to
# be the same as their interior neighbor
def FixBCs(X):
    Num = len(X[0])-1
    X[0] = X[1]
    X[Num] = X[Num-1]
    X[0:Num+1,Num] = X[0:Num+1,Num-1]
    X[0:Num+1,0] = X[0:Num+1,1]
    return(X)

N = FixBCs(N)
P = FixBCs(P)
R = FixBCs(R)

def season(X):
    x = X % 365
    result = ((0.7*math.sin(0.08 * x + 66.5)+1)*.01)
    return result

def dN(N, P, R):
    dN = (season(step*DeltaT) - (d * N) - ((m1*N*P)/(a1 + N)) + (d3 * P) + (d4 * R))
    return(dN)

def dP(N, P, R):
    dP = (((rPhyto*P)+(m1*N*P)/(a1 + N)) - (d1 * P) - ((m2*P*R)/(a2 + P)))
    return(dP)
    
def dR(N, P, R):
    dC = ((rZoo * R) + (m2 * P * R)/(a2 + P) - (d2 * R) - ((theta*P*R)/(a3 + P)))
    return(dC)



# **************************************************************************


# Plot Initial Condition
plt.figure(0,figsize=(8,8))
plt.imshow(P,cmap="BuGn",vmin=0,vmax=10,origin="lower")
plt.colorbar()
plt.title("Time = 0")
plt.savefig(Directory+"/temp.0.png")
plt.close()
P[1:Num,1:Num]
# calculate c used in the relaxation method 
c = DeltaT*D

q = int(Steps/NumPlots)

f = 1 # fig counter

for step in range(int(Steps)):
    #Calculate the new values of T
    N_New[1:Num,1:Num] = N[1:Num,1:Num] + DeltaT*dN(N[1:Num,1:Num],P[1:Num,1:Num], R[1:Num,1:Num]) + \
                     c*(N[2:Num+1,1:Num] + N[0:Num-1,1:Num] + N[1:Num,2:Num+1] \
                        + N[1:Num,0:Num-1] -4*N[1:Num,1:Num])
                     
    P_New[1:Num,1:Num] = P[1:Num,1:Num] + DeltaT*dP(N[1:Num,1:Num],P[1:Num,1:Num], R[1:Num,1:Num]) + \
                     c*(P[2:Num+1,1:Num] + P[0:Num-1,1:Num] + P[1:Num,2:Num+1] \
                        + P[1:Num,0:Num-1] -4*P[1:Num,1:Num])  
                     
    R_New[1:Num,1:Num] = R[1:Num,1:Num] + DeltaT*dR(N[1:Num,1:Num],P[1:Num,1:Num], R[1:Num,1:Num]) + \
                     c*(R[2:Num+1,1:Num] + R[0:Num-1,1:Num] + R[1:Num,2:Num+1] \
                        + R[1:Num,0:Num-1] -4*R[1:Num,1:Num])  
# ***************************************************************
# The above line is equivalent to the following nested for loops:    
#    for i in range(1,N):
#        for j in range(1,N):
#            T_New[i,j] = T[i,j] + \
#                         c*(T[i+1,j] + T[i-1,j] + 
#                         T[i,j+1] + T[i,j-1] - 4*T[i,j])
# ***************************************************************
    N_New = FixBCs(N_New)
    P_New = FixBCs(P_New)
    R_New = FixBCs(R_New)
    N,N_New = N_New, N # Swap arrays
    P,P_New = P_New, P # Swap arrays
    R,R_New = R_New, R

#    image.set_data(T)
#    title.set_text(time_template% (t*Delta_t))
    if (step%q == 0):
        print("I am making plot", f, "out of", NumPlots)
        plt.figure(f,figsize=(8,8))
        plt.imshow(P,cmap="BuGn", origin="lower", vmin = 0, vmax = 0.5)
        plt.title("Time = %.4f days"%(step*DeltaT))
        plt.colorbar()
        plt.savefig(Directory+"/temp."+str(f)+".png")
        plt.close()
        f += 1
   
print("I'm done now. Enjoy your plots.")
    



