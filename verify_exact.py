"""Independent (non-bitset) exact check of g_3(n) lower bound:
enumerate all n-subsets of [N], test whether all 3^n sums sum_i eps_i a_i (eps in {0,1,2})
are distinct, using plain Python sets. Also verifies the AP-freeness of H(A) directly."""
import itertools, sys
def ternary_ok(A):
    S={0}
    for a in A:
        T1={x+a for x in S}; T2={x+2*a for x in S}
        if (S&T1) or (S&T2): return False
        S|=T1|T2
    return len(S)==3**len(A)
def ap3_free(A):
    H={0}
    for a in A: H|={x+a for x in H}
    st=H; L=sorted(H)
    for i,x in enumerate(L):
        for y in L[i+1:]:
            z=2*y-x
            if z>L[-1]: break
            if z in st and z!=y: return False
    return True
n=int(sys.argv[1]); Ns=[int(x) for x in sys.argv[2:]]
for N in Ns:
    wit=None
    for A in itertools.combinations(range(1,N+1),n):
        if ternary_ok(A): wit=A; break
    # cross-check equivalence on the witness if found
    eq = "" if wit is None else f" [AP-free check: {ap3_free(wit)}]"
    print(f"n={n} N={N}: ternary-injective witness = {wit}{eq}")
