#v1.0
#Input: .log file, number of roots, roots between which transition moments are to be calculated
#Output: raw files with dipole, angular momentum and velocity componenents and full operator transitions for python (.raw). Also calls python to do calculations.
#syntax: bash calcmoments.sh <.log> <nroots> <root1> <root2>

SCRIPTS_DIR=$(dirname $0) #variable with the directory of all the script files

#creating raw data file to be loaded on to python
#truncated moments
bash $SCRIPTS_DIR/getmoments.sh $1 $2 | sed '/PROPERTY/ d' | sed '/STATE/ d' | cut -d " " -f 1 --complement | awk '{$1=""; print $0}' | cat > moments.raw

#Full operator transition moments
startline=$(bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep -n '\--------' | cut -d ":" -f 1| sed -n 2p)
endline=$(bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep -n '\--------' | cut -d ":" -f 1| sed -n 3p)
bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | sed "$((startline+1)),$((endline-1)) !d" | cat > momentsfullop.raw

#Energies
bash $SCRIPTS_DIR/getenergies.sh $1 $2 | cut -c 1-43 --complement | cat > energies.raw 

#removing temporary files created by the data getters above




python $SCRIPTS_DIR/getmoments.py $2 $3 $4

