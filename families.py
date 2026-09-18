"""Try explicit structured families for 3-dissociated sets: can any beat 3^(n-1)?
Family 1: {p^i} u {p^i + p^j : (i,j) in E}  (Korsky's graph construction, p=3)
Family 2: {c*3^i} u {3^j} perturbations
Family 3: two-digit sets {3^i + d 3^j}
"""
import itertools, sys
def ternary_ok(A):
    A=sorted(A); S={0}
    for a in A:
        T1={x+a for x in S}; T2={x+2*a for x in S}
        if (S&T1) or (S&T2): return False
        S|=T1|T2
    return len(S)==3**len(A)

def graph_family(p, r, edges):
    """Korsky Thm 1.3 (k=3, q=2): A = {p^i} u {p^i + p^j : {i,j} in E}, 0<=i<r."""
    A=set()
    for i in range(r): A.add(p**i)
    for (i,j) in edges:
        if i!=j: A.add(p**i+p**j)
    return sorted(A)

if __name__=='__main__':
    # Try to build families of size n with small max, for p=3, r around 2n/q
    for n in (5,6,7,8,9,10):
        best=None
        r=max(2, (2*n)//2)   # q = min{p,k}-1 = 2 for k=3 -> edges give 2 per pair
        for r in range(2, n+2):
            # nearly regular graph on r vertices with (n-r) edges? we need n-r edges
            need=n-r
            if need<0: continue
            verts=list(range(r))
            allpairs=[(i,j) for i in verts for j in verts if i<j]
            if need> len(allpairs): continue
            for E in itertools.combinations(allpairs, need):
                A=graph_family(3,r,E)
                if len(A)!=n: continue
                if ternary_ok(A):
                    m=max(A)
                    if best is None or m<best[0]: best=(m,A,r,E)
            if best: break
        print(f"n={n}: best graph-family max = {best[0] if best else None}  3^(n-1)={3**(n-1)}")
        if best: print("   A =", best[1], " r=",best[2])
