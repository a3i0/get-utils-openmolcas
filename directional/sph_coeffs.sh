#Calls the correct pyhton script to do the integration based on command line options.
#Input: raw file with directional data (created by getmoments.py)
#       'directions_sph.inp' created by getdirections.py. Make sure this corresponds with above file (all directions must be present in raw file)
#       Maximum n value of spherical harmonic Y_{n}^{m} to be printed
#Requirements: sph_coeffs_trapz.py and sph_coeffs_clenshaw.py
#Output: formatted coefficients of directional data in dir-velmoments.raw up to maximun n value specified
#

#!/bin/bash

SCRIPTS_DIR=$(dirname $0)

#Assigning options to internal variables using getopts
while getopts ":i:n:f:" arg; do
  case $arg in
    i) method=$OPTARG;;
    n) maxn=$OPTARG;;
    f) rawfile=$OPTARG
  esac
done

case $method in
  trapz) python3 $SCRIPTS_DIR/sph_coeffs_trapz.py $rawfile $maxn;;
  clenshaw-curtis) python3 $SCRIPTS_DIR/sph_coeffs_clenshaw-curtis.py $rawfile $maxn;;
esac
