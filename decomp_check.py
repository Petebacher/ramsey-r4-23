"""decomp_check.py FILE p u: exact check that the graph in FILE (rows of 0/1) has no independent set of size u,
when vertices 0..p-1 induce a circulant graph H (checked here) and the rest are few extra vertices.

Every independent set I splits as X = I n extras (an independent subset of the extras) plus I n H, which lies in
R(X) = H minus X's neighbours. So alpha(F) < u iff |X| + alpha(R(X)) < u for every independent X. H is a circulant,
so H is vertex-transitive and alpha(H) = 1 + alpha(H - N[0]); and alpha(R) <= alpha(H) for every R. Hence:
  - X with |X| + alpha(H) < u needs nothing more;
  - otherwise R(X) is written out and must have no independent set of size u - |X|.
The job list (subgraph file, required size) is written to decomp_<tag>/jobs.txt for two separate solvers.
Nothing here uses how F was built.
    python3 -I decomp_check.py FILE p u alphaH_claim
(alphaH_claim is the value to be proved by the job H - N[0]: no independent set of size alphaH_claim.)
"""
import itertools
import os
import sys

fn, p, u, aclaim = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rows = [l.strip() for l in open(fn) if l.strip()]
n = len(rows)
A = [[int(ch) for ch in r] for r in rows]
assert all(len(r) == n for r in A) and all(A[i][i] == 0 for i in range(n))
assert all(A[i][j] == A[j][i] for i in range(n) for j in range(n))
# H = first p vertices must be a circulant
conn = [A[0][d] for d in range(p)]
assert all(A[i][j] == conn[(j - i) % p] for i in range(p) for j in range(p)), "H is not a circulant"
ext = list(range(p, n))
tag = os.path.splitext(os.path.basename(fn))[0]
out = os.path.join(os.path.dirname(os.path.abspath(fn)), f"decomp_{tag}")
os.makedirs(out, exist_ok=True)


def write(vs, name):
    f = os.path.join(out, name)
    open(f, "w").write("\n".join("".join(str(A[v][w]) for w in vs) for v in vs) + "\n")
    return f


jobs = []
# alpha(H) <= aclaim - 1  <=>  no independent (aclaim - 1)-set in H - N[0]
nonnb0 = [v for v in range(p) if v != 0 and not A[0][v]]
jobs.append((write(nonnb0, "H_minus_N0.txt"), aclaim - 1, "alpha(H) < %d via H - N[0]" % aclaim))
alphaH = aclaim - 1
nX = 0
for r in range(1, len(ext) + 1):
    for X in itertools.combinations(ext, r):
        if any(A[x][y] for x, y in itertools.combinations(X, 2)):
            continue
        nX += 1
        if r + alphaH < u:
            continue
        R = [v for v in range(p) if not any(A[x][v] for x in X)]
        need = u - r
        jobs.append((write(R, "R_" + "_".join(map(str, X)) + ".txt"), need, f"X = {X}, |R| = {len(R)}"))
if 0 + alphaH >= u:
    raise SystemExit("alpha(H) claim too weak for X = empty")
with open(os.path.join(out, "jobs.txt"), "w") as f:
    for fj, need, why in jobs:
        f.write(f"{fj}\t{need}\t{why}\n")
print(f"n = {n}, extras {len(ext)}, independent X subsets {nX}, jobs {len(jobs)} -> {out}/jobs.txt")
for fj, need, why in jobs:
    print(f"  no independent {need}-set in {os.path.basename(fj)}  ({why})")
