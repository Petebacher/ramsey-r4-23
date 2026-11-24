"""c2_build.py p c out: build the C2 graph F from the quartic-residue circulant Q_p and the triangle T = {0, 1, c}.
Vertex order: 0..p-1 = Q_p; p..p+2 = g_1..g_3 (a triangle G = K3); p+3..p+5 = z_1..z_3.
Edges: Q_p; G; g_i ~ h_i (h = 0, 1, c); z_i ~ g_j (j != i); z_i ~ N_Q(h_i); z's pairwise non-adjacent.
Output: p+6 rows of 0/1 characters.
    python3 -I c2_build.py 313 4 F_313_4.txt
"""
import sys

p, c, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
S = {pow(x, 4, p) for x in range(1, p)}
n = p + 6
A = [[0] * n for _ in range(n)]


def e(x, y):
    A[x][y] = A[y][x] = 1


for x in range(p):
    for y in range(x + 1, p):
        if (y - x) % p in S:
            e(x, y)
T = [0, 1, c]
assert all((T[j] - T[i]) % p in S for i in range(3) for j in range(i + 1, 3)), "T is not a triangle"
g = [p, p + 1, p + 2]
z = [p + 3, p + 4, p + 5]
e(g[0], g[1]); e(g[0], g[2]); e(g[1], g[2])
for i in range(3):
    e(g[i], T[i])
    for j in range(3):
        if j != i:
            e(z[i], g[j])
    for w in range(p):
        if (w - T[i]) % p in S:
            e(z[i], w)
open(out, "w").write("\n".join("".join(map(str, r)) for r in A) + "\n")
print(f"wrote {out}: n = {n}, edges = {sum(map(sum, A)) // 2}")
