# get-utils-openmolcas
Scripts for extracting circular dichroism data from .log files of MOLCAS 

## Sections: 
Directional, for directional data
main, for regular data

## Files:
### Main script: calcmoments.sh
syntax: bash calcmoments.sh file.log nroots ri rf \
where file.log is the output file of MOLCAS, nroots is the number of roots used in the calculation (CIRoots keyword in MOLCAS) and ri and rf are the roots for which the transition is to be calculated, i.e, a transition from root ri to root rf. 
