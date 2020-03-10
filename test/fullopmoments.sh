#v1.0
#Input: .log file, number of roots
#Output: creates a file with readable full operator transition moments and also orints it

nroots=$2

grep --after-context=$((($nroots*($nroots-1)/2 + 9))) "Isotropic transition" $1 | cat > fullmoments.dat #n(n-1)/2 max transitions + extra lines
cat fullmoments.dat


