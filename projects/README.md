# Portfolio Genius Lab — Aprile 2026

## Struttura

Il portfolio e' diviso in tre categorie: Tier S (nucleare, flagship), open-source (credibilita'), monetizzabile.

```
projects/
├── tier-s/              # Flagship: Ingegneria Nucleare + AI (massima priorita')
│   ├── 01-nuclearmind.md      # XAI Digital Twin per reattori nucleari
│   ├── 02-fusionedge.md       # Simulatore edge plasma differenziabile [PARCHEGGIATO]
│   └── 03-nucregai.md         # Compliance normativa nucleare con LLM [PARCHEGGIATO]
│
├── open-source/         # Credibilita' accademica/industriale (score <4/5)
│   ├── 01-quantum-bench.md
│   ├── 02-sat-guard.md
│   ├── 03-tinkerworld.md
│   ├── 06-vigipipe.md
│   └── 07-omni-oracle.md
│
├── monetizable/         # Progettati per monetizzazione (score >=4/5)
│   ├── 04-climafin.md         # Climate Finance — 4.5/5
│   ├── 05-seismocheck.md      # Seismic Assessment — 4.5/5
│   ├── 08-spectraforge.md     # Modular Lab Instruments — 4.5/5 [NEW]
│   ├── 09-emi-scout.md        # EMI Pre-Compliance Kit — 4.5/5 [NEW]
│   ├── 10-driftguard.md       # API Schema Drift Detection — 5/5 [NEW]
│   ├── 11-aircomply.md        # IAQ LEED/WELL Compliance — 4.5/5 [NEW]
│   ├── 12-depshield.md        # Supply Chain Security — 4.5/5 [NEW]
│   ├── 13-vibesentry.md       # Predictive Maintenance PMI — 4.5/5 [NEW]
│   ├── 14-gridpulse.md        # Power Quality Monitor — 4/5 [NEW]
│   ├── 15-contractforge.md    # Data Contract Enforcement — 4/5 [NEW]
│   └── 16-buildingiq-lite.md  # Building Energy Optimization — 4/5 [NEW]
│
└── tier-b/              # [LEGACY] Vecchia struttura, vedi sopra
```

---

## Progetti Open-Source (Credibilita')

| # | Nome | Dominio | Status | Note |
|---|------|---------|--------|------|
| 1 | QuantumBench | Quantum Computing | Da iniziare | — |
| 2 | SatGuard | Aerospace | Pubblicato GitHub | Completato |
| 3 | TinkerWorld | Physics Sim | Da iniziare | — |
| 6 | VigiPipe | Pharmacovigilance | F0 completato | Credibilita' pura |
| 7 | OmniOracle | Statistical Discovery | **CHIUSO** | Portfolio piece. Backtest 0/5 tradabili |

---

## Progetti Monetizzabili

### Scorecard Comparativa

| # | Nome | Tipo | Mercato | Ricorr. | Difend. | Scala | WTP | Orig. | **Tot** | MVP |
|---|------|------|---------|---------|---------|-------|-----|-------|---------|-----|
| 10 | **DriftGuard** | SW | 5 | 5 | 4 | 5 | 5 | 4 | **28** | 6-8 sett |
| 8 | **SpectraForge** | HW+SW | 4 | 4 | 5 | 5 | 4 | 5 | **27** | 2 mesi |
| 9 | **EMI Scout** | HW+SW | 3 | 4 | 5 | 5 | 5 | 5 | **27** | 3-4 mesi |
| 11 | **AirComply** | HW+SW | 5 | 5 | 5 | 4 | 4 | 4 | **27** | 2.5 mesi |
| 13 | **VibeSentry** | HW+SW | 5 | 5 | 5 | 4 | 4 | 3 | **26** | 3 mesi |
| 12 | **DepShield** | SW | 5 | 5 | 4 | 5 | 4 | 3 | **26** | 8-10 sett |
| 14 | **GridPulse** | HW+SW | 4 | 5 | 5 | 4 | 4 | 4 | **26** | 3-4 mesi |
| 15 | **ContractForge** | SW | 5 | 5 | 4 | 5 | 4 | 3 | **26** | 8-10 sett |
| 16 | **BuildingIQ Lite** | HW+SW | 5 | 5 | 5 | 4 | 4 | 3 | **26** | 12-16 sett |
| 4 | **ClimaFin** | SW | 5 | 4 | 4 | 4 | 5 | 3 | **25** | — |
| 5 | **SeismoCheck** | SW | 4 | 4 | 5 | 3 | 5 | 4 | **25** | — |

> Ordinati per score totale (6 criteri: 5 monetizzazione + originalita'). Originalita' e scalabilita' hanno peso decisionale maggiore.

### Per Tipo

**Pure Software (fast MVP, no hardware risk):**
- DriftGuard (28) — API schema drift, 6-8 settimane
- DepShield (26) — Supply chain security, 8-10 settimane
- ContractForge (26) — Data contracts, 8-10 settimane
- ClimaFin (25) — Climate finance risk
- SeismoCheck (25) — Seismic assessment

**Hardware + Software (moat piu' forte, MVP piu' lungo):**
- SpectraForge (27) — Lab instruments, 2 mesi
- EMI Scout (27) — EMI testing kit, 3-4 mesi
- AirComply (27) — IAQ compliance, 2.5 mesi
- VibeSentry (26) — Predictive maintenance, 3 mesi
- GridPulse (26) — Power quality, 3-4 mesi
- BuildingIQ Lite (26) — Building energy, 12-16 settimane

### Per Driver di Domanda

**Regolatorio (domanda garantita):**
- AirComply (LEED v5 / WELL v2, obbligatorio per certificazione)
- DepShield (EU Cyber Resilience Act 2026, SBOM obbligatorio)
- ClimaFin (CSRD 2025-2026)

**Pain economico (ROI dimostrabile):**
- VibeSentry (costo downtime >> costo sensori)
- GridPulse (sprechi energetici quantificabili in euro)
- BuildingIQ Lite (risparmio 20-30% bolletta)
- EMI Scout (risparmia $10-30K per test FCC/CE fallito)

**Gap di mercato puro (nessun competitor diretto):**
- DriftGuard (spec-free schema drift detection non esiste)
- SpectraForge (piattaforma lab modulare + software pro non esiste)
- EMI Scout (AI-guided pre-compliance <$1K non esiste)

---

## Progetti Trasversali

| Nome | Cartella | Scopo | Status |
|------|----------|-------|--------|
| **Growth** | `growth/` | Distribuzione e crescita profilo GitHub (Reddit, HN, Dev.to, Twitter, awesome-lists) | Week 1 pre-pubblicazione |

---

## Progetti Tier S — Ingegneria Nucleare + AI

| # | Nome | Dominio | Status | Note |
|---|------|---------|--------|------|
| 1 | **NuclearMind** | Nuclear + XAI | **F0 attivo** | Digital twin spiegabile per sicurezza reattori |
| 2 | FusionEdge | Fusion + ML | Parcheggiato | Simulatore edge plasma differenziabile |
| 3 | NucRegAI | Nuclear + NLP | Parcheggiato | Compliance normativa nucleare con LLM |

---

## Log Decisioni

- **2026-04-02**: Aggiunta categoria Tier S (Ingegneria Nucleare). 3 progetti: NuclearMind (attivo), FusionEdge e NucRegAI (parcheggiati). NuclearMind: XAI digital twin per reattori nucleari con architettura anti-allucinazione a 7 layer defense-in-depth.
- **2026-03-22**: Riorganizzazione portfolio in open-source/ e monetizable/. Aggiunti 9 nuovi progetti monetizzabili da ricerca intensiva (web search, analisi competitor, market sizing). OmniOracle chiuso come portfolio piece dopo backtest negativo (0/5 ROBUST tradabili).
- **2026-03-20**: Aggiunto OmniOracle. F0 completato.
- **2026-03-19**: Aggiunti ClimaFin, SeismoCheck, VigiPipe dopo ricerca su 5 candidati.
- **2026-03-13**: SpecForge (vecchio progetto omonimo, non SpectraForge) eliminato. DSL generico non risolve problema specifico.
- **2026-03-12**: Analisi competitiva. 15 progetti eliminati (competitor diretti).
