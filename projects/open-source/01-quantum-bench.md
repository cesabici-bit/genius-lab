# 11 - QuantumBench

## Benchmark Onesto Quantum vs Classical

**Tier:** B — Originale con Gap di Mercato
**Ranking:** #11
**Status:** Da iniziare

---

## Contesto 2026

- IonQ/Ansys: primo vantaggio quantum pratico documentato (+12% su simulazione medica)
- IBM Quantum: 4.158 qubits (Kookaburra multi-chip), error rate record 0.000015%
- QuEra: riduzione overhead error correction di 100x
- La maggior parte dei claim di "quantum advantage" non confronta equamente con solver classici SOTA

## Cosa Costruiamo

Framework che prende un problema di ottimizzazione, lo risolve sia quantum che classico, e produce benchmark onesto:

1. **Input**: problema in forma QUBO/Ising o formulazione naturale
2. **Quantum solve**: QAOA su hardware reale (via Qiskit/PennyLane + Mitiq error mitigation)
3. **Classical solve**: Gurobi, OR-Tools, simulated annealing
4. **Benchmark report**: tempo, qualità soluzione, costo, scalabilità

## Stack: Python, Qiskit, PennyLane, Mitiq, Gurobi
## Fattibilità: Alta
## Monetizzazione: 2/5 — pura credibilità accademica, paper garantito

## Fonti

- [Quantum Breakthroughs 2025](https://www.networkworld.com/article/4088709/top-quantum-breakthroughs-of-2025.html)
- [DOE Quantum Milestone](https://news.fnal.gov/2026/02/doe-national-quantum-research-centers-reach-milestone-breakthrough-towards-building-scalable-quantum-computers/)
