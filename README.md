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
* Transition dipole moments calculated using the 'MEES' keyword in the RASSI module 
* Full operator Oscillator and Rotatory strengths calculated using the 'TIINENSITIES' keyword in the RASSI module

Output: A file 'tmoments.dat' with the following format: \
Rotatory strengths (mixed): <value> (a.u) <value> (cgs)\
Rotatory strengths (velocity): <value> (a.u) <value> (cgs)\
Rotatory strengths (fulloperator):<value> (a.u) <value> (cgs)\
Oscillator strength (length): <value>\
Oscillator strength (velocity): <value>\
Oscillator strength (fulloperator): <value>\
Dipole strengths (length): <value> (a.u) <value> (cgs)\
Dipole strengths (velocity): <value> (a.u) <value> (cgs)\
Dipole moment (length,vector): <xvalue> <yvalue> <zvalue> (a.u)\
Dipole moment (velocity,vector): <xvalue> <yvalue> <zvalue> (a.u)\
Magnetic strengths (magnitude): <value> (a.u) <value> (cgs)\
Magnetic moment (vector): <xvalue> <yvalue> <zvalue>\
dipole-magnetic angles (length): <value> (radians) <value> (degrees)\
dipole-magnetic angles (velocity): <value> (radians) <value> (degrees)\
Excitation Energy (vertical): <value> (a.u) <value> (eV)
  
Where <value> is the calculated quantity described by the label before ":" on the same row with the units given in brackets ()
after <value>, if needed. For vector quantities the quantities are printed in the order x y z. 
  

  

