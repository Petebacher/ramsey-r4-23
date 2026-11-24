#!/bin/bash
# run_chk.sh GRAPH.adj K P OUTDIR: run chk (independent-set mode) once per lowest vertex v = 0..n-1, P at a time.
# The union of the n subproblems covers every K-set exactly once. Resumable: a v with a result file is skipped.
# Writes OUTDIR/SUMMARY.txt with the counts of NONE and FOUND.
set -u
G=$1; K=$2; P=$3; OUT=$4
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
N=$(head -1 "$G")
date -u +"start %FT%TZ" >> "$OUT/LOG.txt"
sha256sum "$G" >> "$OUT/LOG.txt"
seq 0 $((N-1)) | while read v; do [ -s "$OUT/v$v.txt" ] || echo "$v"; done | \
  xargs -P "$P" -I{} sh -c "'$HERE/chk' '$G' i $K {} \$(({}+1)) > '$OUT/v{}.tmp' 2>&1; mv '$OUT/v{}.tmp' '$OUT/v{}.txt'"
done_n=$(ls "$OUT"/v*.txt | wc -l)
found=$(cat "$OUT"/v*.txt | grep -c FOUND)
none=$(cat "$OUT"/v*.txt | grep -c '^NONE')
{ date -u +"end %FT%TZ"; echo "graph $G mode i K $K n $N results $done_n NONE $none FOUND $found"; grep -h FOUND "$OUT"/v*.txt | head -3; } | tee "$OUT/SUMMARY.txt"
