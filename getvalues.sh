grep "::    RASSI" $1 
grep --after-context=4 "SF State" $1
grep --after-context=16 "Circular Dichroism - mixed" $1 | sed '2,8 d' | sed '3,4 d' | sed '/tensor/ d'
grep --after-context=11 "Isotropic transition" $1 | sed '2,7 d'
