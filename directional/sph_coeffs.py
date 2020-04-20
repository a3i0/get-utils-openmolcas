import numpy as np
import scipy as scp
from scipy import special
import matplotlib
#matplotlib.use('Qt5Agg')
from scipy import integrate
import sys

data=np.loadtxt("dir-velmoments.raw")
angles=np.loadtxt("directions_sph.inp")

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

phipoints

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



#Defining various spherical harmonics (https://en.wikipedia.org/wiki/Table_of_spherical_harmonics)
#s
harm_00=np.array(scp.special.sph_harm(0,0,thetapoints,phipoints))
harm_00=np.real(harm_00)

#p
harm_1min1=complex(0,1)*(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,1,thetapoints,phipoints)+scp.special.sph_harm(1,1,thetapoints,phipoints)) #1min1=1-1
harm_10=np.array(scp.special.sph_harm(0,1,thetapoints,phipoints))
harm_11=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,1,thetapoints,phipoints)-scp.special.sph_harm(1,1,thetapoints,phipoints))

harm_1min1=np.real(harm_1min1)
harm_10=np.real(harm_10)
harm_11=np.real(harm_11)

#d
harm_2min2=complex(0,1)*(1/np.sqrt(2))*np.array(scp.special.sph_harm(-2,2,thetapoints,phipoints)-scp.special.sph_harm(2,2,thetapoints,phipoints))
harm_2min1=complex(0,1)*(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,2,thetapoints,phipoints)+scp.special.sph_harm(1,2,thetapoints,phipoints))
harm_20=np.array(scp.special.sph_harm(0,2,thetapoints,phipoints))
harm_21=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,2,thetapoints,phipoints)-scp.special.sph_harm(1,2,thetapoints,phipoints))
harm_22=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-2,2,thetapoints,phipoints)+scp.special.sph_harm(2,2,thetapoints,phipoints))

harm_2min2=np.real(harm_2min2)
harm_2min1=np.real(harm_2min1)
harm_20=np.real(harm_20)
harm_21=np.real(harm_21)
harm_22=np.real(harm_22)




#norms. We will be dividing the obtained coeffs by the norms as the norms are not exactly zero
#(tested in sph_integrate.py). The orthogonal ones are pretty orthogonal though, so we do not need to worry about
#solving a full linear system of equations
#s----------------------------------------------------------------------------
tempnorm_00=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_00[i]=scp.integrate.trapz(np.multiply(harm_00[i::len_phi],harm_00[i::len_phi]),thetapoints[::len_phi]) #integrating harm^2 over azimuthal theta

norm_00=scp.integrate.trapz(tempnorm_00*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_00=-1.0*norm_00 #to account for reverse direction of integration of phi

#p----------------------------------------------------------------------------
tempnorm_1min1=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_1min1[i]=scp.integrate.trapz(np.multiply(harm_1min1[i::len_phi],harm_1min1[i::len_phi]),thetapoints[::len_phi])

norm_1min1=scp.integrate.trapz(tempnorm_1min1*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_1min1=-1.0*norm_1min1

tempnorm_10=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_10[i]=scp.integrate.trapz(np.multiply(harm_10[i::len_phi],harm_10[i::len_phi]),thetapoints[::len_phi])

norm_10=scp.integrate.trapz(tempnorm_10*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_10=-1.0*norm_10

tempnorm_11=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_11[i]=scp.integrate.trapz(np.multiply(harm_11[i::len_phi],harm_11[i::len_phi]),thetapoints[::len_phi])
norm_11=scp.integrate.trapz(tempnorm_11*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_11=-1.0*norm_11

#d----------------------------------------------------------------------------
tempnorm_2min2=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_2min2[i]=scp.integrate.trapz(np.multiply(harm_2min2[i::len_phi],harm_2min2[i::len_phi]),thetapoints[::len_phi])

norm_2min2=scp.integrate.trapz(tempnorm_2min2*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_2min2=-1.0*norm_2min2

tempnorm_2min1=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_2min1[i]=scp.integrate.trapz(np.multiply(harm_2min1[i::len_phi],harm_2min1[i::len_phi]),thetapoints[::len_phi])
norm_2min1=scp.integrate.trapz(tempnorm_2min1*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_2min1=-1.0*norm_2min1

tempnorm_20=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_20[i]=scp.integrate.trapz(np.multiply(harm_20[i::len_phi],harm_20[i::len_phi]),thetapoints[::len_phi])

norm_20=scp.integrate.trapz(tempnorm_20*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_20=-1.0*norm_20

tempnorm_21=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_21[i]=scp.integrate.trapz(np.multiply(harm_21[i::len_phi],harm_21[i::len_phi]),thetapoints[::len_phi])

norm_21=scp.integrate.trapz(tempnorm_21*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_21=-1.0*norm_21

tempnorm_22=np.zeros(len_phi)
for i in range(len_phi):
    tempnorm_22[i]=scp.integrate.trapz(np.multiply(harm_22[i::len_phi],harm_22[i::len_phi]),thetapoints[::len_phi])

norm_22=scp.integrate.trapz(tempnorm_22*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
norm_22=-1.0*norm_22

# norm_00
# norm_1min1
# norm_10
# norm_11
# norm_2min2
# norm_2min1
# norm_20
# norm_21


#coeffs
#s----------------------------------------------------------------------------
tempc_00=np.zeros(len_phi)
for i in range(len_phi):
    tempc_00[i]=scp.integrate.trapz(np.multiply(harm_00[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_00=scp.integrate.trapz(tempc_00*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_00=-1.0*c_00 #to account for reverse direction of integration of phi

#p----------------------------------------------------------------------------
tempc_1min1=np.zeros(len_phi)
for i in range(len_phi):
    tempc_1min1[i]=scp.integrate.trapz(np.multiply(harm_1min1[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_1min1=scp.integrate.trapz(tempc_1min1*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_1min1=-1.0*c_1min1

tempc_10=np.zeros(len_phi)
for i in range(len_phi):
    tempc_10[i]=scp.integrate.trapz(np.multiply(harm_10[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_10=scp.integrate.trapz(tempc_10*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_10=-1.0*c_10

tempc_11=np.zeros(len_phi)
for i in range(len_phi):
    tempc_11[i]=scp.integrate.trapz(np.multiply(harm_11[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])
c_11=scp.integrate.trapz(tempc_11*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_11=-1.0*c_11

#d----------------------------------------------------------------------------
tempc_2min2=np.zeros(len_phi)
for i in range(len_phi):
    tempc_2min2[i]=scp.integrate.trapz(np.multiply(harm_2min2[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_2min2=scp.integrate.trapz(tempc_2min2*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_2min2=-1.0*c_2min2

tempc_2min1=np.zeros(len_phi)
for i in range(len_phi):
    tempc_2min1[i]=scp.integrate.trapz(np.multiply(harm_2min1[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])
c_2min1=scp.integrate.trapz(tempc_2min1*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_2min1=-1.0*c_2min1

tempc_20=np.zeros(len_phi)
for i in range(len_phi):
    tempc_20[i]=scp.integrate.trapz(np.multiply(harm_20[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_20=scp.integrate.trapz(tempc_20*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_20=-1.0*c_20

tempc_21=np.zeros(len_phi)
for i in range(len_phi):
    tempc_21[i]=scp.integrate.trapz(np.multiply(harm_21[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_21=scp.integrate.trapz(tempc_21*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_21=-1.0*c_21

tempc_22=np.zeros(len_phi)
for i in range(len_phi):
    tempc_22[i]=scp.integrate.trapz(np.multiply(harm_22[i::len_phi],value[i::len_phi]),thetapoints[::len_phi])

c_22=scp.integrate.trapz(tempc_22*np.sin(phipoints[:len_theta]),phipoints[:len_theta])
c_22=-1.0*c_22

#Dividing all coeffs by the spherical harmonic norms
c_00=c_00/norm_00
c_1min1=c_1min1/norm_1min1
c_10=c_10/norm_10
c_11=c_11/norm_11
c_2min2=c_2min2/norm_2min2
c_2min1=c_2min1/norm_2min1
c_20=c_20/norm_20
c_21=c_21/norm_21
c_22=c_22/norm_22

#Dividing all coeffs by norm of input data
c_00_norm=c_00/np.sqrt(norm)
c_1min1_norm=c_1min1/np.sqrt(norm)
c_10_norm=c_10/np.sqrt(norm)
c_11_norm=c_11/np.sqrt(norm)
c_2min2_norm=c_2min2/np.sqrt(norm)
c_2min1_norm=c_2min1/np.sqrt(norm)
c_20_norm=c_20/np.sqrt(norm)
c_21_norm=c_21/np.sqrt(norm)
c_22_norm=c_22/np.sqrt(norm)

#printing to stdout
print('s: ' + str(c_00) + " " + str(c_00_norm))
print('py: ' + str(c_1min1) + " " + str(c_1min1_norm))
print('pz: ' + str(c_10) + " " + str(c_10_norm))
print('px: ' + str(c_11) + " " + str(c_11_norm))
print('dxy: ' + str(c_2min2) + " " + str(c_2min2_norm))
print('dyz: ' + str(c_2min1) + " " + str(c_2min1_norm))
print('dz2: ' + str(c_20) + " " + str(c_20_norm))
print('dxz: ' + str(c_21)+ " " + str(c_21_norm))
print('dx2-y2: ' + str(c_22) + " " + str(c_22_norm))


#Sorting for integration (with treshold)
# thetapoints_sorted_indices=np.argsort(thetapoints)
# thetapoints=np.sort(thetapoints)
# phipoints=np.take(phipoints,thetapoints_sorted_indices)
# value=np.take(value,thetapoints_sorted_indices)
#
# i=0
# j=0
# thrs=1E-3 #threshold for making blocks in data
# while(i<(len(thetapoints)-1)):
    # if(np.abs(thetapoints[i+1]-thetapoints[i])<thrs):
        # i=i+1
        # continue
    # else:
        # phipoints_sorted_indices=np.argsort(phipoints[j:i+1])
        # phipoints[j:i+1]=np.sort(phipoints[j:i+1])
        # value[j:i+1]=np.take(value[j:i+1],phipoints_sorted_indices)
        # j=i+1
        # i=i+1
#
#last remaining block
# phipoints_sorted_indices=np.argsort(phipoints[j:i+1])
# phipoints[j:i+1]=np.sort(phipoints[j:i+1])
# value[j:i+1]=np.take(value[j:i+1],phipoints_sorted_indices)
#
# value_sign=np.sign(value)
# thetapoints




#thetapoints=np.ndarray.flatten(np.tensordot(theta,np.ones(len(phi)), axes=0))
#phipoints=np.ndarray.flatten(np.tensordot(np.ones(len(theta)),phi, axes=0))
#len(phipoints)
#thetapoints


#t = np.linspace(0, 20, 500)
#plt.plot(t, np.sin(t))
#plt.show()
