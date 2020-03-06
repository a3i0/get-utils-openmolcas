#v1.0
#Input = geom file, grid size(factor by which to divide 360). 
#Output = directions.inp, a list of directions along xy and xz concatenated. Has number of directions on top of file. 
#syntax: python3 getdirections.py <input_geom> <grid size>

import numpy as np
import sys

geom=np.loadtxt(sys.argv[1],skiprows=2, usecols=(1,2,3)) #skips first 2 rwos and reads column 2,3 and 4 from first argument passed to py file
natoms=np.loadtxt(sys.argv[1],max_rows=1) #reads first row of input file

com=sum(geom)/natoms #centre of mass. sum() sums up rows 
angle_grid_size=int(sys.argv[2]) #divides 360 degrees into angle_grid_size parts in both xy and xz planes

#Rotation matrices
givens_xy=givens_xy=np.array(([np.cos(2*np.pi/angle_grid_size) , -np.sin(2*np.pi/angle_grid_size) , 0], [np.sin(2*np.pi/angle_grid_size) , np.cos(2*np.pi/angle_grid_size) , 0], [0,0,1]))
givens_xz=np.array(([np.cos(2*np.pi/angle_grid_size) , 0, -np.sin(2*np.pi/angle_grid_size)], [0,1,0], [np.sin(2*np.pi/angle_grid_size) , 0, np.cos(2*np.pi/angle_grid_size)]))

#Initialising direction matrices as natoms x 3 matrices
directions_xy=np.zeros(shape=((angle_grid_size),3))
directions_xz=np.zeros(shape=((angle_grid_size),3))

#updating entries
for i in range(len(directions_xy)):
    if (i==0):
        directions_xy[i]=np.array([1.0,0.0,0.0])
        continue
    directions_xy[i]=np.matmul(givens_xy,directions_xy[i-1])


for i in range(len(directions_xz)):
    if (i==0):
        directions_xz[i]=np.array([1.0,0.0,0.0])
        continue
    directions_xz[i]=np.matmul(givens_xy,directions_xz[i-1])

#shifting by adding com
directions_xy=com+directions_xy
directions_xz=com+directions_xz

alldir=np.concatenate((directions_xy,directions_xz),axis=0) #concatenates matrices along the column direction

#saving in appropriate format for inputting into molcas. header adds lines before data and comments defaults to '#')
np.savetxt('directions.inp', alldir, header=str(len(directions_xy)+len(directions_xz)), comments='')
