#v 1.0.1
grep "RASSI State" $1 | cut -c 1-43 --complement | cat > energies.raw
