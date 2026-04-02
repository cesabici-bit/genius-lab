# CLAUDE.md — NuclearMind

## Progetto
**NuclearMind** — Explainable AI Digital Twin for Nuclear Reactor Safety

## Obiettivo
Framework open-source che combina surrogate models (GNN/PINN) con garanzie formali di interpretabilita' e incertezza calibrata per digital twin di reattori nucleari. L'unico framework XAI-nativo progettato per la licenziabilita' NRC.

## Stack Tecnico

| Componente | Tecnologia | Versione | Motivo |
|-----------|-----------|---------|--------|
| Language | Python | >=3.11 | Ecosistema ML + nucleare. Min 3.11 per SHAP |
| GNN Framework | PyTorch Geometric | 2.7.0 | Migliore lib GNN, attention native, GraphSAGE/GAT |
| DL Framework | PyTorch | 2.11.0 | Flessibilita' PINN loss, standard de facto |
| Conformal Prediction | MAPIE | 1.3.0 | Garanzie matematiche copertura. **API v1: SplitConformalRegressor** |
| Explainability | SHAP + Captum | 0.51.0 / 0.8.0 | SHAP: feature importance. Captum: LayerIntegratedGradients |
| Data Quality | Cleanlab | 2.9.0 | Label error detection, 11K stars |
| Drift Detection | Alibi Detect | 0.13.0 | Drift/outlier detection. Installare con `[torch]` extra |
| UQ/Ensembles | TorchUncertainty | 0.11.0 | Deep ensembles + calibration. NeurIPS D&B 2025 |
| Neutronics Sim | OpenMC | 0.15.3 | Monte Carlo, Python API, MIT. conda-forge only |
| Data Storage | h5py | 3.15.1 | HDF5 con metadati completi |
| Dashboard | Streamlit | 1.56.0 | Prototipazione rapida |
| Testing | pytest + Hypothesis | 9.0.2 / 6.151.10 | Unit + property-based |

> IMPORTANT: ogni dipendenza DEVE avere entry verificata in `verified-deps.toml`

## Architettura

```
┌──────────────────────────────────────────────────────────┐
│                  LAYER 3: TRUST ENGINE                    │
│  Conformal(MAPIE) + Physics Checks + SHAP + Trust Score  │
├──────────────────────────────────────────────────────────┤
│                LAYER 2: SURROGATE ENGINE                  │
│  GraphSAGE Ensemble (5 modelli) + PINN Physics Loss      │
├──────────────────────────────────────────────────────────┤
│                  LAYER 1: DATA ENGINE                     │
│  OpenMC Bridge + HDF5 Dataset + Cleanlab Quality          │
└──────────────────────────────────────────────────────────┘
```

## Package Structure

```
nuclearmind/
├── src/nuclearmind/
│   ├── data/           # Layer 1: Data Engine
│   │   ├── openmc_bridge.py, pwr_geometry.py, dataset.py, mock.py, quality.py
│   ├── surrogate/      # Layer 2: Surrogate Engine
│   │   ├── graph.py, model.py, physics_loss.py, ensemble.py, train.py
│   └── trust/          # Layer 3: Trust Engine
│       ├── conformal.py, physics_checks.py, explain.py, trust_score.py, dashboard.py
├── tests/
├── verify/             # M4: Two-tool verification
└── scripts/
```

## MVP Scope

### IN (MVP)
- [x] Architettura definita (F0)
- [x] Dipendenze verificate (F2)
- [ ] UN tipo di reattore: PWR (17x17 assembly, 289 nodi)
- [ ] UNA quantita' predetta: distribuzione di potenza + keff
- [ ] Dati generati con OpenMC (neutronics pura) + mock data per CI
- [ ] GNN base (GraphSAGE) con ensemble di 5 modelli
- [ ] PINN physics loss (conservation, non-negativity, keff range)
- [ ] Conformal prediction con MAPIE v1 (SplitConformalRegressor)
- [ ] SHAP explanations per ogni predizione
- [ ] Physics checks post-predizione
- [ ] Trust score aggregato con verdict ACCEPT/WARNING/REJECT
- [ ] Streamlit dashboard minimo (5 pannelli)

### OUT (post-MVP)
- Thermal-hydraulics accoppiata (MOOSE/SAM)
- Reattori avanzati (MSR, SFR, HTGR)
- Formal verification (alpha-beta-CROWN)
- Real-time inference / deployment production
- Drift detection online (Alibi Detect) — architettura pronta, implementazione post-MVP
- Captum attention maps avanzate

## Oracoli di Dominio

| Livello | Fonte | Uso |
|---------|-------|-----|
| L2 (sanity) | Duderstadt & Hamilton, "Nuclear Reactor Analysis" | keff range, power distribution shape per PWR |
| L2 (sanity) | IAEA Safety Standards (SSR-2/1) | Limiti operativi: T < T_fusione, keff range |
| L2 (sanity) | NEA/OECD PWR pin-cell benchmark | Valori keff di riferimento |
| L5 (reale) | NPPAD Dataset (thu-inet) — 6 tipi incidente PWR | Validazione su dati reali di incidente |
| L5 (reale) | EBR-II SHRT — dati sperimentali pubblici | Validazione su dati sperimentali |
| L5 (reale) | NRC NUREG/CR reports | Dati sperimentali regolatori |

> Questi oracoli sono la base per i test L2/L5. Ogni test DEVE citare la fonte con `# SOURCE:`.

## Subtask F3 (Implementazione MVP)

### Phase 1: Data Engine

| # | Subtask | Input | Output | Pass/Fail | Size |
|---|---------|-------|--------|-----------|------|
| 1.0 | Environment + Mock Data | ARCHITECTURE.md, verified-deps.toml | pyproject.toml, mock.py, conftest.py | `pip install -e ".[dev]"` OK, mock data rispetta physics constraints (keff [0.95,1.05], power>=0, conservation <1%) | M |
| 1.1 | OpenMC Bridge | 1.0 | openmc_bridge.py, pwr_geometry.py | keff entro 500 pcm da OECD/NEA benchmark. Tests skippati senza OpenMC | L |
| 1.2 | HDF5 Dataset Store | 1.0+1.1 | dataset.py, generate_dataset.py | Round-trip HDF5 bit-exact, to_pyg() produce Data valido, split deterministico | M |
| 1.3 | Data Quality Gate | 1.2 | quality.py | 100% violazioni fisiche catturate, >=80% outlier iniettati flaggati | S |

### Phase 2: Surrogate Engine

| # | Subtask | Input | Output | Pass/Fail | Size |
|---|---------|-------|--------|-----------|------|
| 2.0 | Graph Construction | 1.0 | graph.py | 289 nodi, adj simmetrica, no self-loop, dtype float32 | S |
| 2.1 | GraphSAGE Model | 2.0 | model.py | power_pred shape [289], keff_pred shape [1], gradients non-None, <1M params | M |
| 2.2 | Physics Loss | 2.1 | physics_loss.py | Ogni loss=0.0 su input perfetto, tutte differenziabili | S |
| 2.3 | Ensemble Training | 2.1+2.2 | ensemble.py, train.py | 5 epoch mock <60s CPU, std_power>0, checkpoint load deterministico | L |

### Phase 3: Trust Engine

| # | Subtask | Input | Output | Pass/Fail | Size |
|---|---------|-------|--------|-----------|------|
| 3.0 | Conformal Prediction | 2.3 | conformal.py | Coverage empirica >=93%, lower<=upper per ogni nodo | M |
| 3.1 | Physics Checks | 2.3 | physics_checks.py | Ogni check testato pass+fail, SOURCE: IAEA SSR-2/1 | S |
| 3.2 | SHAP Explanations | 2.3 | explain.py | SHAP additivity >=80% campioni, <30s per sample CPU | M |
| 3.3 | Trust Score | 3.0+3.1+3.2 | trust_score.py | Score in [0,1], physics fail -> REJECT (<0.4), monotonicita' | S |
| 3.4 | Streamlit Dashboard | 3.3 | dashboard.py | 5 pannelli, load <5s, slider aggiorna tutti i pannelli | M |

**Critical path**: 1.0 -> 2.0 -> 2.1 -> 2.2 -> 2.3 -> 3.0/3.1/3.2 (parallel) -> 3.3 -> 3.4
**OpenMC (1.1) fuori dal critical path**: tutto il surrogate/trust funziona con mock data.

## E2E Smoke Test (M3)

**"NuclearMind funziona"** = dato parametri PWR, produce:
1. Predizione power distribution + keff da GNN ensemble
2. Intervalli di confidenza calibrati (conformal prediction)
3. Report validazione fisica (pass/fail per ogni check)
4. Spiegazione SHAP (top features + top nodi)
5. Trust score con verdict (ACCEPT/WARNING/REJECT)

Pipeline: Mock data -> HDF5 -> PyG graph -> GNN ensemble -> conformal -> physics checks -> SHAP -> trust score. Tutto con mock data, gira in CI senza OpenMC.

## Meccanismi Anti-Allucinazione (M1-M4)

### M1: Dependency Lock
- File: `verified-deps.toml` (13 dipendenze verificate via web search)
- Regola: NESSUNA dipendenza nel codice senza entry verificata

### M2: External Oracle Test Pattern
- Regola: ogni test file DEVE avere almeno 1 test con `# SOURCE:` da oracolo esterno
- Oracoli principali: Duderstadt & Hamilton, IAEA SSR-2/1, OECD/NEA benchmark, NPPAD, EBR-II SHRT

### M3: Smoke Before Unit
- Sequenza obbligatoria: smoke test E2E -> unit test -> property-based test
- Lo smoke test produce output leggibile dall'umano e diventa golden snapshot (L4)
- Smoke test definito: test_smoke.py (pipeline completa mock data -> trust score)

### M4: Two-Tool Verification
- Directory `verify/` con `openmc_comparison.py`: confronto diretto OpenMC vs GNN prediction
- Per ogni sample di test: calcola errore relativo, verifica < 5% su test set

## Workflow con Phase Gates

Vedi `genius-lab/CLAUDE.md` per il workflow completo.

### Gate F2 (Architettura) -- COMPLETATO 2026-04-02
- [x] CLAUDE.md progetto creato
- [x] verified-deps.toml con 13 deps verificate via web search
- [x] MAPIE v1.3 breaking change documentata
- [x] Subtask F3 definiti con input/output/pass-fail
- [x] Smoke test E2E definito
- [x] STATUS.md, KNOWN_ISSUES.md, Makefile creati

### Gate F3 (Implementazione) — per subtask
- [ ] `make check-all` verde
- [ ] Output ispezionabile dall'utente

### Gate F4 (Verifica)
- [ ] L1: unit test path critici
- [ ] L2: almeno 3 test con `# SOURCE:` (Duderstadt, IAEA, OECD/NEA)
- [ ] L3: property-based sulle invarianti (conservation, non-negativity, keff range)
- [ ] L4: golden snapshot smoke test revisionato dall'umano
- [ ] L5: confronto con NPPAD dataset o EBR-II SHRT

## Protocollo Correzione Errori

Vedi `genius-lab/CLAUDE.md` per il decision tree completo.
Errori specifici di questo progetto vanno in `KNOWN_ISSUES.md`.
Issues note: EC-001 (MAPIE API), EC-002 (SHAP Python >=3.11).

## Checkpoint Utente Obbligatori
- [ ] F3-1.0: mock data output — physics constraints rispettate?
- [ ] F3-2.3: ensemble training output — loss diminuisce? modelli diversi?
- [ ] F3-3.4: dashboard screenshot — 5 pannelli visibili e sensati?
- [ ] F4: golden snapshot smoke test — pipeline E2E produce output credibile?
- [ ] Prima del release: README, CI, license

## Comandi

```bash
# Install (dev)
pip install -e ".[dev]"

# Check completo
make check-all

# Solo test (no OpenMC)
make test

# Test con OpenMC
make test-openmc

# Smoke test E2E
make smoke

# Genera dataset OpenMC
make generate-data

# Dashboard
streamlit run src/nuclearmind/trust/dashboard.py

# Clean
make clean
```
