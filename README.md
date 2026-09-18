# JSP-000674 / Erdős–Sárközy `g_k(n)`: verification package

Reproducible artifacts for the verification record of **JSP-000674**, which is
**Erdős Problem #817**: for `H(A) = { sum_{a in A} eps_a a : eps_a in {0,1} }`, let `g_k(n)`
be the least `N` such that some `n`-element `A ⊆ {1,...,N}` has `H(A)` free of nonconstant
`k`-term arithmetic progressions. Estimate `g_k(n)`; in particular, is `g_3(n) ≫ 3^n`?

This repository contains computational and verification artifacts only. It does not claim
an award or a new theorem; see `REPORT.md` for the full record and the status caveats of
the resolution.

## Main results recorded here

* `g_3(1..6) = 1, 3, 8, 22, 60, 168`, with witnesses `{1}`, `{1,3}`, `{5,7,8}`,
  `{7,19,21,22}`, `{19,52,57,59,60}`, `{107,145,159,162,164,168}`. The values for `n ≤ 4`
  reproduce Korsky (arXiv:2606.24139, Remark 4.6); `g_3(5) = 60` and `g_3(6) = 168` are
  exhaustive computations of this session (forum posts of 2026-09-17 report the same two
  values with different witnesses, which are also verified here).
* No `A ⊆ [167]` of size 6 and no `A ⊆ [313]` of size 7 is 2-fold subset-sum-distinct, so
  `g_3(6) = 168` exactly. The `n = 7` search is incomplete and does not improve on the
  proven bound `b_7 = 419`.
* `H(A)` is 3-AP-free **iff** `eps -> sum eps_i a_i` is injective on `{0,1,2}^n`
  (Korsky, Prop. 4.1; re-proved in `REPORT.md`), so
  `g_3(n) = min { max_i a_i : that map is injective }`, which makes the search a finite
  computation for each `n`.
* The minimum induced bandwidth (best ordering of `{0,1,2}^n` induced by a positive integer
  linear form) is `8, 22, 59` for `n = 3,4,5`, so at `n = 5` the abstract bandwidth bound 56
  is not attained by any linear form (Korsky's Remark 4.5, made concrete).
* `g_3(n)/3^n` is non-increasing (`A -> {1} ∪ 3A`), so the known ratios are
  `0.333, 0.333, 0.296, 0.272, 0.247, 0.230`.

## Contents

| file | purpose |
| --- | --- |
| `REPORT.md` | full verification record: identification, results, evidence chain, caveats |
| `g3.c` | exhaustive search for `g_3(n)` (bitset DFS over increasing `A ⊆ [N]`) |
| `verify_exact.py` | independent plain-Python exhaustive check of a lower bound `g_3(n) > N` |
| `ground_truth.py` | cheapest checks: enumerate `H(A)`, test 3-AP-freeness, count distinct `{0,1,2}`-sums |
| `induced.py` | induced bandwidth of the ordering of `{0,1,2}^n` by `eps -> sum eps_i a_i` |
| `search2.py` | slower reference implementation of the same search (independent code path) |
| `families.py` | structured families (digit / graph constructions) tried against the trivial bound |
| `shift_unit.c` | unit test of the bitset shift used by `g3.c` |

## Reproduce

```sh
gcc -O2 -o g3 g3.c
./g3 3 1 12        # -> g_3(3) = 8   witness {5,7,8}
./g3 4 1 25        # -> g_3(4) = 22  witness {7,19,21,22}
./g3 5 56 70       # -> g_3(5) = 60  witness {19,52,57,59,60}
python3 verify_exact.py 4 21 22
python3 ground_truth.py
python3 induced.py
```

Validation of `g3.c`: it reproduces the published values `g_3(1..4) = 1,3,8,22`; every
witness it reports is re-verified independently by `verify_exact.py` and `ground_truth.py`,
which enumerate all `3^n` coefficient sums and all `2^n` subset sums respectively.
`shift_unit.c` checks the bitset shift against a naive reference on random sets for shift
amounts 1..600.

## Citations

* P. Erdős, *Problems and results in combinatorial analysis and combinatorial number
  theory*, Graph theory, combinatorics, and applications, Vol. 1 (Kalamazoo 1988), Wiley
  (1991), 397–406.
* P. Erdős, A. Sárközy, *Arithmetic progressions in subset sums*, Discrete Math. **102**
  (1992) 249–264, doi:10.1016/0012-365X(92)90119-Z.
* S. Korsky, *Arithmetic progression-free subset-sum sets*, arXiv:2606.24139 (2026).
* S. Costa, *A negative answer to the Erdős–Sárközy question*, arXiv:2609.06303 (2026),
  doi:10.5281/zenodo.22638810.
* L. J. Billera, S. A. Blanco, *Bandwidth of the product of paths of the same length*,
  Discrete Appl. Math. **161** (2013) 3080–3086, arXiv:1209.3201.
* T. F. Bloom, *Erdős Problem #817*, https://www.erdosproblems.com/817.

`REPORT.md` is the authoritative document; this README is a summary.

## License

MIT (`LICENSE`). The cited papers and the Erdős Problems database are not included.
