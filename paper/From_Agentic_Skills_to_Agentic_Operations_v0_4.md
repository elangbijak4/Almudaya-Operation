# From Agentic Skills to Agentic Operations: A Dynamic Swarm Manifold Abstraction for Multi-Agent Systems

**Almudaya Research Institute**  
*Conceptual & Runtime-Aligned Architecture Paper — Version 0.4 | November 2026*

---

## Abstract

Agentic systems increasingly employ reusable capability packages—commonly termed **Agentic Skills** (`#Skill`)—to equip individual LLM-based agents with domain instructions, procedures, scripts, and progressive-disclosure resources. While Skills excel at encapsulating procedural expertise for single-agent execution, complex missions spanning multiple autonomous agents require an explicit organizational layer that governs dynamic role realization, capability distribution, write fencing, inter-agent routing, resource budgets, bounded iteration semantics, and human approval gates. This paper introduces the **Agentic Operation (`#Operation`, AO)** as a mission-oriented **Dynamic Swarm Manifold** abstraction that lifts procedural single-agent Skills into reusable, runtime-independent collective organizations. Unlike static workflow graphs or rigid org-charts that pre-allocate fixed agent rosters, an Operation (`almudaya.operation/v0.3`) specifies *Role Archetypes* realized on the fly through a set-valued dynamic map $\mu_t: R_{\text{active}}(t) \rightrightarrows B_t$ supporting just-in-time spawning, idle recycling, role coalescing, apoptosis, and formal separation-of-duties (*anti-affinity*). We formally prove a continuous degenerate reduction ($L=1 \leftrightarrow L>1$) showing how single-agent `#Skill` execution emerges as the $B_t = \{b_0\}$ boundary case of an Operation, introduce a typed AST predicate grammar (`PredicateExpr`) for the Operational Behavior Specification (OBS), position AO rigorously against classical organizational MAS models (MOISE+, OperA, JaCaMo) and contemporary agent frameworks/protocols (MetaGPT, AutoGen, CrewAI, LangGraph, MCP, A2A), and demonstrate both a static semantic validator and a 1-to-1 declarative conversion of *PaperOrchestra* (`#Operation-researchPipeline`).

**Keywords:** Agentic AI; Agent Skills; Agentic Operation; Dynamic Swarm Manifold; Multi-Agent Systems; Operational Behavior Specification; Capability Governance.

---

## 1. Introduction

Large language model (LLM) agents increasingly rely on modular capability packages called **Agentic Skills** (`#Skill`) to discover and progressively load procedural expertise when tasks demand specialized workflows [Anthropic, 2025]. However, practical multi-agent software engineering, scientific discovery, and analytical missions expose an **abstraction gap**: sharing identical or complementary `#Skill` packages across several agents does not define *who owns which artifact*, *which roles must remain isolated to prevent confirmation bias*, *how concurrent writes are fenced*, *when agents should be spawned or dissolved*, or *when iterative critique loops must roll back and escalate*.

At the same time, dynamic multi-agent runtimes—such as *Almudaya Multi-Agent*—reject fixed, predefined static agent teams in favor of an **elastic swarm manifold**, where worker processes are spawned just-in-time on the fly, coordinated over a persistent Session Blackboard and GoalLedger, governed by atomic protocols and capability tokens, and dissolved when tasks complete. Encoding such missions solely in ad-hoc orchestration code couples organizational policy to specific runtime codebases, whereas naive static YAML pipelines break emergent swarm adaptability.

We propose **Agentic Operation (`#Operation`, AO)** (`almudaya.operation/v0.3`) to resolve this tension: an explicit, versioned, declarative **Dynamic Swarm Manifold specification** that shapes how multi-agent topologies form, adapt, coordinate, and terminate on the fly.

The paper makes **six** contributions:
- **C1.** It formalizes the **compositional lifting** from single-agent `#Skill` packages to multi-agent `#Operation` manifolds and proves continuous degenerate reduction ($L=1 \leftrightarrow L>1$) back to single-agent Skill execution (**Proposition 1**).
- **C2.** It defines an orthogonal 10-tuple `Operation Definition` (`OD`) and time-indexed `Operation Instance` (`OI(t)`) featuring ephemeral *Role Archetype* lifecycles, *Role Coalescing*, *Anti-Affinity* constraints, and three orchestration regimes (`emergent`, `blueprint_seeded`, `stage_gated`).
- **C3.** It upgrades the **Operational Behavior Specification (OBS)** with a deterministic, typed AST predicate language (`PredicateExpr`), cleanly separating `role` feedback from `resource_evaluator` feedback across four bounded loop scopes.
- **C4.** It establishes a zero-impedance runtime binding to atomic governance protocols (write-fencing `CapabilityToken`s, transactional dead-end/handoff routing, dynamic rules, and `PrGate`) and hierarchical *sub-manifold* delegation with cycle and budget isolation.
- **C5.** It positions Agentic Operation systematically against classical MAS organization models (MOISE+, OperA, JaCaMo) and modern LLM agent ecosystems (MetaGPT, AutoGen, CrewAI, LangGraph, MCP, A2A), and provides an automated **Static Semantic Validator**.
- **C6.** It demonstrates synchronized declarative conversions of *PaperOrchestra* (`#Operation-researchPipeline`) and three dynamic swarm manifold patterns verified at zero schema or semantic errors.

---

## 2. From Agentic Skills to Dynamic Swarm Manifolds

### 2.1 Agentic Skills as Procedural Capability Packages
**Definition 1 (Agentic Skill).** An *Agentic Skill* (`#Skill`) is a discoverable, versionable procedural capability package encapsulating instructions, methods, entry points, and optional tools/references that enables an individual agent to execute a category of tasks via progressive context disclosure [Anthropic, 2025].

### 2.2 Why Multi-Agent Missions Require Organizational Lifting (and Not Static Pipelines)
Distributing missions across agents introduces structural, epistemic, and operational concerns outside `#Skill` scope: (1) *dynamic role composition & cardinality*, (2) *epistemic isolation (anti-affinity)* between generator and verifier roles, (3) *write-fencing and Blackboard ACLs*, (4) *dead-end & handover routing*, (5) *bounded refinement loops with non-regressing rollback*, and (6) *hardware/token budgeting and HITL approval gates*.

At the same time, forcing every mission into a rigid predefined DAG fails when tasks demand **emergent** discovery (e.g., debugging an unknown production defect). Hence an `#Operation` acts as a **Dynamic Swarm Manifold Field**: it defines the *potential roles*, *invariants*, *rules*, and *boundaries* from which the active bot topology emerges and morphs dynamically at runtime.

| Abstraction | Primary Concern | Question Addressed |
|---|---|---|
| **Agent / Bot** | Autonomous runtime process | Which active entity executes an assigned unit of work? |
| **Skill (`#Skill`)** | Procedural capability | How can an agent perform a category of task? |
| **Tool / MCP** | Executable capability interface | What external interface or tool can an authorized role invoke? |
| **Workflow** | Task progression & dependencies | How do tasks depend on and trigger one another? |
| **Memory (Blackboard / PKU)** | Transient & persistent knowledge | What state is shared ephemerally or retained across runs? |
| **Operation (`#Operation`)** | Dynamic swarm organization & mission governance | How is a multi-agent manifold dynamically realized, equipped, fenced, coordinated, and bounded to fulfill a mission? |

---

## 3. Related Work and Conceptual Positioning

While the v0.3 draft cited foundational MAS surveys [Horling & Lesser, 2004; Jennings, 2000; Wooldridge, 2009], positioning `#Operation` rigorously requires direct comparison with **classical declarative MAS organizations**, **modern LLM multi-agent frameworks**, and **agent interoperability protocols**:

1. **Classical MAS Organization Models (MOISE+, OperA, JaCaMo):**
   - **MOISE+** [Hübner et al., 2007] and **JaCaMo** [Boissier et al., 2013] pioneered separating *Structural* (roles, groups, links), *Functional* (social goal schemes), and *Deontic* (permissions/obligations) specifications from concrete agents; **OperA** [Dignum, 2004] formalized organizational contracts and social interaction scenes.
   - *What AO adds:* Classical models assume deterministic BDI/normative agents and static normative obligations, lacking (a) progressive-disclosure `#Skill` bindings tailored to finite-context LLM reasoning, (b) hardware- and token-budgeted ephemeral bot lifecycles ($L=1 \leftrightarrow L>1$ coalescing/apoptosis), and (c) stochastic evaluator-driven bounded refinement loops (`PredicateExpr` acceptance and artifact rollback).
2. **Modern LLM Multi-Agent Frameworks (MetaGPT, AutoGen, CrewAI, LangGraph):**
   - **MetaGPT** [Hong et al., 2024] embeds Standard Operating Procedures (SOPs) into code/prompt templates; **AutoGen** [Wu et al., 2023] structures conversational agent patterns in Python; **CrewAI** offers role/task YAML presets coupled to its Python executor; **LangGraph** models state machines directly in application code.
   - *What AO adds:* AO makes organizational topology, ACG permissions, monotonic write-fencing, OBS loop bounds, and sub-operation contracts **a standalone, schema-validated, runtime-independent specification** rather than library-specific Python control flow.
3. **Interoperability Protocols (MCP and A2A):**
   - **MCP** [Anthropic, 2024] standardizes agent-to-tool/data bindings; **A2A** [Google, 2025] standardizes opaque peer agent task delegation across vendors.
   - *Complementary layer:* `#Operation` sits **above** MCP and A2A—declaring *which Role Archetypes* receive *which MCP server grants* (`mcp.invoke`) and *which governance, budget, and anti-affinity rules* govern A2A/Blackboard delegation.

---

## 4. Formal Model of Agentic Operation v0.3

### 4.1 Orthogonal Operation Definition (`OD`) and Dynamic Instance (`OI(t)`)

To eliminate schema redundancy between agent slots and role cardinalities, `almudaya.operation/v0.3` represents an Operation Definition as an orthogonal 10-tuple:

$$OD = (I, M, R, T, C, W, B, Q, G, X)$$

where $I$ denotes versioned identity metadata; $M$ mission objective, scope, deliverables, acceptance criteria, and paired `input_schema`/`output_schema`; $R$ Role Archetypes, Skill bindings, ACG capabilities, default access modes, ephemeral lifecycle policies, and `anti_affinity` rules; $T$ topology shape, `orchestration_regime`, `continuity` policy, `crystallization_policy`, and `sub_operations`; $C$ message protocol, Blackboard ACLs, and dead-end routing; $W$ optional `seed_stages` and dynamic mutation policy; $B$ OBS (`protocol_bindings`, `loops`, typed `termination`, `recovery`); $Q$ resource contracts, monotonic write fencing, and hardware advisor thresholds; $G$ `dynamic_rules`, `hitl_gates`, `prohibited_actions`, and `hierarchy_safety`; and $X$ runtime integration bindings (Blackboard, PKU, ACG, GoalLedger, MCP) plus observability.

At runtime instant $t$, an Operation Instance is:

$$OI(t) = \bigl(OD, \Theta, E(t), \Sigma(t), K(t)\bigr)$$

with validated mission inputs $\Theta$, live execution environment $E(t)$ (active bot set $B_t$, dynamic realization map $\mu_t$, provisioned tools/models), mutable runtime state $\Sigma(t)$, and checkpoint/recovery metadata $K(t)$.

### 4.2 Dynamic Realization Map $\mu_t$, Coalescing, Anti-Affinity, and $L=1$ Reduction

At step $t$, active roles $R_{\text{active}}(t) \subseteq R$ are mapped to live bot processes $B_t$ via a set-valued map:

$$\mu_t : R_{\text{active}}(t) \rightrightarrows B_t$$

subject to cardinality constraints $\text{card}_{\min}(r) \le |\mu_t(r)| \le \text{card}_{\max}(r)$ for active roles and **Anti-Affinity Invariants** for every pair $(r_i, r_j) \in \text{AntiAffinity}(R)$:
- **`strict_distinct_bot`**: $\mu_t(r_i) \cap \mu_t(r_j) = \emptyset$ at all $t$.
- **`epoch_reset_required`**: $b \in \mu_t(r_i) \cap \mu_{t'}(r_j)$ is permitted across distinct epochs $t' > t$ only after context isolation and `fenceEpoch` increment.

**Proposition 1 (Degenerate $L=1$ Reduction to Single-Agent `#Skill`).**  
*Let $OD$ satisfy `l1_single_agent_fallback = true` and `allow_role_coalescing = true`, with no `strict_distinct_bot` anti-affinity constraint among mandatory roles. Under minimal mission load or hardware pressure where $|B_t| = 1$ ($B_t = \{b_0\}$), the realization map collapses to $\mu_t(r) = \{b_0\}$ for all $r \in R_{\text{active}}(t)$. All assigned `#Skill` sets union onto $b_0$, inter-role messaging $C$ reduces to internal turn transitions, and $OD$ reduces isomorphically to single-agent `#Skill` execution under `PrGate` verification—while preserving the capacity to expand continuously to $|B_{t+1}| > 1$ whenever dynamic task pressure triggers `spawn_worker_bot`.*

This formalizes why `#Operation` is a true **organizational generalization / lifting** of `#Skill`: `#Skill` execution is literally the single-bot $L=1$ boundary of the manifold.

### 4.3 Three Orchestration Regimes and On-the-Fly Crystallization
1. **`emergent` (Stigmergic Swarm):** `seed_stages = []`, `allow_dynamic_task_mutation = true`. Only mission objective, role archetypes, protocol limits, and dynamic rules are declared; task graphs and worker populations grow and dissolve organically.
2. **`blueprint_seeded` (Adaptive Manifold):** `seed_stages` initializes `GoalLedger` tasks, which may split, add specialists, or re-route via `PrMEend`/`PrDE` on the fly.
3. **`stage_gated` (Governed Phase Manifold):** Strict sequential/parallel stage gates are enforced by `PrGate`, while workers inside each stage remain ephemeral (`stage_activated → stage_completed`).

When `crystallization_policy.allow_on_the_fly_synthesis = true`, a Master agent (`BOT000`) can synthesize an ad-hoc `OD` at runtime for novel missions; if `crystallize_on_success = true` and `PrGate` succeeds, the realized topology and effective role bindings are serialized and persisted back to the Registry as a reusable versioned `#Operation`.

---

## 5. Operational Behavior Specification (OBS), Atomic Protocols, and Governance

### 5.1 Deterministic `PredicateExpr` AST
To eliminate free-text runtime ambiguity, all loop predicates (`continuation_predicate`, `acceptance_predicate`, `rollback_predicate`) and `termination` guards are typed ASTs (`PredicateExpr`) combining `all`, `any`, and `not` over `PredicateAtom` comparisons (`eq | neq | gt | gte | lt | lte | in`) addressing validated namespaces (`ledger.*`, `protocol.*`, `budget.*`, `gate.*`, `artifact.*`, `candidate.*`, `accepted.*`, `error.*`, `child.*`) against literal `value` or sibling state `ref`. Furthermore, `feedback_sources` explicitly tags `{ kind: "role" | "resource_evaluator", ref }` so model evaluators (e.g., `visual_critic`) cannot be confused with agent roles.

### 5.2 Protocol & Governance Grounding
Every `v0.3` Operation binds declaratively to 10 atomic `IProtocol` primitives, `ACG`, and `DynamicRules`:
- **Write Concurrency & Blackboard Isolation:** Concurrent edits across workers (`cardinality.max > 1`) are serialized via `PrModerator` `CapabilityToken`s carrying monotonic `fenceEpoch` values and `EXCLUSIVE_WRITE` / `SHARED_READ` / `REVIEW_ONLY` globs, complemented by scoped `blackboard_acl` entries.
- **State Machine Continuity:** Runtime `Σ(t)` aligns across lifecycle states including explicit `paused_hitl` and `paused_master_unavailable` transitions preserving tokens and checkpoints.
- **Sub-Manifold Composition:** Parent Operations delegate `PrModerator` seats (`delegate_moderator: true`) to registered child Operations with partitioned `budget_share_percent` ($\sum \le 100$), schema-checked `input_mapping`/`output_mapping`, cycle detection, and `max_nesting_depth` enforcement.

---

## 6. Automated Static Semantic Validation

A standalone validator (`tools/validate_operations.py`) enforces 9 static checks prior to runtime instantiation: (1) strict Draft 2020-12 schema validation (`additionalProperties: false`); (2) valid paired `input_schema`/`output_schema` and `sample-input.json`; (3) 1-to-1 `deliverables` ↔ `output_schema` parity; (4) `REVIEW_ONLY` least-privilege capability checks and `anti_affinity` vs `l1_single_agent_fallback` satisfiability; (5) role & evaluator resource resolution; (6) intra-operation stage DAG acyclicity; (7) `sub_operations` budget sum $\le 100\%$; (8) cross-operation semver resolution, cycle detection, and `max_nesting_depth`; and (9) parent-child `input_mapping`/`output_mapping` schema type alignment.

---

## 7. Research Agenda and Empirical Evaluation Plan

Future empirical benchmarks (`RQ1`–`RQ5`) will compare (1) single-agent `#Skill` baseline, (2) static non-reusable multi-agent workflow, and (3) `almudaya.operation/v0.3` Dynamic Swarm Manifold executed atop *Almudaya Multi-Agent* across completion rate, hallucination/regression frequency, token consumption, peak resident bots, and recovery time under injected faults.

---

## 8. Conclusion

*Agentic Operation v0.3* reconciles reusable organizational governance with real-time, ephemeral multi-agent swarms. By treating roles as dynamically realized archetypes ($\mu_t$), proving degenerate $L=1$ reduction to `#Skill`, enforcing typed `PredicateExpr` OBS semantics, and binding cleanly to write-fenced `IProtocol` governance, `#Operation` provides an actionable blueprint for adaptive multi-agent engineering.

---

## References

- Anthropic (2024). *Model Context Protocol (MCP) Specification*.
- Anthropic (2025). *Equipping Agents for the Real World with Agent Skills*.
- Boissier, O., Bordini, R. H., Hübner, J. F., Ricci, A., & Santi, A. (2013). *Multi-Agent Oriented Programming with JaCaMo*. Science of Computer Programming, 78(6), 747–761.
- Dignum, V. (2004). *A Model for Organizational Interaction: Based on Agents, Founded in Logic*. PhD Thesis, Utrecht University.
- Google (2025). *Agent2Agent (A2A) Protocol Specification*.
- Hong, S., et al. (2024). *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*. ICLR 2024 (arXiv:2308.00352).
- Horling, B., & Lesser, V. (2004). *A Survey of Multi-Agent Organizational Paradigms*. The Knowledge Engineering Review, 19(4), 281–316.
- Hübner, J. F., Sichman, J. S., & Boissier, O. (2007). *Developing Organised Multiagent Systems Using the MOISE+ Model*. IJAOSE, 1(3/4), 370–395.
- Jennings, N. R. (2000). *On Agent-Based Software Engineering*. Artificial Intelligence, 117(2), 277–296.
- Song, Y., Song, Y., Pfister, T., & Yoon, J. (2026). *PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing*. arXiv:2604.05018.
- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley.
- Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv:2308.08155.

---

## Appendix A: Declarative Conversion of *PaperOrchestra* (`#Operation-researchPipeline`)

Synchronized directly with `almudaya_operation_v0_3/04_research_pipeline/operation.yaml`, the *PaperOrchestra* pipeline [Song et al., 2026] maps to a `stage_gated` hybrid manifold (`almudaya.operation.research-pipeline`, v0.3.0):
- **8 Role Archetypes:** `operation_coordinator` (`master`), `research_planner`, `visualization_specialist`, `literature_specialist`, `citation_verifier`, `manuscript_writer`, `quality_refiner`, and `human_researcher` (`human`).
- **Strict Epistemic Anti-Affinity:** `strict_distinct_bot` separating `manuscript_writer` from both `citation_verifier` and `quality_refiner` (`l1_single_agent_fallback: false`).
- **Typed OBS Loops:** `visual_critique_loop` (`scope: agent`, `feedback_sources: [{ kind: resource_evaluator, ref: visual_critic }]`) and `manuscript_refinement_loop` (`scope: operation`, `feedback_sources: [{ kind: role, ref: quality_refiner }, { kind: resource_evaluator, ref: manuscript_evaluator }]`) encoding the exact overall-score improvement and non-negative subscore tie-breaker predicates alongside regression rollback.
- **10 Contracted Deliverables:** `latex_source`, `pdf`, `bibliography`, `figures`, `research_plan`, `citation_registry`, `claim_evidence_map`, `quality_report`, `revision_history`, and `artifact_manifest`.

---

## Appendix B: Demonstrative Dynamic Swarm Manifold Operations

Three complementary `v0.3` specifications demonstrate the full spectrum of dynamic topologies:
1. **Emergent Swarm Bug Hunt (`01_emergent_bug_hunt`):** `orchestration_regime: emergent`, `seed_stages: []`, `l1_single_agent_fallback: true` with `epoch_reset_required` anti-affinity and `crystallization_policy` enabled.
2. **Iterative Software Quality Loop (`02_iterative_quality_loop`):** `orchestration_regime: blueprint_seeded`, bounded `implement → test → review → evaluate` loop, `strict_distinct_bot` between `developer` and `reviewer`.
3. **Multi-Hierarchical Sub-Manifold (`03_multi_hierarchy_manifold`):** `sub_manifold` parent orchestrating three concrete child Operations (`research-branch` 30%, `technical-assessment` 35%, `integration-quality-gate` 25%) via delegated `PrModerator` seats and verified `input_mapping`/`output_mapping`.

---

## Appendix C: Repository Contract and Verification Results

Each Operation package follows a strict directory contract (`operation.yaml`, `Operation.md`, `schemas/input.schema.json`, `schemas/output.schema.json`, `examples/sample-input.json`). Automated validation via `python tools/validate_operations.py` and `python -m unittest discover -s tests -v` verifies 0 schema or semantic violations across all 7 `v0.3` Operations and all 3 remediated `v0.2` Operations.
