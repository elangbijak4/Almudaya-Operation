# Agentic Operation Specification v0.2

## Definisi
**Agentic Operation (AO)** adalah spesifikasi organisasi kerja multi-agent yang reusable, mission-oriented, deklaratif, dan dapat dieksekusi. Ia mendefinisikan misi, agent slots, roles, Skill bindings, topologi, komunikasi, workflow, Operational Behavior Specification (OBS), resource, governance, dan integrasi runtime.

- **Skill**: bagaimana suatu agent melakukan kapabilitas/prosedur.
- **Workflow**: urutan, dependency, dan transisi tugas.
- **Operation**: bagaimana sejumlah agent diorganisasi, diperlengkapi, dan dikoordinasikan untuk menyelesaikan misi.

Operation bukan sekadar kumpulan Skill dan bukan sinonim Workflow.

## Model formal
`OD = (I, M, A, R, S, T, C, W, B, Q, G, X)`

I identity/version; M mission/scope/deliverables/acceptance; A agent slots; R roles/authority; S Skill bindings; T topology; C communication; W workflow; B OBS; Q resources/budgets; G governance; X runtime integrations.

`OI = (OD, Θ, E, Σ, K)` dengan Θ parameter misi, E execution environment/dependencies, Σ mutable runtime state, K checkpoint/recovery metadata.

## Operational Behavior Specification (OBS)
OBS mendeklarasikan perilaku, bukan kode loop khusus misi:
- `execution_mode`: single_pass, sequential, parallel, iterative, conditional_loop, continuous, hierarchical, composite.
- iteration strategy: unit dan urutan yang diulang.
- feedback mechanism: sumber, evaluator, format, dan routing.
- continuation dan acceptance predicates.
- termination: success, failure, cancellation, deadline.
- recovery: retry, backoff, checkpoint restore, escalation, abort.
- reassignment: kondisi dan batas penggantian agent.
- guards: max iterations, wall-clock, cost/token, concurrency, no-progress, recursion depth.

### Loop scopes
- `task`: retry satu task yang gagal.
- `agent`: satu agent mengulang/refine hasilnya.
- `operation`: siklus kolektif beberapa role diulang.
- `nested_operation`: sub-Operation diulang oleh parent.

Setiap loop harus bounded dan memiliki batas iterasi, deadline, budget, no-progress guard, cancellation, serta idempotency/checkpoint policy yang eksplisit.

## Multi-hierarchical composition
Parent memanggil child melalui `operation_ref` dan kontrak input/output tervalidasi. Child memiliki versi, permission boundary, resource, OBS, status, dan output sendiri. Parent mengelola tujuan global, dependency, concurrency, integrasi hasil, dan final decision. Runtime wajib menerapkan version resolution, cycle detection, `max_nesting_depth`, aggregate budget, child budget isolation, dan cancellation propagation.

## Runtime semantics
Parse/schema validate → resolve dependencies → authorize resources → instantiate Operation Instance → execute workflow/topology per OBS → persist state/events/checkpoints → evaluate predicates → recover/escalate/terminate → emit outputs/audit trace.

`Σ(t+1) = F(OD, Θ, E, Σ(t), events(t))`

F adalah runtime generik. Scheduler, state machine, Loop Engine, router, policy enforcement, dan adapter tetap berupa kode. Yang dideklarasikan adalah logika organisasi dan perilaku spesifik misi.

## Integrasi Almudaya
AUCO memilih Operation; Registry menyimpan versi; Operation Manager mengelola lifecycle; Operation Runtime mengeksekusi deklarasi; Loop Engine menjalankan iterasi; Coordination Engine mengatur delegasi; Agent Manager mengelola agent; Resource Manager mengatur akses/kuota; Blackboard shared state; ACMA continuity/checkpoint/handoff; PKU persistent project knowledge.

## Prinsip
Declarative, model-agnostic, versioned, auditable, least privilege, bounded execution, explicit contracts, adapter-based integration, backward-compatible.
