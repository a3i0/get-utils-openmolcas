#Input: Files loaded by loadtxt: input .raw file with directional data (created by getmoments.py) and 'directions_sph.inp'. Make sure these correspond.
#       Maximum n value of spherical harmonic Y_{n}^{m}
#Output: formatted coefficients of directional data in dir-velmoments.raw up to maximun n value specified using Clenshaw-Curtis quadrature for polar angles
#Syntax: python3 sph_coeffs.py <.raw file>  <maxn>

import numpy as np
import scipy as scp
from scipy import special
from scipy import integrate
from scipy import fft
import sys
import warnings

scp.version.full_version

data=np.loadtxt(sys.argv[1]) #only reads third coulmn.
#data=np.loadtxt('dir-velmoments.raw')
angles=np.loadtxt("directions_sph.inp") #assumes that these are the directions that correspond to the directional values in
                                        #'dir-velmoments.raw'
maxn=int(sys.argv[2])
#maxn=4
#converting to spherical polar coordinates (NOTE: NOT a geographic system like in create_pm3dfile.py)
# r=np.sqrt(np.power(data[:,0],2) + np.power(data[:,1],2) + np.power(data[:,2],2))
# phipoints=np.arccos(np.divide(data[:,2],r)) #range of arccos = [-pi/2,pi/2]


#This method assumes that the directions are created by equally dividing theta and phi into an equal number of points
value=data[:,3]
value=value/9.274E-41 #converting to atomic units
thetapoints=angles[:,0] #note that the range here is usually [-180,180]
phipoints=angles[:,1] #note that the range here is usually [-90,90]
phipoints=90-phipoints #converting from geographic to regular spherical coordinates. Now range is [90,0]
thetapoints=thetapoints*np.pi/180.0 #converting to radians
phipoints=phipoints*np.pi/180.0


if(len(thetapoints) != len(phipoints)):
    sys.exit("Error: The number of theta and phi angles not equal!")

if(len(value) != len(thetapoints)):
    sys.exit("Error: There are more or less data points than angles! Do not use directions from directions_sph.inp")

len_theta=int(np.sqrt(len(thetapoints))) #program only works if these two are equal
len_phi=int(np.sqrt(len(phipoints)))

if(len_phi != len_theta):
    sys.exit('Number of grid points of theta and phi not equal.')






#function for getting real spherical harmonics
def realharm(m,n,theta,phi):
    if(m==0):
        return np.real(scp.special.sph_harm(m,n,theta,phi)) #the returned datatype is float and not complex float

    #General formula of real spherical harmonic
    output=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-np.abs(m),n,theta,phi) + np.sign(m)*(-1)**(np.abs(m))*scp.special.sph_harm(np.abs(m),n,theta,phi))
    if(m < 0):
        output=complex(0,1)*output

    return np.real(output) #the returned datatype is float and not complex float

#function that integrates the product of two functions f1 and f2 using the Clenshaw-Curtis quadrature for polar angles phi and trapezoidal rule for azimulthal theta
#Requires that the input array f1 and f2 have dimension not greater than two
def integrate(f1,f2,theta,phi):
    if((np.ndim(f1)>2)or(np.ndim(f2)>2)):
        sys.exit('Dimension of array(s) to be integrated larger than two')

    len_theta=int(np.sqrt(len(thetapoints)))
    len_phi=int(np.sqrt(len(phipoints)))

   #All the subsequent if statements are to properly subset the numpy arrays when for values of dimension = 1,2 of f1 and f2 (4 cases)
    if((np.ndim(f1)==2)and(np.ndim(f2)==2)): #will return array with one row and len_phi columns
        #print('a')
        temp=np.zeros(shape=(len(f1),len_phi))
        for i in range(len_phi):
            temp[:,i]=scp.integrate.trapz(np.multiply(f1[:,i::len_phi],f2[:,i::len_phi]),theta[::len_phi]) #integrating over azimuthal theta

        tempdct=scp.fft.dct(temp,type=1) #flipping the array important otherwise the fourier coefficients will be all wrong

        integral=tempdct[:,0]
        kmax=(len_phi-2)//2
        k=1
        while(k <= kmax):
            integral=integral + 2.0*tempdct[:,2*k]/(1-(2*k)**2)
            k=k+1

        integral=integral/(len_phi-1)


    if((np.ndim(f1)==1)and(np.ndim(f2)==1)): #will return scalar
        #print('b')
        temp=np.zeros(shape=(len_phi))
        for i in range(len_phi):
            temp[i]=scp.integrate.trapz(np.multiply(f1[i::len_phi],f2[i::len_phi]),theta[::len_phi]) #integrating over azimuthal theta

        tempdct=scp.fft.dct(temp,type=1) #flipping the array important otherwise the fourier coefficients will be all wrong

        integral=tempdct[0]
        kmax=(len_phi-2)//2
        k=1
        while(k <= kmax):
            integral=integral + 2.0*tempdct[2*k]/(1-(2*k)**2)
            k=k+1

        integral=integral/(len_phi-1)

    if((np.ndim(f1)==1)and(np.ndim(f2)==2)): #will return array with one row and len_phi columns
        #print('c')
        temp=np.zeros(shape=(len(f1),len_phi))
        for i in range(len_phi):
            temp[:,i]=scp.integrate.trapz(np.multiply(f1[i::len_phi],f2[:,i::len_phi]),theta[::len_phi]) #integrating over azimuthal theta

        tempdct=scp.fft.dct(temp,type=1) #flipping the array important otherwise the fourier coefficients will be all wrong

        integral=tempdct[:,0]
        kmax=(len_phi-2)//2
        k=1
        while(k <= kmax):
            integral=integral + 2.0*tempdct[:,2*k]/(1-(2*k)**2)
            k=k+1

        integral=integral/(len_phi-1)

    if((np.ndim(f1)==2)and(np.ndim(f2)==1)): #will return array with one row and len_phi columns
        #print('d')
        temp=np.zeros(shape=(len(f1),len_phi))
        for i in range(len_phi):
            temp[:,i]=scp.integrate.trapz(np.multiply(f1[:,i::len_phi],f2[i::len_phi]),theta[::len_phi]) #integrating over azimuthal theta

        tempdct=scp.fft.dct(temp,type=1) #flipping the array important otherwise the fourier coefficients will be all wrong

        integral=tempdct[:,0]
        kmax=(len_phi-2)//2
        k=1
        while(k <= kmax):
            integral=integral + 2.0*tempdct[:,2*k]/(1-(2*k)**2)
            k=k+1

        integral=integral/(len_phi-1)

    return integral

#-------------------------------------------------------------------------------------------------------------------------------------------------

#Integration for normalization coefficient of input data
norm=integrate(value,value,thetapoints,phipoints)
norm


#Vector of spherical harmonics. Order = [(0,0),(-1,1),(0,1),(1,1),(-2,2),(-1,2),(0,2)] where (m,n)and so on
#Real spherical harmonics defined here: https://en.wikipedia.org/wiki/Table_of_spherical_harmonics
sph_harm=np.zeros(shape=(((maxn+1)**2),len(thetapoints)))
counter=0
for i in range(maxn+1):
    for j in range(-i,i+1):
        sph_harm[counter]=np.array(realharm(j,i,thetapoints,phipoints))
        counter=counter+1

#Vector of norms. norm[i] 0 norm of sph_harm[i].
#Norm for testting. do not need to divide by norm as they should be exactly equal to one
sph_norm=integrate(sph_harm,sph_harm,thetapoints,phipoints)


#Vector of coeffs. coeff[i] is the coeff corresponding to spherical harmonic in sph_harm[i]
coeff=integrate(sph_harm,value,thetapoints,phipoints)
coeff

#Dividing all coeffs by the  respective spherical harmonic norms
#coeff=np.divide(coeff,sph_norm)


#Normalized (sum of squares = 1) coeffs of input data
coeff_normalized=coeff/np.sqrt(norm)

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



#Integrations without defining the function integrate:
#Spherical norms:
# tempsph_norm=np.zeros(shape=(len(sph_harm),len_phi))
# for i in range(len_phi):
    # tempsph_norm[:,i]=scp.integrate.trapz(np.multiply(sph_harm[:,i::len_phi],sph_harm[:,i::len_phi]),thetapoints[::len_phi]) #integrating over azimuthal theta
#
# tempdct_sph_norm=scp.fft.dct(np.flip(tempsph_norm),type=1) #flipping the arraw important otherwise the fourier coefficients will be all wrong
#
# sph_norm=tempdct_sph_norm[:,0]
# kmax=(len_phi-2)//2
# k=1
# while(k <= kmax):
    # sph_norm=sph_norm + 2.0*tempdct_sph_norm[:,2*k]/(1-(2*k)**2)
    # k=k+1
#
# sph_norm=sph_norm/(len_phi-1)

#Coefficients:
# tempcoeff=np.zeros(shape=(len(sph_harm),len_phi))
# for i in range(len_phi):
    # tempcoeff[:,i]=scp.integrate.trapz(np.multiply(sph_harm[:,i::len_phi],value[i::len_phi]),thetapoints[::len_phi]) #integrating over azimuthal theta
#
# tempdct_coeff=scp.fft.dct(np.flip(tempcoeff),type=1) #flipping the arraw important otherwise the fourier coefficients will be all wrong
#
# tempdct_coeff
# coeff=tempdct_coeffs[:,0]
# kmax=(len_phi-2)//2
# k=1
# while(k <= kmax):
    # coeff=coeff + 2.0*tempdct_coeff[:,2*k]/(1-(2*k)**2)
    # k=k+1
#
# coeff=coeff/(len_phi-1)
# coeff
