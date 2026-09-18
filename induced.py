"""Induced bandwidth: for A=(a_1..a_n), order the 3^n grid points eps in {0,1,2}^n by
Phi(eps)=sum eps_i a_i; induced_bw(A) = max over grid edges |rank difference|.
Then g_3(n) = min over A of induced_bw(A)  (Korsky's Thm 1.1 proof structure)."""
import itertools, sys
def phi_order(A):
    pts=[(sum(e*a for e,a in zip(eps,A)), eps) for eps in itertools.product((0,1,2),repeat=len(A))]
    pts.sort()
    rank={eps:i for i,(v,eps) in enumerate(pts)}
    mx=0; arg=None
    for eps in rank:
        for c in range(len(A)):
            if eps[c]<2:
                f=list(eps); f[c]+=1
                d=abs(rank[tuple(f)]-rank[eps])
                if d>mx: mx=d; arg=(eps,tuple(f))
    return mx,arg
def induced_bw(A):
    return phi_order(A)[0]
if __name__=='__main__':
    for A in ([1,3,9],[5,7,8],[1,3,9,27],[7,19,21,22],[19,52,57,59,60]):
        print(A, "induced bw =", induced_bw(A))
