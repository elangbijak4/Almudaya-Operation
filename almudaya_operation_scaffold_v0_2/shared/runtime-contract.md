# Runtime Contract

Lifecycle minimum: `draft → validated → resolving → ready → running → succeeded | failed | cancelled | expired | terminated_by_guard`.

Runtime menyediakan schema/semantic validation, version-pinned dependency resolution, role/agent resolution, resource authorization, workflow scheduler, generic Loop Engine, predicate evaluator, cancellation, timeout, checkpoint/recovery, execution trace, dan audit events.

Adapter boundaries: Blackboard (shared scoped state), ACMA (checkpoint/handoff/recovery), PKU (retrieval/persistent knowledge), Resource Manager (tools/models/APIs/data/compute). Runtime tidak bergantung pada vendor model atau backend tertentu.
