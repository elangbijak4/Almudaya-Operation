# Almudaya #Operation-researchPipeline v0.1

Declarative conversion of the five-stage PaperOrchestra research-manuscript workflow into an Almudaya Agentic Operation.

## Contents
- `Operation.md`: human-readable operational specification.
- `operation.yaml`: structured Operation Definition using `almudaya.operation/v0.2`.
- `resources/`: resource requirements, adapters, and budget.
- `skills/`: role-to-Skill bindings.
- `schemas/`: input/output contracts.
- `policies/`: evidence, academic integrity, permissions, and refinement rules.
- `examples/`: sample input contract.
- `docs/paperorchestra-mapping.md`: mapping from the source paper to this Operation.

## Important
This is a declarative scaffold, not an executable implementation of PaperOrchestra. It generalizes the described workflow and does not claim to reproduce the authors' exact prompts, private implementation, or benchmark results. Resource adapters must be supplied by the Almudaya runtime.

## Invocation concept
`/operation run almudaya.operation.research-pipeline`

The UI alias `#Operation-researchPipeline` should resolve to a registry-pinned Operation ID and version.
