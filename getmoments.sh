#v1.2.1
#Input: getvalues.sh, .log file
#Output: readeable files (with dipole, angular momentum and velocity componenets), raw files for python (.raw)

SCRIPTS_DIR=$(dirname $0) #variable with the directory of all the script files

#creating readable data file with dipole, angular momentum and velocity (momentum) components
grep --after-context=8 "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | cat > moments.dat
grep --after-context=8 "PROPERTY: MLTPL  1   COMPONENT:   2" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat
grep --after-context=8 "PROPERTY: MLTPL  1   COMPONENT:   3" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat

grep --after-context=8 "PROPERTY: ANGMOM     COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat
grep --after-context=8 "PROPERTY: ANGMOM     COMPONENT:   2" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat
grep --after-context=8 "PROPERTY: ANGMOM     COMPONENT:   3" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat

grep --after-context=8 "PROPERTY: VELOCITY   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat
grep --after-context=8 "PROPERTY: VELOCITY   COMPONENT:   2" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat
grep --after-context=8 "PROPERTY: VELOCITY   COMPONENT:   3" $1 | sed '2,3 d' | sed '3 d' | cat >> moments.dat



#creating raw data file to be loaded on to python
cat moments.dat | sed '/PROPERTY/ d' | sed '/STATE/ d' | cat > moments.raw
bash $SCRIPTS_DIR/getvalues.sh $1 | sed '17 !d' | cat > momentsfullop.raw
#grep --after-context=6 "Dipole transition strengths (spin-free states)" mol2.log | tail -1 | cat > ostr_raw.dat
#grep --after-context=6 "Velocity transition strengths (spin-free states):" mol2.log | tail -1 | cat >> ostr_raw.dat
bash $SCRIPTS_DIR/getenergies.sh $1 #creates energies.raw

python $SCRIPTS_DIR/getmoments.py #calculates u.m and tiintensity rot strength in cgs units

