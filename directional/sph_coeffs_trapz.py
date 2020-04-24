#Input: Files loaded by loadtxt: input .raw file with directional data (created by getmoments.py) and 'directions_sph.inp'. Make sure these correspond.
#       Maximum n value of spherical harmonic Y_{n}^{m}
#Output: formatted coefficients of directional data in dir-velmoments.raw up to maximun n value specified using regular trapezoidal integration
#Syntax: python3 sph_coeffs.py <.raw file>  <maxn>

import numpy as np
import scipy as scp
from scipy import special
from scipy import integrate
import sys

data=np.loadtxt(sys.argv[1]) #only reads third coulmn.
angles=np.loadtxt("directions_sph.inp") #assumes that these are the directions that correspond to the directional values in
                                        #'dir-velmoments.raw'
maxn=int(sys.argv[2])

#converting to spherical polar coordinates (NOTE: NOT a geographic system like in create_pm3dfile.py)
# r=np.sqrt(np.power(data[:,0],2) + np.power(data[:,1],2) + np.power(data[:,2],2))
# phipoints=np.arccos(np.divide(data[:,2],r)) #range of arccos = [-pi/2,pi/2]


#This method assumes that the directions are created by equally dividing theta and phi into an equal number of points
value=data[:,3]
value=value/9.274E-41 #converting to atomic units
thetapoints=angles[:,0] #note that the range here is usually [-180,180]
phipoints=angles[:,1]
phipoints=90-phipoints #converting from geographic to regular spherical coordinates. Now range is [pi,0]
thetapoints=thetapoints*np.pi/180.0 #converting to radians
phipoints=phipoints*np.pi/180.0


if(len(thetapoints) != len(phipoints)):
    sys.exit("Error: The number of theta and phi angles not equal!")

if(len(value) != len(thetapoints)):
    sys.exit("Error: There are more or less data points than angles! Do not use directions from directions_sph.inp")

len_theta=int(np.sqrt(len(thetapoints)))
len_phi=int(np.sqrt(len(phipoints)))


#Integration for normalization coefficient of input data
tempharm=np.zeros(len_phi)
for i in range(len_phi):
    tempharm[i]=scp.integrate.trapz(np.multiply(value[i::len_phi],value[i::len_phi]),thetapoints[::len_phi]) #integrating harm^2 over azimuthal theta

norm=scp.integrate.trapz(tempharm*np.sin(phipoints[:len_theta]),phipoints[:len_theta]) #integral over polar phi. Volume element = sin(phi)d(phi)
norm=norm*-1 #as integration over phi takes place from pi to 0 (reverse direction)
norm


#function for getting real spherical harmonics
def realharm(m,n,theta,phi):
    if(m==0):
        return np.real(scp.special.sph_harm(m,n,theta,phi)) #the returned datatype is float and not complex float

    #General formula of real spherical harmonic
    output=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-np.abs(m),n,theta,phi) + np.sign(m)*(-1)**(np.abs(m))*scp.special.sph_harm(np.abs(m),n,theta,phi))
    if(m < 0):
        output=complex(0,1)*output

    return np.real(output) #the returned datatype is float and not complex float

#Vector of spherical harmonics. Order = [(0,0),(-1,1),(0,1),(1,1),(-2,2),(-1,2),(0,2)] where (m,n)and so on
#Real spherical harmonics defined here: https://en.wikipedia.org/wiki/Table_of_spherical_harmonics
sph_harm=np.zeros(shape=(((maxn+1)**2),len(thetapoints)))
counter=0
for i in range(maxn+1):
    for j in range(-i,i+1):
        sph_harm[counter]=np.array(realharm(j,i,thetapoints,phipoints))
        counter=counter+1

#Vector of norms. norm[i] 0 norm of sph_harm[i].
#We will be dividing the obtained coeffs by the norms as the norms are not exactly zero
#(tested in sph_integrate.py). The orthogonal ones are pretty orthogonal though, so we do not need to worry about
#solving a full linear system of equations
tempsph_norm=np.zeros(shape=(len(sph_harm),len_phi))
for i in range(len_phi):
    tempsph_norm[:,i]=scp.integrate.trapz(np.multiply(sph_harm[:,i::len_phi],sph_harm[:,i::len_phi]),thetapoints[::len_phi]) #integrating over azimuthal theta

sph_norm=np.array(scp.integrate.trapz(tempsph_norm*np.sin(phipoints[:len_theta]),phipoints[:len_theta]))
sph_norm=sph_norm*-1.0


#Vector of coeffs. coeff[i] is the coeff corresponding to spherical harmonic in sph_harm[i]
tempcoeff=np.zeros(shape=(len(sph_harm),len_phi))
for i in range(len_phi):
    tempcoeff[:,i]=scp.integrate.trapz(np.multiply(sph_harm[:,i::len_phi],value[i::len_phi]),thetapoints[::len_phi]) #integrating over azimuthal theta

coeff=np.array(scp.integrate.trapz(tempcoeff*np.sin(phipoints[:len_theta]),phipoints[:len_theta]))
coeff=coeff*-1.0

#Dividing all coeffs by the  respective spherical harmonic norms
coeff=np.divide(coeff,sph_norm)


#Normalized (sum of squares = 1) coeffs of input data
coeff_normalized=coeff/np.sqrt(norm)

#Reduced rotatory strength values (only valid for s and d)
# A=0.25*np.sqrt(15/np.pi) #constant before angular terms of all d except dz2
# B=0.5*np.sqrt(1/np.pi) #constant before angular terms of s
# R_iso=coeff[0]*B
# if(maxn>=2):
    # R_xy=coeff[4]*A
    # R_yz=coeff[5]*A
    # R_xz=coeff[7]*A
    # R_xx__Ryyby2=coeff[8]*A
    # twoR_zz__R_xx__R_yyby6=coeff[6]*np.sqrt(3)*A

#List of orbital names
sph_harm_names=list() #empty list
if(maxn>=0):
    sph_harm_names=['s']
if(maxn>=1):
    sph_harm_names.extend(['px','py','pz'])
if(maxn>=2):
    sph_harm_names.extend(['dxy','dyz','dz2', 'dxz', 'dx2-y2'])
if(maxn>=3):
    sph_harm_names.extend(['fy(3x2-y2)', 'fxyz', 'fyz2', 'fz3', 'fxz2', 'fz(x2-y2)', 'fx(x2-3y2)'])
if(maxn>=3):
    sph_harm_names.extend(['gxy(x2-y2)', 'gzy3', 'gz2xy', 'gz3y', 'gz4', 'gz3x', 'gz2(x2-y2)','gzx3','gx4+y4'])
if(maxn>=4):
    templist=['higher harmonic']*((maxn+1)**2-25)
    sph_harm_names.extend(templist)


#printing to stdout
print("{0:19s}  {1:14s}   {2:18s}".format('Spherical Harmonic','Coeff','Coeff (normalized)'))
for i in range(len(coeff)):
    #print(sph_harm_names[i]+'     '+str(coeff[i])+'   '+str(coeff_normalized[i]))
    print("{0:19s} {1: 12.8e}  {2: 12.10e}".format(sph_harm_names[i], coeff[i], coeff_normalized[i]))
