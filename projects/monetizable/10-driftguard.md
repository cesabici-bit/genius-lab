# DriftGuard — Spec-Free API Schema Drift Detection

## Dominio
Developer Tools / API Monitoring / Pure Software

## Descrizione
Engine Rust+Python che impara gli schema API dal traffico reale (zero-config, nessuna specifica OpenAPI necessaria), costruisce baseline comportamentali, e alerta quando la struttura cambia — prima che il downstream si rompa.

## Il Problema
Le app moderne dipendono da decine di API esterne. Quando un provider cambia silenziosamente la risposta (campo nullable, tipo cambiato, campo rimosso), il codice si rompe in produzione. I tool esistenti (Pact, OpenAPI validators) richiedono spec scritte a mano che diventano obsolete. Lo "schema drift" e' il bug piu' insidioso delle architetture a microservizi.

## Target Users
- Team backend/platform (10-100 dev)
- Aziende che consumano molte API esterne (fintech, e-commerce, SaaS integrator)
- Decision maker: Engineering Manager / VP Engineering

## Monetizzazione (Score: 5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 5/5 | 100K+ team. API monitoring market >$5B entro 2028 |
| Bisogno ricorrente | 5/5 | Monitoring continuo, alerts giornalieri |
| Difendibilita' | 4/5 | Behavioral learning unico. Nessun competitor spec-free |
| Scalabilita' | 5/5 | Qualsiasi team, qualsiasi linguaggio, qualsiasi API |
| WTP | 5/5 | Team gia' pagano $50-500/mese per API monitoring |

### Revenue Model
- Free: 3 endpoint, 7 giorni retention
- Pro: $49/mese/team (unlimited endpoint, 90 giorni, Slack/PagerDuty)
- Enterprise: $299/mese (SSO, audit log, custom integrations, SLA)

## Stack Tecnico
- Core: Rust (proxy/sniffer ad alte prestazioni)
- ML: Python (modello statistico baseline, anomaly detection)
- Integrazioni: Slack, PagerDuty, Datadog, GitHub Actions
- Deploy: Docker, self-hosted o cloud

## Angolo Accademico
Paper su behavioral schema inference da traffico API — approccio novel nel campo API testing/monitoring.

## MVP Timeline
~6-8 settimane. Pure software, nessun hardware.

## Rischi
- Adozione: team devono fidarsi di un proxy che osserva il traffico (mitigazione: mode sniffer log-only)
- Privacy: traffico API puo' contenere dati sensibili (mitigazione: analisi solo strutturale, no valori)
- Competizione potenziale da Datadog/New Relic se aggiungono feature simile

## Competitor
- Pact: contract testing, richiede spec + adozione bilaterale
- Specmatic: spec-first, stessi limiti
- Datadog Synthetic: monitora availability, non struttura schema
- **GAP documentato**: zero-config, spec-free structural drift detection NON ESISTE come prodotto

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
