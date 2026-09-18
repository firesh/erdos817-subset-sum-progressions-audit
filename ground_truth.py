"""Ground-truth checks (no incremental tricks):
   (a) H(A) 3-AP-free  (explicit subset sums)
   (b) eps -> sum eps_i a_i injective on {0,1,2}^n
   Print both for candidate sets."""
import itertools
def H(A):
    S={0}
    for a in A: S |= {x+a for x in S}
    return S
def is_ap3_free(S):
    st=set(S); L=sorted(st)
    for i,x in enumerate(L):
        for y in L[i+1:]:
            z=2*y-x
            if z>L[-1]: break
            if z in st and z!=y: return False,(x,y,z)
    return True,None
def ternary_injective(A):
    vals=[sum(e*a for e,a in zip(eps,A)) for eps in itertools.product((0,1,2),repeat=len(A))]
    return len(set(vals))==3**len(A), len(set(vals))
for A in ([1,3],[5,7,8],[4,12,14,15],[7,19,21,22],[1,6,18,54,57],[19,52,57,59,60],[1,3,9,27]):
    S=H(A); ok,ap=is_ap3_free(S); ti,cnt=ternary_injective(A)
    print(f"A={A}: |H|={len(S)} 2^n={2**len(A)} H 3-AP-free={ok} (witness AP {ap}) | ternary distinct={ti} ({cnt}/3^{len(A)})")
