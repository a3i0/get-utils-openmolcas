#v2.1
#Input: RASSI State energies, Dipole, velocity and angular momentum components, full operator oscillator and rotatory strengths, number of roots, intial and final roots
#Output: Rot strength in mixed, veocity and for full operator, dipole strength in length, osc strength in velociy and full operator. Excitaion energy. All for specified roots
#Syntax: python3 getmoments.sh <nroots> <initial root> <final root>
#Dependencies: look at files loaded by np.loadtxt(). Should be in correct format

import numpy as np
import sys

#setting values of number of roots, initial root and final root
#defaults
nroots=1
ri=0
rf=1

#slightly failproof assignments
if(sys.argv[1] != 0):
    nroots=int(sys.argv[1])

if(sys.argv[2]!=0 and sys.argv[3]!=0):
    ri=int(sys.argv[2])
    rf=int(sys.argv[3])



energy=np.loadtxt("energies.raw") #loads state energies in a.u
if (ri == rf): #warning for same-root properties
    print('Same root! Transition energy-dependent properties will not be calculated')


E1=energy[rf-1]-energy[ri-1] #excitation energy
E1_ev=E1*27.211 #in eV

data=np.loadtxt("moments.raw")
u=[data[(ri-1),(rf-1)],data[(ri-1+nroots),(rf-1)],data[(ri-1+(2*nroots)),(rf-1)]]
l=[data[((3*nroots)-1+ri),(rf-1)],data[((4*nroots)-1+ri),(rf-1)],data[((5*nroots)-1+ri),(rf-1)]]
v=[data[((6*nroots)-1+ri),(rf-1)],data[((7*nroots)-1+ri),(rf-1)],data[((8*nroots)-1+ri),(rf-1)]]

u=np.array(u)
l=np.array(l)
v=np.array(v)
m=-1.0*-1.0*0.5*l #corrected sign to take mfi instead of mif

#rotatory strengths in mixed
rot_str=np.dot(u,m)
rot_str_cgs=rot_str*471.44e-40
#rotatory strength in velocity
if (ri ==rf):
    rot_str_vel=0

rot_str_vel=-1*np.dot(v,m)/E1
rot_str_vel_cgs=rot_str_vel*471.44e-40
#dipole and magnetic strengths and moments
dip_str_len=abs(np.dot(u,u))
dip_str_len_cgs=dip_str_len*64591e-40
dip_str_vel=abs(np.dot(v,v))
dip_str_vel_cgs=dip_str_vel*64591e-40
mag_str=abs(np.dot(m,m))
m_cgs=m*1.85480e-23/(3.33564e-14)
mag_str_cgs=abs(np.dot(m_cgs,m_cgs)) #units taken from Wikipedia (https://en.wikipedia.org/wiki/Hartree_atomic_units and https://en.wikipedia.org/wiki/Magnetic_moment#Units)
#angle between dipole and magnetic vectors
theta_len=np.arccos(rot_str/(np.sqrt(dip_str_len*mag_str)))
theta_vel=np.arccos(np.dot(v,m)/(np.sqrt(dip_str_vel*mag_str)))
theta_len_degrees=theta_len*180.0/np.pi
theta_vel_degrees=theta_vel*180.0/np.pi

#oscillatory strength in velocity
if (ri == rf):
    osc_str_vel=0

osc_str_vel=2.0*dip_str_vel/(3.0*E1)

#full operator moments
fullopdata=np.loadtxt("momentsfullop.raw")

#default transition matrix values are zero
fulloprot = np.zeros(shape=(nroots,nroots))
fulloposc = np.zeros(shape=(nroots,nroots))

#checking the indices of transition and filling the transition matrix correspondingly
for i in range(len(fullopdata)):
    init=int(fullopdata[i,0])
    final=int(fullopdata[i,1])
    fulloprot[init-1,final-1]=fullopdata[i,3]
    fulloprot[final-1,init-1]=-fulloprot[init-1,final-1] #antisymmetrising
    fulloposc[init-1,final-1]=fullopdata[i,2]
    fulloposc[final-1,init-1]=-fulloposc[init-1,final-1] #antisymmetrising

fulloprot=fulloprot*-1.0 #sign correction

rot_str_fullop=fulloprot[ri-1,rf-1]*1.967e-3 #converting from reduced rot str to atomic units
rot_str_fullop_cgs=rot_str_fullop*471.44e-40 #converting from a.u to cgs
osc_str_fullop=fulloposc[ri-1,rf-1] #unitless

#osdata=np.loadtxt("ostr_raw.dat")
#osc_strength_len=osdata[0,2]
#osc_strength_vel=osdata[1,2]

file=open("tmoments.dat","w")
file.writelines(["Rotatory strengths (mixed): ", str(rot_str), " (a.u) ", str(rot_str_cgs), " (cgs) ", "\n"])
file.writelines(["Rotatory strengths (velocity): ", str(rot_str_vel), " (a.u) ", str(rot_str_vel_cgs), " (cgs) ", "\n"])
file.writelines(["Rotatory strengths (fulloperator):", str(rot_str_fullop), " (a.u) " , str(rot_str_fullop_cgs), " (cgs)", "\n"])
file.writelines(["Oscillator strengths (velocity): " , str(osc_str_vel), "\n"])
file.writelines(["Oscillator strengths (fulloperator):", str(osc_str_fullop), "\n"])
file.writelines(["Dipole strengths (velocity): ", str(dip_str_vel), " (a.u) ", str(dip_str_vel_cgs), " (cgs) ", "\n"])
file.writelines(["Dipole moment (length,vector): ", str(u[0]), " ", str(u[1]), " ", str(u[2]), " (a.u) ", "\n" ])
file.writelines(["Dipole moment (velocity,vector): ", str(v[0]), " ", str(v[1]), " ", str(v[2]), " (a.u) ", "\n" ])
file.writelines(["Magnetic strength (magnitude): ", str(mag_str), " (a.u) ", str(mag_str_cgs), " (cgs) ", "\n"])
file.writelines(["Magnetic moment (vector): ", str(m[0]), " ", str(m[1]), " ", str(m[2]), "\n"])
file.writelines(["dipole-magnetic angle (length): ", str(theta_len), " (radians) ",  str(theta_len_degrees), " (degrees) ", "\n"])
file.writelines(["dipole-magnetic angle (velocity): ", str(theta_vel), " (radians) ",  str(theta_vel_degrees), " (degrees) ", "\n"])
file.writelines(["Excitation Energy (vertical): ", str(E1), " (a.u) ", str(E1_ev), " (eV) ", "\n"])
#file.writelines(["Osccilator strengths (velocity): " , str(osc_strength_vel), "\n"])

file.close()
