# ClimaFin

## Open-Source Climate Financial Risk Assessment Pipeline

**Tier:** B — Originale con Gap di Mercato
**Status:** F0 Setup
**Monetizzazione:** 4.5/5 — open-source core + SaaS layer

---

## Contesto 2026

- EU CSRD in vigore: ~50.000 aziende devono fare climate risk disclosure (2025-2026 wave)
- ISSB S2 adottato globalmente, California climate disclosure da gennaio 2026
- Tool commerciali costano €100K+/anno (MSCI Climate VaR, Moody's, S&P Trucost)
- EIOPA ha esplicitamente chiesto tool open-source per rischio climatico
- Nessun tool open-source va da portfolio → scenario analysis → financial risk → report TCFD/CSRD
- CLIMADA (ETH Zurich) fa solo rischio fisico. OS-Climate è frammentato e immaturo
- Mercato ESG software: $2.1B (2025) → $4.4B (2030), CAGR 16%

## Cosa Costruiamo

Pipeline open-source end-to-end per climate financial risk assessment con reporting normativo.

**In una frase:** "Carica il tuo portfolio, scegli gli scenari climatici NGFS, ottieni Climate VaR e report TCFD/CSRD/ISSB S2 — trasparente, auditabile, gratuito."

## Gap di Mercato Verificato

| Capacità | MSCI Climate VaR | Moody's | CLIMADA | OS-Climate | **ClimaFin** |
|----------|-------------------|---------|---------|------------|-------------|
| Transition risk | ✅ | ✅ | ❌ | Parziale | ✅ |
| Physical risk | ✅ | ✅ | ✅ | Parziale | ✅ (via CLIMADA) |
| NGFS scenarios | ✅ | ✅ | ❌ | ✅ | ✅ |
| Climate VaR | ✅ | ✅ | ❌ | ❌ | ✅ |
| TCFD report | ✅ | ✅ | ❌ | ❌ | ✅ |
| CSRD ESRS E1 | Parziale | Parziale | ❌ | ❌ | ✅ |
| Trasparente/Auditabile | ❌ | ❌ | ✅ | ✅ | ✅ |
| Gratuito | ❌ (€100K+/yr) | ❌ (€100K+/yr) | ✅ | ✅ | ✅ |

## Utenti Target

1. **Corporate per CSRD** — prima volta che fanno climate disclosure, non hanno budget per MSCI
2. **SME quotate (2026)** — ~38.000 aziende EU, budget ESG minimo
3. **Asset manager** — portfolio climate risk per SFDR/TCFD reporting
4. **Ricercatori accademici** — metodologie riproducibili e trasparenti
5. **Banche** — stress test climatici (NGFS scenarios), trasparenza per regolatori

## Stack Tecnico

| Componente | Tecnologia | Versione | Motivo |
|-----------|-----------|---------|--------|
| Core library | Python | 3.12+ | Ecosistema scientifico + geospaziale |
| Climate data | xarray | latest | Multi-dimensional NetCDF data |
| Geospatial | geopandas + rasterio | latest | Asset-level geospatial analysis |
| Scenarios | pyam | latest | NGFS/IIASA scenario data access |
| Physical hazards | CLIMADA | latest | ETH Zurich hazard engine |
| Computation | NumPy + SciPy | latest | Standard scientifico |
| Reports | reportlab/weasyprint | latest | PDF/HTML report generation |

## Roadmap

| Fase | Versione | Cosa | Valore |
|------|----------|------|--------|
| F3a | **v0.1 (MVP)** | NGFS scenarios + transition risk + basic physical risk + Climate VaR + TCFD report | Climate risk assessment in Python |
| F3b | **v0.2** | CSRD ESRS E1 + ISSB S2 + multi-scenario comparison | Compliance reporting |
| F3c | **v0.3** | Granular physical risk + interactive dashboard | Asset-level analysis |
| F3d | **v0.4** | Credit risk adjustment + multi-currency | Valore per banche |
| F3e | **v0.5** | Sector-specific models + adaptation cost-benefit | Tool completo |
| F3f | **v0.6** | API backend + SaaS layer | Monetizzazione |

## Oracoli di Dominio

| Livello | Fonte | Uso |
|---------|-------|-----|
| L2 | NGFS Scenarios V5.0 Technical Documentation | Verifica scenario engine |
| L2 | UNEP FI Pilot Study Results | Cross-check financial translation |
| L2 | Bank of England scenario methodology (2024) | Verifica Climate VaR |
| L5 | Public TCFD reports (Shell, BP, BNP Paribas) | Confronto con report reali |
| L5 | CLIMADA published case studies | Validazione physical risk |
| L5 | NGFS Climate Impact Explorer | Confronto indicatori macro |

## Pre-mortem

1. **Scope creep su physical risk geospaziale** → mitigation: MVP su transition risk, physical risk via CLIMADA integration
2. **Dati NGFS cambiano formato tra versioni** → mitigation: abstraction layer su pyam
3. **Normative evolvono rapidamente** → mitigation: modular reporting engine, update incrementali

## Fonti

- [IFRS S2 Climate-related Disclosures](https://www.ifrs.org/issued-standards/ifrs-sustainability-standards-navigator/ifrs-s2-climate-related-disclosures/)
- [EIOPA - Open-source Tools for Climate Change Risks](https://www.eiopa.europa.eu/tools-and-data/open-source-tools-modelling-and-management-climate-change-risks_en)
- [NGFS Scenarios Portal](https://www.ngfs.net/ngfs-scenarios-portal/)
- [CLIMADA - ETH Zurich](https://climada.ethz.ch/)
- [OS-Climate physrisk (GitHub)](https://github.com/os-climate/physrisk)
- [UNEP FI - Climate Risk Tool Dashboard](https://www.unepfi.org/themes/climate-change/the-sustainability-risk-tool-dashboard/)
- [ESG Software Market (Grand View Research)](https://www.grandviewresearch.com/industry-analysis/esg-software-market-report)
