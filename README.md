# REFLEX — Reproducible Research Prototypes

**Research owner:** Mohammad Amanlou  
**Repository:** https://github.com/MohammadAmanlou/REFLEX  
**Status:** Exploratory mathematical research; **not peer reviewed**, **not a conference submission**, and **not evidence of accepted historical novelty**.

This repository archives the REFLEX research prototypes built on 22 November 2026, progressing from equilibrium/evidence checks to topology-based audits and ultimately **principal-aware robustness** under collusion. The projects formalize *restricted* binary models and compare exact small-instance methods; they do **not** implement general equilibrium-robust, incentive-compatible multi-agent mechanisms or deployed LLM-agent evaluations.

## Research versions

| Version | Code | Research note | Experimental results |
|---|---|---|---|
| Early equilibrium and experimental-authority checks | [`src/reflex_equilibrium_authority_minibench.py`](src/reflex_equilibrium_authority_minibench.py) | Early numerical sanity checks | [`results/reflex_eq_stdout.txt`](results/reflex_eq_stdout.txt) |
| REFLEX-T — audit topology | [`src/reflex_audit_topology_prototype.py`](src/reflex_audit_topology_prototype.py) | [`papers/REFLEX_Audit_Topology_Research_Draft.pdf`](papers/REFLEX_Audit_Topology_Research_Draft.pdf) ([LaTeX](papers/REFLEX_Audit_Topology_Research_Draft.tex)) | [`results/reflex_t_stdout.txt`](results/reflex_t_stdout.txt) |
| REFLEX-P / 6.0 — principal-aware audits | [`src/reflex6_principal_robustness.py`](src/reflex6_principal_robustness.py) | [`papers/REFLEX6_Principal_Aware_Audits.pdf`](papers/REFLEX6_Principal_Aware_Audits.pdf) ([LaTeX](papers/REFLEX6_Principal_Aware_Audits.tex)) | [`results/reflex6_stdout.txt`](results/reflex6_stdout.txt) |

The PDFs and LaTeX sources explicitly link back to this repository. Current main research note: **REFLEX-P / 6.0**.

## Quickstart

Requires Python **3.10+** (CI uses Python 3.11). REFLEX-T and REFLEX-P rely only on the Python standard library. The early numerical benchmark requires NumPy and SciPy.

```bash
python -m pip install -r requirements.txt
python src/reflex_equilibrium_authority_minibench.py
python src/reflex_audit_topology_prototype.py
python src/reflex6_principal_robustness.py
```

Or run `bash reproduce.sh`, which records fresh output files and verifies their equality against the published results under the supported environment.

## Verified restricted-model checks

- **Early benchmark:** binary observation-set separation, Gaussian endpoint error, a diagnostic-adaptive authority-cost toy model, and rank 7/8 for partial observation of a 3-agent interaction.
- **REFLEX-T:** 100 random small-graph cross-checks against exhaustive graph calculations; exhaustive verification of 3 edge-disjoint parity-sensitive cycles; exact binary-symmetric-channel computations.
- **REFLEX-P:** 120 random owner-labelled graph checks against full transcript enumeration; 2,000 Byzantine-principal attack trials; a shared-hub versus independent-owner counterexample; a 12-edge exact audit-design optimum of 21 under the given toy costs.

All result counts are **mathematical/model-level tests**, not participant trials, model evaluations, independent scientific replication, or a claim of publication novelty. For full model assumptions, see the linked notes.

## Repository layout

```text
README.md
requirements.txt
reproduce.sh
.github/workflows/reproducibility.yml
src/
  reflex_equilibrium_authority_minibench.py
  reflex_audit_topology_prototype.py
  reflex6_principal_robustness.py
papers/
  REFLEX_Audit_Topology_Research_Draft.tex
  REFLEX_Audit_Topology_Research_Draft.pdf
  REFLEX6_Principal_Aware_Audits.tex
  REFLEX6_Principal_Aware_Audits.pdf
results/
  reflex_eq_stdout.txt
  reflex_t_stdout.txt
  reflex6_stdout.txt
docs/
  REFLEX_T_README_original.md
  REFLEX6_README_original.md
  RESEARCH_INTEGRITY.md
```

## Rebuilding reports

Run from `papers/` with a TeX installation providing `pdflatex`, `amsmath`, `tikz`, `hyperref`, `lmodern` and the other packages included in the `.tex` preambles:

```bash
cd papers
pdflatex -interaction=nonstopmode -halt-on-error REFLEX6_Principal_Aware_Audits.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX6_Principal_Aware_Audits.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX_Audit_Topology_Research_Draft.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX_Audit_Topology_Research_Draft.tex
```

This repository archives the source/results corresponding to the produced PDFs; the GitHub repository link is part of both report front pages.

## Scientific limitations

The restricted-model proofs are not evidence that the underlying graph/coding results are historically new. The central missing research steps are: a formally specified strategic multi-principal game and implementability theorem, a practical scalable mechanism, real-world agent experiments, contemporary baselines, and independent novelty and proof review. See [`docs/RESEARCH_INTEGRITY.md`](docs/RESEARCH_INTEGRITY.md) before describing any result publicly.
