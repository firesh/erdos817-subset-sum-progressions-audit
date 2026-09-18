"""Exact search for g_3(n) via Proposition 4.1 (Korsky 2026):
H(A) 3-AP-free iff eps -> sum eps_i a_i is injective on {0,1,2}^n.
g_3(n) = min N such that an n-subset A of [N] has all 3^n sums distinct.

Incremental: maintain S_B = { sum eps_i b_i : eps in {0,1,2}^{|B|} } for the current subset B.
Adding a: new sums are S_B + {0,a,2a}; injectivity requires the three translates disjoint.
"""
import sys, time, itertools
from math import comb

def search(n, N, find_all=False, limit=None):
    A=[]; S={0}; sols=[]
    def dfs(start):
        if sols and not find_all: return
        if len(A)==n:
            sols.append(tuple(A)); return
        rem=n-len(A)
        for a in range(start, N+1):
            if a+rem-1>N: break
            T1={x+a for x in S}
            if len(T1)!=len(S): continue
            T1s=T1|S
            T2={x+2*a for x in S}
            if len(T1s|T2)!=len(S)+2*len(S): continue
            A.append(a); old=S.copy(); S.update(T1); S.update(T2)
            dfs(a+1)
            A.pop(); S.clear(); S.update(old)
            if sols and not find_all: return
    dfs(1)
    return sols

def g3(n, lo=None, hi=None, verbose=True):
    if lo is None:
        # lower bound: bandwidth formula (paper Thm 1.1 / Billera-Blanco)
        T=lambda m: sum(comb(m,k)*comb(k,m-k) for k in range(m+1))
        lo=(T(n)-1)//2+sum(T(j) for j in range(n))
    N=lo
    while hi is None or N<=hi:
        t0=time.time(); s=search(n,N)
        if verbose: print(f"  N={N}: {'FOUND '+str(s[0]) if s else 'none'} ({time.time()-t0:.2f}s)", flush=True)
        if s: return N, s[0]
        N+=1
    return None,None

if __name__=='__main__':
    n=int(sys.argv[1]); hi=int(sys.argv[2]) if len(sys.argv)>2 else None
    t0=time.time(); N,A=g3(n,hi=hi)
    print(f"n={n}: g_3 = {N}, witness {A}, total {time.time()-t0:.1f}s")
