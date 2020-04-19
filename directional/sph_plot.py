import numpy as np
import scipy as scp
from scipy import special
import matplotlib
#matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data=np.loadtxt("directions_sph.inp")
#data

angle_grid_size=24

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
myharm1=complex(0,1)*np.array(scp.special.sph_harm(-3,3,thetapoints,phipoints)+scp.special.sph_harm(3,3,thetapoints,phipoints))
myharm1=np.real(myharm1)
harmsign1=np.sign(myharm1)
myharm1=np.abs(myharm1)
myharm1

x1=myharm1*np.cos(thetapoints)*np.sin(phipoints)
y1=myharm1*np.sin(thetapoints)*np.sin(phipoints)
z1=myharm1*np.cos(phipoints)
len(z1)
x1
y1
z1

myharm2=np.array(scp.special.sph_harm(-3,3,thetapoints,phipoints)-scp.special.sph_harm(3,3,thetapoints,phipoints))
myharm2=np.real(myharm2)
harmsign2=np.sign(myharm2)
myharm2=np.abs(myharm2)
myharm2
x2=myharm2*np.cos(thetapoints)*np.sin(phipoints)
y2=myharm2*np.sin(thetapoints)*np.sin(phipoints)
z2=myharm2*np.cos(phipoints)
#x=[1,1,1,2,2,2,3,3,3]
#y=[1,2,3,1,2,3,1,2,3]
#z=[4,4,3,4,4,4,4,4,4]
myharm3=complex(0,1)*np.array(scp.special.sph_harm(-2,3,thetapoints,phipoints)-scp.special.sph_harm(2,3,thetapoints,phipoints))
myharm3=np.real(myharm3)
harmsign3=np.sign(myharm3)
myharm3=np.abs(myharm3)
myharm3
x3=myharm3*np.cos(thetapoints)*np.sin(phipoints)
y3=myharm3*np.sin(thetapoints)*np.sin(phipoints)
z3=myharm3*np.cos(phipoints)

myharm4=np.array(scp.special.sph_harm(-2,3,thetapoints,phipoints)+scp.special.sph_harm(2,3,thetapoints,phipoints))
myharm4=np.real(myharm4)
harmsign4=np.sign(myharm4)
myharm4=np.abs(myharm4)
myharm4
x4=myharm4*np.cos(thetapoints)*np.sin(phipoints)
y4=myharm4*np.sin(thetapoints)*np.sin(phipoints)
z4=myharm4*np.cos(phipoints)

myharm5=complex(0,1)*np.array(scp.special.sph_harm(-1,3,thetapoints,phipoints)+scp.special.sph_harm(1,3,thetapoints,phipoints))
myharm5=np.real(myharm5)
harmsign5=np.sign(myharm5)
myharm5=np.abs(myharm5)
myharm5
x5=myharm5*np.cos(thetapoints)*np.sin(phipoints)
y5=myharm5*np.sin(thetapoints)*np.sin(phipoints)
z5=myharm5*np.cos(phipoints)

myharm6=np.array(scp.special.sph_harm(0,3,thetapoints,phipoints)+scp.special.sph_harm(0,3,thetapoints,phipoints))
myharm6=np.real(myharm6)
harmsign6=np.sign(myharm6)
myharm6=np.abs(myharm6)
myharm6
x6=myharm6*np.cos(thetapoints)*np.sin(phipoints)
y6=myharm6*np.sin(thetapoints)*np.sin(phipoints)
z6=myharm6*np.cos(phipoints)

fig = plt.figure()
ax1 = fig.add_subplot(231, projection='3d')
ax2 = fig.add_subplot(232, projection='3d')
ax3 = fig.add_subplot(233, projection='3d')
ax4 = fig.add_subplot(234, projection='3d')
ax5 = fig.add_subplot(235, projection='3d')
ax6 = fig.add_subplot(236, projection='3d')

ax1.scatter(x1,y1,z1,c=harmsign1)
ax2.scatter(x2,y2,z2,c=harmsign2)
ax3.scatter(x3,y3,z3,c=harmsign3)
ax4.scatter(x4,y4,z4,c=harmsign4)
ax5.scatter(x5,y5,z5,c=harmsign5)
ax6.scatter(x6,y6,z6,c=harmsign6)

plt.show()

#t = np.linspace(0, 20, 500)
#plt.plot(t, np.sin(t))
#plt.show()
