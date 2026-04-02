# SeismoCheck

## Open-Source Code-Compliant Seismic Assessment Pipeline

**Tier:** B — Originale con Gap di Mercato
**Status:** F0 Setup
**Monetizzazione:** 4.5/5 — open-source core + SaaS reports/GUI

---

## Contesto 2026

- Italia, Grecia, Turchia, America Latina: verifica sismica obbligatoria, milioni di edifici pre-normativa
- SAP2000/ETABS costano $3.000-$10.000+ licenza, SeismoBuild €800-5.500
- OpenSees è gratis ma inutilizzabile per professionisti: no GUI, no code compliance, no report
- Nessun tool open-source fa: modello edificio → analisi sismica → verifica normativa → report PDF
- 15+ GUI per OpenSees sviluppate dalla community, nessuna ha raggiunto adozione mainstream
- CSI è passata a licensing cloud-only da luglio 2025 (subscription obbligatoria)
- Paper su OpenSees GUI pubblicato su Nature Scientific Reports (2025)

## Cosa Costruiamo

Pipeline open-source per verifica sismica: dal modello dell'edificio al report tecnico conforme NTC 2018/EC8/ASCE 41.

**In una frase:** "Descrivi il tuo edificio in YAML, ottieni analisi modale, spettro di progetto, verifiche normative e relazione tecnica PDF — tutto automatico, open-source, validato."

## Gap di Mercato Verificato

| Capacità | SAP2000/ETABS | SeismoBuild | OpenSees | PyNite | **SeismoCheck** |
|----------|--------------|-------------|----------|--------|----------------|
| Analisi modale | ✅ | ✅ | ✅ | ❌ | ✅ |
| Pushover | ✅ | ✅ | ✅ | ❌ | ✅ (v0.2) |
| Spettro normativo | ✅ (100+ codici) | ✅ | ❌ | ❌ | ✅ (NTC/EC8/ASCE) |
| Verifiche automatiche | ✅ | ✅ | ❌ | ❌ | ✅ |
| Report PDF | ✅ | ✅ | ❌ | ❌ | ✅ |
| Indice di rischio | ❌ | ✅ | ❌ | ❌ | ✅ |
| Gratuito | ❌ ($3K-10K) | ❌ (€800-5.5K) | ✅ | ✅ | ✅ |
| Python API | ❌ | ❌ | ✅ (OpenSeesPy) | ✅ | ✅ |

## Utenti Target

1. **Piccoli studi di ingegneria** — in zone sismiche (Italia, Grecia, Turchia, LATAM), non possono permettersi SAP2000
2. **Studenti e ricercatori** — verifica sismica senza licenze costose
3. **Ingegneri comunali** — valutazione stock edilizio a scala urbana
4. **Team post-terremoto** — rapid assessment sul campo
5. **Professori** — didattica ingegneria sismica con tool reale

## Stack Tecnico

| Componente | Tecnologia | Versione | Motivo |
|-----------|-----------|---------|--------|
| Core library | Python | 3.12+ | Ecosistema scientifico |
| FEM computation | NumPy + SciPy | latest | Eigenvalue, linear FEM |
| Nonlinear FEM | OpenSeesPy | latest | Pushover/time-history (v0.2+) |
| Visualization | Matplotlib | latest | Mode shapes, pushover curves |
| Reports | reportlab | latest | Relazione tecnica PDF |
| Model input | PyYAML | latest | Building model format |

## Roadmap

| Fase | Versione | Cosa | Valore |
|------|----------|------|--------|
| F3a | **v0.1 (MVP)** | Model loader + linear FEM + modal + spectrum NTC/EC8/ASCE + checks + report PDF | Verifica sismica lineare in Python |
| F3b | **v0.2** | Pushover (OpenSeesPy) + Capacity Spectrum Method + N2 | Analisi non lineare |
| F3c | **v0.3** | EC8 Part 3 + ASCE 41 compliance | Copertura normativa EU + USA |
| F3d | **v0.4** | Time-history + steel structures | Analisi avanzate |
| F3e | **v0.5** | Masonry + building typology templates | Patrimonio edilizio italiano |
| F3f | **v0.6** | Retrofitting suggestions + GUI web | Tool completo |

## Oracoli di Dominio

| Livello | Fonte | Uso |
|---------|-------|-----|
| L2 | Chopra "Dynamics of Structures" | Verifica analisi modale |
| L2 | NTC 2018 / EC8 tabulated spectrum values | Verifica spettro di progetto |
| L2 | FEMA P-695 / NIST GCR 10-917-8 | Verifica pushover |
| L5 | PEER Benchmark Building (Report 2007-12) | Validazione end-to-end |
| L5 | L'Aquila 2009 / Emilia 2012 damage surveys | Confronto rischio vs danno reale |
| L5 | PEER NGA-West2 (21K+ records) | Validazione time-history |

## Pre-mortem

1. **OpenSeesPy dependency instability** → mitigation: linear-only mode senza OpenSees per v0.1
2. **Responsabilità su correttezza strutturale** → mitigation: disclaimers + "verification tool, not design tool"
3. **Complessità normativa (NTC ha centinaia di clausole)** → mitigation: MVP con subset critico (verifiche a taglio, flessione, duttilità)

## Fonti

- [OpenSees at PEER Berkeley](https://peer.berkeley.edu/opensees)
- [SeismoStruct Pricing](https://seismosoft.com/product/seismostruct/)
- [PEER NGA-West2 Database](https://ngawest2.berkeley.edu/)
- [PEER Benchmark Building Report 2007-12](https://peer.berkeley.edu/publications/2007-12)
- [OpenSees GUI — Nature Scientific Reports (2025)](https://www.nature.com/articles/s41598-025-17632-8)
- [WCEE2024 Milan](https://www.wcee2024.it/)
- [Structural Engineering Software Market (WiseGuyReports)](https://www.wiseguyreports.com/reports/structural-engineering-software-market)
