/* fmis.c (Fable review, 24 Nov 2026): own exact checker, written fresh for this review.
   usage: fmis FILE T [threads]
   FILE = n rows of 0/1. Reports: symmetric, edges, number of K4 (exact count by bitset
   intersection), and whether an independent set of size T exists (decision, exact).
   Method: independent set in G = clique in complement C. Branch and bound with greedy
   sequential colouring of C restricted to the candidate set (Tomita-Seki style bound).
   Top level is split by vertex (vertex i with candidates = later non-neighbours in a
   fixed order), run with OpenMP. A witness is printed and re-verified if found. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <omp.h>
#define MAXN 512
#define W (MAXN/64)
typedef uint64_t bs[W];
static int n, T, nw;
static bs adj[MAXN], cad[MAXN];
static volatile int found = 0;
static int witness[MAXN];
static char M[MAXN][MAXN];
static char line[4096];
static inline int pc(const uint64_t *a){int c=0;for(int i=0;i<nw;i++)c+=__builtin_popcountll(a[i]);return c;}
typedef struct { unsigned long long nodes; int cur[MAXN]; } ctx;
static void expand(ctx *c, uint64_t *P, int size){
    if(found) return;
    c->nodes++;
    int order[MAXN], col[MAXN], m=0;
    bs U; memcpy(U,P,sizeof(bs));
    int k=0;
    while(1){
        int any=0; for(int i=0;i<nw;i++) if(U[i]){any=1;break;}
        if(!any) break;
        k++;
        bs Q; memcpy(Q,U,sizeof(bs));
        while(1){
            int v=-1; for(int i=0;i<nw;i++) if(Q[i]){v=i*64+__builtin_ctzll(Q[i]);break;}
            if(v<0) break;
            Q[v>>6] &= ~(1ULL<<(v%64)); U[v>>6] &= ~(1ULL<<(v%64));
            for(int i=0;i<nw;i++) Q[i] &= ~cad[v][i];
            order[m]=v; col[m]=k; m++;
        }
    }
    for(int j=m-1;j>=0;j--){
        if(size+col[j]<T) return;
        int v=order[j];
        c->cur[size]=v;
        if(size+1>=T){
            #pragma omp critical
            { if(!found){found=1; memcpy(witness,c->cur,sizeof(int)*T);} }
            return;
        }
        bs NP; int any=0;
        for(int i=0;i<nw;i++){NP[i]=P[i] & cad[v][i]; if(NP[i]) any=1;}
        if(any) expand(c,NP,size+1);
        if(found) return;
        P[v>>6] &= ~(1ULL<<(v%64));
    }
}
int main(int argc,char**argv){
    if(argc<3){fprintf(stderr,"usage\n");return 2;}
    FILE*f=fopen(argv[1],"r"); if(!f){perror("open");return 2;}
    T=atoi(argv[2]); int th=argc>3?atoi(argv[3]):8; omp_set_num_threads(th);
    n=0; int L0=-1;
    while(fgets(line,sizeof line,f)){
        int L=strlen(line);
        while(L>0){ char ch=line[L-1]; if(ch=='\n'||ch=='\r'||ch==' ') L--; else break; }
        if(L==0) continue;
        if(L>MAXN||n>=MAXN){fprintf(stderr,"too big\n");return 2;}
        if(L0<0)L0=L;
        if(L!=L0){fprintf(stderr,"ragged row %d\n",n);return 2;}
        for(int j=0;j<L;j++){ if(line[j]!='0'){ if(line[j]!='1'){fprintf(stderr,"bad char row %d\n",n);return 2;} } M[n][j]=line[j]-'0'; }
        n++;
    }
    fclose(f);
    if(L0!=n){fprintf(stderr,"not square: %d rows, %d cols\n",n,L0);return 2;}
    nw=(n+63)/64; long edges=0; int sym=1,diag=1;
    for(int i=0;i<n;i++){ if(M[i][i])diag=0; for(int j=0;j<n;j++){ if(M[i][j]!=M[j][i])sym=0; if(M[i][j]) if(i<j) edges++; } }
    printf("file=%s n=%d edges=%ld symmetric=%d zero_diag=%d T=%d threads=%d\n",argv[1],n,edges,sym,diag,T,th);
    if(sym==0||diag==0){printf("RESULT: INVALID INPUT\n");return 3;}
    for(int i=0;i<n;i++)for(int j=0;j<n;j++){ if(i==j)continue; if(M[i][j]) adj[i][j>>6]|=1ULL<<(j%64); else cad[i][j>>6]|=1ULL<<(j%64); }
    /* K4 and triangle count: for each edge i<j, common neighbours k>j; then common neighbours l>k of i,j,k */
    unsigned long long k4=0,tri=0;
    #pragma omp parallel for schedule(dynamic) reduction(+:k4,tri)
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(M[i][j]){
        bs Cm; for(int w=0;w<nw;w++) Cm[w]=adj[i][w] & adj[j][w];
        for(int w=0;w<nw;w++){ uint64_t x=Cm[w]; while(x){ int k=w*64+__builtin_ctzll(x); x &= x-1; if(k<=j) continue; tri++;
            for(int w2=0;w2<nw;w2++){ uint64_t y=Cm[w2] & adj[k][w2]; while(y){ int l=w2*64+__builtin_ctzll(y); y &= y-1; if(l>k) k4++; } } } }
    }
    printf("triangles=%llu K4_count=%llu\n",tri,k4);
    fflush(stdout);
    double t0=omp_get_wtime(); unsigned long long tot=0;
    #pragma omp parallel
    { ctx c; c.nodes=0;
      #pragma omp for schedule(dynamic,1) nowait
      for(int i=0;i<n;i++){
        if(found) continue;
        bs P; memset(P,0,sizeof P);
        for(int j=i+1;j<n;j++) if(!M[i][j]) P[j>>6]|=1ULL<<(j%64);
        c.cur[0]=i;
        if(T<=1){
            #pragma omp critical
            { if(!found){found=1;witness[0]=i;} }
            continue; }
        if(pc(P)+1<T) continue;
        expand(&c,P,1);
      }
      #pragma omp atomic
      tot+=c.nodes;
    }
    printf("nodes=%llu wall=%.1fs\n",tot,omp_get_wtime()-t0);
    if(found){
        int ok=1; for(int a=0;a<T;a++)for(int b=a+1;b<T;b++){ if(witness[a]==witness[b]) ok=0; if(M[witness[a]][witness[b]]) ok=0; }
        printf("RESULT: independent set of size %d exists: YES (witness verified=%d):",T,ok);
        for(int a=0;a<T;a++)printf(" %d",witness[a]);
        printf("\n");
    } else printf("RESULT: independent set of size %d exists: NO\n",T);
    return 0;
}
