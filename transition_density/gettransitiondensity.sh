#Script for generating transition density as a product of two wavefunctions
#Input: Two cube files corresponding to two wavefunctions.
#Output: Cube file with the volumetric data of two simply multplied
#Requirements: Thje cube files must be in Gaussian cube format
#              The input cube files must be for the same molecule and have the same number
#              of grid points, box size and all other parameters except volumetric data
#Syntax: bash gettransitondensity.sh <cube file 1> <cube file 2>

SCRIPTS_DIR=$(dirname $0)

inputcube1=$1
inputcube2=$2
outputcube="transition_density.cube"

natoms=$(sed '3 !d' n.cube | awk '{print $1}')
data_init=$(($natoms+3+1+2+1))

sed "$data_init,$ !d" $inputcube1 > ${inputcube1}.raw #delete lines from data_init till last line
sed "$data_init,$ !d" $inputcube2 > ${inputcube2}.raw

paste ${inputcube1}.raw ${inputcube2}.raw | awk '{for (i=1; i<(NF/2); i++) { printf "%s ", $i*$(NF/2+i)}; printf "%s\n", $(NF/2)*$NF }' > ${outputcube}.raw
sed "$data_init,$ d" $inputcube1 > $outputcube
cat ${outputcube}.raw >> $outputcube

rm ${inputcube1}.raw ${inputcube2}.raw ${outputcube}.raw
