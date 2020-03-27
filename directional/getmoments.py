#v1.1
#Input: full operator oscillator and rotatory strengths for each direction, number of roots, intial and final roots and number of directions.
#Direction file directions_cart.inp, files loaded by np.loadtxt()
#Output: Directional rot strentght and oscillator strength for full operator.
#        Directional Rotatory strengths for mixed and veloxity gauge. All for specified roots
#Syntax: python3 getmoments.sh <nroots> <initial root> <final root> <number of directions>
#Dependencies: look at files loaded by np.loadtxt(). Should be in correct format

import numpy as np
import sys
import os

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
#directions=np.loadtxt("directions.raw")
#if(ndir != len(directions)):
#    print('Number of directions not equal!')
directions=np.loadtxt("directions_cart.inp")




#full operator moments
fullopdata=np.loadtxt("fullopmoments.raw") #Format: x y z rot. str. osc. str.. '0 0 0 0' when direction changes
fullmoments=np.zeros(shape=(nroots,nroots,ndir)) #Only Rot. strength for now

k=0
for i in range(len(fullopdata)):
    if(fullopdata[i,0]==0):
        k=k+1
        continue
    init=int(fullopdata[i,0])
    final=int(fullopdata[i,1])
    fullmoments[init-1,final-1,k]=fullopdata[i,3]
    fullmoments[final-1,init-1,k]=fullmoments[init-1,final-1,k]

if(k!=ndir):
    print('All directions not accounted for!')


#i=1
#while (i<=ndir):
    #creating correct file name to open
#    filename_1="momentsfullop_"
#    filename_2=str(i)
#    filename_3=".raw"
#    filename=filename_1+filename_2+filename_3
#    fullopdata=np.loadtxt(filename)
#
    #default transition matrix values are zero
#    fulloprot = np.zeros(shape=(nroots,nroots))
#    fulloposc = np.zeros(shape=(nroots,nroots))
#


    #checking the indices of transition and filling the transition matrix correspondingly
#    for j in range(len(fullopdata)):
#        init=int(fullopdata[j,0])
#        final=int(fullopdata[j,1])
#        fulloprot[init-1,final-1]=fullopdata[j,3]
#        fulloprot[final-1,init-1]=fulloprot[init-1,final-1] #symmetrising
#        fulloposc[init-1,final-1]=fullopdata[j,2]
#        fulloposc[final-1,init-1]=fulloposc[init-1,final-1] #symmetrising

#    rot_str_fullop=fulloprot[ri-1,rf-1]*1.967e-3 #converting from reduced rot str to atomic units
#    rot_str_fullop_cgs=rot_str_fullop*471.44e-40 #converting from a.u to cgs
#    osc_str_fullop=fulloposc[ri-1,rf-1] #unitless

#    file=open("dir-fullmoments.raw","a")
    #file.writelines(["Rotatory strengths (mixed): ", str(rot_str), " (a.u) ", str(rot_str_cgs), " (cgs) ", "\n"])
    #file.writelines(["Rotatory strengths (velocity): ", str(rot_str_vel), " (a.u) ", str(rot_str_vel_cgs), " (cgs) ", "\n"])
#    file.writelines([str(directions[i-1,0]), " ", str(directions[i-1,1]), " ", str(directions[i-1,2]), " ",  str(rot_str_fullop_cgs), " ", str(osc_str_fullop), "\n"])
    #file.writelines(["Dipole strengths (length): " , str(dip_str_len), " (a.u) ",  str(dip_str_len_cgs), " (cgs)", "\n"])
    #file.writelines(["Oscillator strengths (velocity): " , str(osc_str_vel), "\n"])
    #file.writelines(["Excitation Energy: ", str(E1), " (a.u) ", str(E1_ev), " (eV) ", "\n"])
    #file.writelines(["Osccilator strengths (velocity): " , str(osc_strength_vel), "\n"])
#    file.close()

#    i=i+1
#    continue

fullmoments_cgs=fullmoments*9.274E-41

#File check
if os.path.exists("dir-fullmoments.raw"):
        os.remove("dir-fullmoments.raw")

for i in range(ndir):
    file=open("dir-fullmoments.raw","a")
    file.writelines([str(directions[i,0])," ",str(directions[i,1])," ",str(directions[i,2]), " ", str(fullmoments_cgs[ri-1,rf-1,i]), "\n"])
    file.close()

#Truncated Operator moments
velmoments=np.zeros(shape=(nroots,nroots,ndir)) #3D array with all moments of all directions
veldata=np.loadtxt("velmoments.raw")
for k in range(ndir): #This loop assumes that velmoments.raw and mixmoments.raw have moments for all roots
    for i in range(nroots):
        for j in range(i+1,nroots):
            velmoments[i,j,k] = veldata[j-(i+1) + i*nroots - i*(i+1)//2 + k*(nroots*(nroots-1))//2 , 2]
            velmoments[j,i,k] = velmoments[i,j,k] #symmetrising

mixmoments=np.zeros(shape=(nroots,nroots,ndir))
mixdata=np.loadtxt("mixmoments.raw")
for k in range(ndir):
    for i in range(nroots):
        for j in range(i+1,nroots):
            mixmoments[i,j,k] = mixdata[j-(i+1) + i*nroots - i*(i+1)//2 + k*(nroots*(nroots-1))//2 , 2]
            mixmoments[j,i,k] = mixmoments[i,j,k]

#Converting to cgs
velmoments_cgs=velmoments*9.274E-41
mixmoments_cgs=mixmoments*9.274E-41

#printing to file
if os.path.exists("dir-velmoments.raw"):
        os.remove("dir-velmoments.raw")
if os.path.exists("dir-mixmoments.raw"):
        os.remove("dir-mixmoments.raw")

for i in range(ndir):
    file1=open("dir-velmoments.raw","a")
    file2=open("dir-mixmoments.raw","a")

    file1.writelines([str(directions[i,0])," ",str(directions[i,1])," ",str(directions[i,2]), " ", str(velmoments_cgs[ri-1,rf-1,i]), "\n"])
    file2.writelines([str(directions[i,0])," ",str(directions[i,1])," ",str(directions[i,2]), " ", str(mixmoments_cgs[ri-1,rf-1,i]), "\n"])


    file1.close()
    file2.close()
