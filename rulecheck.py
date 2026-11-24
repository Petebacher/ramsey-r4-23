"""rulecheck.py: test the exact condition for candidate rule C2 (twin block over a matched K_{k-1}).

Construction F(H, T): G = K_{k-1} on g_1..g_{k-1}; H any graph with omega(H) < k and alpha(H) = a; T = (h_1..h_{k-1}) a
K_{k-1} in H; matching edges g_i h_i; extras z_1..z_{k-1}, z_i joined to G - g_i and to N_H(h_i); Z independent.
Target: F is a (k, a+2)-graph, n(F) = n(H) + 2(k-1) (2.3.h gives n(H) + 2k - 3 for these inputs).

Claimed exact condition (derived in RULECHECK.md), for k >= 4:
    F is valid  <=>  for every S subset of T with |S| >= 3:  alpha(H - N(S)) <= a + 1 - |S|
where N(S) is the union of the open neighbourhoods N_H(h), h in S (it contains S because T is a clique).
For k = 3 the construction always has a triangle (z_1, g_2, h_2).

Lie detector: the broken variant checks only S = T. It must disagree with the truth on some instances with k >= 5.
    python3 -I rulecheck.py [trials]   (standard library only; graphs.json holds the small library inputs)
"""
import itertools
import json
import os
import random
import sys

def popcount(x):
    return x.bit_count()


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def find_cliques(adj, n, size, limit, rng=None):
    """adj: list of bitmasks. Return up to `limit` cliques (tuples) of the given size."""
    out = []
    order = list(range(n))
    if rng:
        rng.shuffle(order)
    pos = {v: i for i, v in enumerate(order)}
    # relabel so that vertex order is random
    radj = [0] * n
    for v in range(n):
        m = 0
        for w in bits(adj[v]):
            m |= 1 << pos[w]
        radj[pos[v]] = m

    def rec(cur, cand):
        if len(out) >= limit:
            return
        need = size - len(cur)
        if need == 0:
            out.append(tuple(sorted(order[i] for i in cur)))
            return
        if popcount(cand) < need:
            return
        c = cand
        while c:
            if popcount(c) < need or len(out) >= limit:
                return
            b = c & -c
            v = b.bit_length() - 1
            c ^= b
            rec(cur + [v], c & radj[v])
    rec([], (1 << n) - 1)
    return out


def has_clique(adj, n, size):
    return len(find_cliques(adj, n, size, 1)) > 0


def omega(adj, n):
    k = 1
    while has_clique(adj, n, k + 1):
        k += 1
    return k if n else 0


def alpha(adj, n):
    full = (1 << n) - 1
    cadj = [(full ^ adj[v]) & ~(1 << v) for v in range(n)]
    return omega(cadj, n)


def to_adj(n, edges):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj



HERE = os.path.dirname(os.path.abspath(__file__))


def build(nH, aH, T):
    k1 = len(T)
    n = k1 + nH + k1
    adj = [0] * n

    def ae(x, y):
        adj[x] |= 1 << y
        adj[y] |= 1 << x
    for i, j in itertools.combinations(range(k1), 2):
        ae(i, j)
    for i in range(nH):
        for j in bits(aH[i] >> (i + 1) << (i + 1)):
            ae(k1 + i, k1 + j)
    for i, h in enumerate(T):
        ae(i, k1 + h)
        z = k1 + nH + i
        for j in range(k1):
            if j != i:
                ae(z, j)
        for w in bits(aH[h]):
            ae(z, k1 + w)
    return n, adj


def induced_alpha(aH, keep):
    idx = list(keep)
    pos = {v: i for i, v in enumerate(idx)}
    sub = [0] * len(idx)
    for v in idx:
        m = 0
        for w in bits(aH[v]):
            if w in pos:
                m |= 1 << pos[w]
        sub[pos[v]] = m
    return alpha(sub, len(idx)) if idx else 0


def predict(nH, aH, a, T, broken=False):
    sizes = [len(T)] if broken else range(3, len(T) + 1)
    for s in sizes:
        for S in itertools.combinations(T, s):
            cov = 0
            for h in S:
                cov |= aH[h]
            keep = [v for v in range(nH) if not cov >> v & 1]
            if induced_alpha(aH, keep) > a + 1 - s:
                return False
    return True


def truth(nH, aH, a, T, k):
    n, adj = build(nH, aH, T)
    return (not has_clique(adj, n, k)) and alpha(adj, n) <= a + 1


def run_instance(nH, aH, k, tag, stats, maxT=40):
    a = alpha(aH, nH)
    Ts = find_cliques(aH, nH, k - 1, maxT)
    for T in Ts:
        t = truth(nH, aH, a, T, k)
        p = predict(nH, aH, a, T)
        b = predict(nH, aH, a, T, broken=True)
        st = stats.setdefault(tag, [0, 0, 0, 0])
        st[0] += 1
        st[1] += t
        st[2] += (p != t)
        st[3] += (b != t)
    return len(Ts)


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    lib = json.load(open(os.path.join(HERE, "graphs.json")))
    stats = {}
    # library inputs, k = 4 (the solver-design cases)
    for nm in ["R43_8_0", "R43_8_1", "R43_8_2", "P9", "P13", "P17"]:
        g = lib[nm]
        aH = to_adj(g["n"], [tuple(e) for e in g["edges"]])
        stats_one = {}
        run_instance(g["n"], aH, 4, nm, stats_one, maxT=10 ** 6)
        stats.update(stats_one)
    # random inputs, k = 4, 5, 6: random graphs with omega < k
    rng = random.Random(1)
    for k in (4, 5, 6):
        done = 0
        while done < trials:
            nH = rng.randint(k + 2, 16)
            p = rng.uniform(0.3, 0.8)
            edges = [(i, j) for i in range(nH) for j in range(i + 1, nH) if rng.random() < p]
            aH = to_adj(nH, edges)
            if has_clique(aH, nH, k) or not has_clique(aH, nH, k - 1):
                continue
            run_instance(nH, aH, k, f"random k={k}", stats, maxT=6)
            done += 1
    print("| inputs | triangles/cliques T tested | F valid | condition wrong | broken variant wrong |")
    print("|---|---|---|---|---|")
    for tag, (tot, ok, bad, bbad) in stats.items():
        print(f"| {tag} | {tot} | {ok} | {bad} | {bbad} |")


if __name__ == "__main__":
    main()
