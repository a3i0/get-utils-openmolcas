# get-utils-openmolcas
Scripts for extracting circular dichroism data from .log files of MOLCAS 

## Sections: 
Directional, for directional data
main, for regular data

## Files:
### Main script: calcmoments.sh
Syntax: bash calcmoments.sh file.log nroots ri rf \
where file.log is the output file of MOLCAS, nroots is the number of roots used in the calculation (CIRoots keyword in MOLCAS) and ri and rf are the roots for which the transition is to be calculated, i.e, a transition from root ri to root rf. 

.log file must have the following:
* Directional CD data calculated using 'Directions' keyword along with keyword 'CD' in RASSI
* Directional CD and oscillator strength data of full operator calculated using the 'Directions' \'
  keyword along with keyword 'TIINTENSITIES' in RASSI. 

Output: Three files, 'dir-velmoments.raw', 'dir-mixmoments.raw' and 'dir-fullmoments.raw' with the following format: \
<x-coordinate> <y-coordinate> <z-coordinate> <rotatory strength in cgs units>
  
### Direction generator: getdirections.py
Syntax: python getdirections.py <grid size>

Output: Generates two files:\
* 'directions_sph.inp' with azimuthal angle $\theta$ in the range $[0,2\pi]$ and geographic polar angles $\phi$ in the range $[-\pi/2,\pi/2]$.\
Format: If $\theta$ is an array of ordered (in ascending) of $\theta$ values and $\vec{\phi}$ is the corresponding array for $\phi$,

$\; \; \; \vec{\theta}\bigotimes\mathbb{I} \; \; \;  \mathbb{I}\bigotimes\vec{\phi}$



* 'directions_cart.inp' with the corresponding cartesian coordinate, using a geographical system for the polar angle $\phi$



