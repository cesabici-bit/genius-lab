# Known Issues — NuclearMind

> Questo file persiste tra sessioni. Claude lo legge a inizio sessione per evitare errori ricorrenti.
> Aggiungere OGNI errore significativo con analisi causa radice.

## Formato Entry

```
### EC-NNN: Titolo breve
- **Data**: YYYY-MM-DD
- **Sintomo**: cosa si osserva
- **Causa**: perche' e' successo
- **Fix**: cosa e' stato fatto
- **Prevenzione**: come evitarlo in futuro
- **Status**: OPEN | FIXED | WORKAROUND
```

## Issues

### EC-001: MAPIE v1.3 API completamente riscritta
- **Data**: 2026-04-02
- **Sintomo**: MapieRegressor non esiste in MAPIE >=1.0
- **Causa**: MAPIE v1.0 ha ristrutturato l'API. MapieRegressor -> SplitConformalRegressor/CrossConformalRegressor. alpha -> confidence_level. fit() -> fit() + conformalize()
- **Fix**: Usare la nuova API documentata in verified-deps.toml
- **Prevenzione**: Verificare SEMPRE la versione corrente via web search prima di usare qualsiasi libreria. Non fidarsi di esempi pre-2025.
- **Status**: OPEN (da applicare in F3-3.0)

### EC-002: SHAP richiede Python >=3.11
- **Data**: 2026-04-02
- **Sintomo**: shap >=0.50 non installa su Python 3.10
- **Causa**: SHAP ha droppato supporto Python 3.10 nella v0.50+
- **Fix**: Impostare Python >=3.11 come requisito minimo in pyproject.toml
- **Prevenzione**: Controllare python_requires di ogni dipendenza durante M1
- **Status**: OPEN (da applicare in F3-1.0)
