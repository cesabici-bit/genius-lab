# GridPulse — Power Quality Monitor per PMI

## Dominio
Energy / Industrial IoT / Hardware + Software

## Descrizione
Monitor qualita' elettrica multi-punto a $249/nodo (vs $3K-15K) con pinze amperometriche non-invasive. Rileva sag, swell, armoniche (fino 63a), transient. ML correla anomalie PQ con salute equipment e quantifica sprechi in euro.

## Il Problema
Qualita' elettrica scadente causa danni silenziosi: motori surriscaldati, elettronica degradata, sprechi 2-5% bolletta. Analizzatori professionali (Fluke, Dranetz) costano $3K-15K per punto, sono portatili (non permanenti). PMI con 10-50 macchine non monitorano nulla — quando un PLC si brucia, non sanno che era un transiente notturno.

## Target Users
- Manifatture con macchine sensibili (CNC, saldatrici)
- Piccoli data center (100K+ globalmente)
- Edifici commerciali con equipment sensibile
- Elettricisti e energy auditor
- Installatori fotovoltaico+storage (PQ issues nuovi)

## Monetizzazione (Score: 4/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 4/5 | $12B+ power monitoring market |
| Bisogno ricorrente | 5/5 | Monitoring continuo, report mensili |
| Difendibilita' | 5/5 | ML correlazione PQ-equipment. Analog design complesso |
| Scalabilita' | 4/5 | Globale (50Hz EU / 60Hz US — due firmware) |
| WTP | 4/5 | Energy audit market $6B+. ROI quantificabile |

### Revenue Model
- Hardware: $249/nodo (BOM ~$70)
- SaaS: $29/nodo/mese (dashboard, ML anomaly detection, report)
- Energy audit report: $99/report automatico trimestrale
- 20 nodi/impianto: $4,980 hardware + $580/mese

## Stack Tecnico
- Hardware: ESP32-S3, ADS131M04 (24-bit ADC, 4ch, 32kSPS), SCT-013 split-core CT, circuito sensing tensione isolato
- Firmware: C (ESP-IDF), FFT on-device per armoniche
- Backend: FastAPI, TimescaleDB
- Frontend: React + Plotly (spettro armoniche real-time)
- ML: anomaly detection, correlazione eventi PQ con macchine

## Angolo Accademico
Paper su affordable PQ monitoring validato contro IEC 61000-4. ML per correlazione PQ-equipment health.

## MVP Timeline
~3-4 mesi. Armoniche +1 mese. ML correlazione +1-2 mesi.

## Rischi
- Analog design accurato per misure su rete 230V richiede competenza specifica
- Sicurezza elettrica: pinze split-core sono non-invasive (no contatto diretto), ma serve attenzione
- Certificazione UL/CE per prodotto connesso a rete (se non split-core puro)

## Competitor
- Fluke 1770: $6K-12K, portatile, singolo punto
- Dranetz HDPQ: $8K+, enterprise
- Sense: consumer $299, single-phase, no PQ analysis
- IoTaWatt: open-source, solo energia, no armoniche/transient
- **GAP**: affordable, permanente, multi-punto PQ con ML per PMI

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
