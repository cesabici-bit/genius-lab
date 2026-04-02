# SpectraForge — Piattaforma Modulare Open-Source per Strumenti da Laboratorio

## Dominio
Scientific Instruments / Hardware + Software

## Descrizione
Piattaforma modulare con base unica (Raspberry Pi 5 + PCB custom) e moduli intercambiabili: spettrofotometro, fluorimetro, turbidimetro, colorimetro, plate reader. Software professionale con calibrazione, audit trail GLP, integrazione LIMS, API Python.

## Il Problema
Un lab universitario o startup biotech paga $10K-$50K per strumento (Thermo Fisher, Agilent). I progetti open-source esistenti sono one-off senza piattaforma unificata ne' software professionale.

## Target Users
- Lab universitari (150K+ globalmente)
- Biotech/pharma startup
- Lab ambientali in paesi in via di sviluppo
- Community bio lab (300+ globalmente)

## Monetizzazione (Score: 4.5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 4/5 | 50K+ lab underserved. TAM $67M+ |
| Bisogno ricorrente | 4/5 | Consumabili + SaaS calibrazione + nuovi moduli |
| Difendibilita' | 5/5 | Piattaforma + software ecosystem. Hardware copiabile, ecosystem no |
| Scalabilita' | 5/5 | Globale, qualsiasi disciplina scientifica |
| WTP | 4/5 | Lab abituati a pagare per strumenti. $350 vs $15K = no-brainer |

### Revenue Model
- Hardware: base $200, moduli $50-150 (BOM ~$170, margine ~50%)
- SaaS: $29/mese per lab (calibrazione cloud, dashboard multi-strumento)
- Certificazione: protocolli calibrazione pre-validati $199/anno
- Consumabili: cuvette, standard di calibrazione

## Difendibilita'
Ogni modulo validato contro strumento commerciale = paper pubblicabile. L'ecosistema software (calibrazione certificata, audit trail, LIMS, API Python) e' il vero moat. Network effect: piu' moduli = piu' valore per chi ha gia' la base.

## Stack Tecnico
- Hardware: Raspberry Pi 5, PCB custom (KiCad), 3D print (PLA), componenti ottici (LED, fotodiodi, CMOS)
- Firmware: Python (RPi)
- Backend: FastAPI, SQLite/DuckDB
- Frontend: React dashboard
- ADC: ADS1115 o MCP3424 (16-24 bit)

## Angolo Accademico
Ogni modulo = paper ("Low-cost open-source X achieves R2=0.99X against [commercial equivalent]"). Massima credibilita' per costo minimo.

## MVP Timeline
~2 mesi per base + primo modulo (spettrofotometro). Un nuovo modulo ogni 6-8 settimane.

## Rischi
- Calibrazione accurata richiede reference standard (investimento una tantum ~$500-2K)
- Per usi regolamentati (pharma), serve validazione formale (lungo)
- Supporto hardware piu' complesso del puro software

## Competitor
- Thermo Fisher, Agilent, Shimadzu: $10K-$100K, non competitor diretti (fascia diversa)
- OpenPCR ($499): singola funzione, no piattaforma
- Hackuarium simple-spectro: hobbyist, no software professionale
- **GAP**: nessuno combina modularita' open hardware + software professionale + validazione scientifica

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
