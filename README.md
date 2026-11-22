# REFLEX — Reproducible Research Prototypes

**Research owner:** Mohammad Amanlou  
**Repository:** https://github.com/MohammadAmanlou/REFLEX  
**Status:** Exploratory mathematical research; **not peer reviewed**, **not a conference submission**, and **not evidence of accepted historical novelty**.

This repository archives the REFLEX research prototypes built on 22 November 2026, progressing from equilibrium/evidence checks to topology-based audits through **principal-aware robustness, a topology–incentive frontier, and no-state-oracle refutable certification**. The projects formalize *restricted* binary models and compare exact small-instance methods; they do **not** implement general equilibrium-robust, incentive-compatible multi-agent mechanisms or deployed LLM-agent evaluations.

## Research versions

| Version | Code | Research note | Experimental results |
|---|---|---|---|
| Early equilibrium and experimental-authority checks | [`src/reflex_equilibrium_authority_minibench.py`](src/reflex_equilibrium_authority_minibench.py) | Early numerical sanity checks | [`results/reflex_eq_stdout.txt`](results/reflex_eq_stdout.txt) |
| REFLEX-T — audit topology | [`src/reflex_audit_topology_prototype.py`](src/reflex_audit_topology_prototype.py) | [`papers/REFLEX_Audit_Topology_Research_Draft.pdf`](papers/REFLEX_Audit_Topology_Research_Draft.pdf) ([LaTeX](papers/REFLEX_Audit_Topology_Research_Draft.tex)) | [`results/reflex_t_stdout.txt`](results/reflex_t_stdout.txt) |
| REFLEX-P / 6.0 — principal-aware audits | [`src/reflex6_principal_robustness.py`](src/reflex6_principal_robustness.py) | [`papers/REFLEX6_Principal_Aware_Audits.pdf`](papers/REFLEX6_Principal_Aware_Audits.pdf) ([LaTeX](papers/REFLEX6_Principal_Aware_Audits.tex)) | [`results/reflex6_stdout.txt`](results/reflex6_stdout.txt) |
| **REFLEX 7.0 — topology–incentive frontier** | [`src/reflex7_economic_frontier.py`](src/reflex7_economic_frontier.py) | [`papers/REFLEX7_Topology_Incentive_Frontier.pdf`](papers/REFLEX7_Topology_Incentive_Frontier.pdf) ([LaTeX](papers/REFLEX7_Topology_Incentive_Frontier.tex)) | [`results/reflex7_stdout.txt`](results/reflex7_stdout.txt) |

| **REFLEX 8.0 — no-state-oracle refutable certification** | [`src/reflex8_refutable_certification.py`](src/reflex8_refutable_certification.py) | [`papers/REFLEX8_No_Oracle_Certification.pdf`](papers/REFLEX8_No_Oracle_Certification.pdf) ([LaTeX](papers/REFLEX8_No_Oracle_Certification.tex)) | [`results/reflex8_stdout.txt`](results/reflex8_stdout.txt) |

The PDFs and LaTeX sources explicitly link back to this repository. Current main research note: **REFLEX 8.0**. Read [`docs/REFLEX8_README.md`](docs/REFLEX8_README.md) for exact assumptions, equilibrium-safety scope, and limitations.


## REFLEX 9 working prototype: complementary witness assembly

The code in [`src/reflex9_witness_assembly_game.py`](src/reflex9_witness_assembly_game.py) implements a **restricted, exact finite pure-Nash game** for witness fragments owned by multiple independent principals. It computes minimal owner cuts, enumerates corrupt-owner sets and pure Nash profiles, and contrasts completion-only prizes with individually paid, independently verifiable valid fragments. The [seven unit tests](tests/test_reflex9_witness_assembly.py) include a silent equilibrium despite a large completion prize, a robust two-witness example under one corrupted owner, and a single-owner-cut failure. Run:

```bash
python src/reflex9_witness_assembly_game.py
python -m unittest discover -s tests -v
```

**Research-integrity boundary:** The evaluator fixes a false proposal; every owner identity and primitive fragment is assumed verifiable. Byzantine owners can withhold but not forge other owners' evidence. The script does **not** implement an unconstrained strategic equilibrium oracle, reliable sensor semantics, real LLM-agent behaviour, or the full proposed joint optimizer. The professor-facing proposal discusses these as research questions, not established experimental achievements.

## Quickstart

Requires Python **3.10+** (CI uses Python 3.11). REFLEX-T and REFLEX-P rely only on the Python standard library. The early benchmark and REFLEX 7.0's small audit-policy LP require NumPy/SciPy.

```bash
python -m pip install -r requirements.txt
python src/reflex_equilibrium_authority_minibench.py
python src/reflex_audit_topology_prototype.py
python src/reflex6_principal_robustness.py
python src/reflex7_economic_frontier.py
python src/reflex8_refutable_certification.py
```

Or run `bash reproduce.sh`, which records fresh output files and verifies their equality against the published results under the supported environment.

## Verified restricted-model checks

- **Early benchmark:** binary observation-set separation, Gaussian endpoint error, a diagnostic-adaptive authority-cost toy model, and rank 7/8 for partial observation of a 3-agent interaction.
- **REFLEX-T:** 100 random small-graph cross-checks against exhaustive graph calculations; exhaustive verification of 3 edge-disjoint parity-sensitive cycles; exact binary-symmetric-channel computations.
- **REFLEX-P:** 120 random owner-labelled graph checks against full transcript enumeration; 2,000 Byzantine-principal attack trials; a shared-hub versus independent-owner counterexample; a 12-edge exact audit-design optimum of 21 under the given toy costs.
- **REFLEX 7.0:** exact weighted false-certificate cost; explicit forgery; 103 eligible random-graph checks against exhaustive transcript search; separate abstention threshold; 27-constraint audit LP with synthetic optimum 3.690. These are **restricted mathematical examples**; no general all-equilibria incentive-compatibility or LLM study has been established.

- **REFLEX 8.0:** 180 exhaustive random small-graph transcript checks; exact detection/correction thresholds; 32 ambiguous attacked transcripts in the two-triangle safe-only regime; access-custody cut comparison and cost-2.2 toy grant design; pure Nash challenge-game counterexamples. This is NOT an all-equilibria proof for unrestricted reporting games or an LLM evaluation.

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
  reflex7_economic_frontier.py
  reflex8_refutable_certification.py
papers/
  REFLEX_Audit_Topology_Research_Draft.tex
  REFLEX_Audit_Topology_Research_Draft.pdf
  REFLEX6_Principal_Aware_Audits.tex
  REFLEX6_Principal_Aware_Audits.pdf
  REFLEX7_Topology_Incentive_Frontier.tex
  REFLEX7_Topology_Incentive_Frontier.pdf
  REFLEX8_No_Oracle_Certification.tex
  REFLEX8_No_Oracle_Certification.pdf
results/
  reflex_eq_stdout.txt
  reflex_t_stdout.txt
  reflex6_stdout.txt
  reflex7_stdout.txt
  reflex8_stdout.txt
docs/
  REFLEX_T_README_original.md
  REFLEX6_README_original.md
  RESEARCH_INTEGRITY.md
  REFLEX7_README.md
  REFLEX8_README.md
```

## Rebuilding reports

Run from `papers/` with a TeX installation providing `pdflatex`, `amsmath`, `tikz`, `hyperref`, `lmodern` and the other packages included in the `.tex` preambles:

```bash
cd papers
pdflatex -interaction=nonstopmode -halt-on-error REFLEX6_Principal_Aware_Audits.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX6_Principal_Aware_Audits.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX_Audit_Topology_Research_Draft.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX_Audit_Topology_Research_Draft.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX7_Topology_Incentive_Frontier.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX8_No_Oracle_Certification.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX8_No_Oracle_Certification.tex
pdflatex -interaction=nonstopmode -halt-on-error REFLEX7_Topology_Incentive_Frontier.tex
```

This repository archives the source/results corresponding to the produced PDFs; the GitHub repository link is part of all available report front pages.

## Scientific limitations

The restricted-model proofs are not evidence that the underlying graph/coding results are historically new. The central missing research steps are: an unrestricted all-equilibria strategic multi-principal truth-elicitation theorem without any local evidence assumptions, a practical scalable mechanism, real-world agent experiments, contemporary baselines, and independent novelty and proof review. See [`docs/RESEARCH_INTEGRITY.md`](docs/RESEARCH_INTEGRITY.md) before describing any result publicly.
