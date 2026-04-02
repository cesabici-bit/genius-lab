# State of the Art: AI Anti-Hallucination Tools, Frameworks & Techniques (April 2026)

> **Purpose**: Foundation research for a safety-critical nuclear engineering AI project where hallucinations could mean nuclear accidents.
> **Date**: 2026-04-02
> **Scope**: GitHub repositories, academic techniques, industry standards, specific tools

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [GitHub Repositories & Open-Source Tools](#2-github-repositories--open-source-tools)
3. [Academic/Industry State of the Art](#3-academicindustry-state-of-the-art)
4. [Specific Tool Deep-Dives](#4-specific-tool-deep-dives)
5. [Nuclear-Specific Regulatory Landscape](#5-nuclear-specific-regulatory-landscape)
6. [Architecture Recommendations for Nuclear AI](#6-architecture-recommendations-for-nuclear-ai)
7. [Sources](#7-sources)

---

## 1. Executive Summary

The anti-hallucination landscape in 2026 is mature but fragmented. No single tool solves the problem. For **safety-critical nuclear AI**, the winning strategy is a **defense-in-depth architecture** combining multiple layers:

| Layer | Technique | Tools |
|-------|-----------|-------|
| **L0: Data Quality** | Label error detection, data validation | Cleanlab, Great Expectations |
| **L1: Physics Constraints** | PINNs, domain-informed architecture | DeepXDE, PINA, NeuralPDE.jl |
| **L2: Uncertainty Quantification** | Conformal prediction, ensembles, Bayesian | MAPIE, TorchUncertainty, Uncertainty Toolbox |
| **L3: Output Validation** | Guardrails, structured output, range checks | Guardrails AI, NeMo Guardrails, Pydantic |
| **L4: Formal Verification** | Provable bounds on NN outputs | alpha-beta-CROWN, Marabou 2.0 |
| **L5: Explainability** | Feature attribution, interpretability | SHAP, Captum, Alibi, LIT |
| **L6: Drift/Anomaly Detection** | OOD detection, data drift monitoring | Alibi Detect, Cleanlab |
| **L7: Human-in-the-Loop** | Conformal validation, deferral policies | Custom + conformal prediction |

**Key finding**: The nuclear industry is actively developing AI regulatory frameworks (NRC/IAEA/CNSC joint principles published Sept 2024), but no nuclear-specific AI V&V standard exists yet. This is an opportunity to become THE reference.

---

## 2. GitHub Repositories & Open-Source Tools

### 2.1 Hallucination Detection (LLM-focused)

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [cvs-health/uqlm](https://github.com/cvs-health/uqlm) | 1,133 | UQ-based LLM hallucination detection | Medium - UQ concepts transferable |
| [EdinburghNLP/awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection) | 1,064 | Curated paper list on hallucination detection | High - reference for techniques |
| [potsawee/selfcheckgpt](https://github.com/potsawee/selfcheckgpt) | 608 | Zero-resource black-box hallucination detection | Low - LLM-specific |
| [KRLabsOrg/LettuceDetect](https://github.com/KRLabsOrg/LettuceDetect) | 537 | Lightweight hallucination detection for RAG | Low - RAG-specific |
| [Infosys/Infosys-Responsible-AI-Toolkit](https://github.com/Infosys/Infosys-Responsible-AI-Toolkit) | 285 | Safety, explainability, fairness, hallucination | Medium - comprehensive toolkit |

**Assessment**: LLM hallucination detection tools are NOT directly applicable to numerical/physics AI predictions. The concepts (consistency checking, uncertainty estimation) transfer, but the tools need adaptation.

### 2.2 Uncertainty Quantification Frameworks

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [uncertainty-toolbox/uncertainty-toolbox](https://github.com/uncertainty-toolbox/uncertainty-toolbox) | 1,981 | Metrics, calibration, visualization for predictive UQ | **CRITICAL** - calibration metrics |
| [torch-uncertainty/torch-uncertainty](https://github.com/torch-uncertainty/torch-uncertainty) | 486 | PyTorch framework for UQ (ensembles, MC dropout, etc.) | **CRITICAL** - production UQ |
| [deel-ai/puncc](https://github.com/deel-ai/puncc) | 378 | Conformal prediction for UQ | **HIGH** - guaranteed coverage |
| [deel-ai/deel-lip](https://github.com/deel-ai/deel-lip) | 101 | Lipschitz-constrained networks (certified robustness) | **HIGH** - provable bounds |
| [ENSTA-U2IS-AI/awesome-uncertainty-deeplearning](https://github.com/ENSTA-U2IS-AI/awesome-uncertainty-deeplearning) | 792 | Surveys, papers, codes for UQ in deep learning | **HIGH** - reference collection |

### 2.3 Conformal Prediction Libraries

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [scikit-learn-contrib/MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | 1,527 | sklearn-compatible conformal prediction intervals | **CRITICAL** - production-ready |
| [aangelopoulos/conformal-prediction](https://github.com/aangelopoulos/conformal-prediction) | 1,026 | Lightweight conformal prediction implementation | **HIGH** - reference impl |
| [valeman/awesome-conformal-prediction](https://github.com/valeman/awesome-conformal-prediction) | 1,195 | Curated list of CP resources | **HIGH** - reference |
| [ml-stat-Sustech/TorchCP](https://github.com/ml-stat-Sustech/TorchCP) | 454 | PyTorch conformal prediction toolbox | **HIGH** - deep learning native |
| [henrikbostrom/crepes](https://github.com/henrikbostrom/crepes) | 561 | Python conformal prediction package | **HIGH** - alternative to MAPIE |
| [aangelopoulos/conformal-time-series](https://github.com/aangelopoulos/conformal-time-series) | 139 | CP for time-series (reactor transients!) | **CRITICAL** - time-series UQ |
| [JuliaTrustworthyAI/ConformalPrediction.jl](https://github.com/JuliaTrustworthyAI/ConformalPrediction.jl) | 147 | Julia conformal prediction | Medium - Julia ecosystem |

### 2.4 Physics-Informed Neural Networks (PINNs)

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [idrl-lab/PINNpapers](https://github.com/idrl-lab/PINNpapers) | 1,464 | Must-read papers on PINNs | **HIGH** - reference |
| [SciML/NeuralPDE.jl](https://github.com/SciML/NeuralPDE.jl) | 1,180 | PINN solvers in Julia (SciML ecosystem) | **CRITICAL** - production PDE solver |
| [rezaakb/pinns-torch](https://github.com/rezaakb/pinns-torch) | 856 | PINNs in PyTorch | **HIGH** - PyTorch native |
| [mathLab/PINA](https://github.com/mathLab/PINA) | 726 | Physics-Informed Neural networks for Advanced modeling | **HIGH** - advanced PINNs |
| [benmoseley/FBPINNs](https://github.com/benmoseley/FBPINNs) | 534 | Finite Basis PINNs (scalable) | **HIGH** - scalability |
| [i207M/PINNacle](https://github.com/i207M/PINNacle) | 412 | NeurIPS 2024 PINN benchmark | **HIGH** - benchmarking |

### 2.5 Formal Verification of Neural Networks

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [Verified-Intelligence/alpha-beta-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN) | 356 | GPU-accelerated NN verifier (VNN-COMP winner 2021-2025) | **CRITICAL** - provable bounds |
| [NeuralNetworkVerification/Marabou](https://github.com/NeuralNetworkVerification/Marabou) | 320 | Versatile formal analyzer for NNs | **CRITICAL** - SMT-based verification |
| [Verified-Intelligence/CROWN-Reach](https://github.com/Verified-Intelligence/CROWN-Reach) | 9 | Reachability analysis for NN-controlled systems | **CRITICAL** - control systems |

### 2.6 Explainability / Interpretability

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [slundberg/shap](https://github.com/slundberg/shap) | 25,223 | Game-theoretic ML explanations | **CRITICAL** - feature attribution |
| [pytorch/captum](https://github.com/pytorch/captum) | 5,590 | PyTorch model interpretability | **CRITICAL** - deep learning XAI |
| [PAIR-code/lit](https://github.com/PAIR-code/lit) | 3,645 | Google's Learning Interpretability Tool | **HIGH** - interactive analysis |
| [SeldonIO/alibi](https://github.com/SeldonIO/alibi) | 2,622 | ML explanations (counterfactual, anchors) | **HIGH** - diverse methods |
| [SeldonIO/alibi-detect](https://github.com/SeldonIO/alibi-detect) | 2,511 | Outlier, adversarial, drift detection | **CRITICAL** - production monitoring |

### 2.7 AI Guardrails / Output Validation

| Repository | Stars | Description | Nuclear Relevance |
|-----------|-------|-------------|-------------------|
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | 6,622 | LLM output validation framework | **HIGH** - output validation patterns |
| [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | 5,908 | Programmable guardrails for LLM systems | **HIGH** - flow control |
| [cleanlab/cleanlab](https://github.com/cleanlab/cleanlab) | 11,404 | Data quality, label errors, data-centric AI | **CRITICAL** - data quality |

---

## 3. Academic/Industry State of the Art

### 3.1 Hallucination Detection Techniques (2024-2026)

Five major families of detection techniques:

1. **Uncertainty Estimation**: Token-level or prediction-level confidence scoring. Linear probes on hidden activations to predict hallucination labels per token in real-time.
2. **Consistency Checking**: SelfCheckGPT-style sampling consistency. Multiple forward passes to detect inconsistent outputs.
3. **Knowledge Grounding (RAG)**: Span-level verification where each claim is matched against retrieved evidence. Graph-Augmented RAG for multi-hop reasoning.
4. **Confidence Calibration**: "Rewarding Doubt" (2025) integrates calibration into RL training. Uncertainty-aware RLHF variants.
5. **Formal Verification**: Provable bounds on NN outputs via alpha-beta-CROWN or Marabou.

**For nuclear AI**: Families 1, 2, and 5 are most relevant. RAG (family 3) is useful for documentation/procedure lookup. Family 4 is LLM-specific.

### 3.2 Conformal Prediction

**What it is**: A distribution-free, model-agnostic framework that converts any point prediction into a prediction set/interval with **finite-sample, guaranteed marginal coverage**.

**Core guarantee**: Given exchangeable calibration data and a user-specified error rate alpha, the prediction set contains the true value with probability >= 1-alpha. This is a **hard statistical guarantee**, not a heuristic.

**Why it matters for nuclear**: It provides the ONLY uncertainty quantification method with mathematically provable coverage guarantees under minimal assumptions (just exchangeability, not i.i.d.).

**Key variants**:
- **Split conformal**: Simple, calibration-set based
- **Conformal risk control**: Extends beyond coverage to arbitrary loss functions
- **Conformal time series**: For reactor transient prediction (Angelopoulos et al.)
- **Robust conformal**: Maintains guarantees under adversarial perturbations (VRCP, 2025)
- **Federated conformal**: For distributed learning scenarios

**Limitations**:
- Marginal coverage only (not conditional on specific inputs)
- Prediction sets can be large if model is poorly calibrated
- Exchangeability assumption may not hold for non-stationary processes (requires adaptive methods)
- Does not improve the model, only quantifies its uncertainty

### 3.3 Physics-Informed Neural Networks (PINNs)

**How they constrain outputs**: PINNs embed physical laws (PDEs) directly into the loss function. The network minimizes both data misfit AND PDE residuals, forcing outputs to be physically consistent.

**Nuclear applications** (2025 literature):
- Neutron diffusion equation solving (R2-PINN, 2025)
- Nuclear level density prediction via multi-task PINN
- Reactor transient prediction with transfer learning (TL-PINN)

**Critical limitations identified in 2025**:
- Training is often ill-conditioned with unbalanced gradients between PDE/boundary/data residuals
- Under noise or parameter uncertainty, inverse problems become non-identifiable
- Multiple parameter sets can produce nearly identical residuals (fundamental fragility)
- PINN V&V remains an open challenge

**Assessment for nuclear**: PINNs are promising but NOT sufficient alone. Must be combined with UQ (conformal prediction on PINN outputs) and formal verification where feasible.

### 3.4 Retrieval Augmented Generation (RAG) for Domain Grounding

**What it is**: Augments AI outputs by retrieving relevant documents from a knowledge base before generating responses.

**Nuclear relevance**:
- Grounding operator support systems in regulatory documents (NRC, IAEA)
- Procedure lookup during emergency scenarios
- Knowledge management for nuclear engineering databases

**Advanced architectures (2025)**:
- Graph-Augmented RAG for multi-hop reasoning over nuclear knowledge graphs
- Confidence-Calibrated RAG with document ordering affecting certainty
- Span-level verification where each generated claim is matched against evidence

**Limitations**:
- Even well-curated RAG can fabricate citations
- Multi-module architecture introduces security vulnerabilities
- Requires high-quality, curated knowledge base (nuclear standards, codes, procedures)

### 3.5 Formal Verification of Neural Networks

**State of the art (2025)**:

**alpha-beta-CROWN** (Verified-Intelligence):
- Winner of VNN-COMP for 5 consecutive years (2021-2025), #1 in all scored benchmarks
- GPU-accelerated bound propagation + branch-and-bound
- Supports ReLU, tanh, sigmoid activations
- Can verify Lyapunov stability (critical for control systems)
- **Limitation**: Scales to ~thousands of neurons, not millions. Verification is NP-hard.

**Marabou 2.0** (Stanford):
- SMT-based neural network verifier
- 7 different analysis techniques (IBP, symbolic bounds, DeepPoly, LP, MILP, etc.)
- Supports proof production (certifiable results)
- **Limitation**: Slower than alpha-beta-CROWN on large networks

**NNV 2.0**: Additional neural network verification tool for reachability analysis.

**Assessment for nuclear**: Formal verification is THE gold standard for safety-critical applications but is limited to smaller networks. Strategy: verify critical subsystems (safety classifiers, trip logic) with formal methods; use UQ + monitoring for larger models.

### 3.6 Epistemic vs. Aleatoric Uncertainty

| Type | Source | Reducible? | How to Quantify |
|------|--------|------------|-----------------|
| **Aleatoric** | Data noise, sensor errors, inherent randomness | No (irreducible) | Heteroscedastic output heads, quantile regression |
| **Epistemic** | Model limitations, insufficient training data | Yes (with more data/better model) | Ensembles, MC dropout, BNNs, conformal prediction |

**Methods for disentangling**:
- **Deep Ensembles**: Train N independent models (typically 5-10). Variance across ensemble = epistemic. Mean variance within each model = aleatoric. Best overall UQ performance.
- **MC Dropout**: Single model, multiple stochastic forward passes with dropout enabled at inference. Cheaper than ensembles but may underestimate uncertainty.
- **Bayesian Neural Networks (BNNs)**: Full posterior over weights. Gold standard in theory, but computationally expensive and hard to scale.
- **Evidential Deep Learning**: Single forward pass, outputs parameters of a higher-order distribution.

**For nuclear**: Deep ensembles are the recommended starting point (best performance/complexity tradeoff). Combine with conformal prediction for guaranteed coverage.

### 3.7 Ensemble Methods for Uncertainty Estimation

**Deep Ensembles** (Lakshminarayanan et al., 2017):
- Train M models (typically M=5) with different random seeds
- Prediction = mean of ensemble; uncertainty = variance
- **Pros**: Simple, effective, parallelizable, best calibration
- **Cons**: M-fold training and storage cost

**MC Dropout** (Gal & Ghahramani, 2016):
- Single model, T forward passes with dropout at inference
- **Pros**: Single model to train, lightweight
- **Cons**: Underestimates uncertainty in low-data regions, flat variance profiles

**Snapshot Ensembles**: Save checkpoints during cyclic LR training. Free diversity.

**BatchEnsemble**: Shared weights + rank-1 perturbations. 4x cheaper than full ensembles.

**2025 consensus**: Combine MC Dropout + Deep Ensembles + last-layer Bayesian inference + explicit calibration for most robust UQ. For safety-critical: always add conformal prediction on top.

### 3.8 Safety Standards for AI in Safety-Critical Industries

| Standard | Industry | Key Requirements | Nuclear Equivalent |
|---------|----------|------------------|-------------------|
| **DO-178C** | Aerospace | 5 DALs (A-E), MC/DC coverage, traceability | IEC 61513 |
| **ISO 26262** | Automotive | ASIL A-D, fault trees, FMEA | IEC 61513 |
| **IEC 61508** | Generic safety | SIL 1-4, probabilistic failure targets | Parent of IEC 61513 |
| **IEC 61513** | Nuclear I&C | Requirements for safety-critical nuclear I&C | **Direct standard** |
| **IEC 62138** | Nuclear software | Software for non-safety and safety I&C | Complements 61513 |

**AI-specific standards (emerging)**:
- **IEEE 2801-2022**: Recommended Practice for Quality Management of Datasets for Medical AI
- **ISO/IEC 42001:2023**: AI Management System standard
- **EU AI Act (2024)**: Risk-based classification, nuclear falls under "high-risk"
- **NRC/CNSC/ONR Joint Principles (Sept 2024)**: First international nuclear AI principles document

**Gap**: No nuclear-specific AI V&V standard exists yet. This is the opportunity.

### 3.9 AI Guardrails Landscape (2026)

**Guardrails AI** (guardrails-ai):
- Python framework for validating/structuring LLM outputs
- Composable pipeline of validators (Guard pattern)
- 6,622 stars, actively maintained

**NeMo Guardrails** (NVIDIA):
- Programmable guardrails for conversational systems
- Colang scripting language for flow control
- 5,908 stars, strong enterprise backing
- Best starting point for most teams (NVIDIA docs + community)

**Pydantic / Instructor**:
- Structured output validation with automatic retries
- <5ms overhead, simplest path to reliable structured output

**For nuclear AI**: Guardrails concepts (input validation, output range checking, consistency verification) are directly applicable even outside LLM contexts. Build custom validators for physical plausibility.

---

## 4. Specific Tool Deep-Dives

### 4.1 Guardrails AI (guardrails-ai/guardrails)
- **URL**: https://github.com/guardrails-ai/guardrails
- **Stars**: 6,622 | **Last updated**: 2026-04-02
- **What it does**: Adds input/output validation to LLM pipelines. Composable Guard pipelines with validators for toxicity, PII, JSON structure, semantic similarity, etc.
- **Nuclear relevance**: HIGH for any LLM-based operator support system. Patterns (validator chains, retry logic, structured output) are transferable to numerical AI.
- **Limitations**: LLM-focused; does not handle numerical physics predictions directly. Would need custom validators for nuclear-specific constraints.

### 4.2 NeMo Guardrails (NVIDIA)
- **URL**: https://github.com/NVIDIA-NeMo/Guardrails
- **Stars**: 5,908 | **Last updated**: 2026-04-02
- **What it does**: Programmable guardrails using Colang (a domain-specific language). Controls conversation flow, blocks harmful outputs, enforces topical boundaries.
- **Nuclear relevance**: HIGH for operator assistance chatbots. Colang's flow control could enforce nuclear procedure compliance.
- **Limitations**: Designed for conversational AI, not numerical prediction pipelines.

### 4.3 Uncertainty Toolbox
- **URL**: https://github.com/uncertainty-toolbox/uncertainty-toolbox
- **Stars**: 1,981 | **Last updated**: 2026-03-27
- **What it does**: Python toolbox for predictive UQ: calibration metrics (ECE, MCE, sharpness), recalibration methods, visualization. Model-agnostic.
- **Nuclear relevance**: **CRITICAL**. Use to evaluate whether your model's uncertainty estimates are well-calibrated. If a model says "95% confident", does it get it right 95% of the time?
- **Limitations**: Evaluation/metrics only, does not produce uncertainty estimates itself.

### 4.4 TorchUncertainty
- **URL**: https://github.com/torch-uncertainty/torch-uncertainty
- **Stars**: 486 | **Last updated**: 2026-04-01
- **What it does**: PyTorch framework for UQ covering classification, regression, segmentation. Implements deep ensembles, MC dropout, evidential learning, SWAG, and more.
- **Nuclear relevance**: **CRITICAL**. Production-ready UQ for PyTorch models. Directly usable for nuclear prediction models.
- **Limitations**: Younger library, smaller community than individual method implementations.

### 4.5 MAPIE (Conformal Prediction)
- **URL**: https://github.com/scikit-learn-contrib/MAPIE
- **Stars**: 1,527 | **Last updated**: 2026-04-01
- **What it does**: scikit-learn-compatible conformal prediction for regression and classification. Provides prediction intervals with guaranteed coverage.
- **Nuclear relevance**: **CRITICAL**. The ONLY method providing hard statistical guarantees on coverage. Essential for any safety-critical prediction.
- **Limitations**: sklearn-based (not native PyTorch). For deep learning, use TorchCP or puncc instead.

### 4.6 Cleanlab
- **URL**: https://github.com/cleanlab/cleanlab
- **Stars**: 11,404 | **Last updated**: 2026-04-02
- **What it does**: Detects label errors, outliers, duplicates in datasets. Data-centric AI: fix the data, not just the model.
- **Nuclear relevance**: **CRITICAL**. Nuclear training data quality is paramount. Label errors in safety-critical training data could be catastrophic. 86.6-97.5% accuracy in detecting label errors (2025 medical imaging study).
- **Limitations**: Requires model predictions (out-of-fold) to detect errors. Works best with classification/simple regression.

### 4.7 SHAP
- **URL**: https://github.com/slundberg/shap
- **Stars**: 25,223 | **Last updated**: 2026-04-02
- **What it does**: Game-theoretic feature attribution for any ML model. Shows which features contributed to each prediction.
- **Nuclear relevance**: **CRITICAL** for regulatory compliance. Operators and regulators need to understand WHY a model made a prediction. Required for IEC 61513 traceability.
- **Limitations**: Computationally expensive for large models. Kernel SHAP is model-agnostic but slow; TreeSHAP is fast but tree-only.

### 4.8 Captum (PyTorch)
- **URL**: https://github.com/pytorch/captum
- **Stars**: 5,590 | **Last updated**: 2026-04-02
- **What it does**: Model interpretability for PyTorch. Integrated Gradients, GradCAM, Layer Conductance, Neuron Attribution, etc.
- **Nuclear relevance**: **CRITICAL** for deep learning models. Provides gradient-based explanations that are computationally efficient.
- **Limitations**: PyTorch-only. Gradient-based methods can be noisy and may not reflect true feature importance.

### 4.9 Alibi + Alibi Detect (SeldonIO)
- **URL**: https://github.com/SeldonIO/alibi (2,622 stars) | https://github.com/SeldonIO/alibi-detect (2,511 stars)
- **Last updated**: 2026-03-30 / 2026-04-02
- **What it does**: Alibi = ML explanations (counterfactuals, anchors, ALE). Alibi Detect = outlier detection, adversarial detection, drift detection.
- **Nuclear relevance**: **CRITICAL** for production monitoring. Drift detection catches when the model's operating environment changes (new fuel types, different reactor conditions). Outlier detection flags inputs the model has never seen.
- **Limitations**: Some methods are slow for real-time use. Drift detection requires careful threshold tuning.

### 4.10 alpha-beta-CROWN
- **URL**: https://github.com/Verified-Intelligence/alpha-beta-CROWN
- **Stars**: 356 | **Last updated**: 2026-03-30
- **What it does**: GPU-accelerated formal verification of neural networks. Proves properties like "for all inputs in region X, the output is always in safe range Y".
- **Nuclear relevance**: **CRITICAL** for safety classifiers and trip logic. Can formally verify that a NN-based safety system will ALWAYS trigger a shutdown when needed.
- **Limitations**: NP-hard problem. Practical for networks up to ~thousands of neurons. Cannot verify transformer-scale models. Requires careful problem formulation.

### 4.11 Marabou 2.0
- **URL**: https://github.com/NeuralNetworkVerification/Marabou
- **Stars**: 320 | **Last updated**: 2026-03-30
- **What it does**: SMT-based neural network formal verification. 7 analysis techniques. Supports proof production.
- **Nuclear relevance**: **CRITICAL**. Proof production is essential for nuclear safety cases. Can certify that verified properties hold.
- **Limitations**: Slower than alpha-beta-CROWN. Performance gap on larger networks.

### 4.12 LIT (Google Learning Interpretability Tool)
- **URL**: https://github.com/PAIR-code/lit
- **Stars**: 3,645 | **Last updated**: 2026-04-01
- **What it does**: Interactive visual tool for understanding ML model behavior. Supports NLP, tabular, and image models.
- **Nuclear relevance**: HIGH for model development and debugging. Interactive exploration helps domain experts understand model behavior.
- **Limitations**: Primarily a visualization/exploration tool, not a production monitoring solution.

---

## 5. Nuclear-Specific Regulatory Landscape

### 5.1 NRC (US Nuclear Regulatory Commission)

**Key Documents**:
- **ML-24241A252** (Sept 2024): "Considerations for Developing AI Systems in Nuclear Applications" - Joint NRC/CNSC/ONR principles paper
- **ML-24290A059** (Oct 2024): "Regulatory Framework Gap Assessment for AI in Nuclear Applications" - Reviewed 500+ Regulatory Guides, found framework generally sufficient with targeted gaps
- **ML-25269A196** (Sept 2025): NRC AI Strategic Plan
- **ML-24194A116**: NRC AI Project Plan

**Key findings from NRC gap assessment**:
- Current nuclear safety framework (10 CFR, Regulatory Guides) is generally sufficient for AI
- Targeted areas need additional clarification
- No AI-specific regulations proposed yet
- Focus on existing safety principles: defense-in-depth, redundancy, diversity

### 5.2 IAEA

- Launched CRP J02024 on computer security for nuclear AI applications
- IAEA Nuclear Energy Series report on "Considerations for Deploying AI in Nuclear"
- Focus areas: cybersecurity, safety case methodology, workforce readiness

### 5.3 International Collaboration

The NRC, CNSC (Canada), ONR (UK) have established trilateral collaboration on nuclear AI regulation. Also engaging with France and Germany through IAEA and OECD/NEA.

### 5.4 Relevant Standards

| Standard | Scope | Status |
|---------|-------|--------|
| IEC 61513 | Nuclear I&C safety | Active, being reviewed for AI applicability |
| IEC 62138 | Nuclear software | Active |
| ASME V&V 10 | Computational modeling verification | Active, UQ guidance |
| IEEE 2801-2022 | Dataset quality for AI | Published |
| ISO/IEC 42001:2023 | AI management system | Published |
| EU AI Act | Risk-based AI regulation | In force, nuclear = high-risk |

### 5.5 The Opportunity

**No nuclear-specific AI V&V standard exists.** The NRC/IAEA are actively seeking input. A project that demonstrates a rigorous, defense-in-depth approach to trustworthy AI in nuclear engineering could:
1. Become the reference implementation cited by regulators
2. Influence emerging standards
3. Establish credibility as THE authority in this space

---

## 6. Architecture Recommendations for Nuclear AI

### 6.1 Defense-in-Depth Stack

```
                    NUCLEAR AI TRUST ARCHITECTURE
    ================================================================

    INPUT LAYER
    [Data Quality: Cleanlab] -> [Drift Detection: Alibi Detect]
         |                              |
         v                              v
    PREDICTION LAYER
    [Physics-Constrained Model: PINN/Hybrid]
    [Deep Ensemble (M=5-10 models)]
         |
         v
    UNCERTAINTY LAYER
    [Conformal Prediction: MAPIE/TorchCP] -> Guaranteed coverage
    [Calibration Check: Uncertainty Toolbox] -> Calibration metrics
         |
         v
    VALIDATION LAYER
    [Physical Plausibility: Custom range/consistency checks]
    [Formal Verification: alpha-beta-CROWN on safety subsystems]
         |
         v
    EXPLAINABILITY LAYER
    [SHAP/Captum: Feature attribution per prediction]
    [LIT: Interactive exploration for operators]
         |
         v
    DECISION LAYER
    [Conformal deferral: If prediction set too wide -> human]
    [Hard limits: If output violates physics -> REJECT]
    [Audit trail: Full traceability for every prediction]
```

### 6.2 Recommended Tool Stack

| Layer | Primary Tool | Backup/Alternative |
|-------|-------------|-------------------|
| Data quality | Cleanlab | Great Expectations |
| UQ framework | TorchUncertainty | Custom ensembles |
| Conformal prediction | MAPIE (sklearn) or TorchCP (PyTorch) | puncc (deel-ai) |
| Calibration metrics | Uncertainty Toolbox | Custom |
| Drift detection | Alibi Detect | Custom KS tests |
| Explainability | SHAP + Captum | Alibi |
| Formal verification | alpha-beta-CROWN | Marabou 2.0 |
| Output validation | Custom (Pydantic models) | Guardrails AI patterns |
| Physics constraints | DeepXDE / PINA | Custom PINN loss |

### 6.3 Key Design Principles

1. **No single point of failure**: Every prediction must pass through multiple independent validation layers
2. **Quantified uncertainty on EVERY output**: Never return a point prediction without a confidence interval
3. **Conformal guarantees**: Use conformal prediction for hard statistical coverage guarantees
4. **Formal verification for safety classifiers**: If a NN makes yes/no safety decisions, formally verify it
5. **Graceful degradation**: When uncertain, defer to human; when very uncertain, trigger conservative safety action
6. **Full audit trail**: Every prediction logged with input, output, uncertainty, explanation, and validation status
7. **Continuous monitoring**: Drift detection catches distribution shift in real-time
8. **Physics-first**: Domain constraints encoded in architecture (PINNs) AND validated post-hoc

---

## 7. Sources

### Regulatory Documents
- [NRC AI Portal](https://www.nrc.gov/ai)
- [NRC AI Principles Paper (ML-24241A252)](https://www.nrc.gov/docs/ML2424/ML24241A252.pdf)
- [NRC Regulatory Framework Gap Assessment (ML-24290A059)](https://www.nrc.gov/docs/ML2429/ML24290A059.pdf)
- [NRC AI Strategic Plan](https://www.nrc.gov/docs/ML2313/ML23132A305.pdf)
- [IAEA Nuclear Safety Review 2025](https://www.iaea.org/sites/default/files/gc/gc69-inf2.pdf)
- [IAEA AI in Nuclear Technologies](https://www-pub.iaea.org/MTCD/publications/PDF/p15866-PUB2119_web.pdf)

### Academic Surveys
- [Hallucination Detection in Foundation Models for Decision-Making (ACM Computing Surveys)](https://dl.acm.org/doi/10.1145/3716846)
- [Conformal Prediction: A Data Perspective (ACM Computing Surveys)](https://dl.acm.org/doi/10.1145/3736575)
- [From Aleatoric to Epistemic: UQ Techniques in AI (arXiv 2501.03282)](https://arxiv.org/abs/2501.03282)
- [Fundamental flaws of PINNs and explainability (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S0360835225008502)
- [Trustworthy AI for nuclear safety (J. Nuclear Science & Technology 2025)](https://www.tandfonline.com/doi/full/10.1080/00223131.2025.2532066)
- [Reliability verification for AI in nuclear I&C (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S1738573325006643)
- [Formal Verification and Control With Conformal Prediction (IEEE)](https://ieeexplore.ieee.org/iel8/5488303/11274416/11274485.pdf)
- [Disentangling Aleatoric and Epistemic Uncertainty in PINNs (arXiv 2601.03673)](https://arxiv.org/html/2601.03673)
- [Marabou 2.0 Paper](https://theory.stanford.edu/~barrett/pubs/WIZ+24.pdf)
- [Neural Network Verification Tutorial](https://neural-network-verification.com/)
- [TorchUncertainty Paper (arXiv 2511.10282)](https://arxiv.org/html/2511.10282v1)
- [Engineering the RAG Stack (arXiv 2601.05264)](https://arxiv.org/html/2601.05264v1)

### Industry Reports
- [AI Guardrails Comparison 2026 (Galileo)](https://galileo.ai/blog/best-ai-guardrails-platforms)
- [Guardrails AI vs NeMo Guardrails Comparison](https://is4.ai/blog/our-blog-1/guardrails-ai-vs-nemo-guardrails-comparison-2026-352)
- [AI Agent Guardrails Production Guide 2026](https://authoritypartners.com/insights/ai-agent-guardrails-production-guide-for-2026/)
- [Awesome Safety-Critical Systems](https://awesome-safety-critical.readthedocs.io/)

### Curated Lists
- [awesome-conformal-prediction](https://github.com/valeman/awesome-conformal-prediction)
- [awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection)
- [awesome-uncertainty-deeplearning](https://github.com/ENSTA-U2IS-AI/awesome-uncertainty-deeplearning)
- [PINNpapers](https://github.com/idrl-lab/PINNpapers)
