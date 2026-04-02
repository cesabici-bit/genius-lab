# NuclearMind — Architettura Fondazionale

> "Every prediction must be verifiable, explainable, and carry calibrated uncertainty."

## Principi Fondamentali (non negoziabili)

### P1: Physics-First, ML-Second
Il modello ML non sostituisce la fisica — la accelera. Ogni predizione DEVE essere
consistente con le leggi di conservazione (massa, energia, momento). Se il ML viola
la fisica, la fisica vince.

### P2: Uncertainty is a Feature, not a Bug
Ogni predizione ha DUE output: il valore e la sua incertezza calibrata. Un modello
che dice "non lo so" e' piu' utile di uno che dice qualcosa di sbagliato con sicurezza.
Usiamo conformal prediction per garanzie matematiche di copertura.

### P3: Explainability by Design
Non aggiungiamo XAI a posteriori su un modello black-box. L'architettura stessa e'
progettata per essere interpretabile: attention maps sui nodi del grafo del reattore,
feature importance per ogni predizione, concept-based explanations per i regolatori.

### P4: Defense-in-Depth
Nessun singolo meccanismo anti-allucinazione basta. Stratifichiamo 7 layer indipendenti
di validazione. Se un layer fallisce, gli altri catturano l'errore.

### P5: Fail-Safe by Default
Se l'incertezza supera la soglia o i layer di validazione non concordano, il sistema
NON produce una predizione — segnala all'operatore umano. Mai una predizione non
validata.

### P6: Reproducibility as Law
Ogni risultato deve essere riproducibile: seed fissati, versioni di dipendenze bloccate,
dati di training versionati, modelli con checksum. Se non e' riproducibile, non esiste.

---

## Architettura a 3 Strati

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 3: TRUST ENGINE                     │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Conformal│  │  Physics  │  │  Formal  │  │  Human-in- │  │
│  │Prediction│  │  Checks   │  │  Verify  │  │  the-Loop  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
│       └──────────────┴──────────────┴──────────────┘         │
│                         TRUST SCORE                          │
├──────────────────────────────────────────────────────────────┤
│                   LAYER 2: SURROGATE ENGINE                  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              GNN Reactor Graph Model                  │    │
│  │  (nodi = componenti/zone, archi = accoppiamenti)     │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │              PINN Physics Encoder                     │    │
│  │  (loss = data_loss + physics_loss + boundary_loss)   │    │
│  ├──────────────────────────────────────────────────────┤    │
│  │              Ensemble (N modelli indipendenti)        │    │
│  │  (epistemic uncertainty via disagreement)             │    │
│  └──────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│                  LAYER 1: DATA ENGINE                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  OpenMC   │  │  MOOSE/  │  │  Dataset  │  │  Cleanlab  │  │
│  │  Bridge   │  │  SAM     │  │  Store    │  │  Quality   │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
│                                                              │
│  Input: geometria reattore, condizioni operative, materiali  │
│  Output: dataset di training verificato e versionato         │
└──────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Data Engine

### Scopo
Generare, curare e versionare dataset di training da simulatori ad alta fedelta'.

### Componenti

#### 1.1 OpenMC Bridge
- Interfaccia Python che parametrizza geometria e materiali
- Genera batch di simulazioni Monte Carlo (neutronics)
- Output: flussi neutronici, keff, distribuzioni di potenza
- **Anti-allucinazione**: ogni simulazione ha il suo seed e log di configurazione

#### 1.2 MOOSE/SAM Bridge (futuro)
- Per dati thermal-hydraulici (temperature, portate, pressioni)
- Accoppiamento con OpenMC per dati multifisici

#### 1.3 Dataset Store
- Formato: HDF5 con metadati completi (versione codice, parametri, data)
- Versionamento: DVC (Data Version Control) o simile
- Schema fisso: ogni sample ha input (parametri) + output (quantita' fisiche) + metadata
- **Anti-allucinazione**: data provenance tracciata per ogni sample

#### 1.4 Data Quality (Cleanlab)
- Rileva label errors e outlier nel dataset
- Calcola confidence score per ogni sample
- Rimuove o flagga dati sospetti PRIMA del training
- **Anti-allucinazione**: nessun dato corrotto entra nel training

---

## Layer 2: Surrogate Engine

### Scopo
Modelli ML che approssimano i simulatori ad alta fedelta' in tempo reale.

### Architettura del Modello

#### 2.1 GNN Reactor Graph
Il reattore e' rappresentato come un GRAFO:
- **Nodi**: zone/componenti del reattore (fuel assemblies, canali di refrigerazione,
  riflettore, barrette di controllo)
- **Archi**: accoppiamenti fisici tra componenti (neutronici, termici, idraulici)
- **Node features**: proprieta' locali (composizione, temperatura, densita')
- **Edge features**: coefficienti di accoppiamento

Perche' GNN:
1. Rispetta la topologia fisica del reattore (non tratta i dati come vettori piatti)
2. Generalizza naturalmente a reattori di dimensioni diverse
3. Le attention maps sui nodi/archi forniscono spiegazioni interpretabili
4. Argonne ha dimostrato la fattibilita' (ma non ha rilasciato il codice)

Architettura specifica:
```
Input: grafo G = (V, E, X_v, X_e) + parametri operativi globali
  │
  ├─ Message Passing layers (GraphSAGE o GAT) x N
  │   └─ Attention weights → spiegabilita' (quali accoppiamenti contano)
  │
  ├─ Global pooling → stato globale del reattore
  │
  └─ Output heads:
      ├─ Distribuzione di potenza (per nodo)
      ├─ Distribuzione di temperatura (per nodo)
      ├─ keff (scalare globale)
      └─ Margini di sicurezza (per nodo)
```

#### 2.2 PINN Physics Encoder
La loss function include termini fisici:
```
L_total = L_data + lambda_1 * L_physics + lambda_2 * L_boundary + lambda_3 * L_conservation

dove:
  L_data = MSE tra predizione e simulazione ad alta fedelta'
  L_physics = residuo delle equazioni di diffusione neutronica
  L_boundary = rispetto condizioni al contorno
  L_conservation = bilancio energetico (energia in = energia out + accumulo)
```

**Anti-allucinazione**: il modello non puo' convergere su soluzioni che violano la fisica.

#### 2.3 Deep Ensemble
- N modelli (es. 5) addestrati indipendentemente con inizializzazioni diverse
- Media delle predizioni = output
- Varianza delle predizioni = incertezza epistemica
- **Anti-allucinazione**: alta varianza = "non lo so" → deferral a simulazione completa

---

## Layer 3: Trust Engine

### Scopo
Validare OGNI predizione prima che raggiunga l'utente.

### Componenti

#### 3.1 Conformal Prediction (MAPIE/TorchCP)
- Fornisce **intervalli di predizione con copertura garantita**
- Es: "con il 95% di probabilita', keff e' tra 1.001 e 1.015"
- Garanzia matematica: la copertura e' valida per QUALSIASI distribuzione dei dati
- Unico metodo con garanzie teoriche, non dipende dal modello
- **Anti-allucinazione**: l'utente vede sempre l'incertezza, mai solo un punto

#### 3.2 Physics Consistency Checks
Batteria di controlli post-predizione:
- keff in range fisico (es. 0.8 < keff < 1.3)
- Temperature sotto limiti materiali
- Bilancio energetico rispettato (|E_in - E_out - E_stored| < epsilon)
- Nessuna temperatura negativa
- Flusso neutronico non-negativo
- Gradienti termici sotto soglia di stress
- **Anti-allucinazione**: se QUALSIASI check fallisce → predizione rifiutata

#### 3.3 Formal Verification (alpha-beta-CROWN)
Per sottosistemi safety-critical (es. classificatore di incidente):
- Dimostra MATEMATICAMENTE che per certi input, l'output e' sempre corretto
- Es: "per qualsiasi combinazione di parametri in questo range, il classificatore
  identifica sempre lo scenario LOCA"
- Applicabile solo a reti piccole (classificatori, non il GNN completo)
- **Anti-allucinazione**: PROVA, non test, che il safety classifier funziona

#### 3.4 Explainability Engine (SHAP + Captum)
Per OGNI predizione:
- **SHAP values**: quanto ogni input contribuisce alla predizione
- **GNN attention maps**: quali nodi/accoppiamenti guidano il risultato
- **Concept-based explanations**: "la temperatura sale perche' la barra di controllo
  X e' stata estratta del Y%" — in linguaggio ingegneristico, non ML
- **Anti-allucinazione**: se la spiegazione non ha senso fisico, il modello sta
  probabilmente allucinando

#### 3.5 Trust Score Aggregato
```python
trust_score = f(
    ensemble_agreement,      # modelli concordano?
    conformal_width,         # intervallo stretto?
    physics_checks_passed,   # fisica rispettata?
    explanation_coherence,   # spiegazione sensata?
    data_similarity          # input simile al training set?
)

if trust_score < THRESHOLD:
    return DeferralToSimulation(input)  # fallback a OpenMC/MOOSE
else:
    return Prediction(value, uncertainty, explanation)
```

#### 3.6 Drift Detection (Alibi Detect)
- Monitora se la distribuzione degli input cambia nel tempo
- Se il reattore opera in condizioni mai viste nel training → alert
- **Anti-allucinazione**: previene predizioni fuori distribuzione

#### 3.7 Human-in-the-Loop
- Dashboard con predizione + incertezza + spiegazione + trust score
- L'operatore puo' accettare, rifiutare, o chiedere simulazione completa
- Ogni decisione umana viene loggata per audit
- **Anti-allucinazione**: l'umano e' l'ultimo layer di difesa

---

## Stack Tecnologico

### Core
| Componente | Tool | Versione | Motivo |
|-----------|------|----------|--------|
| Language | Python | 3.12+ | Ecosistema ML + nucleare |
| GNN Framework | PyTorch Geometric | latest | Migliore lib GNN, attention native |
| PINN | PyTorch | latest | Flessibilita' nella loss function |
| Conformal Prediction | MAPIE | latest | 1527 stars, mantenuto, garanzie teoriche |
| Explainability | SHAP + Captum | latest | Standard de facto, SHAP 25K stars |
| Data Quality | Cleanlab | latest | 11K stars, rileva label errors |
| Drift Detection | Alibi Detect | latest | 2.5K stars, production-ready |
| Formal Verification | alpha-beta-CROWN | latest | VNN-COMP winner 2021-2025 |
| UQ | TorchUncertainty | latest | Deep ensembles + calibration |

### Simulation (Data Generation)
| Componente | Tool | Versione | Motivo |
|-----------|------|----------|--------|
| Neutronics | OpenMC | latest | 995 stars, Python API, MIT |
| Thermal-Hydraulics | MOOSE/SAM | latest | INL standard, 2189 stars |
| Risk Analysis | RAVEN | latest | UQ e sensitivity analysis |

### Infrastructure
| Componente | Tool | Versione | Motivo |
|-----------|------|----------|--------|
| Data Versioning | DVC | latest | Git per dati |
| Experiment Tracking | MLflow | latest | Standard de facto |
| Testing | pytest + Hypothesis | latest | Unit + property-based |
| CI/CD | GitHub Actions | — | Standard |
| Dashboard | Streamlit | latest | Prototipazione veloce |

---

## Pipeline Anti-Allucinazione (per ogni predizione)

```
Input (parametri reattore)
    │
    ▼
[1] Data Similarity Check ── input fuori distribuzione? ──→ ALERT + Deferral
    │ ok
    ▼
[2] Ensemble Forward Pass (N modelli)
    │
    ├─ Media predizioni → valore
    ├─ Varianza predizioni → incertezza epistemica
    │
    ▼
[3] Conformal Prediction ── intervallo troppo largo? ──→ WARNING + widen bounds
    │ ok
    ▼
[4] Physics Checks ── violazioni? ──→ REJECT predizione
    │ ok
    ▼
[5] Explainability ── spiegazione incoerente? ──→ FLAG per review
    │ ok
    ▼
[6] Trust Score ── sotto soglia? ──→ DEFERRAL a simulazione completa
    │ ok
    ▼
Output: Prediction(value, confidence_interval, explanation, trust_score)
```

Ogni step e' loggato. Ogni rifiuto/deferral e' tracciato. Zero predizioni non validate.

---

## MVP Scope (Fase 3)

### IN:
- UN tipo di reattore: PWR (piu' dati disponibili, NPPAD dataset)
- UNA quantita' predetta: distribuzione di potenza
- Dati generati con OpenMC (neutronics pura, no TH accoppiata)
- GNN base (GraphSAGE) con ensemble di 5 modelli
- Conformal prediction con MAPIE
- SHAP explanations
- Physics checks (keff range, potenza non-negativa, conservazione)
- Streamlit dashboard minimo

### OUT (per ora):
- Thermal-hydraulics accoppiata
- Reattori avanzati (MSR, SFR, HTGR)
- Formal verification (alpha-beta-CROWN)
- Real-time inference
- MOOSE/SAM integration
- Deployment production

---

## Metriche di Successo

### Tecniche
- Errore relativo medio < 5% rispetto a OpenMC su test set
- Copertura conformal prediction ≥ 95% (verificata empiricamente)
- 100% dei physics checks passati su predizioni accettate
- Speedup ≥ 100x rispetto a simulazione OpenMC completa
- SHAP explanations consistenti per ≥ 90% delle predizioni

### Progetto
- Primo commit con smoke test funzionante entro F3
- Paper-ready results entro F4
- GitHub stars > pyMAISE (29) entro 3 mesi dal rilascio
- Citazione in almeno 1 paper/report entro 1 anno
