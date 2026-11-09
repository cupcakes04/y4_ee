---
name: research
description: Universal bridge between external research/literature (Gemini Notebook, web synthesis) and local workspace execution (Antigravity). Use to package local constraints into an external research packet, or to ingest a finalized technical specification into local code and tests.
---

# Universal Research-to-Execution Protocol

Maintain the local repository as the single source of truth (SSOT). Isolate open-ended conceptual exploration from bounded workspace implementation.

---

## 1. Outward Protocol: Package Context (Local -> Research)
Run when theoretical uncertainty, algorithm selection, or architectural decisions require external literature review.

1. **Scan Workspace Boundaries:**
   - Locate the target component, module, or schema.
   - Extract only non-negotiable constraints:
     - **I/O contracts:** Data schemas, types, dimensions, serialization formats.
     - **Resource bounds:** Compute limits, latency/throughput targets, memory ceilings, hardware interfaces.
     - **Environment bounds:** Runtime versions, OS, locked third-party dependencies.
2. **Compile Research Packet:**
   - Create a clean Markdown file under `docs/research/` (e.g., `docs/research/<topic>_brief.md`).
   - Include only three sections:
     1. **Target Objective:** Exact problem to solve and current failure/bottleneck mode.
     2. **Operating Envelopes:** The extracted I/O, resource, and environment constraints.
     3. **Evaluation Criteria:** Concrete conditions a proposed solution must satisfy to be viable.
   - *Rule:* Never copy raw source trees or implementation boilerplate into the brief.
3. **Yield Control:**
   - Output the file path and notify the user to feed the brief into external tools (NotebookLM, Deep Research, papers).

---

## 2. Inward Protocol: Ingest & Execute (Research -> Local)
Run when returning with a resolved technical decision, mathematical model, or external research outcome.

1. **Validate Specification:**
   - Read the incoming specification from `docs/research/` (or user prompt).
   - Reject ambiguous prose. The spec must define:
     - Exact algorithmic steps, formulas, or architectural state machines.
     - Interface signatures matching the local workspace.
     - Edge-case handling and numerical/logical boundary behavior.
2. **Construct Execution Plan:**
   - Break the implementation into sequential, atomic units:
     1. Type definitions, interfaces, and schemas.
     2. Core logic implementation.
     3. Boundary validation, error handling, and stability guards.
     4. Automated tests asserting the spec's expected outcomes.
3. **Implement & Verify:**
   - Apply edits directly to local workspace files.
   - Run the project's native build, lint, or test commands through the terminal.
   - **Triage Failures:**
     - *Syntactic / Integration errors:* Resolve locally inside the workspace.
     - *Theoretical / Invariant failures (math diverges, core contract violated):* Halt. Log the failure mechanics to `docs/research/<topic>_divergence.md` and prompt for clarification.

---

## Operating Invariants

* **Keep External Media Out of Git:** Do not save PDFs, vendor tars, or raw datasets in the project tree.
* **No Speculative Architecture:** If mathematical formulas or core interface contracts are missing from the spec, halt and request the missing invariants before writing code.
* **Deterministic Verification:** A task is only complete when local automated tests (unit, integration, or simulation) pass against the spec criteria.