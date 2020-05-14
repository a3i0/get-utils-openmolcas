#bash script file for extracting dipole and magnetic dipole vectors from tmoments.dat
#and putting them in a file for python.
#Input: xyz_file, tmoments.dat
#Output: dip_len_value.raw, dip_vel_value.raw, mag_value.raw
#Requirements: getproperty-images.py
#Syntax: getproperty-images.sh xyz_file.xyz

SCRIPTS_DIR=$(dirname $0)

grep -i 'dipole moment' tmoments.dat | grep -i 'length'| cut -d ':' -f 2 | awk '{print $1 " "  $2 " " $3}' > dip_len_value.raw
grep -i 'dipole moment' tmoments.dat | grep -i 'velocity'| cut -d ':' -f 2 | awk '{print $1 " "$2 " " $3}' > dip_vel_value.raw
grep -i 'magnetic moment' tmoments.dat | cut -d ':' -f 2 | awk '{print $1 " " $2 " " $3}' > mag_value.raw

python3 $SCRIPTS_DIR/getproperty-images.py $1

rm dip_len_value.raw dip_vel_value.raw mag_value.raw
