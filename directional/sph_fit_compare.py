#Input: formatted coefficient file from sph_coeffs (should have at least maxn=2)
#        raw files velrotstr and mixrotstr with single data of rotatory strength in cgs
#Output: Difference between fitted coefficients and OpenMOLCAS-calculated values
#Syntax: python3 sph_fit_compare <coeff file>

import numpy as np
import sys
import os

coeffs=np.loadtxt(sys.argv[1], skiprows=1, usecols=1)
velrotstr_cgs=np.loadtxt('velrotstr.raw')
mixrotstr_cgs=np.loadtxt('mixrotstr.raw')

A=0.25*np.sqrt(15/np.pi) #constant before angular terms of all d except dz2
B=0.5*np.sqrt(1/np.pi) #constant before angular terms of s

velrotstr=velrotstr_cgs/9.274e-41
mixrotstr=mixrotstr_cgs/9.274e-41

velerror= coeffs[0]*B-velrotstr
mixerror=coeffs[0]*B-mixrotstr

print(velerror,mixerror)
