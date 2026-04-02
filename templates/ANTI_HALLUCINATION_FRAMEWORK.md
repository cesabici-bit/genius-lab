# Framework Anti-Allucinazione Generalizzato — Genius Lab

> Applicabile a TUTTI i progetti del portfolio. Nato dalla ricerca NuclearMind (2026-04-02),
> generalizzato per qualsiasi dominio.

## Principio Fondamentale

> "Un sistema AI che non sa dire 'non lo so' e' piu' pericoloso di uno che sbaglia."

Ogni progetto che produce output ML/AI DEVE implementare almeno i layer applicabili
di questo framework. L'obiettivo non e' zero errori (impossibile) ma **zero errori
silenziosi**: ogni errore deve essere catturato, segnalato, e gestito.

---

## I 7 Layer Defense-in-Depth

### Layer 1: Data Quality (OBBLIGATORIO per tutti)

**Cosa fa:** Assicura che i dati di input/training siano corretti e puliti.

**Tool consigliati:**
| Tool | Stars | Cosa fa | Quando usarlo |
|------|-------|---------|---------------|
| Cleanlab | 11.4K | Rileva label errors, outlier | Training ML |
| Great Expectations | 9.8K | Data validation rules | Pipeline dati |
| Pandera | 3.2K | Schema validation dataframes | Progetti Python/pandas |

**Implementazione minima:**
```python
# Ogni dataset di training deve avere:
# 1. Schema definito (tipi, range, nullable)
# 2. Controllo completezza (no missing critici)
# 3. Controllo duplicati
# 4. Distribuzione statistiche loggata (per drift detection)
```

**Applicabilita' per dominio:**
- **Nucleare (NuclearMind):** Cleanlab su dataset simulati + data provenance per ogni sample
- **Finance (ClimaFin):** Great Expectations su dati di mercato + range checks su prezzi
- **Hardware/IoT (SpectraForge, GridPulse):** Schema validation su dati sensori + outlier detection
- **NLP/Regulatory (NucRegAI):** Deduplicazione documenti + verifica encoding
- **Simulazione (TinkerWorld, FusionEdge):** Validazione output simulatore vs range fisici noti

---

### Layer 2: Domain Constraints (OBBLIGATORIO per tutti)

**Cosa fa:** Vincola il modello/output a rispettare le leggi del dominio.

**Questo NON e' un semplice range check.** E' l'encoding della conoscenza di dominio
nel sistema stesso.

**Pattern per dominio:**

| Dominio | Vincoli | Implementazione |
|---------|---------|-----------------|
| Nucleare | Conservazione energia/massa, keff range, T < T_fusione | PINN loss terms |
| Fisica | Conservazione energia/momento, F=ma | PINN loss terms |
| Finance | No prezzi negativi, rendimenti plausibili, somma pesi = 1 | Hard constraints in ottimizzazione |
| Chimica | Bilancio stechiometrico, concentrazioni non-negative | Constraint layer |
| Ingegneria strutturale | Tensioni < carico ultimo, deformazioni < limiti normativi | Post-processing checks |
| NLP/Regulatory | Output in vocabolario noto, citazioni verificabili | Grounding + RAG |
| IoT/Sensori | Range fisico sensore, rate of change massimo, correlazioni note | Rule engine |

**Implementazione:**
```python
class DomainConstraints:
    """Ogni progetto definisce i suoi vincoli."""

    def check(self, prediction) -> ConstraintResult:
        """Ritorna PASS/FAIL/WARNING per ogni vincolo."""
        results = []
        for constraint in self.constraints:
            results.append(constraint.evaluate(prediction))
        return ConstraintResult(results)

    def as_loss_term(self) -> Callable:
        """Per PINN: ritorna un termine di loss differenziabile."""
        ...
```

---

### Layer 3: Uncertainty Quantification (OBBLIGATORIO per output ML)

**Cosa fa:** Ogni predizione ha un valore E un'incertezza calibrata.

**Tool consigliati:**
| Tool | Stars | Metodo | Pro | Contro |
|------|-------|--------|-----|--------|
| MAPIE | 1.5K | Conformal Prediction | Garanzie matematiche di copertura | Solo tabular/regression |
| TorchCP | 454 | Conformal Prediction | PyTorch native | Piu' nuovo |
| TorchUncertainty | 486 | Deep Ensembles + calibration | Completo | Complessita' |
| Uncertainty Toolbox | 2K | Metriche calibrazione | Leggero, eval only | Non produce UQ |

**Gerarchia di metodi (dal piu' forte al piu' debole):**

1. **Conformal Prediction** — garanzie teoriche di copertura. Usare SEMPRE se possibile.
   ```python
   # "Con 95% di probabilita', il valore e' in [a, b]"
   # Valido per QUALSIASI distribuzione. Non dipende dal modello.
   from mapie.regression import MapieRegressor
   mapie = MapieRegressor(estimator, method="plus", cv=5)
   y_pred, y_intervals = mapie.predict(X_test, alpha=0.05)
   ```

2. **Deep Ensembles** — N modelli indipendenti, varianza = incertezza epistemica.
   Piu' costoso (Nx compute) ma cattura "non lo so" per input fuori distribuzione.

3. **MC Dropout** — dropout a inference time, varianza come proxy di incertezza.
   Economico ma meno affidabile.

4. **Softmax temperature scaling** — solo per classificazione, calibra le probabilita'.
   Il minimo indispensabile.

**Regola:** Per progetti safety-critical (nucleare, strutturale, medico) → conformal + ensemble.
Per gli altri → almeno conformal prediction.

---

### Layer 4: Output Validation (OBBLIGATORIO per tutti)

**Cosa fa:** Batteria di controlli automatici sull'output PRIMA che raggiunga l'utente.

**Pattern universale:**
```python
class OutputValidator:
    def validate(self, output) -> ValidationResult:
        checks = [
            self.range_check(output),          # valori in range fisico/logico
            self.consistency_check(output),     # parti dell'output coerenti tra loro
            self.conservation_check(output),    # quantita' conservate rispettate
            self.monotonicity_check(output),    # relazioni note rispettate
            self.historical_check(output),      # output simile a casi noti?
        ]

        if any(c.failed for c in checks):
            return ValidationResult.REJECT(checks)
        if any(c.warning for c in checks):
            return ValidationResult.FLAG(checks)
        return ValidationResult.PASS(checks)
```

**Esempi per dominio:**
- **Nucleare:** T < T_fusione, keff in [0.8, 1.3], bilancio energetico, flusso >= 0
- **Finance:** rendimenti < 100%/giorno, portafoglio pesi sommano a 1, Sharpe plausibile
- **IoT:** lettura sensore in range hardware, rate of change plausibile
- **NLP:** output in lingua attesa, lunghezza plausibile, no contenuto tossico
- **Simulazione:** energia totale conservata, nessuna velocita' > c, nessuna massa < 0

---

### Layer 5: Formal Verification (OPZIONALE, per safety-critical)

**Cosa fa:** DIMOSTRA matematicamente proprieta' del modello per certi input.

**Tool:**
| Tool | Stars | Cosa fa |
|------|-------|---------|
| alpha-beta-CROWN | 356 | Verifica formale reti neurali (winner VNN-COMP 2021-2025) |
| Marabou | 320 | SMT-based neural network verifier |
| ERAN | 250 | Abstract interpretation per reti neurali |

**Quando usarlo:**
- Sottosistemi safety-critical (classificatori di incidenti, alert systems)
- Reti piccole (< qualche centinaio di neuroni per layer)
- Quando serve una PROVA, non un test

**Quando NON usarlo:**
- Modelli grandi (GNN, transformer) — troppo costoso computazionalmente
- Output continui con alta dimensionalita'
- Prototipi/MVP — aggiungere dopo la validazione empirica

**Applicabilita':**
- **NuclearMind:** safety classifier (LOCA si/no) → verificabile formalmente
- **VigiPipe:** signal detection (reazione avversa si/no) → verificabile
- **AirComply:** threshold classifier (compliance si/no) → verificabile
- **Non applicabile:** surrogati complessi, modelli generativi, regressione ad alta dimensionalita'

---

### Layer 6: Explainability (OBBLIGATORIO per progetti con utenti umani)

**Cosa fa:** Spiega PERCHE' il modello ha prodotto quell'output.

**Tool:**
| Tool | Stars | Tipo | Best for |
|------|-------|------|----------|
| SHAP | 25.2K | Feature importance (Shapley values) | Qualsiasi modello |
| Captum | 5.6K | PyTorch interpretability | Reti neurali PyTorch |
| Alibi Explain | 2.4K | Counterfactuals, anchors | Classificazione |
| LIT | 3.5K | Google, interactive visualization | NLP models |

**3 livelli di spiegazione (scegliere in base al pubblico):**

1. **Tecnico** (per sviluppatori/ricercatori):
   - SHAP values per feature
   - Attention maps
   - Gradient-based attribution

2. **Ingegneristico** (per domain experts):
   - "La temperatura sale perche' la barra di controllo X e' stata estratta del Y%"
   - Concept-based explanations in linguaggio del dominio

3. **Executive** (per decisori/regolatori):
   - Confidence level (alto/medio/basso)
   - Top 3 fattori che guidano la predizione
   - Confronto con casi storici simili

**Regola anti-allucinazione:** Se la spiegazione non ha senso nel dominio, il modello
sta probabilmente allucinando. La spiegazione e' un DETECTOR di allucinazioni, non
solo una feature di usabilita'.

---

### Layer 7: Human-in-the-Loop (OBBLIGATORIO per decisioni ad alto impatto)

**Cosa fa:** L'umano e' l'ultimo layer di difesa.

**Pattern:**
```python
class HumanGate:
    """Decide quando chiedere all'umano."""

    def should_defer(self, prediction, trust_score, context) -> bool:
        return (
            trust_score < self.threshold
            or prediction.uncertainty > self.max_uncertainty
            or prediction.is_novel_scenario
            or context.requires_regulatory_approval
        )
```

**Implementazione per dominio:**
- **Nucleare:** Dashboard operatore con predizione + incertezza + spiegazione + trust score
- **Finance:** Alert con raccomandazione + confidence + rationale
- **IoT/Hardware:** Semaforo (verde/giallo/rosso) con drill-down disponibile
- **Regulatory:** Report generato + sezioni flaggate per review umana

---

## Matrice Applicabilita' per Progetto

| Layer | NuclearMind | FusionEdge | NucRegAI | ClimaFin | SpectraForge | GridPulse | VibeSentry |
|-------|:-----------:|:----------:|:--------:|:--------:|:------------:|:---------:|:----------:|
| L1 Data Quality | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ |
| L2 Domain Constraints | ★★★ | ★★★ | ★★ | ★★ | ★★★ | ★★★ | ★★★ |
| L3 UQ (Conformal) | ★★★ | ★★★ | ★ | ★★★ | ★★ | ★★★ | ★★★ |
| L4 Output Validation | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ | ★★★ |
| L5 Formal Verify | ★★★ | ★ | — | — | — | — | ★ |
| L6 Explainability | ★★★ | ★★ | ★★★ | ★★★ | ★★ | ★★ | ★★ |
| L7 Human-in-Loop | ★★★ | ★★ | ★★★ | ★★ | ★ | ★★ | ★★ |

★★★ = critico, ★★ = importante, ★ = nice-to-have, — = non applicabile

---

## Trust Score Generalizzato

Ogni progetto che produce output AI/ML dovrebbe calcolare un trust score composito:

```python
def compute_trust_score(
    ensemble_agreement: float,    # 0-1, accordo tra modelli ensemble
    conformal_width: float,       # ampiezza intervallo conformal (normalizzata)
    physics_checks: float,        # 0-1, frazione di check fisici passati
    explanation_coherence: float, # 0-1, coerenza della spiegazione col dominio
    data_similarity: float,       # 0-1, similarita' input col training set
) -> float:
    """
    Trust score composito. Se < soglia → deferral/warning.

    Pesi configurabili per dominio (safety-critical = pesi piu' alti
    su physics_checks e ensemble_agreement).
    """
    weights = get_domain_weights()  # configurati per progetto

    score = (
        weights.ensemble * ensemble_agreement
        + weights.conformal * (1 - conformal_width)  # stretto = meglio
        + weights.physics * physics_checks
        + weights.explanation * explanation_coherence
        + weights.similarity * data_similarity
    )

    return score / sum(weights.values())
```

---

## Checklist per Nuovo Progetto

Prima di scrivere codice ML/AI, rispondere a queste domande:

- [ ] Quali sono i vincoli di dominio? (L2)
- [ ] Qual e' il range fisicamente/logicamente valido per ogni output? (L4)
- [ ] Quali metriche di incertezza servono? (L3)
- [ ] Chi e' l'utente finale? Che tipo di spiegazione serve? (L6)
- [ ] Ci sono sottosistemi safety-critical verificabili formalmente? (L5)
- [ ] Quando il sistema deve deferire all'umano? (L7)
- [ ] Quali sono le fonti di dati e come ne garantiamo la qualita'? (L1)

---

## Dipendenze Verificate (comuni a piu' progetti)

Queste dipendenze sono state verificate via web search il 2026-04-02 e sono disponibili
per qualsiasi progetto del portfolio:

| Pacchetto | Versione | URL Docs | Scopo |
|-----------|----------|----------|-------|
| MAPIE | ≥0.9 | https://mapie.readthedocs.io | Conformal prediction |
| Cleanlab | ≥2.6 | https://docs.cleanlab.ai | Data quality |
| SHAP | ≥0.45 | https://shap.readthedocs.io | Feature importance |
| Captum | ≥0.7 | https://captum.ai | PyTorch interpretability |
| Alibi Detect | ≥0.12 | https://docs.seldon.io/projects/alibi-detect | Drift/outlier detection |
| TorchUncertainty | ≥0.3 | https://torch-uncertainty.github.io | Deep ensembles + calibration |
| alpha-beta-CROWN | latest | https://github.com/Verified-Intelligence/alpha-beta-CROWN | Formal verification |
| Uncertainty Toolbox | ≥0.2 | https://github.com/uncertainty-toolbox/uncertainty-toolbox | UQ metrics |

---

## Referenze

### Papers
- Guo et al. "On Calibration of Modern Neural Networks" (ICML 2017) — perche' la calibrazione e' necessaria
- Vovk et al. "Algorithmic Learning in a Random World" (2022) — teoria conformal prediction
- Lakshminarayanan et al. "Simple and Scalable Predictive Uncertainty" (NeurIPS 2017) — deep ensembles
- Ribeiro et al. "Why Should I Trust You?" (KDD 2016) — LIME, spiegabilita'
- Lundberg & Lee "A Unified Approach to Interpreting Model Predictions" (NeurIPS 2017) — SHAP

### Standard
- NRC/CNSC/ONR Joint AI Principles for Nuclear (Sept 2024)
- NRC NUREG-2261 "AI Strategic Plan FY2023-2027"
- IEC 61513 — Nuclear power plants, I&C systems (traceability requirements)
- IEEE 1012 — System, Software, and Hardware V&V

### Tool Repos
- https://github.com/scikit-learn-contrib/MAPIE
- https://github.com/cleanlab/cleanlab
- https://github.com/shap/shap
- https://github.com/pytorch/captum
- https://github.com/SeldonIO/alibi-detect
- https://github.com/torch-uncertainty/torch-uncertainty
- https://github.com/Verified-Intelligence/alpha-beta-CROWN
