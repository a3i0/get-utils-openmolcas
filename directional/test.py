import numpy as np
import scipy as scp
from scipy import special
from scipy import integrate
import sys

angle_grid_size=36

theta=np.linspace(0,360,(angle_grid_size+1)) #range of angles
phi=np.linspace(0,180,4*(angle_grid_size+1))
theta=theta*np.pi/180.0
phi=phi*np.pi/180.0
#theta
#phi

thetapoints=np.ndarray.flatten(np.tensordot(theta,np.ones(len(phi)), axes=0))
phipoints=np.ndarray.flatten(np.tensordot(np.ones(len(theta)),phi, axes=0))
phipoints

def realharm(m,n,theta,phi):
    if(m==0):
        return np.real(scp.special.sph_harm(m,n,theta,phi)) #the returned datatype is float and not complex float

    #General formula of real spherical harmonic
    output=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-np.abs(m),n,theta,phi) + np.sign(m)*(-1)**(np.abs(m))*scp.special.sph_harm(np.abs(m),n,theta,phi))
    if(m < 0):
        output=complex(0,1)*output

    return np.real(output)

len_theta=int(np.sqrt(len(thetapoints)))
len_phi=int(np.sqrt(len(phipoints)))

len_theta=len(theta)
len_phi=len(phi)
len_phi
len_theta

len(thetapoints)
len(phipoints)
thetapoints[37]

maxn=4

sph_harm=np.zeros(shape=(((maxn+1)**2),len(thetapoints)))
counter=0
for i in range(maxn+1):
    for j in range(-i,i+1):
        sph_harm[counter]=np.array(realharm(j,i,thetapoints,phipoints))
        counter=counter+1

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
tempsph_norm=np.zeros(shape=(len(sph_harm),len_theta))
for i in range(len_theta):
    tempsph_norm[:,i]=scp.integrate.trapz(np.multiply(sph_harm[:,(i*len_phi):((i+1)*len_phi)],sph_harm[:,(i*len_phi):((i+1)*len_phi)])*np.sin(phipoints[:len_phi]),phipoints[:len_phi]) #integrating over azimuthal theta

len(thetapoints[::len_phi])
np.shape(sph_harm[:,0::len_phi])

tempsph_norm[1]
sph_norm=np.array(scp.integrate.trapz(tempsph_norm,thetapoints[::len_phi]))
sph_norm=sph_norm

np.shape(tempsph_norm)
len(phipoints[:len_phi])
len(thetapoints[::len_phi])
phipoints[1:2]
sph_norm
