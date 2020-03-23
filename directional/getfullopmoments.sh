#v1.0
#Input: .log file, number of roots
#Output: creates a file with readable directional full operator transition moments and also prints it
#Syntax: bash getfullmoments.dat <.log> <nroots>

nroots=$2

grep --after-context=$(((3*$nroots*($nroots-1)/2 + 9))) "Transition moment strengths" $1 | cat > fullmoments.dat #n(n-1)/2 max transitions + extra lines
cat fullmoments.dat


