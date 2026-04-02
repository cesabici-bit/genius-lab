# CLAUDE.md — Genius Lab Portfolio

## Progetto

Portfolio di 20 progetti innovativi ordinati per qualità/impatto. Obiettivo: massima credibilità accademica/industriale, poi monetizzazione. Ogni progetto ha il suo file dettagliato in `projects/`.

## Struttura Cartella

```
genius-lab/
├── CLAUDE.md              # Questo file (workflow, meccanismi, regole)
├── templates/             # Template riusabili per ogni progetto
│   ├── PROJECT_CLAUDE.md.template
│   ├── verified-deps.toml.template
│   ├── KNOWN_ISSUES.md.template
│   ├── STATUS.md.template
│   └── Makefile.template
├── projects/
│   ├── README.md          # Riepilogo e tracking status con fasi
│   └── tier-b/            # Progetti con gap di mercato verificato
└── [project-name]/        # Cartelle codice per ogni progetto attivo
    ├── CLAUDE.md           # Specifico del progetto
    ├── verified-deps.toml  # M1: dependency lock
    ├── KNOWN_ISSUES.md     # Registro errori persistente
    ├── STATUS.md           # Continuita' tra sessioni
    └── Makefile            # con target check-all
```

## Meccanismi Anti-Allucinazione Strutturali (M1-M4)

> Le regole anti-allucinazione sono PRINCIPI. Questi sono i MECCANISMI che li forzano.

### M1: Dependency Lock (`verified-deps.toml`)

Ogni progetto ha un file `verified-deps.toml` che registra OGNI dipendenza dopo verifica web search:

```toml
[[dependency]]
name = "poliastro"
version = "0.18.0"
verified_date = "2026-03-12"
verified_via = "https://docs.poliastro.space/en/stable/"
methods_used = ["Orbit.from_classical", "Maneuver.hohmann"]
```

**REGOLA**: nessuna dipendenza nel codice senza entry verificata in questo file.

### M2: External Oracle Test Pattern

Ogni test non-triviale DEVE citare la fonte del valore atteso:

```python
def test_hohmann_transfer():
    """L2: Vallado, 'Fundamentals of Astrodynamics', 4th ed, Ex 6-1, p.327."""
    # SOURCE: Vallado p.327 — Expected delta-v: 3.935 km/s
    result = compute_hohmann(EARTH_ORBIT, MARS_ORBIT)
    assert abs(result.delta_v - 3.935) < 0.05
```

**REGOLA**: ogni test file deve avere almeno 1 test con `# SOURCE:` da oracolo esterno.

### M3: Smoke Before Unit

Sequenza obbligatoria per ogni modulo:
1. Scrivi UN smoke test E2E che produce output leggibile dall'umano
2. POI scrivi i unit test
3. POI property-based test

Lo smoke test diventa il golden snapshot (L4). Mai il contrario.

### M4: Two-Tool Verification (solo per progetti numerici)

Per SatGuard e QuantumBench: directory `verify/` con script che risolvono lo stesso problema usando tool/metodo diverso. CI confronta gli output.

### Oracoli di Dominio per Progetto

| Progetto | Oracoli L2 | Oracoli L5 |
|----------|-----------|-----------|
| SatGuard | Vallado 5th Ed (propagazione), Alfano 2005 (Pc tabulati), NASA CARA MATLAB | CelesTrak SOCRATES, CDM storici Space-Track, collisione Iridium-Cosmos 2009 |
| QuantumBench | Qiskit textbook, MaxCut risultati noti, OR-Tools reference | Paper IonQ/Ansys con dati |
| TinkerWorld | Rapier test suite, scenari fisici noti (moto proiettile) | Ispezione visiva utente |

---

## Workflow con Phase Gates

### Fase 0: Inizio Sessione (OGNI sessione)
1. Leggi `STATUS.md` del progetto
2. Leggi `KNOWN_ISSUES.md`
3. Leggi CLAUDE.md del progetto
4. Esegui `make check-all` per verificare stato
5. Comunica all'utente: "Riprendo da [X]. Prossimo: [Y]. Cambiamenti?"

### Fase 1: RICERCA
- Almeno 3 web search per competitor/stato dell'arte
- Identifica oracoli di dominio (fonti per L2/L5)
- Scrivi scope document (IN/OUT)
- **Gate**: utente approva scope

### Fase 2: ARCHITETTURA (Plan Mode, `Shift+Tab`)
- Definisci moduli e interfacce
- Verifica OGNI dipendenza via web search -> popola `verified-deps.toml`
- Definisci lo smoke test ("cosa vuol dire che funziona?")
- Pre-mortem: 3 cose che possono andare storte
- Decomponi in subtask con input/output/pass-fail
- **Gate**: utente approva architettura

### Fase 3: IMPLEMENTAZIONE (per ogni subtask)
1. Dichiara il subtask (input, output, pass/fail)
2. Scrivi smoke test o L2 test PRIMA (se applicabile)
3. Implementa il codice
4. Esegui `make check-all`
5. Mostra output all'utente
6. Commit solo dopo check-all verde
- **Gate subtask**: check-all passa + utente vede output
- **Gate fase**: tutti i subtask completi, smoke test produce output ispezionabile

### Fase 4: VERIFICA (5 livelli)
- L1: Unit test sui path critici
- L2: Almeno 3 test con valori da fonti esterne (con `# SOURCE:`)
- L3: Property-based test sulle invarianti core
- L4: Golden snapshot salvato, umano revisiona 1 volta
- L5: Confronto con dati reali (se disponibili)
- **Gate**: report di copertura dei 5 livelli. Utente approva snapshot L4.

### Fase 5: DEPLOY & PUBLISH
- README con installazione, uso, output esempio
- CI (GitHub Actions) con `check-all`
- License + CHANGELOG
- **Gate**: CI verde + README completo + OK utente

---

## Protocollo Correzione Errori

### Decision Tree

```
Errore trovato
|-- Dipendenza sbagliata (API inesistente)
|   -> Revert -> Web search API corretta -> Aggiorna verified-deps.toml -> Reimplementa
|-- Bug logico (formula sbagliata)
|   |-- 1 tentativo -> Fix + aggiungi test con oracolo esterno
|   +-- 2 tentativo fallito -> STOP -> /clear -> Rileggi spec -> Reimplementa da zero
|-- Difetto di design (astrazione sbagliata)
|   -> NON patchare -> Revert a ultimo checkpoint -> Plan Mode -> Ridisegna
+-- Problema di integrazione
    -> Scrivi integration test PRIMA -> Poi fixa l'interfaccia
```

### Error Class Registry

Ogni progetto ha `KNOWN_ISSUES.md` con analisi causa radice di ogni errore significativo.
Claude lo legge a inizio sessione per evitare errori ricorrenti.

---

## Continuita' tra Sessioni

Ogni progetto ha `STATUS.md` con: fase corrente, ultimo subtask, prossimo subtask, blockers, log sessioni.
- Ogni sessione INIZIA leggendo STATUS.md
- Ogni sessione FINISCE aggiornandolo

---

## Template per Progetto

Ogni progetto DEVE avere PRIMA di scrivere codice:

1. `CLAUDE.md` — progetto, stack verificato, architettura, scope, oracoli, subtask
2. `verified-deps.toml` — dependency lock (M1)
3. `KNOWN_ISSUES.md` — registro errori persistente
4. `STATUS.md` — stato per continuita' tra sessioni
5. `Makefile` con target `check-all` (types + lint + test + smoke + deps)

Template disponibili in `templates/`.

## Regole Anti-Allucinazione (Principi)

1. **NEVER guess library APIs**: Cerca sempre la documentazione reale via web search prima di usare una libreria. Se non trovi la doc, chiedi all'utente.
2. **NEVER fabricate URLs/endpoints**: Ogni URL deve essere verificato. Se non sei sicuro che esista, dillo.
3. **NEVER assume versions**: Controlla la versione attuale di ogni dipendenza prima di installarla.
4. **ALWAYS show sources**: Per ogni decisione tecnica non banale, indica la fonte (doc, paper, issue GitHub).
5. **FAIL FAST**: Se un approccio non funziona dopo 2 tentativi, fermarsi e ripensare. Non brute-forceare.
6. **CHECKPOINT**: Dopo ogni blocco logico significativo: esegui test, mostra output, attendi conferma.
7. **COMPUTE don't RECALL**: Mai generare valori numerici dalla "memoria". Ogni valore CALCOLATO o CITATO con fonte.

> I meccanismi strutturali (M1-M4) che forzano queste regole sono definiti sopra.

## Sistema di Verifica Errori

### Pre-coding checks:
- [ ] Dipendenze esistono e sono alla versione dichiarata?
- [ ] API/endpoint documentati e funzionanti?
- [ ] Nessun conflitto con dipendenze esistenti?

### Post-coding checks:
- [ ] Tutti i test passano?
- [ ] Nessun warning/error in console?
- [ ] Il codice fa ciò che la spec richiede? (non di più, non di meno)
- [ ] Nessuna vulnerabilità di sicurezza introdotta?
- [ ] L'output è verificabile dall'utente?

### Per ogni sessione di lavoro:
- [ ] Leggere il file progetto (`projects/tier-X/NN-nome.md`) PRIMA di iniziare
- [ ] Aggiornare status nel README dopo completamento
- [ ] Se si scoprono nuove info, aggiornare il file progetto

## Comandi Utili

```bash
# Struttura progetti
ls projects/tier-s/ projects/tier-a/ projects/tier-b/

# Status tracking
cat projects/README.md
```

## Stack Comuni

| Tool | Versione | Uso |
|------|---------|-----|
| Node.js | 22 LTS | Runtime JS |
| Python | 3.12+ | Backend, ML |
| Rust | stable | Performance-critical |
| Next.js | 15 | Frontend web |
| FastAPI | latest | API Python |
| PostgreSQL | 16+ | Database relazionale |
| SQLite | 3.45+ | Database embedded |
| Docker | latest | Containerizzazione |

## Ruolo dell'Umano nelle Sessioni

> Claude DEVE ricordare queste istruzioni all'utente a inizio sessione e ai checkpoint.

### A inizio sessione, mostrare:
```
PROMEMORIA PER L'UMANO:
- Io leggo STATUS.md e riprendo da dove eravamo
- Tu devi solo rispondere ai GATE (approvazione/rifiuto) e verificare:
  1. OUTPUT SMOKE TEST: ti mostro l'output, tu confermi se ha senso
  2. GOLDEN SNAPSHOT (L4): ti mostro il risultato, tu approvi 1 volta
  3. VALORI NUMERICI (L2): ti cito la fonte, tu verifichi che la fonte sia corretta
  4. SCOPE: ti presento IN/OUT, tu approvi prima che io codifichi
- Se qualcosa non ti convince: Esc + correggi subito. Dopo 2 fix falliti -> /clear
- Puoi dire "skip" se vuoi saltare una verifica (a tuo rischio)
```

### Ai checkpoint, mostrare:
```
CHECKPOINT: [cosa sto chiedendo]
- Cosa ho fatto: [riassunto 1-2 righe]
- Cosa ti mostro: [output/snapshot/valore]
- Cosa devi verificare: [cosa specifica guardare]
- Risposta attesa: OK / problema trovato / skip
```

## Comunicazione

- Essere conciso e diretto
- Indicare `file:line` quando si referenzia codice
- Segnalare "CHECKPOINT: verifica utente" quando serve input umano
- Non over-engineerizzare: minima complessita' per il task corrente
