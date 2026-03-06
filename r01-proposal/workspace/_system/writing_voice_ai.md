# AI/ML Domain Writing Voice
## Overrides for Artificial Intelligence / Machine Learning Sections

> **This file overrides `writing_voice.md` for AI/ML-domain content only.**
> Read by: `r01-writer-ai`, `r01-writer-integrator` (for AI-specific aim framing).
> Precedence: this file > `writing_voice.md` > `style_guide.md`.
> Updated by: `r01-evolution` after Draft Feedback Checkpoints with AI-domain corrections.

---

## Dimension Overrides

Only dimensions that differ from the generic voice are listed here. For all other dimensions, follow `writing_voice.md`.

### Dimension 1: Argumentative Style — Override

**Current calibration:** Limitation-of-existing-AI-first. The PI consistently: acknowledges existing AI success → pivots to real-world limitations → proposes a solution that directly addresses those limitations. The pivot is explicit and named, not implied.

**Evidence:** Observed in 2023Sepsis and consistent with Cardiotoxicity framing. The PI names the specific failure mode of existing AI before proposing the solution.

**Preferred:**
> "Despite the widely reported success of AI algorithms, fewer AI systems claim victory in real-world decision-making. The aforementioned AI-based content moderation systems seems to work well on social media platforms (e.g., Twitter), but it relies on human crowd workers to review or revise the algorithm prediction within a human-in-the-loop system architecture..." [2023Sepsis]

Also preferred:
> "While there is growing interest in using AI/ML models and AI-RPM tools to support clinical decision-making, major challenges remain: privacy concerns with commercial devices (e.g., smart speakers), false alerts due to a lack of patient context, the difficulty of interpreting and deriving insights from large amounts of fragmented data, a lack of appropriate clinician trust in and reliance on AI predictions in the system, and increased provider workload when the tools do not align with clinical workflow." [2025PostSurgery]

**Avoided:**
> Machine learning has shown promise in sepsis prediction, but there is room for improvement in this area.

### Dimension 2: Technical Depth — Override

**Current calibration:** Architecture-explicit with mathematical notation. For every ML method, specify: model family, architecture variant, input representation, loss function, optimization strategy, and evaluation protocol. The PI writes actual mathematical formulas with all parameters defined — this is unusually rigorous for R01 proposals and is a distinctive voice trait. Never say "we will use deep learning" without naming the specific architecture.

**Evidence:** Observed in 2023Sepsis: "The sepsis risk is defined as f_w(x,t) = H_0(t)exp(β^T s(x^(i))), a product of a baseline hazard function, H_0(t) = (ν/λ)(λt)^(ν-1), and the patient-specific sepsis risk which depends on the output of the transformer..." Full formulas with defined parameters appear in the Approach section.

**Preferred:**
> "We will use large-scale complex GI surgical EHR data (n=24,755) from OSUWMC to train an effective Weibull Cox proportional hazards (WCPH) model for time-dependent complication risk assessment. A Transformer neural network will be employed to model multimodal temporal medical event histories and estimate WCPH parameters." [2025PostSurgery]

Also preferred (mathematical notation):
> "The sepsis risk is defined as f_w(x,t) = H_0(t)exp(β^T s(x^(i))), a product of a baseline hazard function, H_0(t) = (ν/λ)(λt)^(ν-1)..." [2023Sepsis]

**Avoided:**
> We will use a transformer model on EHR data with cross-validation.

### Dimension 4: Hedging Tolerance — Override

**Current calibration:** Benchmark-grounded confidence. Make claims about model performance only when grounded in preliminary data or published baselines. For untested claims, use "We expect" with a specific rationale. Never claim SOTA without citing the current SOTA and the margin of improvement. Technical feasibility claims use "will" without hedging; performance claims use "expect" or "hypothesize" unless backed by preliminary data.

**Evidence:** Observed in 2023Sepsis: "We hypothesize that the onset of sepsis can be predicted before its clinical recognition." / "This method is expected to significantly improve the performance of sepsis onset prediction." Both hedge on outcomes, not on methods.

**Preferred:**
> "We will extract the data from the OSUWMC system and split the datasets into a 70% training set, a 10% validation set, and a 20% test set. We will train the model in the training set and select the model that achieves the best AUROC and AUPRC in the validation set to evaluate the performance in the test set." [2025PostSurgery — no hedging on method]

**Avoided:**
> Our advanced deep learning model will significantly outperform all existing approaches.

### Dimension 6: Interdisciplinary Framing — Override

**Current calibration:** HCAI-philosophy-explicit. When connecting AI to clinical use, always explain how model outputs translate to actionable clinical information. Address interpretability explicitly (Shapley values, attention maps, concept-based explanations) and describe how clinicians interact with them. The PI's explicit design paradigm is "Human-Centered AI (HCAI)" — name it as such and frame AI design around clinical workflow, not algorithmic capability.

**Evidence:** Observed in all 3 proposals. The Sepsis proposal grounds AI design in a four-step physician workflow. The Surgery proposal frames REACH-AI as a system that "integrates the system seamlessly into clinical workflow through human-centered designs." The Cardiotoxicity proposal explicitly names "HCAI system to support explainable human-AI decision-making."

**Preferred:**
> "To address these challenges, we propose a Human-Centered Artificial Intelligence (HCAI) system to collaborate with human domain experts in the high-stake and high-uncertainty decision-making process." [2023Sepsis]

**Avoided:**
> The model will provide interpretable predictions to clinicians.

---

## AI-Specific Conventions

### Baseline Comparison Ladder
The PI always compares against a three-tier ladder. Table format is preferred for presenting results:
1. **Clinical baseline**: Existing clinical scoring systems (SOFA, APACHE-II, NEWS-2, qSOFA, MEWS, SIRS) or current standard of care
2. **Statistical baseline**: Logistic regression or equivalent simple model on the same features
3. **ML baseline**: Best published ML result on the same or comparable dataset (with citation)

Outperforming only other deep learning models is insufficient for NIH reviewers. The clinical baseline comparison is mandatory. Observed in 2023Sepsis: "We will compare the proposed model with widely used warning scores (qSOFA, MEWS, NEWS, and SIRS) and DL-based risk prediction models."

### Uncertainty Quantification
The PI explicitly addresses epistemic, aleatoric, and propagated uncertainty. This is distinctive and should be included in any Approach section describing a predictive model. Observed in 2023Sepsis: "The extent of this bias depends on the nature of the function. When h(δ,x) is small enough (i.e, with local linearity) in the neighborhood near the imputed mean value µ_x, the propagated uncertainty is still accurate and able to guide the active sensing."

### Human-Centered AI Philosophy
The PI frames AI design around clinical workflow, not algorithmic capability. "HCAI" is the explicit design paradigm and should be named as such. The design process starts with an examination of the clinical workflow, identifies gaps, and then proposes AI capabilities to address those specific gaps. AI supports clinical expertise; it does not replace it.

### Ablation Studies
The PI pre-registers component ablations to justify pipeline complexity. Each component of a multi-stage pipeline should have a corresponding ablation study planned in the Approach section. This demonstrates that the complexity is justified and that each component contributes measurably.

### Model Specification Checklist
For every model described in Approach, specify:
- [ ] Architecture family and variant (with citation)
- [ ] Input representation and feature engineering
- [ ] Training procedure (optimizer, learning rate schedule, batch size, epochs)
- [ ] Regularization strategy (dropout, weight decay, early stopping)
- [ ] Evaluation protocol (cross-validation type, temporal split details, held-out test)
- [ ] Performance metrics (primary: AUROC, AUPRC; secondary: sensitivity, specificity, calibration)
- [ ] Class imbalance handling (oversampling, loss weighting, threshold optimization)
- [ ] Hyperparameter selection (grid search, Bayesian optimization, with validation set)

### External Validation and Generalizability
Address in every AI aim:
- Source of training data and its representativeness
- External validation plan (different institution, different time period, or both)
- Prospective validation plan if applicable
- Dataset shift considerations (temporal, demographic, institutional)
- Plan for multi-site deployment or federated learning if claiming generalizability

### Computational Reproducibility
Specify:
- Software frameworks and versions (PyTorch 2.x, scikit-learn 1.x)
- Hardware requirements (GPU type and memory for training)
- Random seed management
- Code and model sharing plan (GitHub, model registry)
- Data preprocessing pipeline reproducibility

---

## Anti-Hype Language Guide

Replace vague AI hype with precise technical language. Real examples from the PI's proposals show the pattern:

| Avoid | Use Instead | Real Example from PI |
|-------|-------------|----------------------|
| "revolutionary AI approach" | "achieves X% improvement over [baseline] on [benchmark]" | "a 94% prediction AUROC for sepsis, which is at the same level or higher than the performance of human experts" [2023Sepsis] |
| "state-of-the-art deep learning" | "[specific architecture] trained on [specific data]" | "We will use large-scale complex GI surgical EHR data (n=24,755) from OSUWMC to train an effective Weibull Cox proportional hazards (WCPH) model" [2025PostSurgery] |
| "cutting-edge AI" | "[method name] [citation], which addresses [specific limitation]" | "Despite the widely reported success of AI algorithms, fewer AI systems claim victory in real-world decision-making" [2023Sepsis] |
| "unprecedented accuracy" | "AUROC 0.87 (95% CI 0.84–0.90), compared to 0.71 for [baseline]" | "We will compare the proposed model with widely used warning scores (qSOFA, MEWS, NEWS, and SIRS)...on various metrics, including AUROC, AUPRC, sensitivity, and specificity" [2023Sepsis] |
| "leveraging the power of AI" | "using [specific method] to [specific task]" | "We will leverage Transformer as the backbone to predict the sepsis onset from the arrival at the hospital" [2023Sepsis] |
| "AI-driven insights" | "[model] generates [specific output] for [specific clinical decision]" | "provide consolidated summaries and visualizations of multimodal data that clinicians can easily interpret and act upon" [2025PostSurgery] |

---

## Feedback History

| Date | Project | Change | Source |
|------|---------|--------|--------|
| 2026-03-05 | All | Dim 1, 2, 4, 6 overrides updated; Baseline Comparison Ladder, Uncertainty Quantification, HCAI Philosophy, Ablation Studies conventions added; Anti-Hype table updated with real proposal quotes | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery) |

---

*Last updated: 2026-03-05. Seeded from PI's prior R01 proposals. Updated by evolution agent after AI-domain feedback.*
