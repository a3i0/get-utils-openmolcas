
#Syntax: bash sph_fit_compare.sh <coeff file> <.log file> <nroots> <ri> <rf>
SCRIPTS_DIR=$(dirname $0)

nroots=$3
ri=$4
rf=$5
logfile=$2
coefffile=$1

#creating tmoments.dat
bash ${SCRIPTS_DIR}/../calcmoments.sh $logfile $nroots $ri $rf
grep 'Rotatory strength' tmoments.dat | grep 'velocity' | awk '{print $6}' > velrotstr.raw
grep 'Rotatory strength' tmoments.dat | grep 'mixed' | awk '{print $6}' > mixrotstr.raw

python3 $SCRIPTS_DIR/sph_fit_compare.py $coefffile
rm velrotstr.raw
rm mixrotstr.raw
