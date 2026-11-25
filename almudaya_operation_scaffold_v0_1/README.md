# Almudaya Agentic Operations — PoC Scaffold v0.1

This scaffold contains three illustrative, reusable Operation Definitions:

1. `01_scientific_literature_review` — hierarchical research organization.
2. `02_software_feature_delivery` — hybrid software delivery organization.
3. `03_dataset_analysis` — pipeline-oriented analysis with an independent validation stage.

## Directory contract

Each Operation directory contains:
- `operation.yaml`: declarative Operation Definition.
- `schemas/input.schema.json`: example input contract.
- `schemas/output.schema.json`: example output contract.
- `README.md`: purpose and instantiation notes.

## Format note

`operation.yaml` is written as JSON syntax, which is valid YAML 1.2. This avoids
requiring a YAML emitter to inspect or parse the example. A production schema
should be formalized and versioned before being treated as a stable API.

## Runtime integration requirements

This is a PoC **document scaffold**, not an executable plugin by itself.
To execute it, Almudaya Multi-Agent needs:
1. an Operation Definition parser and schema validator;
2. an Operation Registry and version resolver;
3. an instantiation engine mapping role slots to available bot runtimes;
4. Skill and resource resolvers;
5. a communication adapter implementing `almudaya.operation-message.v1`;
6. lifecycle, monitoring, persistence, and audit support;
7. explicit permission enforcement and human approval gates.

The scaffold intentionally does not assume internal API names or existing
Blackboard/ACMA interfaces. Bind those through adapters rather than duplicating
their responsibilities.

## Suggested PoC demonstration

Run each Operation with mock agents first. Verify role assignment, message
handoffs, required acknowledgements, artifact contracts, failure reporting,
and final validation. Only then connect real tools or external side effects.
