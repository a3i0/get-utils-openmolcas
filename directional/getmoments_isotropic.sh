#Different version for isotropic files
#Input: .log file with isotropic full moments. 
#Output: Files with directional velocity gague and directional mixed gauge CD values
#Syntax: bash getmoments.sh <.log file>


line_init_vel=$(grep 'Circular Dichroism' $1  --line-number | cut -d ":" -f 1 | sed '2,3 d')
line_final_vel=$(grep 'Circular Dichroism' $1  --line-number | cut -d ":" -f 1 | sed '1 d'| sed '2 d')

sed "$line_init_vel,$((line_final_vel-1))! d" $1 > velmoments.dat

line_init_mix=$line_final_vel
line_final_mix=$(grep 'Isotropic transition ' $1  --line-number | cut -d ":" -f 1)

sed "$line_init_mix,$((line_final_mix-1))! d" $1 > mixmoments.dat
