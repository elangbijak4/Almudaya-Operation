# Scientific Literature Review Operation

**Operation ID:** `almudaya.scientific-literature-review`  
**Version:** `0.1.0`  
**Status:** PoC declarative specification

## Purpose

Produce a traceable and evidence-grounded literature review for a defined research question.

## Files

- `operation.yaml` — complete declarative Operation Definition.
- `schemas/input.schema.json` — illustrative input contract.
- `schemas/output.schema.json` — illustrative output contract.

## Instantiation

An Operation Manager should load `operation.yaml`, validate the definition,
bind mission-specific parameters, resolve agent roles to available agent
runtimes, provision declared resources, and create an Operation Instance.

## Important

This folder is a **declarative PoC scaffold**, not a claim of immediate
executable compatibility with an existing Almudaya Multi-Agent runtime.
A loader/validator and runtime adapters must implement the schema and
message contract before execution. Do not enable external side effects
without explicit authorization.
