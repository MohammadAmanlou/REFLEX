#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results/reproduced
python src/reflex_equilibrium_authority_minibench.py > results/reproduced/reflex_eq_stdout.txt
python src/reflex_audit_topology_prototype.py > results/reproduced/reflex_t_stdout.txt
python src/reflex6_principal_robustness.py > results/reproduced/reflex6_stdout.txt
python src/reflex7_economic_frontier.py > results/reproduced/reflex7_stdout.txt
python src/reflex8_refutable_certification.py > results/reproduced/reflex8_stdout.txt
for case in reflex_eq reflex_t reflex6 reflex7 reflex8; do
  diff -u "results/${case}_stdout.txt" "results/reproduced/${case}_stdout.txt"
done
echo 'PASS: all five REFLEX result transcripts match the archived output.'
