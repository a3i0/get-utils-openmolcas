#v1.0
#Input: full operator oscillator and rotatory strengths for each direction, number of roots, intial and final roots and number of directions
#Output: Directional rot strentght and oscillator strength for full operator. All for specified roots
#Syntax: python3 getmoments.sh <nroots> <initial root> <final root> <number of directions>
#Dependencies: look at files loaded by np.loadtxt(). Should be in correct format

import numpy as np
import sys

#setting values of number of roots, initial root and final root
#defaults
nroots=1
ri=0
rf=1
ndir=1

#slightly failproof assignments
if(sys.argv[1] != 0):
    nroots=int(sys.argv[1])

if(sys.argv[2]!=0 and sys.argv[3]!=0): 
    ri=int(sys.argv[2])
    rf=int(sys.argv[3])

if(sys.argv[4] != 0):
    ndir=int(sys.argv[4])

#File with directions
directions=np.loadtxt("directions.raw")
if(ndir != len(directions)):
    print('Number of directions not equal!')


#full operator moments
i=1
while (i<=ndir):
    #creating correct file name to open
    filename_1="momentsfullop_"
    filename_2=str(i)
    filename_3=".raw"
    filename=filename_1+filename_2+filename_3
    fullopdata=np.loadtxt(filename)
    
    #default transition matrix values are zero
    fulloprot = np.zeros(shape=(nroots,nroots))
    fulloposc = np.zeros(shape=(nroots,nroots))
    
    #checking the indices of transition and filling the transition matrix correspondingly
    for j in range(len(fullopdata)):
        init=int(fullopdata[j,0])
        final=int(fullopdata[j,1])
        fulloprot[init-1,final-1]=fullopdata[j,3]
        fulloprot[final-1,init-1]=fulloprot[init-1,final-1] #symmetrising
        fulloposc[init-1,final-1]=fullopdata[j,2]
        fulloposc[final-1,init-1]=fulloposc[init-1,final-1] #symmetrising
    
    rot_str_fullop=fulloprot[ri-1,rf-1]*1.967e-3 #converting from reduced rot str to atomic units
    rot_str_fullop_cgs=rot_str_fullop*471.44e-40 #converting from a.u to cgs
    osc_str_fullop=fulloposc[ri-1,rf-1] #unitless
    
    file=open("tmoments.dat","a")
    #file.writelines(["Rotatory strengths (mixed): ", str(rot_str), " (a.u) ", str(rot_str_cgs), " (cgs) ", "\n"])
    #file.writelines(["Rotatory strengths (velocity): ", str(rot_str_vel), " (a.u) ", str(rot_str_vel_cgs), " (cgs) ", "\n"])
    file.writelines([str(directions[i-1,0]), " ", str(directions[i-1,1]), " ", str(directions[i-1,2]), " ",  str(rot_str_fullop_cgs), " (cgs) ", str(osc_str_fullop), "\n"])
    #file.writelines(["Dipole strengths (length): " , str(dip_str_len), " (a.u) ",  str(dip_str_len_cgs), " (cgs)", "\n"])
    #file.writelines(["Oscillator strengths (velocity): " , str(osc_str_vel), "\n"])
    #file.writelines(["Excitation Energy: ", str(E1), " (a.u) ", str(E1_ev), " (eV) ", "\n"])
    #file.writelines(["Osccilator strengths (velocity): " , str(osc_strength_vel), "\n"])
    file.close()
    
    i=i+1
    continue




