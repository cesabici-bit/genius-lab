# EMI Scout — Kit Pre-Compliance EMI Testing con AI

## Dominio
Electronics / EMC Testing / Hardware + Software

## Descrizione
Kit a $999 (vs $27K+) per test EMI pre-compliance: ricevitore SDR, sonde near-field calibrate, software AI che interpreta le emissioni e suggerisce fix specifici al PCB ("picco a 48MHz dal SPI clock — aggiungi ferrite su MOSI").

## Il Problema
Ogni prodotto elettronico deve passare FCC/CE prima della vendita. Test in lab accreditato: $5K-15K/sessione. 50%+ delle startup hardware fallisce al primo test. Attrezzatura pre-compliance in casa: $27K+. Le startup non hanno modo di verificare prima.

## Target Users
- Hardware startup (50K+ globalmente)
- Piccoli produttori elettronici
- Consulenti EMC
- Lab universitari di elettronica

## Monetizzazione (Score: 4.5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 3/5 | 50K hardware startup. Nicchia ma in crescita |
| Bisogno ricorrente | 4/5 | Ogni nuovo prodotto richiede test. SaaS mensile |
| Difendibilita' | 5/5 | Database pattern EMI -> cause -> fix. Migliora con ogni utente |
| Scalabilita' | 5/5 | FCC (US) + CE (EU) + qualsiasi mercato |
| WTP | 5/5 | Risparmia $10K-$30K per test fallito. ROI immediato |

### Revenue Model
- Hardware kit: $999 (BOM ~$250)
- SaaS: $49/mese per analisi AI, database fix, aggiornamenti limiti normativi
- Report pre-compliance: $99 ciascuno (PDF formattato per lab)
- Training: corso online "Pass FCC/CE First Time" $299

## Stack Tecnico
- Hardware: Airspy HF+ SDR ($170), sonde near-field custom (loop filo), comb generator calibrazione
- Software: Python (SciPy FFT, Plotly/Matplotlib), AI analysis (LLM fine-tuned o expert system)
- Database: limiti FCC Part 15, EN 55032, pattern EMI noti

## Angolo Accademico
Paper su ML per classificazione automatica sorgenti EMI da spettro near-field.

## MVP Timeline
~3-4 mesi (SDR + sonde + analisi spettrale base). AI guidance +2-3 mesi.

## Rischi
- Dynamic range SDR economici limita accuratezza (mitigazione: caratterizzazione incertezza)
- Risultati pre-compliance != certificazione ufficiale (disclaimer chiaro)
- Richiede conoscenza EMC per validare i suggerimenti AI

## Competitor
- Rohde & Schwarz FPC1500: $5,500 solo analyzer, no AI
- Signal Hound SM200C: $3,400, no software EMC
- Tekbox sonde: $200 solo sonde, no receiver
- RF Explorer: $300 handheld, bandwidth limitata
- **GAP**: nessuno combina SDR affordable + sonde calibrate + AI-guided EMC analysis <$1K

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
