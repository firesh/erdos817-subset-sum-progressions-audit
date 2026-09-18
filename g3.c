/* g_3(n) = least N such that some n-element A subset of [N] has H(A) free of
   nonconstant 3-term arithmetic progressions, equivalently (Korsky 2026, Prop. 4.1)
   eps -> sum_{i<=n} eps_i a_i injective on {0,1,2}^n.
   Exhaustive DFS over increasing A with an incremental bitset ternary sum-set.
   Necessary and sufficient one-step condition: with S = ternary sum-set of the
   elements chosen so far and a the next element, S, S+a, S+2a must be pairwise
   disjoint, i.e. S & (S+a) = 0 and S & (S+2a) = 0. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 16
#define WORDS 96                 /* 6144 bits */

static int n, N;
static unsigned long long S[WORDS];
static int sol[MAXN];
static int found;
static long long nodes;

static void shift_into(unsigned long long *dst, const unsigned long long *src, int sh) {
    int w = sh >> 6, b = sh & 63;
    memset(dst, 0, sizeof(unsigned long long) * WORDS);
    for (int i = w; i < WORDS; i++) {
        unsigned long long v = src[i - w] << b;
        if (b && i - w - 1 >= 0) v |= src[i - w - 1] >> (64 - b);
        dst[i] = v;
    }
}
static int disjoint(const unsigned long long *x, const unsigned long long *y) {
    for (int i = 0; i < WORDS; i++) if (x[i] & y[i]) return 0;
    return 1;
}

static void dfs(int start, int k) {
    if (found) return;
    if (k == n) { found = 1; return; }
    int rem = n - k;
    for (int a = start; a <= N; a++) {
        if (a + rem - 1 > N) break;
        nodes++;
        unsigned long long t1[WORDS], t2[WORDS], u[WORDS], old[WORDS];
        shift_into(t1, S, a);
        if (!disjoint(S, t1)) continue;
        shift_into(t2, S, 2 * a);
        if (!disjoint(S, t2)) continue;
        for (int i = 0; i < WORDS; i++) u[i] = S[i] | t1[i] | t2[i];
        memcpy(old, S, sizeof(S));
        memcpy(S, u, sizeof(S));
        sol[k] = a;
        dfs(a + 1, k + 1);
        if (found) return;
        memcpy(S, old, sizeof(S));
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]);
    int lo = (argc > 2) ? atoi(argv[2]) : 1;
    int hi = (argc > 3) ? atoi(argv[3]) : 100000;
    for (N = lo; N <= hi; N++) {
        memset(S, 0, sizeof(S)); S[0] = 1ULL;
        found = 0; nodes = 0;
        clock_t t0 = clock();
        dfs(1, 0);
        double el = (double)(clock() - t0) / CLOCKS_PER_SEC;
        if (found) {
            printf("g_3(%d) = %d  witness {", n, N);
            for (int i = 0; i < n; i++) printf("%d%s", sol[i], i + 1 < n ? "," : "");
            printf("}  nodes=%lld time=%.2fs\n", nodes, el);
            return 0;
        }
        printf("N=%d: none (nodes=%lld, %.2fs)\n", N, nodes, el); fflush(stdout);
    }
    return 1;
}
