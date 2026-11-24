#!/bin/bash
# Rebuild the 319-vertex graph from scratch and check it with three independently written exact programs.
# Needs: python3 (standard library only), gcc with OpenMP.
# Default run: about 45 to 60 minutes on 8 cores (three whole-graph searches for an independent 23-set, 9 to 20 minutes
# each). Everything here is a direct exact check of the finished graph; nothing rests on the theorem alone.
#   bash reproduce.sh quick    (skips the three whole-graph independent-set searches; about 2 minutes)
set -e
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
echo "== Rebuild from scratch (Q313 = quartic residues mod 313, triangle T = {0, 1, 4})"
python3 build.py 313 4 rebuilt.txt
cmp rebuilt.txt R4_23_320.txt
echo "rebuilt graph is byte-identical to R4_23_320.txt"
(echo 319; cat R4_23_320.txt) > R4_23_320.adj
gcc -O3 -fopenmp -o fclq fclq.c
gcc -O3 -fopenmp -o fmis fmis.c
gcc -O3 -o chk chk.c
echo "== The rule's condition and the exact decomposition (fclq on each part)"
python3 decomp_check.py R4_23_320.txt 313 23 22
while IFS=$'\t' read f need why; do
  echo "-- $why: independent $need-set?"
  ./fclq "$f" "$need" i 8 | tee "$f.out" | grep RESULT
  grep -q "exists: no" "$f.out"
done < decomp_R4_23_320/jobs.txt
echo "== No K4: fclq and fmis (fmis prints the exact K4 count)"
./fclq R4_23_320.txt 4 c 8 | tee out_fclq_c4.txt | grep RESULT; grep -q "exists: no" out_fclq_c4.txt
./fmis R4_23_320.txt 3 8 | tee out_fmis_count.txt | grep K4_count; grep -q "K4_count=0" out_fmis_count.txt
echo "== Positive control: an independent 22-set exists (fclq)"
./fclq R4_23_320.txt 22 i 8 | tee out_fclq_i22.txt | grep RESULT; grep -q "exists: YES" out_fclq_i22.txt
if [ "$1" != "quick" ]; then
  echo "== Whole graph, method 1: fclq, no independent 23-set"
  ./fclq R4_23_320.txt 23 i 8 | tee out_fclq_i23.txt | grep RESULT; grep -q "exists: no" out_fclq_i23.txt
  echo "== Whole graph, method 2: fmis, no independent 23-set"
  ./fmis R4_23_320.txt 23 8 | tee out_fmis_i23.txt | grep RESULT; grep -q "exists: NO" out_fmis_i23.txt
  echo "== Whole graph, method 3: chk, one subproblem per lowest vertex, no independent 23-set"
  rm -rf out_chk_i23; bash run_chk.sh R4_23_320.adj 23 8 out_chk_i23
  grep -q "NONE 319 FOUND 0" out_chk_i23/SUMMARY.txt
fi
echo "== Rule lie detector (small and random cases)"
python3 rulecheck.py 300
echo "ALL CHECKS PASSED"
