#Input: getmoments_isotropic.sh, .log file with one set of velocity and mixed rotatory strenghts
#calcmoments_tensor.py, angle_grid_size (factor by which to divide 360)
#Output: File with velocity and length gauge rotatory strength tensors for all roots
#with format <root1> <root2> <isotropic value> <Rxx> <Rxy> <Rxz> <Ryy> <Ryz> <Rzz>.
#Also calls python to run calcmoments_tensor.py
#Syntax: bash gettensors.sh <.log file> <nroots> <root1> root2> <angle_grid_size>

nroots=$2
ri=$3
rf=$4
angle_grid_size=$5

SCRIPTS_DIR=$(dirname $0)

bash $SCRIPTS_DIR/getmoments_isotropic.sh $1

grep 'tensor' velmoments.dat --after-context=1 | cut -d ":" -f 2 | sed 'n; d' > velmoments1.tmp #file with tensor
grep 'tensor' velmoments.dat --after-context=1 | cut -d ":" -f 2 | sed '1d; n; d' > velmoments2.tmp #file with roots and isotropic value
grep 'tensor' mixmoments.dat --after-context=1 | cut -d ":" -f 2 | sed 'n; d' > mixmoments1.tmp
grep 'tensor' mixmoments.dat --after-context=1 | cut -d ":" -f 2 | sed '1d; n; d' > mixmoments2.tmp

paste -d ' ' velmoments2.tmp velmoments1.tmp > veltensor.raw
paste -d ' ' mixmoments2.tmp mixmoments1.tmp > mixtensor.raw

#python3 $SCRIPTS_DIR/com.py $geomfile
python3 $SCRIPTS_DIR/calcmoments_tensor.py $nroots $ri $rf $angle_grid_size
