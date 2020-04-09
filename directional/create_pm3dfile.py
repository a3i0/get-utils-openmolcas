#v1.1
#Input: input file with format (x y z value) where x,y,z lie on a unit sphere
#Output: file with angles (theta phi abs(value) value signof(value)) with correct format for use in gnuplot with 4-column pm3d. Note that angles are accoirding to 'geographical' spherical polar coordinates and angle in degrees
#syntax: python create_pm3dfile.py <input file>

import numpy as np
import sys
import os

data=np.loadtxt(sys.argv[1])

r=np.sqrt(np.power(data[:,0],2) + np.power(data[:,1],2) + np.power(data[:,2],2))
phi=np.arcsin(np.divide(data[:,2],r)) #range of arcsin = [-pi/2,pi/2]
theta=np.arctan2(data[:,1],data[:,0]) #range of arctan2 = [-pi,pi]
value=data[:,3]

#converting to degrees
phi=phi*(180.0/np.pi)
theta=theta*(180.0/np.pi)


#Sorting with treshold
theta_sorted_indices=np.argsort(theta)
theta=np.sort(theta)
phi=np.take(phi,theta_sorted_indices)
value=np.take(value,theta_sorted_indices)

i=0
j=0
thrs=1E-3 #threshold for making blocks in data
while(i<(len(theta)-1)):
    if(np.abs(theta[i+1]-theta[i])<thrs):
        i=i+1
        continue
    else:
        phi_sorted_indices=np.argsort(phi[j:i+1])
        phi[j:i+1]=np.sort(phi[j:i+1])
        value[j:i+1]=np.take(value[j:i+1],phi_sorted_indices)
        j=i+1
        i=i+1

#last remaining block
phi_sorted_indices=np.argsort(phi[j:i+1])
phi[j:i+1]=np.sort(phi[j:i+1])
value[j:i+1]=np.take(value[j:i+1],phi_sorted_indices)

value_sign=np.sign(value)

#Transposing arrays into coumns vectors and concatenating along columns
output=np.concatenate((theta[:,np.newaxis],phi[:,np.newaxis],np.absolute(value[:,np.newaxis]), value[:,np.newaxis] , value_sign[:,np.newaxis]), axis=1)

#np.savetxt('output.dat', output)

#Writing to file in correct format
if os.path.exists("directional.gnuplot"):
  os.remove("directional.gnuplot")

#np.savetxt("directional_gnuplot",output)
file=open("directional.gnuplot","ab")

i=0
while(i<(len(theta)-1)):
    np.savetxt(file,output[i,:] ,fmt="%1.5E",delimiter=' ', newline=' ')
    np.savetxt(file,['\n'],fmt='%s',newline='')
    if(np.abs(theta[i+1]-theta[i])<thrs):
        i = i+1
        continue
    else:
        np.savetxt(file,['\n'], fmt= "%s", newline='')
        i=i+1
        continue

#last block
np.savetxt(file,output[i,:],fmt="%1.5E", delimiter=' ', newline=' ')
file.close()

#print(output)
