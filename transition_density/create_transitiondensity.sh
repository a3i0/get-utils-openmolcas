#Redners image of molecule from cube file
#Syntax: create_transitiondensity.sh  -f <.cube file> (-r rendering method) (-x camera's x position -y camera's y position -z camera's z position)

SCRIPTS_DIR=$(dirname $0)
renderer=opengl #default renderer
#default camera positions
camera_dir_x=1
camera_dir_y=-1
camera_dir_z=-0.15

while getopts "r:i:f:x:y:z:" arg; do
  case $arg in
    r) renderer=$OPTARG;;
    #i) cube_file1=$OPTARG;;
    #f) cube_file2=$OPTARG;;
    f) cube_file=$OPTARG;;
    x) camera_dir_x=$OPTARG;;
    y) camera_dir_y=$OPTARG;;
    z) camera_dir_z=$OPTARG;;
  esac
done



#bash $SCRIPTS_DIR/gettransitiondensity.sh $cube_file1 $cube_file2
#cube_file="transition_density.cube" #must be the same as the variable 'outputcube' from gettransitondensity.sh

python3 $SCRIPTS_DIR/create_transitiondensity.py $cube_file $renderer $camera_dir_x $camera_dir_y $camera_dir_z
