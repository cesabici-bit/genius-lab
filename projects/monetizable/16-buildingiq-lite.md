# BuildingIQ Lite — AI Energy Optimization per Edifici Commerciali Medi

## Dominio
Building Energy / IoT / Hardware + Software

## Descrizione
Gateway a $299 che si collega al BMS esistente via BACnet/Modbus. Impara pattern occupazione e caratteristiche termiche dell'edificio. Usa reinforcement learning per ottimizzare schedule HVAC autonomamente. Target: 75% degli edifici medi (1000-5000 m2) che non hanno alcuna ottimizzazione.

## Il Problema
Il 75% degli edifici commerciali medi non ha sistema di ottimizzazione energetica. HVAC funziona con timer fissi, sprecando 20-30% energia. Sistemi enterprise (Honeywell, Siemens, Johnson Controls) costano $50K-200K e richiedono installazione professionale. Per un ufficio di 2000 m2 non ha senso economico.

## Target Users
- Property manager e facility manager
- Proprietari edifici commerciali (uffici, retail, scuole)
- Corporate real estate (ESG mandates)
- HVAC contractor

## Monetizzazione (Score: 4/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 5/5 | 5.9M edifici commerciali solo US. $8.4B building energy mgmt |
| Bisogno ricorrente | 5/5 | Ottimizzazione continua, report mensili |
| Difendibilita' | 5/5 | RL model specifico per edificio + integrazione BACnet/Modbus |
| Scalabilita' | 4/5 | Globale ma norme HVAC diverse per paese |
| WTP | 4/5 | Savings-sharing model: paghi solo se risparmi |

### Revenue Model
- Gateway hardware: $299 (BOM ~$80)
- SaaS: $149/edificio/mese (ottimizzazione, dashboard, report energia)
- Savings-sharing alternativo: 20% dei risparmi energetici verificati
- Upsell: sensori occupazione aggiuntivi, integrazione fotovoltaico

## Stack Tecnico
- Hardware: Raspberry Pi 4/5 + interfaccia BACnet (BAC0 library) / Modbus (pymodbus)
- Backend: FastAPI, PostgreSQL
- ML: Reinforcement Learning (Stable Baselines3), thermal model dell'edificio
- Frontend: React dashboard con visualizzazione risparmi

## Angolo Accademico
Paper su RL per ottimizzazione HVAC in brownfield buildings — area di ricerca attiva.

## MVP Timeline
~12-16 settimane. Piu' lungo perche' richiede accesso a edificio reale per validare.

## Rischi
- Accesso a edificio reale per testing (mitigazione: partnership con facility manager locale)
- BACnet/Modbus hanno molte varianti/implementazioni (integrazione complessa)
- Responsabilita' se il RL causa discomfort occupanti
- MVP piu' lungo di progetti pure software

## Competitor
- Honeywell, Siemens, JCI: enterprise $100K+
- 75F (acquisita JCI): mid-market ma $10K+ iniziale
- Facilio: cloud-based, enterprise-focused
- **GAP**: sub-$500 entry point per edifici medi, self-installable

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
