#Input:
#Output: Files with directional velocity gague and directional mixed gauge CD values

nroots=$2
ri=$2 #Initial and final roots
rf=$3

line_init_vel=$(grep 'Circular Dichroism' $1  --line-number | cut -d ":" -f 1 | sed '2,3 d')
line_final_vel=$(grep 'Circular Dichroism' $1  --line-number | cut -d ":" -f 1 | sed '1 d'| sed '2 d')

sed "$line_init_vel,$((line_final_vel-1))! d" $1 > velmoments.dat

line_init_mix=$line_final_vel
line_final_mix=$(grep 'Transition ' $1 -m 1 --line-number | cut -d ":" -f 1)

sed "$line_init_mix,$((line_final_mix-1))! d" $1 > mixmoments.dat
