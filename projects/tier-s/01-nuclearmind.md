# NuclearMind — Explainable AI Digital Twin for Nuclear Reactor Safety

## Status: F0 (Inizializzazione) — 2026-04-02

## Elevator Pitch
Framework open-source che combina surrogate models (GNN/PINN) con garanzie formali di
interpretabilita' e incertezza calibrata per digital twin di reattori nucleari. L'unico
framework XAI-nativo progettato per la licenziabilita' NRC.

## Il Gap (verificato con ricerca 2026-04-02)

### Cosa ESISTE:
| Tool | Cosa fa | Cosa manca |
|------|---------|------------|
| OpenMC (995 stars) | Monte Carlo neutronics | No ML/surrogate built-in |
| MOOSE/SAM (2189 stars) | Multiphysics FEM | ML nascente (ProbML nuovo) |
| RAVEN (254 stars) | Risk analysis, UQ | Solo ML classico, no DL/GNN |
| pyMAISE (29 stars) | ML benchmarking nucleare | Solo classico, no digital twin, no real-time |
| Argonne GNN Digital Twin | GNN per EBR-II, gFHR | **NON open-source** |
| ARMI (263 stars) | Automation framework | No ML built-in |

### Cosa NON ESISTE (il nostro spazio):
1. **Nessun framework integrato** simulation + surrogate + XAI + digital twin
2. **Nessun GNN nuclear digital twin open-source** (Argonne lo ha provato ma e' chiuso)
3. **Nessun framework XAI-first** per AI nucleare (pyMAISE ha XAI come feature, non come principio)
4. **Nessun benchmark con leaderboard** aperto per AI nucleare
5. **Nessun framework PINN pacchettizzato** per uso nucleare

## Framework Monetizzazione (5 criteri)
1. Mercato ampio: Si (tutte le utility nucleari, laboratori, universita') — ma <10K clienti paganti diretti
2. Bisogno ricorrente: Si (ogni nuova analisi di sicurezza)
3. Difendibilita': Alta (competenza di dominio + validazione)
4. Scalabilita': Si (universale per qualsiasi tipo di reattore)
5. Willingness to pay: Media (industria nucleare spende, ma preferisce tool validati NRC)

**Score: 3.5/5 → OPEN SOURCE per credibilita'**

Coerente con obiettivo #1 del portfolio: visibilita' e credibilita' accademica/industriale.

## Differenziatore Chiave: Architettura Anti-Allucinazione

> "Se un modello AI sbaglia la previsione di un reattore nucleare, le conseguenze sono
> catastrofiche. NuclearMind non e' un altro wrapper ML — e' un framework dove ogni
> predizione e' verificabile, spiegabile, e ha garanzie matematiche di copertura."

### 7 Layer Defense-in-Depth (dalla ricerca)

```
L7: Human-in-the-Loop ← deferral quando incerto
L6: Explainability ← SHAP/Captum/attention maps per OGNI predizione
L5: Formal Verification ← alpha-beta-CROWN per sottosistemi safety-critical
L4: Output Validation ← range fisici, consistency checks, conservation laws
L3: Uncertainty Quantification ← deep ensembles + conformal prediction (MAPIE)
L2: Physics Constraints ← PINN loss terms, conservation laws nel training
L1: Data Quality ← Cleanlab, drift detection (Alibi Detect), data provenance
```

Nessun layer singolo basta. La combinazione di layer indipendenti e' cio' che rende
il sistema trustworthy.

## Target Audience
1. **Ricercatori nucleari** che vogliono surrogati veloci ma affidabili
2. **Utility/vendor** che devono dimostrare compliance AI alla NRC
3. **Regolatori** che cercano un reference framework per V&V di AI nucleare
4. **Studenti** che vogliono imparare AI applicata al nucleare

## Oracoli di Dominio

### L2 (Domain Sanity)
- Vallado 5th Ed — propagazione orbitale (se applicabile)
- Duderstadt & Hamilton — Nuclear Reactor Analysis, valori di benchmark
- IAEA Safety Standards — limiti operativi
- NEA/OECD AI/ML Benchmark Phase 1 (CHF) e Phase 2 (PUR-1)

### L5 (Validazione Reale)
- Dataset NPPAD (thu-inet) — 6 tipi di incidente PWR
- EBR-II Shutdown Heat Removal Tests (SHRT) — dati sperimentali pubblici
- OECD/NEA benchmark results
- NRC NUREG/CR reports con dati sperimentali

## Competitori e Posizionamento

| | pyMAISE | Argonne GNN | RAVEN | **NuclearMind** |
|---|---------|-------------|-------|-----------------|
| Open source | Si | **No** | Si | **Si** |
| Deep Learning | No | Si (GNN) | No | **Si (GNN+PINN+Transformer)** |
| XAI nativo | Parziale | No | No | **Si (core principle)** |
| Digital twin | No | Si | No | **Si** |
| Incertezza calibrata | No | No | Si (classico) | **Si (conformal)** |
| Benchmarks | 9 | 0 pub. | 0 | **Si + leaderboard** |
| Formal verification | No | No | No | **Si (safety subsystems)** |
| NRC-ready | In progress | No | Parziale | **Si (design goal)** |

## Rischi (Pre-mortem)
1. **Dati di training insufficienti** — Mitigazione: pipeline automatica OpenMC/SAM
2. **GNN troppo complesso per spiegare** — Mitigazione: architettura a 2 livelli (GNN veloce + modello interpretabile di validazione)
3. **Scope creep** — Mitigazione: MVP su UN tipo di reattore (PWR), poi espansione
4. **Validazione contro dati reali** — Mitigazione: usare dataset pubblici (EBR-II SHRT, NPPAD)
5. **Competizione da lab nazionali** — Mitigazione: open-source community-driven vs closed

## Referenze Chiave
- Argonne GNN Digital Twin: https://www.anl.gov/article/virtual-models-paving-the-way-for-advanced-nuclear-reactors
- pyMAISE: https://github.com/aims-umich/pyMAISE
- NPPAD Dataset: https://github.com/thu-inet/NuclearPowerPlantAccidentData
- NRC AI Gap Assessment: https://www.nrc.gov/docs/ML2429/ML24290A059.pdf
- NRC/CNSC/ONR Joint AI Principles (Sept 2024)
- NEA AIxpertise Project: https://www.oecd-nea.org/jcms/pl_100138/
- MAPIE (conformal prediction): https://github.com/scikit-learn-contrib/MAPIE
- alpha-beta-CROWN: https://github.com/Verified-Intelligence/alpha-beta-CROWN
- Cleanlab: https://github.com/cleanlab/cleanlab
- Alibi Detect: https://github.com/SeldonIO/alibi-detect
