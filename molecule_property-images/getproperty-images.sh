#bash script file for extracting dipole and magnetic dipole vectors from tmoments.dat
#and putting them in a file for python.
#Input: xyz_file, tmoments.dat, rendering method
#Output: dip_len_value.raw, dip_vel_value.raw, mag_value.raw
#Requirements: getproperty-images.py
#Syntax: getproperty-images.sh xyz_file.xyz -f <.xyz file> (-r rendering method) (-x camera's x position -y camera's y position -z camera's z position)

SCRIPTS_DIR=$(dirname $0)
renderer=opengl #default renderer
#default camera positions
camera_dir_x=1
camera_dir_y=-1
camera_dir_z=-0.15

while getopts "r:f:x:y:z:" arg; do
  case $arg in
    r) renderer=$OPTARG;;
    f) geom_file=$OPTARG;;
    x) camera_dir_x=$OPTARG;;
    y) camera_dir_y=$OPTARG;;
    z) camera_dir_z=$OPTARG;;
  esac
done


grep -i 'dipole moment' tmoments.dat | grep -i 'length'| cut -d ':' -f 2 | awk '{print $1 " "  $2 " " $3}' > dip_len_value.raw
grep -i 'dipole moment' tmoments.dat | grep -i 'velocity'| cut -d ':' -f 2 | awk '{print $1 " "$2 " " $3}' > dip_vel_value.raw
grep -i 'magnetic moment' tmoments.dat | cut -d ':' -f 2 | awk '{print $1 " " $2 " " $3}' > mag_value.raw


python3 $SCRIPTS_DIR/getproperty-images.py $geom_file $renderer $camera_dir_x $camera_dir_y $camera_dir_z

#rm dip_len_value.raw dip_vel_value.raw mag_value.raw
