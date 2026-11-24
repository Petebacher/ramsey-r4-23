# R(4,23) ≥ 320

This repository gives a graph on 319 vertices that contains no clique of 4 vertices and no independent set of 23 vertices. It shows that the Ramsey number R(4,23) is at least 320. Both properties are checked directly on the finished graph by three independently written exact programs.

The graph comes from a small rule, called Theorem TB here, which adds 6 vertices to a graph with no K4 instead of the 5 that the general published step adds, whenever a simple condition on one triangle holds. The rule is a conditional variant, for k = 4, of a construction of Xu, Shao and Radziszowski (2011); see "Credit" below.

## Result

| Bound | Graph file | Vertices | Previous public value | Gain |
|---|---|---|---|---|
| R(4,23) ≥ 320 | `R4_23_320.txt` | 319 | no source prints a value; 319 is what published rules give from known graphs | +1 |

**Honest size of the gain.** No source we could find prints any lower bound for R(4,23). The value 319 follows from the Burr-Erdős-Faudree-Schelp step R(k,l) ≥ R(k,l−1) + 2k − 3 (the survey's item 2.3.e) applied to R(4,22) ≥ 314. The graph improves that by one. The input graph is old and well known; the new part is the rule and the check that its condition holds for this graph.

**Prior art, as of 24 November 2026.**
- The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, DS1 revision 18, April 2026): Table IIa's row for k = 4 ends at R(4,22) ≥ 314. Note 2.2(g) credits that bound first to an unpublished 2011 manuscript of Li Qiao, Su Wenlong, Luo Haipeng and Wu Kang, and then to Lindsay and Cain (arXiv 1510.06102, 2015), who also give R(4,25) ≥ 458. There is no entry for R(4,23).
- Increments in the survey give at most 319 here: the 2k − 3 step gives 314 + 5 = 319, and item 2.3.h (a common part with no K3) gives the same from the pair (22, 2). The 2k − 2 step is published for k ≥ 5 only (see Credit).
- We also found nothing for R(4,23) in: the Leaps in Bounds tracker (its R(4,l) rows end at l = 15); Didin's Zenodo record 10.5281/zenodo.22112873 (R(4,21) ≥ 260 only); Exoo and Tatarevic, "New lower bounds for 28 classical Ramsey numbers" (2015, R(4,l) up to l = 16); Google Research's `ramsey_number_bounds` folder (up to R(4,21)); AlphaEvolve (arXiv 2603.09172, scope r, s ≤ 22); Yu (arXiv 2608.18169, R(4,20)); Tatarevic (arXiv 2608.06531, k ≥ 5); Jang's gluing repository (its rule H gives at most 272 to 275 here, and D and DG do not apply to k = 4); and the Quantavane repository.
- We did not search zbMATH Open or MathSciNet for this cell, nor social media, MathOverflow or mailing lists, so this is the result of a limited search, not a claim about everything that is known.

## The input graph

H = Q313: vertices 0 to 312, with x and y adjacent when x − y is a nonzero fourth power modulo 313 (313 is prime and 1 mod 8, so −1 is a fourth power and the graph is undirected). It is 78-regular, has no K4, and its largest independent set has 21 vertices (Li-Su-Luo-Wu; Lindsay-Cain). That is what gives R(4,22) ≥ 314. We recheck all of this below; nothing is taken on trust.

## The construction

Take the triangle T = {h_1, h_2, h_3} = {0, 1, 4} of H. Add six vertices:
- g_1, g_2, g_3 (vertices 313, 314, 315), forming a triangle, with g_i joined to h_i;
- z_1, z_2, z_3 (vertices 316, 317, 318), pairwise **not** adjacent, with z_i joined to g_j for j ≠ i and to every neighbour of h_i in H (not to h_i itself).

`build.py` builds this from scratch with the Python standard library (`python3 build.py 313 4 out.txt`); the result is byte-identical to `R4_23_320.txt`.

## Theorem TB

**Theorem TB.** Let k ≥ 4, let H be a graph with no K_k and with no independent set of more than a vertices, and let T = {h_1, ..., h_{k−1}} be a clique of H. Write N(S) for the set of vertices adjacent to at least one vertex of S. If alpha(H − N(S)) ≤ a + 1 − |S| for every S ⊆ T with |S| ≥ 3, then the graph F built as above (a clique g_1 ... g_{k−1} with g_i ~ h_i, and pairwise non-adjacent z_1 ... z_{k−1} with z_i ~ g_j for j ≠ i and z_i ~ N_H(h_i)) has n(H) + 2k − 2 vertices, no K_k, and no independent set of a + 2 vertices. So R(k, a+2) ≥ n(H) + 2k − 1. If the condition fails for some S, F does contain an independent set of a + 2 vertices.

For k = 4 the condition is a single inequality: **alpha(H − N(T)) ≤ a − 2.** For Q313 with T = {0, 1, 4}, H − N(T) has 121 vertices and its largest independent set has exactly 19 = 21 − 2 vertices, so the condition holds (with nothing to spare). It holds for every triangle of Q313 (every triangle maps to one of 14 triangles {0, 1, c}, and a separate review checked all 14; that run is not shipped).

**Proof. Cliques.** Z = {z_i} is independent, so a clique contains at most one z. Each g_i has exactly one neighbour in H, namely h_i, so a clique meeting both G and H has exactly one vertex in each. A clique containing z_i is of one of three kinds: (a) z_i with vertices of G − g_i only, at most k − 1 vertices; (b) z_i, g_j and h_j, a triangle that nothing else extends (another g_l is not adjacent to h_j, and no vertex of H other than h_j is adjacent to g_j); (c) z_i with vertices of N_H(h_i) only, which together with h_i form a clique of H, so there are at most k − 2 of them. A clique with no z lies in G, in H, or is an edge g_i h_i. Since k ≥ 4, every clique has at most k − 1 vertices. (For k = 3, case (b) is a triangle, so the rule needs k ≥ 4.)

**Independent sets.** Let I be independent and let I_Z = I ∩ Z have s elements. Because G is a clique and g_l is adjacent to every z_i with i ≠ l, I contains a vertex of G only if s ≤ 1, and then that vertex is g_i with I_Z ⊆ {z_i}.
- s = 0: at most 1 + a vertices.
- s = 1, I_Z = {z_i}: I ∩ H avoids N(h_i). If g_i ∈ I then h_i ∉ I, so (I ∩ H) + h_i is independent in H, hence |I ∩ H| ≤ a − 1 and |I| ≤ a + 1. If g_i ∉ I then |I| ≤ 1 + a.
- s = 2, I_Z = {z_i, z_j}: I ∩ H avoids N(h_i) ∪ N(h_j), which contains h_i (T is a clique), so (I ∩ H) + h_i is independent, |I ∩ H| ≤ a − 1 and |I| ≤ a + 1.
- s ≥ 3, I_Z indexed by S: I ∩ H ⊆ H − N(S), so |I| ≤ s + alpha(H − N(S)) ≤ a + 1 by the condition.

So alpha(F) ≤ a + 1. Conversely, if alpha(H − N(S)) ≥ a + 2 − |S| for some S with |S| ≥ 3, then {z_i : h_i ∈ S} together with a largest independent set of H − N(S) is independent of size a + 2. ∎

**Credit: the parent construction.** The graph F is the graph of **Theorem 3 of Xu Xiaodong, Shao Zehui and S. P. Radziszowski, "More constructive lower bounds on classical Ramsey numbers", SIAM J. Discrete Math. 25 (2011) 394-400**, in the special case H = M = K_{k−1}, t = 2, with every edge inside the twin block deleted. XSR use that special case with a split of K_{k−1} into K_2 and K_{k−3} to prove R(k, s+1) ≥ R(k, s) + 2k − 2 for k ≥ 5 (their Corollary 3), and they note that for k = 4 this special case of the partition does not satisfy the assumptions of their theorem. We read the paper in the author's copy (cs.rit.edu/~spr/PUBL/paper68.pdf) and did not check the theorem numbers against the journal print. TB splits the twin block into k − 1 single vertices (so the twins are pairwise non-adjacent). XSR's independence argument then no longer applies, and the condition alpha(H − N(S)) ≤ a + 1 − |S| is exactly what replaces it. TB is therefore not a special case of XSR's Theorem 3 (whose hypothesis fails for k = 4) but a one-step conditional variant of it. We found no published statement of TB or of its k = 4 condition, within the limited search described above.

**Why k = 4 only.** For k ≥ 5, XSR's Corollary 3 already gives the same +2k − 2 step without any condition, so TB adds nothing there. For k = 3 the construction always contains a triangle. For k = 4 the best general published step is +5 (2k − 3), and TB gives +6 whenever its condition holds.

**Applying it twice.** The 319-vertex graph again satisfies the k = 4 condition (with 22 in place of 21) on every triangle we tested, so a second step gives R(4,24) ≥ 326. That is not a new bound: Jang's rule H gives the same value (R(4,22) + 12), and the survey's item 2.3.h gives 327, because an 8-vertex (4,3)-graph and Q313 share an induced 5-cycle (8 + 313 + 5 + 1). It is not part of this release.

## Verification

Everything below was run on the files in this repository (sha256 values in `SHA256SUMS`). The graph file has 319 lines, each a string of 319 characters 0/1, with no spaces and no header. Its sha256 is `668bdf8a2cbc49f18e0a68e3402a1a7126d88e08aa51fde90d7f6ba45c80de77`. The same matrix with a first line "319" (the input format of `chk`) has sha256 `30163d5807456b2c34b256e92d1c6bbe2a38cb1ea91d1a14d9268baae368aee2`.

**Three whole-graph exact searches.** The three programs were written separately (fclq and fmis for two separate review passes, chk by another working session) and share no code. All three find no independent set of 23 vertices in the whole graph:

| Program | Method | Result on R4_23_320.txt | Log |
|---|---|---|---|
| `fclq.c` | branch and bound; at each node the candidate set is peeled into r − 1 greedy colour classes and only the rest is branched on | no K4; no independent 23-set (4,064,829,835 nodes, 535 s wall, 8 threads) | `logs/fclq_R4_23_320_indep23.log` |
| `fmis.c` | exact K4 count by bitset intersection; independent sets as cliques of the complement, Tomita-Seki colouring bound, top level split by vertex | K4 count 0 (58,614 triangles); no independent 23-set (5,660,971,838 nodes, 803.5 s wall, 8 threads); control: an independent 22-set exists | `logs/fmis_out_319_*.log` |
| `chk.c` with `run_chk.sh` | Tomita-style colour-bounded search, one subproblem per lowest vertex (319 subproblems cover every 23-set exactly once) | all 319 subproblems NONE (5,660,971,870 nodes, 18.6 min wall on 6 workers). Not in the shipped logs: no K4 (`./chk R4_23_320.adj c 4 0 319` prints NONE in under a second), and a control in which a copy with vertex 318 isolated was caught at once | `logs/chk_F313_i23/` |

**An exact decomposition**, independent of how the graph was built (`decomp_check.py`). It checks that vertices 0 to 312 form a circulant. Every independent set meets the six added vertices in one of 14 independent subsets X (the empty set and 13 others). The 7 subsets with |X| ≤ 1 are covered by alpha(H) ≤ 21. The other 7, together with alpha(H) ≤ 21 itself, give 8 independence questions on parts of H: alpha(H) ≤ 21 (via H − N[0], 234 vertices), the three (g_i, z_i) cases (234 vertices each), the three z-pairs (171 vertices each), and X = Z (H − N(T), 121 vertices, which is the rule's condition). All 8 pass in fclq (`logs/fclq_decomp_*.log`) and in fmis (`logs/fmis_out_313_*.log`).

**The rule itself** (`rulecheck.py`, standard library only). It builds F for every triangle of six small library graphs and for 4,500 random graphs with k = 4, 5 and 6 (about 15,700 pairs of a graph and a clique T in all), and compares the exact validity of F with the condition. There are 0 disagreements. A deliberately weakened condition (checking S = T only) is caught 177 times for k = 5 and 6, which shows the test can fail (`logs/rulecheck_1500.log`).

**Reproduce.** `bash reproduce.sh` checks the hashes, rebuilds the graph and compares it byte for byte, compiles the three checkers, runs the decomposition, the K4 checks and a positive control, the three whole-graph searches (about 45 to 60 minutes on 8 cores), and the rule test. `bash reproduce.sh quick` skips the three whole-graph searches (about 30 seconds; `logs/reproduce_quick_run.log`). It needs python3 and gcc with OpenMP.

## Not claimed here

The same rule may apply to the quartic-residue circulant on 457 vertices (Lindsay and Cain, alpha = 24), which would give a 463-vertex graph for R(4,26). The exact searches of that whole graph are not finished. We make no claim about R(4,26) in this release.

## Files

- `R4_23_320.txt`: the graph.
- `build.py`: builds the graph from scratch.
- `decomp_check.py`: the exact decomposition (writes the 8 subgraphs and the job list).
- `fclq.c`, `fmis.c`, `chk.c`, `run_chk.sh`: the three exact checkers.
- `rulecheck.py`, `graphs.json`: the rule test, with the small library graphs ((4,3;8)-graphs, Paley graphs of order 9, 13 and 17, K3).
- `reproduce.sh`: runs everything.
- `logs/`: the original outputs. The first lines of some logs show working file names (for example F_313_4.txt, which is R4_23_320.txt, and g313/X_316_317.txt, which is the part R_316_317.txt). In the two fmis whole-graph logs and in reproduce_quick_run.log a directory path was removed from one line; nothing else in them was changed.

## Licence and citation

Code (`build.py`, `decomp_check.py`, `rulecheck.py`, `fclq.c`, `fmis.c`, `chk.c`, `run_chk.sh`, `reproduce.sh`) is under the MIT License; the graph, `graphs.json` and this README are under CC BY 4.0 (see `LICENSE`). Please cite this repository (`CITATION.cff`) and Xu, Shao and Radziszowski (2011) for the parent construction.

This work was directed by Peter J. Chrisbacher. The search, construction, proof and checks were carried out with AI coding agents (Anthropic's Claude Code), working under fixed rules: every claim needs independently written exact checks and a check of published results before any announcement. A separate AI review re-derived the proof of Theorem TB, found the parent construction in Xu, Shao and Radziszowski (2011), and wrote two of the three checkers shipped here (fclq.c in an earlier review, fmis.c for this graph); chk.c was written by a different AI working session. The three programs share no code, but fmis and chk use the same textbook method (their node counts on the whole graph nearly coincide), so they are separate code, not separate algorithms; fclq is a different search.

## Glossary

- **Ramsey number R(k, l):** the smallest n such that every graph on n vertices has a clique of k vertices or an independent set of l vertices. A graph on n vertices with neither shows R(k, l) ≥ n + 1.
- **Clique, K_k:** a set of k vertices that are pairwise adjacent. **Independent set:** a set of pairwise non-adjacent vertices; alpha(H) is the size of the largest one.
- **N(S), N[x]:** the vertices adjacent to at least one vertex of S; N[x] is x together with its neighbours.
- **Circulant:** a graph on 0..p−1 where adjacency depends only on the difference of the two vertices mod p.
- **Twin block:** the added vertices z_i, each copying the neighbourhoods of a matched pair (g_i, h_i).
- **DS1:** Radziszowski's dynamic survey *Small Ramsey Numbers*, Electronic Journal of Combinatorics.
- **XSR:** Xu, Shao and Radziszowski, SIAM J. Discrete Math. 25 (2011) 394-400.
- **Positive control:** a run that must answer "yes", showing the checker can find what it looks for.
