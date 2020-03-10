init=$((${2}+5))
nblocks=$(($2/4 + 1))
#--------------------------------------------------------------------------------------------------
grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat > moments.dat

grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
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
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: ANGMOM     COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   2" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: ANGMOM     COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: ANGMOM     COMPONENT:   3" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
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
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: VELOCITY   COMPONENT:   2" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   2" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat

grep --after-context=$init "PROPERTY: VELOCITY   COMPONENT:   3" $1 | sed '2,3 d' | cat > tmp.dat
i=1
while ((i<$nblocks)) 
do
	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: VELOCITY   COMPONENT:   3" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
	cat tmp_x.dat | cat > tmp.dat
	let i++
done
cat tmp.dat | cat >> moments.dat


#init=$((${2}+5))
#nblocks=$(($2/4 + 1))
#grep --after-context=$init "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | cat > tmp.dat
#
#i=1
#while ((i<$nblocks)) 
#do
#	grep --after-context=$(($init+$i*(${2}+3))) "PROPERTY: MLTPL  1   COMPONENT:   1" $1 | sed '2,3 d' | sed '3 d' | sed '1,8 d'| cut -c 13- | cat >tmp${i}.dat
#	paste tmp.dat tmp${i}.dat | cat > tmp_x.dat
#	cat tmp_x.dat | cat > tmp.dat
#	let i++
#done
