#v1.0
#Input: .log file, number of roots, roots between which transition moments are to be calculated
#Output: raw files with directional (one file for each) full operator transition moments for python (.raw). Also calls python to do calculations.
#syntax: bash calcmoments.sh <.log> <nroots> <root1> <root2>

SCRIPTS_DIR=$(dirname $0) #variable with the directory of all the script files


#array with all the lines between which data is located
dataholders=($(bash $SCRIPTS_DIR/getfullopmoments.sh $1 $2 | grep -n '\---------------------------------------------------------------'| cut -d ":" -f 1))
len_dataholders=${#dataholders[@]} #length of this array

rm -f momentsfullop* #removing file to prevent append errors in python
rm -f tmoments.dat 

#File with all the directions
bash $SCRIPTS_DIR/getdirections.sh $1 $2 > directions.raw
 
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

python3 $SCRIPTS_DIR/getmoments.py $2 $3 $4 $((len_dataholders/2))
#removing temporary files created by the data getters above
rm momentsfullop*
