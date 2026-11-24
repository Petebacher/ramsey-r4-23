// chk graph.adj mode(c|i) K lo hi : exact decision, SECONDARY's own checker (W474 corextras), independent of TERTIARY code.
// Is there a K-clique (c) or independent K-set (i) whose LOWEST-index vertex v lies in [lo, hi)?  Subproblem for v:
// clique of size K-1 inside {u > v : u ~ v}. Union over v = 0..n-1 covers every set exactly once (split is exact).
// Search: Tomita MCQ-style branch and bound, greedy colouring of the candidate set, branch in reverse colour order,
// prune when |current| + colour <= K - 1 ... i.e. cannot reach K. Prints "FOUND v1 .. vK" (and exits 1) or
// "NONE lo hi nodes=<count>" (exit 0). n <= 1024.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define W 16
typedef struct { uint64_t w[W]; } B;
static int n, K, nw; static B adj[1024]; static int cur[128]; static long long nodes = 0;
static inline int pc(const B *a) { int c = 0; for (int i = 0; i < nw; i++) c += __builtin_popcountll(a->w[i]); return c; }
static inline int isempty(const B *a) { for (int i = 0; i < nw; i++) if (a->w[i]) return 0; return 1; }
static inline int first(const B *a) { for (int i = 0; i < nw; i++) if (a->w[i]) return i * 64 + __builtin_ctzll(a->w[i]); return -1; }
static inline void clr(B *a, int v) { a->w[v >> 6] &= ~(1ULL << (v & 63)); }
static inline void set(B *a, int v) { a->w[v >> 6] |= 1ULL << (v & 63); }
static int found = 0;
// expand: cur has d vertices, P = common candidates
static void expand(B P, int d) {
  nodes++;
  int m = pc(&P); if (d + m < K) return;
  // greedy colouring: order[] vertices, col[] colour numbers (non-decreasing)
  int order[1024], col[1024], cnt = 0, c = 0;
  B U = P;
  while (!isempty(&U)) {
    c++; B Q = U;
    while (!isempty(&Q)) {
      int v = first(&Q); clr(&Q, v); clr(&U, v);
      for (int j = 0; j < nw; j++) Q.w[j] &= ~adj[v].w[j];
      order[cnt] = v; col[cnt] = c; cnt++;
    }
  }
  for (int i = cnt - 1; i >= 0; i--) {
    if (d + col[i] < K) return;
    int v = order[i]; cur[d] = v;
    if (d + 1 == K) { found = 1; return; }
    B Q; for (int j = 0; j < nw; j++) Q.w[j] = P.w[j] & adj[v].w[j];
    expand(Q, d + 1); if (found) return;
    clr(&P, v);
  }
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 2; }
  FILE *f = fopen(argv[1], "r"); char mode = argv[2][0]; K = atoi(argv[3]); int lo = atoi(argv[4]), hi = atoi(argv[5]);
  if (fscanf(f, "%d", &n) != 1 || n > 1024) return 2; nw = (n + 63) / 64;
  char *row = malloc(n + 8);
  memset(adj, 0, sizeof adj);
  for (int i = 0; i < n; i++) {
    if (fscanf(f, "%s", row) != 1 || (int)strlen(row) != n) { fprintf(stderr, "bad row %d\n", i); return 2; }
    for (int j = 0; j < n; j++) if (j != i) { int e = row[j] == '1'; if (mode == 'i') e = !e; if (e) set(&adj[i], j); }
  }
  // symmetry check
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (((adj[i].w[j >> 6] >> (j & 63)) & 1) != ((adj[j].w[i >> 6] >> (i & 63)) & 1)) { fprintf(stderr, "not symmetric\n"); return 2; }
  if (hi > n) hi = n;
  for (int v = lo; v < hi; v++) {
    B P; memset(&P, 0, sizeof P);
    for (int u = v + 1; u < n; u++) if ((adj[v].w[u >> 6] >> (u & 63)) & 1) set(&P, u);
    cur[0] = v;
    if (K == 1) { found = 1; }
    else expand(P, 1);
    if (found) { printf("FOUND"); for (int i = 0; i < K; i++) printf(" %d", cur[i]); printf("\n"); return 1; }
  }
  printf("NONE %d %d nodes=%lld\n", lo, hi, nodes); return 0;
}
