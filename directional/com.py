#Input: geom.xyz file
#Output= geom.com file with centre of mass of given input geometry mixdata as column vector
#syntax: python3 com.py <geom.xyz file>

import numpy as np
import sys

filename=sys.argv[1]

geom=np.loadtxt(filename,skiprows=2, usecols=(1,2,3)) #skips first 2 rows and reads column 2,3 and 4 from first argument passed to py file
natoms=np.loadtxt(filename,max_rows=1) #reads first row of input file

com=sum(geom)/natoms #centre of mass. sum() sums up rows
np.savetxt(filename[:-3]+'com', com)
