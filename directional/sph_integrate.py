import numpy as np
import scipy as scp
from scipy import special
import matplotlib
#matplotlib.use('Qt5Agg')
from scipy import integrate

data=np.loadtxt("directions_sph.inp")
#data

angle_grid_size=36

theta=np.linspace(0,360,angle_grid_size+1) #range of angles
phi=np.linspace(0,180,angle_grid_size+1)
theta=theta*np.pi/180.0
phi=phi*np.pi/180.0
#theta
#phi

thetapoints=np.ndarray.flatten(np.tensordot(theta,np.ones(len(phi)), axes=0))
phipoints=np.ndarray.flatten(np.tensordot(np.ones(len(theta)),phi, axes=0))
phipoints
thetapoints

#complex(0,1)*np.array([complex(0,1), complex(0,3)])
myharm1=complex(1,0)*np.array(scp.special.sph_harm(0,1,thetapoints,phipoints))
myharm1=np.real(myharm1)
harmsign1=np.sign(myharm1)

myharm2=complex(1,0)*np.array(scp.special.sph_harm(0,0,thetapoints,phipoints))
myharm2=np.real(myharm2)
harmsign2=np.sign(myharm2)

myharm3=(1/np.sqrt(2))*complex(0,1)*np.array(scp.special.sph_harm(-1,1,thetapoints,phipoints)+scp.special.sph_harm(1,1,thetapoints,phipoints))
myharm3=np.real(myharm3)
harmsign3=np.sign(myharm3)

myharm4=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,1,thetapoints,phipoints)-scp.special.sph_harm(1,1,thetapoints,phipoints))
myharm4=np.real(myharm4)
harmsign4=np.sign(myharm4)


tempharm=np.zeros(len(phi))
for i in range(len(phi)):
    tempharm[i]=scp.integrate.trapz(np.multiply(myharm2[i::len(phi)],myharm2[i::len(phi)]),thetapoints[::len(phi)]) #integrating harm^2 over azimuthal theta

scp.integrate.trapz(tempharm*np.sin(phipoints[:len(theta)]),phipoints[:len(theta)]) #integral over polar phi. Volume element = sin(phi)d(phi)

#shuffling test
import random
def my_shuffle(array): #function that actually returns a shuffled array
        random.shuffle(array)
        return array

thetapoints_shuffled=np.ndarray.flatten(np.tensordot(my_shuffle(theta),np.ones(len(phi)), axes=0))
phipoints_shuffled=np.ndarray.flatten(np.tensordot(np.ones(len(theta)),my_shuffle(phi), axes=0))

myharm1_shuffled=complex(1,0)*np.array(scp.special.sph_harm(0,1,thetapoints_shuffled,phipoints_shuffled))
myharm1_shuffled=np.real(myharm1_shuffled)
harmsign1_shuffled=np.sign(myharm1_shuffled)

myharm2_shuffled=complex(1,0)*np.array(scp.special.sph_harm(0,0,thetapoints_shuffled,phipoints_shuffled))
myharm2_shuffled=np.real(myharm2_shuffled)
harmsign2=np.sign(myharm2_shuffled)

myharm3_shuffled=(1/np.sqrt(2))*complex(0,1)*np.array(scp.special.sph_harm(-1,1,thetapoints_shuffled,phipoints_shuffled)+scp.special.sph_harm(1,1,thetapoints_shuffled,phipoints_shuffled))
myharm3_shuffled=np.real(myharm3_shuffled)
harmsign3_shuffled=np.sign(myharm3_shuffled)

myharm4_shuffled=(1/np.sqrt(2))*np.array(scp.special.sph_harm(-1,1,thetapoints_shuffled,phipoints_shuffled)-scp.special.sph_harm(1,1,thetapoints_shuffled,phipoints_shuffled))
myharm4_shuffled=np.real(myharm4_shuffled)
harmsign4_shuffled=np.sign(myharm4_shuffled)

tempharm_shuffled=np.zeros(len(phi))
for i in range(len(phi)):
    tempharm_shuffled[i]=scp.integrate.trapz(np.multiply(myharm2_shuffled[i::len(phi)],myharm2_shuffled[i::len(phi)]),thetapoints_shuffled[::len(phi)]) #integrating harm^2 over azimuthal theta

scp.integrate.trapz(tempharm*np.sin(phipoints_shuffled[:len(theta)]),phipoints_shuffled[:len(theta)])

#t = np.linspace(0, 20, 500)
#plt.plot(t, np.sin(t))
#plt.show()
