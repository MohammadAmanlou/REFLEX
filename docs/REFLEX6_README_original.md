# REFLEX-P / 6.0 technical research package

Prepared 22 November 2026 for Mohammad Amanlou.

## Contents
- `REFLEX6_Principal_Aware_Audits.pdf`: six-page technical working paper, with mathematical definitions, two-sided proof of the principal-aware Byzantine robustness frontier, an exact decoder, principal-disjoint-cycle certificate, structural monotonicity lemma, audit-design optimization, extensive direct prior-art comparisons, and a formal list of open research gaps.
- `REFLEX6_Principal_Aware_Audits.tex`: editable LaTeX source. Compile with `pdflatex` twice. No externally required image files.
- `reflex6_principal_robustness.py`: standalone Python 3.9+ numerical and exhaustive verification code, no third-party dependencies.
- `REFLEX6_README.md`: this file.

## Reproduce
`python reflex6_principal_robustness.py`

Expected checks: 120/120 random complete transcript enumerations; 2000/2000 owner-level attack trials; hub counterexample with edge distance 3 and owner-transversal 1; three independent owner-disjoint triangles with threshold 3; 9 Sybil delegates of one principal threshold 1; 12-edge optimization cost 21.

## Important scope limitations
The document is a working research note, NOT a paper ready for conference submission, a peer-reviewed scientific discovery, or proof of global historical novelty. It proves a structural identification result under a strictly defined authenticated owner map, known sensitivity labels, and at most k fully compromised principals. The endogenous strategic reporting/equilibrium mechanism, robust source semantics, scalable synthesis, and real-world experiments remain open problems. Group Feedback Vertex Set, signed graphs, and corruption-resistant coding are close mathematical predecessors. Prior work must be distinguished theorem-by-theorem before any novelty claim.

Nothing in this package has been sent to a professor, university, or conference.
