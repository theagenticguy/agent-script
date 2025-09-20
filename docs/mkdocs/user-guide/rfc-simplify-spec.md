---
title: RFC - Simplify Specification and Use RFC 2119 Language
---

# RFC: Simplify Agent Script Specification and Enforce RFC 2119 Terminology

This RFC proposes changes to the Agent Script specification addressing the suggestions in Issue #1. It focuses on simplifying the interaction model structure and standardizing requirement language using RFC 2119 keywords.

## Goals

- Reduce structural complexity in the interaction model
- Remove redundant or overlapping sections
- Clarify requirement levels with RFC 2119 terminology

## Summary of Proposed Changes

1. Simplify Interaction Model
   - Replace nested `Phase -> Step -> ComplexStep` hierarchy with a flatter model where phases contain a sequence of tasks.
   - Allow optional labels and grouping without enforcing multi-level nesting.
2. De-duplicate Sections
   - Fold overlapping concepts:
     - Merge `key_capabilities` with `core_competencies` under a unified `capabilities` map.
     - Merge `tool_usages` into `communication_protocols` as a narrative section, or into `capabilities` as capability-specific notes.
3. RFC 2119 Language
   - Replace ambiguous language with clearly scoped requirements using MUST, SHOULD, MAY as defined in RFC 2119.

## Detailed Design

### 1) Interaction Model Simplification

Current:

```python
class ComplexStep(BaseModel):
    description: str
    steps: dict[str, str] | None

class Phase(BaseModel):
    description: str
    steps: dict[str, str | ComplexStep]
    end_of_phase_instructions: str | None

class InteractionModel(BaseModel):
    description: str
    phases: dict[str, Phase]
```

Proposed:

```python
class Task(BaseModel):
    title: str | None = None
    description: str

class Phase(BaseModel):
    title: str | None = None
    description: str | None = None
    tasks: list[Task]
    end_instructions: str | None = None

class InteractionModel(BaseModel):
    overview: str | None = None
    phases: list[Phase]
```

Validation:
- Phases MUST be provided as an ordered list (no numeric key parsing).
- Tasks within each phase MUST preserve author order; numbering MAY be rendered by tooling.
- `end_instructions` MAY appear for any phase.

Migration Strategy:
- Parser SHOULD accept both formats during a deprecation window.
- CLI converters SHOULD render the simplified structure; nested ComplexStep content SHOULD be flattened into sequential tasks using prefix labels (e.g., "Synthesis - ...").

### 2) Section Consolidation

Unify capabilities:

```python
capabilities: dict[str, str]
```

Rules and approach:
- Keep `rules` as DO/DO-NOT lists.
- Consolidate `approach`, `guiding_principles`, and `communication_protocols` into a single optional `guidance` markdown field for narrative guidance.

MCP integration:
- Keep existing validation tying `mcp_integration` keys to `frontmatter.tools` MCP servers. Error/warning semantics MUST be preserved.

### 3) RFC 2119 Requirements

Key requirements (non-exhaustive):
- Frontmatter `name` and `description` MUST be non-empty.
- `interaction_model.phases` MUST contain at least one phase.
- MCP `mcp_integration` keys MUST equal the set of MCP servers derived from tools when provided; when `tools` declare MCP servers but `mcp_integration` omits some, a warning SHOULD be emitted.
- Tooling MAY auto-number phases/steps for presentation.

## Backward Compatibility

- The JSON and Markdown converters SHOULD support both old and new schemas during a transition period.
- A conversion utility SHOULD be provided to upgrade existing specs, with idempotent output.

## Tooling Impact

- Update Pydantic models to the proposed structures.
- Adjust Markdown ↔ JSON drivers to read/write the simplified model.
- Update examples and documentation to reflect the new fields.

## Alternatives Considered

- Keep hierarchical `ComplexStep` and rely on UI rendering: rejected due to higher complexity and minimal practical benefit.
- Enforce numeric keys: replaced by ordered lists to reduce parsing constraints and avoid renumbering friction.

## Open Questions

- Should `guidance` remain a single markdown blob or be split into discrete subsections for searchability? Initial proposal uses a single field for flexibility.
- Do we need a `tags` or `categories` field to support discovery? Out of scope for this RFC but MAY be added later.

## Appendix: RFC 2119

This RFC uses requirement keywords as defined in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

## References

- Issue #1: https://github.com/theagenticguy/agent-script/issues/1
- RFC 2119: https://datatracker.ietf.org/doc/html/rfc2119
- RFC 8174: https://www.rfc-editor.org/rfc/rfc8174

