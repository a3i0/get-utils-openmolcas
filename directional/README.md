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
* 'directions_sph.inp' with azimuthal angle <img src="/directional/tex/27e556cf3caa0673ac49a8f0de3c73ca.svg?invert_in_darkmode&sanitize=true" align=middle width=8.17352744999999pt height=22.831056599999986pt/> in the range <img src="/directional/tex/57e00d58bd259da9dc7986c73476b955.svg?invert_in_darkmode&sanitize=true" align=middle width=42.83683799999999pt height=24.65753399999998pt/> and geographic polar angles <img src="/directional/tex/f50853d41be7d55874e952eb0d80c53e.svg?invert_in_darkmode&sanitize=true" align=middle width=9.794543549999991pt height=22.831056599999986pt/> in the range <img src="/directional/tex/7c0876e2c6b579316b5e58cf99289514.svg?invert_in_darkmode&sanitize=true" align=middle width=82.02077729999998pt height=24.65753399999998pt/>.\
Format: If <img src="/directional/tex/27e556cf3caa0673ac49a8f0de3c73ca.svg?invert_in_darkmode&sanitize=true" align=middle width=8.17352744999999pt height=22.831056599999986pt/> is an array of ordered (in ascending) of <img src="/directional/tex/27e556cf3caa0673ac49a8f0de3c73ca.svg?invert_in_darkmode&sanitize=true" align=middle width=8.17352744999999pt height=22.831056599999986pt/> values and <img src="/directional/tex/2464fe5f1f3d919b17461575b6892cd6.svg?invert_in_darkmode&sanitize=true" align=middle width=23.40490844999999pt height=32.16441360000002pt/> is the corresponding array for <img src="/directional/tex/f50853d41be7d55874e952eb0d80c53e.svg?invert_in_darkmode&sanitize=true" align=middle width=9.794543549999991pt height=22.831056599999986pt/>,\
<img src="/directional/tex/e7388821d9725754b4ca7607a6cbf19f.svg?invert_in_darkmode&sanitize=true" align=middle width=38.31045734999999pt height=32.16441360000002pt/>  <img src="/directional/tex/2be688c08d74e24b789333e2a00d9d52.svg?invert_in_darkmode&sanitize=true" align=middle width=41.778001649999986pt height=32.16441360000002pt/>

* 'directions_cart.inp' with the corresponding cartesian coordinate, using a geographical system for the polar angle <img src="/directional/tex/f50853d41be7d55874e952eb0d80c53e.svg?invert_in_darkmode&sanitize=true" align=middle width=9.794543549999991pt height=22.831056599999986pt/>



