# 07 — OmniOracle

## One-liner
Motore di scoperta automatica di verita' statistiche non banali da dati pubblici eterogenei cross-domain.

## Concept
Un sistema che ingerisce decine di migliaia di serie temporali pubbliche (economia, clima, salute, trasporti, brevetti, social), scopre automaticamente relazioni causali non banali tramite information theory + causal discovery, e le presenta con rigore statistico completo. Un "oracolo universale" che estrae conoscenza nascosta dall'intersezione di dati che nessuno ha mai incrociato.

## Dominio
Statistical Discovery / Causal Inference / Alternative Data / OSINT

## Gap di Mercato (confermato con ricerca marzo 2026)
- **causaLens** ($45M raised) e' il competitor piu' diretto ma focus su decisioni aziendali (pricing, supply chain), NON su discovery esplorativo da dati pubblici cross-domain
- **Tigramite** e' il piu' vicino tecnicamente ma e' una libreria, non un prodotto con ingestione + validazione + output
- **Kensho/Bloomberg** hanno i dati ma no causal discovery automatizzato
- **Eagle Alpha/Nasdaq DL** vendono dati grezzi, non insight causali
- **Palantir** integra dati ma $10M+/anno e richiede team dedicato
- Nessun tool open/pubblico fa discovery causale automatica cross-domain a scala
- Ricerca completa: `.claude/plans/vast-crunching-flurry.md`

## Stack
Python 3.12+ — Pandas, Scipy, Scikit-learn, Statsmodels, DuckDB, HTTPX, Plotly

## Architettura (5 strati)
1. **Ingest Layer** — Async fetchers da fonti pubbliche (FRED, World Bank) → serie temporali normalizzate
2. **Storage** — DuckDB: tabella universale feature x tempo x geo
3. **Discovery Engine** — MI screening (scarta 99%) → Granger causality
4. **Validation Filter** — FDR (Benjamini-Hochberg) + Out-of-sample temporale
5. **Output** — Hypothesis cards con score, p-value, lag, confidence interval

## MVP Scope (COMPLETATO)
- [x] Ingestione da 2 fonti (FRED + World Bank)
- [x] 49 serie FRED curate (economia, mercati, commodity, lavoro, housing)
- [x] MI screening su tutte le coppie
- [x] Granger causality sulle coppie sopravvissute
- [x] FDR correction (Benjamini-Hochberg)
- [x] Out-of-sample temporal validation
- [x] Output: hypothesis cards con score, p-value, lag, fonti
- [x] Smoke test 5/5 PASS, golden snapshot L4 approvato

## Post-MVP (roadmap F5)
- [ ] Scaling a 500+ variabili (FRED + World Bank + Eurostat)
- [ ] Proprietary trading: backtest + paper trading su segnali causali
- [ ] API pubblica (FastAPI) con free tier
- [ ] Dashboard interattiva (Plotly)
- [ ] DAG discovery (PC algorithm)
- [ ] Transfer entropy (non-linear)
- [ ] LLM plausibility scoring
- [ ] Scaling a 50K+ variabili

## Oracoli di Dominio
- L2: Correlazioni note in letteratura (oil → CPI, Fed Funds → Unemployment, Okun's Law)
- L5: Relazioni FRED note che il sistema deve riscoprire senza hint (5 validate in test)

## Monetizzazione: 4.5/5 (rivista dopo ricerca mercato marzo 2026)
1. **Mercato ampio**: hedge funds (2000+), consulenze, accademici, gov — SI
2. **Bisogno ricorrente**: dati cambiano continuamente, nuove relazioni emergono — SI
3. **Difendibilita'**: pipeline + brand + community, ma algoritmi replicabili — PARZIALE
4. **Scalabilita'**: funziona globalmente, cross-settore per design — SI
5. **WTP**: hedge funds spendono media $1.6M/anno in alt data — SI

## Strategia Multi-Verticale (Business Plan marzo 2026)

### Verticali (in ordine di priorita')
0. **Proprietary trading** — Uso diretto dei segnali causali per investimenti personali. ROI piu' alto, zero clienti necessari, validazione definitiva del motore
1. **Finanza/Trading** — TAM $7-10B, WTP altissima, competizione intensa
2. **Consulenza strategica** — TAM $1-3B, consulenti rivendono insight ai clienti
3. **Ricerca accademica** — Basso revenue ma critico per credibilita'
4. **Intelligence/Gov** — TAM $3-5B, alto valore ma procurement lento
5. **Giornalismo dati** — Basso revenue, alto valore PR
6. **Policy/Governo** — Lento ma stabile, contratti pluriennali

### Modello Revenue: Ibrido (Subscription + Usage)
- Tier Free (top 100 verita') → Professional ($499/mo) → Enterprise ($2-10K/mo) → Data Licensing ($50-500K/anno)
- Proprietary trading come revenue stream #0 (bootstrapping)

### Sequenza di Lancio
- Fase 0 (mesi 0-3): Proprietary trading (backtest + paper trading) + credibilita' (open source + paper)
- Fase 1 (mesi 3-6): Validazione trading + community
- Fase 2 (mesi 6-12): Tier Professional, API pubblica
- Fase 3 (mesi 12-24): Enterprise
- Fase 4 (mesi 24-36): Data licensing, gov, scaling 50K+ variabili

> Business plan completo: `.claude/plans/vast-crunching-flurry.md`

## Autonomia AI: ~70%
- Alto: pipeline di ingestione, statistical screening, implementazione algoritmi noti, test
- Medio: tuning filtri FDR/OOS, scelta soglie, interpretazione risultati
- Basso: validazione dominio-specifica delle verita', decisioni di business/trading

## Rischi
1. **Correlazioni spurie** → FDR + OOS + disclaimer + review umana (CRITICO per credibilita')
2. **Overfitting segnali trading** → OOS validation rigorosa, walk-forward, mai ottimizzare su test set
3. **Perdita capitale trading** → Paper trading 3 mesi, micro-posizioni (1-5%), stop loss
4. **API fonti cambiano** → Cache aggressiva, multi-fonte per indicatore
5. **Non-stazionarieta'** → Test ADF + differenziazione (implementato)
6. **Bus factor = 1** → Open source + documentazione + community

## Verifica (73 test)
- L1 unit: 46 test (storage, stationarity, MI, Granger, FDR, OOS)
- L2 oracle: 11 test con `# SOURCE:` da fonti esterne
- L3 property-based: 6 test (Hypothesis)
- L5 real data: 10 test (5 relazioni FRED note + 5 stats pipeline)
- M4 cross-tool: verify/ con alt_mi + alt_granger (15/16 match)
- Lint: ruff clean
- Smoke: 5/5 PASS, L4 golden snapshot approvato

## Status
- F0: DONE (2026-03-20)
- F1: DONE — ricerca competitor, oracoli identificati, scope approvato
- F2: DONE — architettura, verified-deps.toml, smoke test definito
- F3: DONE — 14 subtask completati (ST-01 → ST-14), 73 test
- F4: DONE — L1-L5 verificati, M4 cross-tool, golden snapshot approvato
- **F5: IN CORSO** — business plan completato, prossimo: discovery reale 500+ variabili + backtest trading
