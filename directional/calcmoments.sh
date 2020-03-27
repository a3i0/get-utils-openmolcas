#v1.0
#Input: .log file, number of roots, roots between which transition moments are to be calculated. getfullopmoments,sh, getmoments.sh, getmoments.py
#Output: raw files with directional (one file for each) full operator transition moments for python (.raw). Also calls python to do calculations.
#syntax: bash calcmoments.sh <.log> <nroots> <root1> <root2>

SCRIPTS_DIR=$(dirname $0) #variable with the directory of all the script files
nroots=$2

#array with all the lines between which data is located
dataholders=($(bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep -n '\---------------------------------------------------------------'| cut -d ":" -f 1))
len_dataholders=${#dataholders[@]} #length of this array

rm -f momentsfullop* #removing file to prevent append errors in python
rm -f tmoments.dat

#File with all the directions
#bash $SCRIPTS_DIR/getdirections.sh $1 $2 > directions.raw

#Creating one data file for each direction
i=0
while ((i<$((len_dataholders/2))))
do
        startline=${dataholders[$((2*i))]}
        endline=${dataholders[$(((2*i)+1))]}
       #echo $startline
       #echo $endline
       bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | sed "$((startline+1)),$((endline-1)) !d" | sed '/maximum/ d' | sed '/minimum/ d'| cat > momentsfullop_$((i+1)).raw
        let i++
done

#Truncated Operators
#Creating velmoments.dat and mixmoment.dat
bash $SCRIPTS_DIR/getmoments.sh $1

ndir=$((len_dataholders/2))
i=0
#rm -f velmoments.raw

sed '1,4 d' velmoments.dat | sed '/Direction/d' | sed '/From/d' | sed '/--/d' | sed "s/^ *//g" > velmoments.raw
sed '1,9 d' mixmoments.dat | sed '/Direction/d' | sed '/From/d' | sed '/--/d' | sed "s/^ *//g" > mixmoments.raw
#while ((i<$ndir))
#do
#  grep 'Red. rot. str.' velmoments.dat -m $((i+1)) --after-context=$(((nroots*(nroots-1))/2 + 1)) | sed '1,2 d' >> velmoments.raw
#  let i++
#done
#i=0
#rm -f mixmoments.raw
#while ((i<$ndir))
#do
#  grep 'Red. rot. str.' mixmoments.dat -m $((i+1)) --after-context=$(((nroots*(nroots-1))/2 + 1)) | sed '1,2 d' >> mixmoments.raw
#  let i++
#done



python3 $SCRIPTS_DIR/getmoments.py $2 $3 $4 $((len_dataholders/2))
#removing temporary files created by the data getters above
rm momentsfullop*
#rm velmoments.raw
#rm mixmoments.raw
