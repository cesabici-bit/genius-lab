# AirComply — Monitor IAQ Compliance-Grade per LEED v5 / WELL v2

## Dominio
Building Compliance / IoT / Hardware + Software

## Descrizione
Sensore IAQ a $199 (vs $800-1200) con CO2, PM2.5, TVOC, temp/umidita'. Software genera automaticamente report LEED v5 e WELL v2, gestisce audit trail e calibrazione. Il sensore piu' economico che soddisfa i requisiti di certificazione.

## Il Problema
LEED v5 (aprile 2025) e WELL v2 richiedono monitoraggio continuo IAQ con intervalli specifici, soglie, e reporting. Sensori compliance-grade costano $800-1200 (Kaiterra). Sensori consumer ($50-100) non hanno audit trail ne' reporting certificato. Il 75% degli edifici medi non ha monitoraggio. Violazioni: multa da $10K+.

## Target Users
- Proprietari/gestori edifici che cercano LEED/WELL
- Contractor HVAC e commissioning agents
- Corporate real estate (ESG)
- Co-working, scuole, ospedali
- Consulenti ambientali

## Monetizzazione (Score: 4.5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 5/5 | $5.19B IAQ market. 6B+ sq ft sotto WELL |
| Bisogno ricorrente | 5/5 | Monitoring continuo + calibrazione periodica |
| Difendibilita' | 5/5 | Certificazione compliance (RESET Air), audit trail, template LEED/WELL |
| Scalabilita' | 4/5 | Globale ma norme diverse per paese (LEED/WELL sono internazionali) |
| WTP | 4/5 | Obbligatorio per certificazione. $199 vs $800 = risparmio enorme |

### Revenue Model
- Hardware: $199/sensore (BOM ~$58)
- SaaS: $19/sensore/mese (dashboard, report, alert, calibrazione)
- Bundle certificazione: $499/edificio (template + documentazione)
- Edificio 50 sensori: $9,950 hardware + $950/mese ricorrente

## Stack Tecnico
- Hardware: ESP32-S3, Sensirion SCD41 (CO2), SPS30 (PM2.5), SGP41 (TVOC), BME280
- Firmware: C/Arduino (ESP-IDF)
- Backend: FastAPI, PostgreSQL (audit trail)
- Frontend: React dashboard
- Report: generazione PDF automatica formato LEED/WELL

## Angolo Accademico
Paper validazione sensori low-cost vs reference instruments. Contributo a standard IAQ monitoring.

## MVP Timeline
~2.5 mesi. Compliance reporting completo in mese 4.

## Rischi
- Calibrazione NIST-tracciabile richiede investimento iniziale (~$2K reference instruments)
- Certificazione RESET Air richiede processo formale (tempo)
- Sensori Sensirion hanno lead time variabile

## Competitor
- Kaiterra Sensedge: $800-1200. RESET certified. Troppo caro per piccoli edifici
- Awair Omni: ~$400. Consumer-grade reporting, no template LEED
- PurpleAir: $229. Outdoor-focused, no compliance features
- **GAP**: nessun device sub-$250 con reporting LEED v5/WELL v2 built-in

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
