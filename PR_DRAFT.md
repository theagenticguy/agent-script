# Draft PR: Simplify Agent Script Specification and Adopt RFC 2119 Terminology

This draft PR proposes an approach to address Issue #1 by simplifying the specification structure and standardizing requirement language.

## Summary

- Simplify the interaction model by flattening the hierarchy
- Consolidate overlapping sections for clarity
- Adopt RFC 2119 requirement terminology (MUST/SHOULD/MAY)

## Changes Included

- Add RFC document: `docs/mkdocs/user-guide/rfc-simplify-spec.md`
- Link RFC from `README.md`
- (Docs) Add link entry in docs index to surface the RFC

## Rationale

The current hierarchical model (Phases → Steps → ComplexStep) increases complexity without clear downstream benefits. A flatter structure maintains expressiveness while improving readability and tooling ergonomics. RFC 2119 terms reduce ambiguity and improve consistency.

## Migration

- During a transition window, tooling SHOULD support both old and new schemas
- Provide a converter to flatten nested steps into sequential tasks with prefixed labels

## References

- Issue #1: https://github.com/theagenticguy/agent-script/issues/1
- RFC 2119: https://datatracker.ietf.org/doc/html/rfc2119
- RFC 8174: https://www.rfc-editor.org/rfc/rfc8174

---

If approved, follow-up PRs will implement model and converter changes in `packages/agent-script-spec` and `src/agent_script_tools`.

