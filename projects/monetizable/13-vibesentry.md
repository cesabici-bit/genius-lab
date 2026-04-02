# VibeSentry — Manutenzione Predittiva Affordable per PMI

## Dominio
Industrial IoT / Predictive Maintenance / Hardware + Software

## Descrizione
Sensori vibrazione+acustica a $89/nodo (vs $500-2000 enterprise) con ESP32-S3, MEMS accelerometro, MEMS microfono, edge ML (TinyML), mesh LoRa per fabbriche senza WiFi. Dashboard cloud con alert e predizioni di guasto.

## Il Problema
PMI manifatturiere (5-50 macchine) fanno run-to-failure: aspettano che pompe, motori, compressori si rompano. Downtime non pianificato costa 3-5% del fatturato. Sistemi enterprise (Augury, SKF) costano $100K+ per impianto — fuori budget per una fabbrica con 20 dipendenti.

## Target Users
- PMI manifatturiere (250K+ solo in EU)
- Officine meccaniche, food processing, falegnamerie
- Manutenzione HVAC edifici commerciali
- Facility manager

## Monetizzazione (Score: 4.5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 5/5 | $14B PdM market. Segmento PMI $2-3B |
| Bisogno ricorrente | 5/5 | Monitoring continuo, SaaS mensile |
| Difendibilita' | 5/5 | Edge ML migliora con dati. LoRa mesh per ambienti industriali |
| Scalabilita' | 4/5 | Globale. Qualsiasi macchina rotante |
| WTP | 4/5 | ROI chiaro: costo downtime >> costo sensori |

### Revenue Model
- Hardware: $89/nodo (BOM ~$25), gateway $149 (BOM ~$45), starter kit 10 nodi $799
- SaaS: $15/nodo/mese (dashboard, alert, ML predictions)
- Servizi: setup on-site + calibrazione baseline $500-1500/fabbrica
- 100 clienti x 20 nodi: $178K hardware + $360K ARR

## Stack Tecnico
- Hardware: ESP32-S3, ICM-42688 accelerometro, ICS-43434 microfono, SX1276 LoRa
- Firmware: C/Arduino (ESP-IDF), TensorFlow Lite Micro
- Backend: FastAPI, TimescaleDB
- Frontend: React + Plotly
- ML training: CWRU Bearing Dataset, MAFAULDA (pubblici)

## Angolo Accademico
Paper su edge ML anomaly detection con MEMS su ESP32. Validazione contro dataset noti (CWRU).

## MVP Timeline
~3 mesi (singolo sensore + dashboard). Mesh LoRa mese 4-5.

## Rischi
- Ambienti industriali ostili (vibrazioni, temperature, polvere) — serve enclosure IP65
- LoRa in ambienti metallici richiede tuning antenna
- Calibrazione iniziale per ogni tipo di macchina

## Competitor
- Augury: enterprise, $100K+. Raised $300M+
- SKF Enlight: premium pricing
- Seeed Studio kit: $30 componente, no prodotto (no ML, no mesh, no dashboard)
- Tractian: mid-market ma ancora costoso
- **GAP**: turnkey, affordable, SME-targeted con edge ML + mesh

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
