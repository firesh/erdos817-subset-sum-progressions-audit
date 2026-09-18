# JSP-000674 — live random draw and verification record (2026-09-18)

Draw: `secrets.randbits(64)` = 12559660459902590178, one uniform choice over the 1022 JSP
records (`random.Random(seed).choice`). Result: **JSP-000674**. The pre-existing
`work/problem-triage` queue was deliberately not reused.

## 1. Identification of the original problem

JSP-000674 has empty source rows. Its one-line description is a paraphrase of
**Erdős Problem #817** (https://www.erdosproblems.com/817), whose source is

* P. Erdős, *Problems and results in combinatorial analysis and combinatorial number
  theory*, in: Graph theory, combinatorics, and applications, Vol. 1 (Kalamazoo, MI, 1988),
  Wiley (1991), 397–406 (Zbl 840.05094, MR 93g:05136), and whose lower-bound remark is
  standardly attributed to P. Erdős and A. Sárközy, *Arithmetic progressions in subset
  sums*, Discrete Math. 102 (1992) 249–264, doi:10.1016/0012-365X(92)90119-Z.

Statement (verbatim from the database):

> Let $k\geq 3$ and define $g_k(n)$ to be the minimal $N$ such that $\{1,\ldots,N\}$
> contains some $A$ of size $|A|=n$ such that
> $\langle A\rangle=\{\sum_{a\in A}\epsilon_a a:\epsilon_a\in\{0,1\}\}$ contains no
> non-trivial $k$-term arithmetic progression. Estimate $g_k(n)$. In particular, is it
> true that $g_3(n)\gg 3^n$?

"How large a containing interval is necessary" is therefore exactly "how small can
$\max A$ be". Identification evidence: the record sits in the 1991 block of the catalog
(entries 666–675 all read "no later than 1991"), its area is recorded as additive
combinatorics, and its neighbours JSP-000673 and JSP-000675 are Erdős problems of the same
vintage. The database status for #817 is **OPEN** and its Formal Conjectures formalisation
(only the "in particular" part) is tagged `research open` and ends in `sorry`.

**Structural characterisation** (Korsky, arXiv:2606.24139, Prop. 4.1, independently
re-verified here): for $A\subset\mathbb{Z}_{>0}$, $H(A)$ is free of non-constant 3-term
arithmetic progressions **iff** $\varepsilon\mapsto\sum_i\varepsilon_i a_i$ is injective on
$\{0,1,2\}^n$; the two directions are proved from `u+w = 2v` and from the non-zero
difference vector $\delta\in\{-2,\dots,2\}^n$. Equivalently $A$ is 2-fold
subset-sum-distinct (Bae 2002). Hence

$$g_3(n)=\min\Big\{\max_i a_i:\ (a_i)\in\mathbb{Z}_{>0}^n,\
\varepsilon\mapsto\textstyle\sum_i\varepsilon_i a_i\ \text{injective on }\{0,1,2\}^n\Big\},$$

which makes $g_3(n)$ a finite computation for each $n$.

## 2. Independent computations

`g3.c` searches increasing $A\subset[N]$ by DFS with an incremental bitset ternary sum-set,
accepting $a$ exactly when $S\cap(S+a)=\varnothing$ and $S\cap(S+2a)=\varnothing$ (sufficient
and necessary for the extended map to stay injective). Validation: it reproduces the
published values $g_3(1..4)=1,3,8,22$; every witness was re-checked by `ground_truth.py`
(all $3^n$ coefficient sums distinct **and** all $2^n$ subset sums 3-AP-free) and by an
independent Python enumerator `verify_exact.py`.

| $n$ | $g_3(n)$ | witness | $b_n$ (bandwidth bound) | $3^{n-1}$ | search |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | {1} | 1 | 1 | complete |
| 2 | 3 | {1,3} | 3 | 3 | complete |
| 3 | 8 | {5,7,8} | 8 | 9 | complete |
| 4 | 22 | {7,19,21,22} | 21 | 27 | complete |
| 5 | **60** | {19,52,57,59,60} | 56 | 81 | complete |
| 6 | 168 (literature), $\ge163$ here | {107,145,159,162,166,168} | 152 | 243 | incomplete: $N\le162$ excluded |
| 7 | — | — | 419 | 729 | incomplete: $N\le313$ excluded |

$b_n=\frac{T_n-1}{2}+\sum_{j<n}T_j$, $T_j=[x^j](1+x+x^2)^j$, is the exact bandwidth of
$\{0,1,2\}^n$ (Billera–Blanco, DAM 161 (2013) 3080–3086, arXiv:1209.3201 Thm. 2.3 with
$P_2^n$), which is Korsky's Thm. 1.1. Checked numerically: $b_n=1,3,8,21,56,152,419,1169$
matches Billera–Blanco Table 1, column $n=2$.

Additional verified observations.

* $g_3(n)/3^n$ is non-increasing, because $A\mapsto\{1\}\cup 3A$ is admissible when $A$ is
  (a relation $c_0+\sum_i c_i 3a_i=0$ forces $3\mid c_0$, so $c_0=0$), hence
  $g_3(n+1)\le 3g_3(n)$. Ratios: $0.333,0.333,0.296,0.272,0.247,0.230$.
* The extremal sets for $n\le5$ are exactly the "offsets from the maximum" sets
  $\{G_n-G_k:0\le k<n\}$ with $(G_n)=(0,1,3,8,22,60)$; the pattern fails at $n=6$:
  $\{108,146,160,165,167,168\}$ is **not** admissible, checked directly.
* Extremality of the powers of three is *not* about $\max$: for $n=4$ the admissible set
  minimising $\sum_i a_i^2$ is $\{1,3,9,27\}$ (value 820, giving ternary sums
  $0,\dots,80$ exactly), while the minimiser of $\max$ is $\{7,19,21,22\}$. This is the
  variance remark of the forum thread, re-verified here.
* Minimum *induced* bandwidth (the bandwidth of the ordering of $\{0,1,2\}^n$ by $\Phi_A$,
  minimised over admissible $A$) is $8,22,59$ for $n=3,4,5$; at $n=5$ it is strictly below
  $g_3(5)=60$, so the abstract grid bandwidth $b_n$ is not attained by any linear form
  there. This is Korsky's Remark 4.5 "bandwidth barrier" in concrete form.

## 3. The asked question has been answered, negatively

**Claim.** $g_3(n)\gg 3^n$ is false; indeed $g_3(n)=o(3^n)$.

Chain of evidence, all checked here except where marked:

1. **Korsky, arXiv:2606.24139** (23 Jun 2026): characterisation (Prop. 4.1), finite bound
   $g_3(n)\ge b_n$ (Thm. 1.1, via the exact Billera–Blanco bandwidth of the ternary grid),
   adaptive lower bound for $k\ge4$ (Thm. 1.2), digit construction (Thm. 1.3). Read and
   verified against the primary sources; a separate verification report is in
   `../problem-triage/refs/`. The paper's own framing ("remains open") is out of date.
2. **OpenAI construction** (exposition https://www.erdosproblems.com/static/1-proof.pdf,
   from the machine-checked disproof of Erdős #1): gives integers $n,R,D,E$ and coefficients
   $a_0(t),\dots,a_n(t)$ with $kD<R^n$, $a_i(t)/t^n\to D>0$, $a_i(t)>0$ for large $t$, and
   $x\mapsto\sum_i a_i(t)x_i$ injective on $\{0,\dots,Q-1\}^{n+1}$ whenever
   $Q\le(t-E)R$. Traced in the exposition itself through Lemma 4.1 (separation
   $\|L_B(z)\|_\infty\ge R$), Lemma 5.1 ($\|E(z)\|_\infty\le E_B\|L_B(z)\|_\infty$),
   Proposition 5.2, and equations (16), (21)–(25); each step is elementary and correct given
   $kD<R^n$.
3. **Costa, arXiv:2609.06303** (5 Sep 2026, V2 Zenodo 10.5281/zenodo.22638810): base-three
   expansion. With $A_\ell=\{3^j a_i(t_\ell):0\le i\le n,\ 0\le j<\ell\}$,
   $t_\ell=E+\lceil 3^\ell/R\rceil$, a collision of $\{0,1,2\}$-coefficient vectors yields
   equal $x_i=\sum_j\delta_{i,j}3^j\in[0,3^\ell-1]$, box-injectivity forces equal $x_i$, and
   base-3 uniqueness forces equal digits. Then
   $\max A_\ell\le 3^{\ell-1}\max_i a_i(t_\ell)=(D/(3R^n)+o(1))3^{(n+1)\ell}<\varepsilon
   3^{(n+1)\ell}$, so $g_3(d\ell)\le\varepsilon 3^{d\ell}$ with $d=n+1$.
4. **From liminf to lim**: combined with the monotonicity in §2, $\liminf=0$ upgrades to
   $\lim_n g_3(n)/3^n=0$, i.e. $g_3(n)=o(3^n)$ for all $n$ (this upgrade is in the
   thread of 17 Sep 2026, not in the preprint).
5. **Sharper quantitative form**: a forum comment of 17 Sep 2026 (Korsky, adapting a
   construction of B. Alexeev) gives $g_3(n)\ll 3^n/n^{1/3}$, with
   $g_3(n)\le((3/4)^{1/3}+o(1))\,3^n/n^{1/3}$.
6. **Formal verification artifact — reproduced here**: Zenodo record 22638810 (V2,
   7 Sep 2026) ships `erdos817_negative_lean.zip`, a 3185-line single-file Lean 4
   certificate (`import Mathlib`, toolchain `leanprover/lean4:v4.34.0-rc1`, no
   `sorry`/`admit`/`axiom`, ending in `#print axioms`). It was built in this session on an
   independent machine against the pinned Mathlib revision: `Build completed successfully
   (8708 jobs)`, no errors, and
   `'ErdosSarkozy817.not_erdos_817' depends on axioms: [propext, Classical.choice,
   Quot.sound]` — i.e. the negation of `3^n = O(g_3(n))` is kernel-checked for the Formal
   Conjectures definition of `g`. Details, commands and the raw transcript are in `LEAN.md`
   and `lean-build.log`. This is third-party work that is being reproduced, not claimed.

**Status caveats.** The database still displays #817 as OPEN, lists Costa's entry under
"proof claims" as a **partial** proof, and states that appearing there is no guarantee of
correctness. The Lean certificate is distributed as a Zenodo archive rather than as a
public repository with a branch and a pinned commit, so it does not meet the awards
repository's pinning convention even though it now compiles here. Costa's preprint is unrefereed, 13 days old, and its one non-elementary input
is an AI-generated construction. The classification used here is therefore **verified
argument, unrefereed resolution**: enough for a maintainer-review record update, not enough
for an award claim.

Still open after all of this: the size of $g_3(n)$ between $c\,3^n/\sqrt n$ and
$O(3^n/n^{1/3})$ (exact constants, the true polynomial exponent), the exact value
$g_3(7)$ and beyond, and the whole $k\ge4$ range where $g_k(n)^{1/n}$ is only known to lie
between $(k-1)/(k-2)$ and $\min_{p\ge3}p^{2/(\min\{p,k\}-1)}$.

## 4. Artifacts in this directory

| file | content |
| --- | --- |
| `g3.c` | exhaustive search for $g_3(n)$ (bitset DFS, validated against the literature) |
| `verify_exact.py` | independent plain-Python exhaustive lower-bound check |
| `ground_truth.py` | direct $H(A)$ 3-AP check and ternary-injectivity count |
| `induced.py`, `induced_min.py` | induced bandwidth of the ordering by $\Phi_A$ |
| `search2.py`, `families.py`, `heuristic.py`, `bw*.py`, `shift_unit.c`, `dbg*.c` | audit trail of the derivation and of the bugs found on the way |
| `README.md` | one-command reproduction of every number above |
| `LEAN.md` | record of the Lean certificate retrieval and build attempt |
| `pkg/` | the subset published as a public GitHub repository |

No Lean proof was produced locally; the certificate is third-party and is only being
reproduced, not claimed.
