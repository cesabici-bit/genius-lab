# DepShield — ML-Powered Software Supply Chain Security

## Dominio
Developer Tools / Security / Pure Software

## Descrizione
Tool che genera SBOM automatici, monitora dipendenze per attacchi supply chain (typosquatting, dependency confusion, pacchetti malevoli), e usa ML per triage intelligente — riduce 80% falsi positivi classificando alert per rischio reale nel contesto del progetto.

## Il Problema
Attacchi supply chain software +156% YoY. EU Cyber Resilience Act rende SBOM obbligatorio dal 2026. Tool enterprise (Snyk, Checkmarx) costano $50K+/anno e generano 10K+ alert/mese con 63% falsi positivi. Team piccoli senza security dedicato non gestiscono il volume.

## Target Users
- Team sviluppo 10-200 dev senza security team dedicato
- Startup SaaS
- Agenzie di sviluppo software
- Aziende EU che devono conformarsi a CRA 2026

## Monetizzazione (Score: 4.5/5)

| Criterio | Score | Note |
|----------|-------|------|
| Mercato ampio | 5/5 | 30M+ dev globalmente. $3.5B supply chain security market |
| Bisogno ricorrente | 5/5 | Monitoring continuo, nuove CVE ogni giorno |
| Difendibilita' | 4/5 | ML triage migliora con dati utenti (network effect) |
| Scalabilita' | 5/5 | Qualsiasi linguaggio, qualsiasi team, globale |
| WTP | 4/5 | SBOM obbligatorio EU crea domanda. Snyk ha dimostrato WTP |

### Revenue Model
- Free: 3 repo, SBOM base, scan settimanale
- Pro: $29/mese/repo (real-time monitoring, ML triage, CI/CD)
- Team: $199/mese unlimited (policy enforcement, compliance reports)

## Stack Tecnico
- Scanner: Rust (parsing lock file ad alta velocita')
- ML: Python (modello triage addestrato su NVD/OSV)
- SBOM: formato SPDX e CycloneDX
- Integrazioni: GitHub Actions, GitLab CI, npm, PyPI, Cargo
- Deploy: CLI + cloud service

## Angolo Accademico
Primo sistema ML-based per SBOM vulnerability triage — direzione inesplorata (confermato da survey arXiv 2025).

## MVP Timeline
~8-10 settimane. Pure software.

## Rischi
- Snyk/GitHub Dependabot potrebbero aggiungere ML triage (mitigazione: muoversi veloce, open-core)
- Qualita' ML dipende da dati di training (mitigazione: NVD/OSV pubblici + feedback utenti)
- Mercato affollato nel segmento enterprise, meno nel mid-market

## Competitor
- Snyk, Checkmarx: $50K+/anno, enterprise
- OWASP Dependency-Check: free, no ML, alti falsi positivi
- Socket.dev: npm/PyPI focused, no SBOM lifecycle
- GitHub Dependabot: gratuito ma alert non triaged, molto rumore
- **GAP**: ML triage + SBOM compliance per <$200/mese non esiste

## Status
Da iniziare. Richiede F1 (ricerca) prima di codice.
