#v2.0
#Input: log file
#Output: Readable file with RASSI state energies in a.u
#Syntax: bash getenergies.sh <.log>

grep "RASSI State" $1
