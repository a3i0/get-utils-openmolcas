#v1.0
#Input: getfullopmoments.sh, .log file, number of roots
#output: Directions calculated with full operator in .log file
#Syntax: bash getdirections.sh <.log> <nroots>

SCRIPTS_DIR=$(dirname $0)

bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep 'Direction of the k-vector:' | cut -d ":" -f 2

