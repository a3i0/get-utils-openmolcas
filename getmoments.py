#v1.3
#Input: RASSI State energies, Dipole, velocity and angular momentum components, full operator oscillator and rotatory strengths
#Output: Rot strength in mixed, veocity and for full operator, dipole strength in length, osc strength in velociy and full operator
#Dependencies: look at files loaded by np.loadtxt(). Should be in correct format

import numpy as np

energy=np.loadtxt("energies.raw") #loads state energies in a.u
E1=energy[1]-energy[0] #first excitation energy

data=np.loadtxt("moments.raw")
u=[data[0,2],data[3,2],data[6,2]]
l=[data[9,2],data[12,2],data[15,2]]
v=[data[18,2],data[21,2],data[24,2]]

u=np.array(u)
l=np.array(l)
v=np.array(v)
m=-0.5*l

#rotatory strengths in mixed
rot_str=np.dot(u,m)
rot_str_cgs=rot_str*471.44e-40
#rotatory strength in velocity
rot_str_vel=-1*np.dot(v,m)/E1
rot_str_vel_cgs=rot_str_vel*471.44e-40
#dipole strengths in length and velocity 
dip_str_len=abs(np.dot(u,u))
dip_str_len_cgs=dip_str_len*471.44e-40
dip_str_vel=abs(np.dot(v,v))
#oscillatory strength in velocity
osc_str_vel=2.0*dip_str_vel/(3.0*E1)
osc_str_vel_cgs=osc_str_vel*471.44e-40

#full operator moments
fullopdata=np.loadtxt("momentsfullop.raw") 
rot_str_fullop=fullopdata[3]*1.967e-3 #converting from reduced rot str to atomic units
rot_str_fullop_cgs=rot_str_fullop*471.44e-40 #converting from a.u to cgs
osc_str_fullop=fullopdata[2] #already in atomic units
osc_str_fullop_cgs=osc_str_fullop*471.44e-40

#osdata=np.loadtxt("ostr_raw.dat")
#osc_strength_len=osdata[0,2]
#osc_strength_vel=osdata[1,2]
#osc_strength_len_cgs=osc_strength_len*471.44e-40
#osc_strength_vel_cgs=osc_strength_vel*471.44e-40

file=open("moments.dat","a")
file.writelines(["Rotatory strengths (mixed): ", str(rot_str), "(a.u) ", str(rot_str_cgs), "(cgs) ", "\n"])
file.writelines(["Rotatory strengths (velocity): ", str(rot_str_vel), "(a.u) ", str(rot_str_vel_cgs), "(cgs) ", "\n"])
file.writelines(["Rotatory strengths (full operator):", str(rot_str_fullop), "(a.u) " , str(rot_str_fullop_cgs), "(cgs)", "\n"])
file.writelines(["Dipole strengths (length): " , str(dip_str_len), "(a.u) ",  str(dip_str_len_cgs), "(cgs)", "\n"])
file.writelines(["Oscillator strengths (velocity): " , str(osc_str_vel), "(a.u) ",  str(osc_str_vel_cgs), "(cgs)", "\n"])
file.writelines(["Oscillator strengths (full operator):", str(osc_str_fullop), "(a.u) " , str(osc_str_fullop_cgs), "(cgs)", "\n"])

#file.writelines(["Osccilator strengths (velocity): " , str(osc_strength_vel), "(a.u) ",  str(osc_strength_vel_cgs), "(cgs)", "\n"])

file.close()

