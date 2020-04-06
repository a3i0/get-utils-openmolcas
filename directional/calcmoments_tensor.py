#Input: veltensor.raw, mixtensor.raw, nroots, grid size of angles (factor by which to divide 360),
#initial and final roots of selected transition
#Output:
#Syntax: python3 calcmoments_tensor.py <nroots> <ri> <rf> <angle_grid_size>

import numpy as np
import sys
import os

veldata=np.loadtxt('veltensor.raw')
mixdata=np.loadtxt('mixtensor.raw')

nroots=int(sys.argv[1])
ri=int(sys.argv[2])
rf=int(sys.argv[3])
angle_grid_size=int(sys.argv[4])

#checking if the tensor corresponds to the transition root indices
if(len(veldata) != len(mixdata)):
    print('number of data points in mix and velocity files do not match!')
    sys.exit()

for i in range(len(veldata)):
    if(veldata[i,2]-np.mean([veldata[i,3],veldata[i,6],veldata[i,8]]) > 1e-4):
        print('The transition root indices do not match with the tensor (velocity)!')
        sys.exit()
    if(mixdata[i,2] != np.mean([mixdata[i,3],mixdata[i,6],mixdata[i,8]])> 1e-4):
        print('The transition root indices do not match with the tensor (mixed)!')
        sys.exit()


#Creating tensor for specified transition root indices
veltensor=np.zeros(shape=(3,3))
for i in range(len(veldata)):
    if(veldata[i,0]==ri):
        for j in range(nroots-int(veldata[i,0])): #file does not have transition index ri=nroots
            if(veldata[i+j,1]==rf):
                veltensor[0,0]=veldata[i+j,3]
                veltensor[0,1]=veldata[i+j,4]
                veltensor[0,2]=veldata[i+j,5]
                veltensor[1,1]=veldata[i+1,6]
                veltensor[1,2]=veldata[i+j,7]
                veltensor[2,2]=veldata[i+j,8]

mixtensor=np.zeros(shape=(3,3))
for i in range(len(mixdata)):
    if(mixdata[i,0]==ri):
        for j in range(nroots-int(mixdata[i,0])): #file does not have transition index ri=nroots
            if(mixdata[i+j,1]==rf):
                mixtensor[0,0]=mixdata[i+j,3]
                mixtensor[0,1]=mixdata[i+j,4]
                mixtensor[0,2]=mixdata[i+j,5]
                mixtensor[1,1]=mixdata[i+1,6]
                mixtensor[1,2]=mixdata[i+j,7]
                mixtensor[2,2]=mixdata[i+j,8]

#symmetrising
veltensor[1,0]=veltensor[0,1]
veltensor[2,0]=veltensor[0,2]
veltensor[2,1]=veltensor[1,2]
mixtensor[1,0]=mixtensor[0,1]
mixtensor[2,0]=mixtensor[0,2]
mixtensor[2,1]=mixtensor[1,2]

#unit conversion
veltensor=veltensor*9.274e-41
mixtensor=mixtensor*9.274e-41
#sign convention fix
veltensor=veltensor*-1.0
mixtensor=mixtensor*-1.0

#tensor rotation to get value at angle
theta=np.linspace(-180,180,angle_grid_size+1) #range of angles. Angles as defined by gnuplot's spherical mapping (geographical)
phi=np.linspace(-90,90,angle_grid_size+1)
u=np.array([np.cos(theta*np.pi/180.0)*np.cos(phi*np.pi/180.0) , np.sin(theta*np.pi/180.0)*np.cos(phi*np.pi/180.0) , np.sin(phi*np.pi/180.0)]) #returns 3xangle_grid_size array with each angle multiplication on each column



veldir=np.einsum('ij,jk->i', np.transpose(u), np.matmul(veltensor,u)) #effiecient, vectorised and no redundant calculations (which simple matmuls would have)
mixdir=np.einsum('ij,jk->i', np.transpose(u), np.matmul(mixtensor,u))

#saving
velfile=open('dir-velmoments_fromtensor.raw','w')
mixfile=open('dir-mixmoments_fromtensor.raw','w')
for i in range(len(theta)):
    velfile.writelines([str(theta[i]), ' ', str(phi[i]), ' ' , str(veldir[i]), '\n'])
    mixfile.writelines([str(theta[i]), ' ', str(phi[i]), ' ' , str(mixdir[i]), '\n'])

#print(veldir)
#print(mixdir)

#veltensor=np.zeros(shape=(nroots,nroots,3,3)) #inefficient. change if possible
#mixtensor=np.zeros(shape=(nroots,nroots,3,3))
