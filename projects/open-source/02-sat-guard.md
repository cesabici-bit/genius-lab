# SatGuard

## Open-Source Conjunction Assessment + 3D Orbital Visualization

**Tier:** B — Originale con Gap di Mercato
**Status:** F0 Setup
**Monetizzazione:** 2/5 — credibilità accademica/spaziale → open source

---

## Contesto 2026

- 30.000+ oggetti tracciati in orbita, milioni non tracciati
- Mega-costellazioni (Starlink 6.000+, OneWeb, Kuiper) stanno facendo esplodere il numero di congiunzioni
- Commercial Orbital Outpost nel MIT Top 10 Breakthrough 2026
- USA sta trasferendo conjunction assessment dal DoD al Dipartimento del Commercio (TraCSS)
- Nessuna pipeline open-source completa in Python per conjunction assessment
- NASA CARA pubblica algoritmi solo in MATLAB; Orekit è Java; poliastro non ha conjunction assessment

## Cosa Costruiamo

Pipeline open-source end-to-end per conjunction assessment + globo 3D interattivo con tutti gli oggetti in orbita.

**In una frase:** "Scrivi il NORAD ID del tuo satellite, ottieni screening congiunzioni, probabilità collisione, alert, e una mappa 3D di tutto ciò che orbita la Terra."

## Gap di Mercato Verificato

Nessun tool open-source fa tutto questo insieme:

| Capacità | NASA CARA | Orekit | poliastro | stuffin.space | LeoLabs | **SatGuard** |
|----------|-----------|--------|-----------|---------------|---------|-------------|
| Linguaggio | MATLAB | Java | Python | JS | Commerciale | Python + JS |
| TLE ingest | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Conjunction screening | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Pc calculation | ✅ | Parziale | ❌ | ❌ | ✅ | ✅ |
| CDM output | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Globe 3D | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Risk visualization | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gratuito | ✅ | ✅ | ✅ | ✅ | ❌ ($2.5K/mese/sat) | ✅ |

## Utenti Target

1. **Operatore SmallSat/CubeSat** — ha 1-5 satelliti, non ha STK, vuole sapere se è in pericolo
2. **Ricercatore/Dottorando** — scrive paper su conjunction assessment, vuole dati e metodi riproducibili
3. **Professore di Astrodynamica** — vuole visualizzazioni chiare per insegnare
4. **Startup spaziale (10-50 sat)** — non può permettersi LeoLabs, ha un ingegnere Python

## Stack Tecnico

| Componente | Tecnologia | Versione | Motivo |
|-----------|-----------|---------|--------|
| Core library | Python | 3.12+ | Ecosistema scientifico, target audience |
| Propagazione | sgp4 (Python) | latest | Implementazione ufficiale C++ con binding Python |
| Calcolo numerico | NumPy/SciPy | latest | Standard scientifico |
| Spatial indexing | scipy.spatial.KDTree | - | Screening O(N log N) |
| Visualizzazione 2D | Matplotlib | latest | Plot orbite, Pc evolution |
| Globe 3D | CesiumJS | latest | Standard per visualizzazione geospaziale, usato da NASA/ESA |
| Web frontend | React + Resium | latest | Binding React per CesiumJS |
| API backend | FastAPI | latest | Serve dati al globe, API per CLI |
| Core computazionale | Rust (futuro) | stable | Performance per screening batch (post-MVP) |
| Test PBT | Hypothesis | 6.151.9 | Property-based testing |

## Architettura

```
Space-Track.org / CelesTrak (dati gratuiti)
         │
         ▼
┌─────────────────┐
│  1. INGEST       │  TLE/GP elements via API + CDM
│                  │  Parsing formato CCSDS standard
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. PROPAGATE    │  SGP4 analitico + numerico opzionale
│                  │  Gestione covarianza (incertezza)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. SCREEN       │  Filtra coppie < soglia distanza
│                  │  Spatial indexing (k-d tree)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. ASSESS       │  Pc: Foster, Chan, Alfano, Monte Carlo
│                  │  Covariance realism assessment
└────────┬────────┘
         │
         ▼
┌─────────────────┐       ┌──────────────────────┐
│  5. OUTPUT       │──────▶│  6. GLOBE 3D          │
│  CDM, CSV, PDF   │       │  CesiumJS + React     │
│  Alert webhook   │       │  30K+ oggetti          │
│  CLI report      │       │  Click to inspect      │
└─────────────────┘       │  Conjunction view      │
                          │  Heatmap, filtri       │
                          │  Time slider           │
                          └──────────────────────┘
```

## Roadmap

| Fase | Versione | Cosa | Valore per l'utente |
|------|----------|------|---------------------|
| F3a | **MVP** | Library Python: ingest TLE + propagate SGP4 + screen + Pc (Foster, Chan, Alfano) + CDM output | "Posso fare conjunction assessment in Python" |
| F3b | **v0.2** | CLI + alert webhook + covariance assessment + Pc evolution tracking | "Posso automatizzare il monitoraggio" |
| F3c | **v0.3** | **Globe 3D (CesiumJS)**: tutti gli oggetti in orbita, click to inspect, filtri per tipo/owner/orbita | **"Il momento virale"** — porta d'ingresso visiva |
| F3d | **v0.4** | Globe: conjunction visualization 3D, heatmap densità, time slider, "show siblings" (frammenti stessa origine) | Didattica, wow factor, comunicazione |
| F3e | **v0.5** | Constellation screening batch + fleet.yaml + report PDF + compliance | Valore operativo per startup |
| F3f | **v0.6** | Maneuver planning + historical replay (Iridium-Cosmos 2009) | Tool completo |

## MVP Scope

### IN (MVP — v0.1)
- [ ] Ingest TLE da Space-Track.org e CelesTrak
- [ ] Propagazione SGP4 (libreria sgp4)
- [ ] Conjunction screening con spatial indexing
- [ ] Calcolo Pc: metodo Foster, Chan, Alfano
- [ ] Validazione Monte Carlo
- [ ] Output CDM formato CCSDS
- [ ] API Python pulita: `sg.Catalog`, `sg.screen()`, `sg.CollisionProb`
- [ ] CLI base: `satguard screen --norad-id XXXXX`

### OUT (post-MVP)
- Globe 3D (v0.3)
- Constellation management (v0.5)
- Maneuver planning (v0.6)
- Web dashboard con auth (v0.6+)
- Core Rust per performance (quando necessario)
- Integrazione space weather
- ML-based prediction (stile Kessler/Oxford)

## Oracoli di Dominio

| Livello | Fonte | Uso |
|---------|-------|-----|
| L2 (sanity) | Vallado "Fundamentals of Astrodynamics" 5th Ed — esercizi risolti (propagazione, orbital elements) | Verifica calcoli orbitali base |
| L2 (sanity) | Alfano 2005 "Numerical Implementation of Spherical Object Collision Probability" — valori tabulati | Verifica calcolo Pc |
| L2 (sanity) | NASA CARA Analysis Tools (MATLAB) — risultati di riferimento | Cross-check algoritmi Pc |
| L5 (reale) | CelesTrak SOCRATES — screening 3x/giorno, dati pubblici | Confronto output screening con riferimento operativo |
| L5 (reale) | CDM storici da Space-Track | Confronto Pc calcolati vs Pc ufficiali |
| L5 (reale) | Collisione Iridium 33 vs Cosmos 2251 (2009-02-10) — evento documentato | Replay e validazione end-to-end |

## Pre-mortem

1. **Dati Space-Track richiedono account** → mitigation: supportare anche CelesTrak (no login) come fallback
2. **SGP4 ha precisione limitata (km-level dopo giorni)** → mitigation: documentare limiti, offrire propagazione numerica opzionale
3. **Covarianze non disponibili nei TLE** → mitigation: covarianze stimate (empiriche), documentare che Pc senza covarianza reale è indicativo

## Competitor Reference

- **stuffin.space**: globe 3D open source con oggetti orbitali. Solo visualizzazione, zero analisi. SatGuard aggiunge il motore di conjunction assessment
- **NASA CARA Tools**: algoritmi Pc in MATLAB. SatGuard li porta in Python con pipeline completa
- **Orekit**: Java, feature-complete ma pesante. SatGuard è Python-native, leggero, Jupyter-friendly
- **caspy (UT Austin)**: screening Python ma scope limitato, poco mantenuto
- **LeoLabs**: $2.500/mese/satellite. SatGuard è gratuito
- **Kessler (Oxford/ESA)**: ML per predire CDM. Complementare, non competitore

## Fonti

- [MIT Breakthrough — Commercial Orbital Outpost](https://www.technologyreview.com/2026/01/12/1130697/10-breakthrough-technologies-2026/)
- [NASA CARA Homepage](https://www.nasa.gov/cara/)
- [NASA CARA_Analysis_Tools GitHub](https://github.com/nasa/CARA_Analysis_Tools)
- [Alfano 2005 — Collision Probability](https://link.springer.com/article/10.1007/BF03546397)
- [Balali et al. 2022 — Review of Pc Methods](https://link.springer.com/article/10.1007/s42064-021-0125-x)
- [CelesTrak SOCRATES](https://www.celestrak.org/SOCRATES/)
- [Hall et al. 2023 — Multistep Pc Algorithm](https://ntrs.nasa.gov/api/citations/20230010175/downloads/Hall_Baars_Casali_ASC_2023_08_13_PcMultiStep_Paper.pdf)
- [Vallado — Fundamentals of Astrodynamics, 5th Ed](https://astrobooks.com/vallado5hb.aspx)
- [caspy — UT Austin ASTRIA](https://github.com/ut-astria/caspy)
- [Kessler ML Library (ESA SDC8)](https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/226/SDC8-paper226.pdf)
