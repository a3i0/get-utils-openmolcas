#v2.0.1
#Input: .log file, number of roots
#Output: readable files (with dipole, angular momentum and velocity componenets) to stdout
#Syntax: bash getmoments.sh <.log> <nroots>


#creating readable data file with dipole, angular momentum and velocity (momentum) components
init=$((${2}+5)) #variable for value of after-context for first block
nblocks=$(($2/4 + 1)) #molcas prints at most 4 columns of moments in one line

#--------------------------------------------------------------------------------------------------
grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '1,2 d'|  sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat > moments.dat

grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   2" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   3" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat
#--------------------------------------------------------------------------------------------------
grep --after-context=$init "PROPERTY: ANGMOM     COMPONENT:   1" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   1" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: ANGMOM     COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   2" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: ANGMOM     COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   3" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done

cat tmp.dat | cat >> moments.dat
#-----------------------------------------------------------------------------------------------------
grep --after-context=$init "PROPERTY: VELOCITY   COMPONENT:   1" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   1" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: VELOCITY   COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   2" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: VELOCITY   COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   3" $1 | sed '1,2 d' | sed 1,$(($i*($2+3)))' 'd | cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat
#-------------------------------------------------------------------------------------------------------
#removing tmp files
rm -f tmp.dat tmp_x.dat

#printing created file to stdout
cat moments.dat


