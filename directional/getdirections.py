#v1.0
#Input = geom file, grid size(factor by which to divide 360). 
#Output = directions.inp, a list of directions in cartesian and spherical coordinates. 
#syntax: python3 getdirections.py <input_geom> <grid size>

import numpy as np
import sys

geom=np.loadtxt(sys.argv[1],skiprows=2, usecols=(1,2,3)) #skips first 2 rows and reads column 2,3 and 4 from first argument passed to py file
natoms=np.loadtxt(sys.argv[1],max_rows=1) #reads first row of input file

com=sum(geom)/natoms #centre of mass. sum() sums up rows 
angle_grid_size=int(sys.argv[2]) #divides 360 degrees into angle_grid_size parts in both xy and xz planes

theta=np.linspace(0,360,angle_grid_size+1)
phi=np.linspace(-90,90,angle_grid_size+1)
r=1
directions_sph=np.zeros(shape=((angle_grid_size+1)**2,3))

index=0
for i in range(angle_grid_size+1):
    for j in range(angle_grid_size+1):
        index=index+1
        directions_sph[index-1,0]=theta[i]
        directions_sph[index-1,1]=phi[j]
        directions_sph[index-1,2]=1

x=np.cos(theta*(np.pi/180.0))*np.cos(phi*(np.pi/180.0))
y=np.sin(theta*(np.pi/180.0))*np.cos(phi*(np.pi/180.0))
z=np.sin(phi*(np.pi/180.0))
directions_cart=np.zeros(shape=((angle_grid_size+1)**2,3))

index=0
for i in range(angle_grid_size+1):
    for j in range(angle_grid_size+1):
        index=index+1
        directions_cart[index-1,0]=np.cos(directions_sph[index-1,0]*(np.pi/180.0))*np.cos(directions_sph[index-1,1]*(np.pi/180.0))
        directions_cart[index-1,1]=np.sin(directions_sph[index-1,0]*(np.pi/180.0))*np.cos(directions_sph[index-1,1]*(np.pi/180.0))
        directions_cart[index-1,2]=np.sin(directions_sph[index-1,1]*(np.pi/180.0))




                
#shifting by adding com
#directions_xy=com+directions_xy
#directions_xz=com+directions_xz
#directions=directions+com

#alldir=np.concatenate((directions_xy,directions_xz),axis=0) #concatenates matrices along the column direction

#saving in appropriate format for inputting into molcas. header adds lines before data and comments defaults to '#')
np.savetxt('directions_sph.inp', directions_sph)
np.savetxt('directions_cart.inp', directions_cart)

