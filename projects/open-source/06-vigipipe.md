# VigiPipe

## Open-Source Pharmacovigilance Signal Detection Pipeline

**Tier:** B — Originale con Gap di Mercato
**Status:** F0 Setup
**Monetizzazione:** 3.4/5 — open-source puro (asset di credibilità)

---

## Contesto 2026

- Centinaia di paper FAERS-based all'anno, ognuno ricostruisce la stessa pipeline ad-hoc
- Oracle Argus Safety domina (~60% market share) a $250K-$1M+ — inaccessibile per accademia/piccole pharma
- vigipy (12 stars GitHub): solo algoritmi, nessuna pipeline integrata
- OpenVigil: solo query web su openFDA API, nessuna analisi locale
- READUS-PV (2024): nuova linea guida 32-item per reporting DPA, nessun tool la implementa
- FDA FAERS completamente pubblico: 30M+ report, quarterly updates
- 42% piccole/medie pharma citano costi licensing come barriera

## Cosa Costruiamo

Pipeline open-source per signal detection da dati FAERS: ingestione → analisi → report conforme READUS-PV.

**In una frase:** "Scarica i dati FAERS, cerca segnali di sicurezza per qualsiasi farmaco con 4 metodi statistici, ottieni un report READUS-PV compliant — riproducibile, validato, gratuito."

## Gap di Mercato Verificato

| Capacità | Oracle Argus | OpenVigil | vigipy | **VigiPipe** |
|----------|-------------|-----------|--------|-------------|
| FAERS ingestion | ✅ | Via API | ❌ | ✅ (CSV diretto) |
| Data cleaning | ✅ | ❌ | ❌ | ✅ |
| PRR/ROR | ✅ | Parziale | ✅ | ✅ |
| BCPNN | ✅ | ❌ | ✅ | ✅ |
| MGPS | ✅ | ❌ | ✅ | ✅ |
| READUS-PV report | ❌ | ❌ | ❌ | ✅ |
| Pipeline E2E | ✅ | ❌ | ❌ | ✅ |
| Riproducibile | ❌ (black-box) | Parziale | ✅ | ✅ |
| Gratuito | ❌ ($250K+) | ✅ | ✅ | ✅ |

## Utenti Target

1. **Ricercatori accademici** — centinaia di paper FAERS/anno, ognuno reinventa la pipeline
2. **Piccole/medie pharma e biotech** — 42% non possono permettersi Argus
3. **CROs** — signal detection per clienti senza licenze enterprise
4. **Studenti di farmacologia/regulatory science** — nessun tool didattico standard
5. **Regolatori in paesi in via di sviluppo** — non possono permettersi tool enterprise

## Stack Tecnico

| Componente | Tecnologia | Versione | Motivo |
|-----------|-----------|---------|--------|
| Core library | Python | 3.12+ | Ecosistema scientifico |
| Data processing | pandas | latest | FAERS CSV manipulation |
| Statistics | NumPy + SciPy | latest | Chi², Fisher exact, Bayesian |
| Bayesian | PyMC | latest | BCPNN implementation |
| Visualization | matplotlib + plotly | latest | Forest plots, dashboards |
| Reports | reportlab | latest | READUS-PV PDF reports |

## Roadmap

| Fase | Versione | Cosa | Valore |
|------|----------|------|--------|
| F3a | **v0.1 (MVP)** | FAERS ingest + 4 DPA methods + known signal validation + READUS-PV report | Reproducible FAERS signal detection |
| F3b | **v0.2** | RxNorm mapping + MedDRA SOC + time evolution | Drug name normalization robusta |
| F3c | **v0.3** | EudraVigilance + Canada Vigilance + multi-database | Copertura dati globale |
| F3d | **v0.4** | NLP narrative processing + time-trend detection | Analisi avanzata |
| F3e | **v0.5** | Web dashboard + signal monitoring | Monitoraggio continuo |
| F3f | **v0.6** | ICH E2B(R3) parsing + institutional integration | Integrazione aziendale |

## Oracoli di Dominio

| Livello | Fonte | Uso |
|---------|-------|-----|
| L2 | Evans et al. 2001 — PRR formula + worked examples | Verifica PRR |
| L2 | Bate et al. 1998 — BCPNN algorithm + WHO-UMC test cases | Verifica BCPNN |
| L2 | DuMouchel 1999 — GPS/MGPS paper + examples | Verifica MGPS |
| L5 | Rofecoxib (Vioxx) → Myocardial Infarction (withdrawn 2004) | Must-detect signal |
| L5 | Rosiglitazone (Avandia) → Cardiovascular events (restricted 2010) | Must-detect signal |
| L5 | Cerivastatin (Baycol) → Rhabdomyolysis (withdrawn 2001) | Must-detect signal |

## Pre-mortem

1. **MedDRA non è free** → mitigation: lavorare con FAERS pre-coded Preferred Terms, non serve MedDRA completo
2. **Drug name normalization è complessa** → mitigation: v0.1 con normalizzazione base, RxNorm in v0.2
3. **FAERS data quality variabile** → mitigation: deduplication robusta + documentare limitazioni

## Fonti

- [FDA FAERS Data](https://open.fda.gov/data/faers/)
- [READUS-PV Guideline — Drug Safety (2024)](https://link.springer.com/article/10.1007/s40264-024-01421-9)
- [vigipy — GitHub](https://github.com/Shakesbeery/vigipy)
- [OpenVigil](https://openvigil.sourceforge.net/)
- [Evans et al. 2001 — PRR](https://pubmed.ncbi.nlm.nih.gov/11575286/)
- [Bate et al. 1998 — BCPNN](https://pubmed.ncbi.nlm.nih.gov/9860006/)
- [DuMouchel 1999 — MGPS](https://link.springer.com/article/10.1023/A:1018598911768)
- [Pharmacovigilance Software Market (Precedence Research)](https://www.precedenceresearch.com/pharmacovigilance-and-drug-safety-software-market)
