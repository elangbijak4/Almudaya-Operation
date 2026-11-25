# Operation: Research Pipeline

**ID:** `almudaya.operation.research-pipeline`  
**Version:** `0.1.0`  
**Alias:** `#Operation-researchPipeline`  
**Pattern:** hybrid workflow, parallel specialist branches, bounded nested feedback loops.

## 1. Mission

Transform researcher-provided pre-writing materials into a structured, evidence-grounded scientific manuscript package. The Operation plans the paper, develops visual assets and a targeted literature review in parallel, writes the manuscript, and iteratively refines it against explicit quality criteria.

This Operation assists researchers. It does not independently establish scientific truth, guarantee novelty, or assume authorship/accountability.

## 2. Input model

Required inputs:
- `idea_summary`: research problem, proposed method, theoretical foundation, and claimed contribution.
- `experimental_log`: datasets, experimental setup, baselines, metrics, results, ablations, and observations.
- `latex_template`: target LaTeX template or template package reference.
- `venue_guidelines`: formatting, scope, citation, and submission requirements.

Optional input:
- `existing_figures`: user-provided diagrams, plots, and other visual assets.
- `bibliography_seed`: known references or BibTeX file.
- `author_instructions`: preferred narrative, constraints, and author decisions.

The Operation must distinguish missing information from information that can safely be derived. It must not invent experimental outcomes, citations, or author claims.

## 3. Organizational topology

Hybrid topology:
- `operation_coordinator`: owns mission, plan approval, stage scheduling, artifact integration, and escalation.
- `research_planner`: creates section outline, visualization plan, targeted literature strategy, and citation hints.
- `visualization_specialist`: creates conceptual diagrams, plots, and captions; obtains visual critique and revises assets.
- `literature_specialist`: discovers candidate literature, verifies identities/metadata, synthesizes sources, and creates citation registry/BibTeX.
- `citation_verifier`: validates bibliographic identity, DOI/identifier, metadata, and manuscript-to-reference consistency.
- `manuscript_writer`: drafts sections and integrates verified figures, tables, and citations into LaTeX.
- `quality_refiner`: evaluates the complete manuscript, generates actionable feedback, and proposes revisions.
- `human_researcher`: approves research framing, disputed claims, final scientific interpretation, and submission readiness.

## 4. Workflow

### Stage 1 — Outline generation
The planner inspects all supplied materials and creates:
- manuscript outline and section-level content plan;
- visualization plan with figure purpose, data source, and intended form;
- literature search strategy, thematic clusters, and citation hints;
- traceability map from claims to input evidence.

Output: `research_plan.json`.

### Stage 2A — Plot generation (parallel branch)
The visualization specialist follows the plan to produce:
- statistical plots derived from supplied experimental data;
- conceptual diagrams derived from the method description;
- captions and source/provenance metadata.

A visual critique loop evaluates factual correspondence, legibility, completeness, and consistency with the manuscript. The agent revises until accepted or a guard is reached.

Output: figure files, editable/source artifacts where available, captions, and `visual_asset_registry.json`.

### Stage 2B — Literature review (parallel branch)
The literature specialist:
1. discovers candidate sources using approved search resources;
2. deduplicates candidate records;
3. verifies bibliographic identity and metadata using authoritative metadata resources;
4. applies publication-date and relevance constraints;
5. builds a citation registry and BibTeX;
6. synthesizes literature into themes, methodological comparisons, and research-gap evidence.

Citation verification is rate-limited and may run sequentially even when candidate discovery is parallel. Unverified references must be marked unresolved and excluded from verified-citation claims.

Output: `citation_registry.json`, `.bib`, source evidence records, literature synthesis, and draft Introduction/Related Work content.

### Stage 3 — Section writing
The manuscript writer integrates the outline, verified literature, experimental log, figures, and tables into the supplied LaTeX template. It drafts remaining sections, extracts numeric values only from the experimental log, and maintains claim-to-evidence traceability.

Output: complete LaTeX draft and manuscript artifact manifest.

### Stage 4 — Iterative content refinement
The quality refiner evaluates the manuscript using configured criteria, produces structured review feedback, and proposes targeted revisions.

A candidate revision is accepted only if:
- overall quality score improves; or
- overall score ties and no required subscore regresses, subject to the configured acceptance rule.

If a revision decreases the overall score or violates a hard constraint, restore the previous accepted version. Stop at the iteration limit, deadline, budget limit, or no-progress guard.

Output: accepted manuscript version, evaluation reports, and revision history.

### Stage 5 — Finalization
Compile LaTeX to PDF, validate references and cross-references, check figure/table inclusion, inspect compilation errors, and produce the submission package. Human approval is required before external submission or publication.

## 5. Operational behavior (OBS)

Execution mode: `composite`.

- Stage 1 is sequential and produces the execution plan.
- Stages 2A and 2B are parallel branches.
- Stage 3 waits for required outputs from both branches.
- Stage 4 is an operation-level refinement loop.
- Plot critique is a nested agent-level/branch loop.
- Citation metadata verification is a rate-limited task sequence.
- Stage 5 is a finalization gate.

Default guards in this scaffold:
- maximum 3 manuscript refinement iterations;
- maximum 4 visual revision iterations per figure batch;
- maximum 2 retry attempts for retryable tasks;
- bounded wall-clock and cost budget;
- no-progress detection;
- cancellation propagation;
- explicit human approval for external submission.

These are configurable defaults, not claims about PaperOrchestra's exact internal configuration.

## 6. Quality and evidence policy

- Every empirical claim must trace to experimental-log evidence or an explicitly cited source.
- Never fabricate references, DOI values, datasets, metrics, or results.
- A search result is not itself citation verification.
- Separate verified references from candidate/unverified references.
- Generated conceptual diagrams must not introduce unsupported mechanisms or results.
- Plots must derive from supplied data or explicitly identified transformations.
- Numerical values in tables must trace to the experimental log.
- Record provenance for figures, tables, citations, and manuscript claims.
- LLM-based reviewers are advisory evaluators, not substitutes for expert judgment.
- The human researcher retains responsibility for scientific validity, originality, authorship, and submission.

## 7. Resource model

Resources are capability declarations, not hard-coded vendor dependencies:
- LLM/model endpoint for planning, synthesis, writing, and review;
- literature search provider;
- bibliographic metadata verification provider;
- scholarly full-text/abstract retrieval where licensed and available;
- plotting and diagram generation tools;
- optional image/VLM critique adapter;
- LaTeX compiler;
- artifact storage and versioning;
- optional DOI resolver and plagiarism/similarity checker.

Secrets must be injected by the Resource Manager and never exposed in Operation files or agent prompts.

## 8. Integration with Almudaya

- Blackboard: stage state, task coordination, artifact references, feedback, and decisions.
- ACMA: checkpoints, recovery, handoff, and continuity across agent/model changes.
- PKU: project context, approved terminology, prior research decisions, and reusable knowledge.
- Operation Registry: version-pinned Operation and child capability definitions.
- Resource Manager: resource resolution, access policy, quota, and budget.

## 9. Outputs

Minimum output package:
- `paper.tex`
- `paper.pdf`
- `references.bib`
- `figures/`
- `tables/` (where applicable)
- `research_plan.json`
- `citation_registry.json`
- `claim_evidence_map.json`
- `quality_review.json`
- `revision_history.json`
- `artifact_manifest.json`

## 10. Invocation

`/operation run almudaya.operation.research-pipeline`

`#Operation-researchPipeline` is a user-facing selector/alias. The runtime resolves it to the registered Operation ID and exact version.
