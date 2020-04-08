#v1.0
#Input: .log file, number of roots, roots between which transition moments are to be calculated. getfullopmoments.sh, getmoments.sh, getmoments.py
#Output: raw file with directional full operator transition moments (rotatory and oscillatory) for python (.raw). Also calls python to do calculations.
#syntax: bash calcmoments.sh <.log> <nroots> <root1> <root2>

SCRIPTS_DIR=$(dirname $0) #variable with the directory of all the script files
nroots=$2

#array with all the lines between which data is located
dataholders=($(bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep -n '\---------------------------------------------------------------'| cut -d ":" -f 1))
len_dataholders=${#dataholders[@]} #length of this array
ndir=$((len_dataholders/2))


#File with all the directions
#bash $SCRIPTS_DIR/getdirections.sh $1 $2 > directions.raw

#creating fullop raw files.
#Format= -1 x y
#         root1 root2 osc.str. rot.str.
bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | sed '/maximum/d' | sed '/minimum/d' |  sed -e '/Time for/,+100d'| sed -e '/++/,+2d' | sed '/for osc./,+2d' | sed '/--/d' | sed 's/Direction of the k-vector:/-1/g' | sed '/^[[:space:]]*$/d' | awk '{print $1 " " $2 " " $3 " "  $4}' > fullopmoments.raw


#Truncated Operators
#Creating velmoments.dat and mixmoment.dat
bash $SCRIPTS_DIR/getmoments.sh $1
#creating trunctaed operator raw files.
#Format = -1 x y z
#          root1 root2 rot.str. 0
cat velmoments.dat | sed '/^++/,+2d' | sed '/From/d' | sed '/--/d' | sed 's/Direction of the k-vector:/-1/g' | sed '/^[[:space:]]*$/d' | awk '{print $1 " " $2 " " $3 " " $4 " " 0}' | awk '{print $1 " "$2 " " $3 " " $4}' > velmoments.raw
cat mixmoments.dat | sed '/^++/,+7d' | sed '/From/d' | sed '/--/d' | sed 's/Direction of the k-vector:/-1/g' | sed '/^[[:space:]]*$/d' | awk '{print $1 " " $2 " " $3 " " $4 " " 0}' | awk '{print $1 " "$2 " " $3 " " $4}' > mixmoments.raw
 

#sed '1,4 d' velmoments.dat | sed '/Direction/d' | sed '/From/d' | sed '/--/d' | sed "s/^ *//g" > velmoments.raw
#sed '1,9 d' mixmoments.dat | sed '/Direction/d' | sed '/From/d' | sed '/--/d' | sed "s/^ *//g" > mixmoments.raw




python3 $SCRIPTS_DIR/getmoments.py $2 $3 $4 $ndir
#removing temporary files created by the data getters above
#rm velmoments.raw
#rm mixmoments.raw
#rm fullopmoments.raw
