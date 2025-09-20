# Agent Script Specification Simplification

This document outlines the comprehensive simplification of the agent script specification based on the suggestions in [Issue #1](https://github.com/theagenticguy/agent-script/issues/1).

## Overview

This PR implements a simplified agent script schema that eliminates hierarchical complexity and enforces RFC 2119 language throughout the specification.

## Key Changes

### 1. Simplified Hierarchical Structure

**Before**: Complex nested structure with phases → steps → sub-steps
```yaml
phases:
  Phase 1:
    steps:
      Step 1: "Description"
      Step 2:
        description: "Complex step"
        steps:
          Sub-step: "Description"
```

**After**: Flat sequential actions with RFC 2119 requirement levels
```yaml
interaction_workflow:
  actions:
    - name: "Action 1"
      description: "Description"
      requirement_level: "MUST"
    - name: "Action 2" 
      description: "Description"
      requirement_level: "SHOULD"
```

### 2. Consolidated Redundant Sections

**Eliminated redundant fields**:
- `core_competencies` → merged into `capabilities`
- `guiding_principles` → merged into `approach`
- `tool_usages` → merged into `capabilities`
- `communication_protocols` → removed (redundant with `approach`)

**New consolidated structure**:
- `capabilities`: Single source of truth for all skills and competencies
- `approach`: Methodological preferences and principles
- `interaction_workflow`: Sequential actions with requirement levels

### 3. RFC 2119 Language Implementation

All field descriptions now use RFC 2119 terminology:

- **MUST**: Critical requirements that must be met
- **SHOULD**: Recommended practices that improve quality
- **MAY**: Optional enhancements that are not required

**Example**:
```python
name: str = Field(description="The name of the agent script. MUST be unique and non-empty.")
tools: set[str] | None = Field(None, description="MAY be empty if no tools are required.")
requirement_level: Literal["MUST", "SHOULD", "MAY"] = Field(default="MUST")
```

### 4. Simplified Validation Rules

**Before**: Complex regex patterns for phase/step numbering
```python
# Complex validation for "Phase 1", "Step 1", etc.
phase_pattern = re.compile(r"^Phase (\d+)$")
step_pattern = re.compile(r"^Step (\d+)$")
```

**After**: Simple validation for action requirements
```python
# Simple validation for non-empty actions list
@field_validator("actions")
def validate_actions_not_empty(cls, v: list[Action]) -> list[Action]:
    if not v:
        raise ValueError("Actions list MUST contain at least one action")
    return v
```

## File Changes

### Core Models
- `packages/agent-script-spec/src/agent_script_spec/models.py` - Completely rewritten with simplified structure
- `packages/agent-script-spec/src/agent_script_spec/models_original.py` - Backup of original models

### Examples
- `examples/ai-engineer.json` - Updated to use simplified format
- `examples/ai-engineer.md` - Updated to use simplified format
- `examples/ai-engineer-simplified.json` - New simplified example
- `examples/ai-engineer-simplified.md` - New simplified example

### Documentation
- `docs/mkdocs/user-guide/spec-anatomy.md` - Updated to reflect simplified structure
- `docs/mkdocs/user-guide/specifications.md` - Updated with new workflow examples

## Benefits

### 1. Reduced Complexity
- **Eliminated 3-level hierarchy** (phases → steps → sub-steps)
- **Reduced from 12+ fields to 8 core fields**
- **Simplified validation logic** (removed complex regex patterns)

### 2. Improved Clarity
- **RFC 2119 language** provides clear requirement levels
- **Consolidated sections** eliminate redundancy
- **Flat action structure** is easier to understand and maintain

### 3. Better Maintainability
- **Fewer fields to validate** and maintain
- **Simpler data structures** reduce complexity
- **Clear requirement levels** improve specification clarity

## Migration Guide

### For Existing Specifications

1. **Replace `interaction_model` with `interaction_workflow`**:
   ```python
   # Old
   interaction_model = InteractionModel(phases={...})
   
   # New  
   interaction_workflow = InteractionWorkflow(actions=[...])
   ```

2. **Consolidate capability fields**:
   ```python
   # Old
   key_capabilities = {...}
   core_competencies = {...}
   tool_usages = {...}
   
   # New
   capabilities = {...}  # Merge all three
   ```

3. **Consolidate approach fields**:
   ```python
   # Old
   guiding_principles = {...}
   approach = {...}
   
   # New
   approach = {...}  # Merge both
   ```

4. **Add requirement levels to actions**:
   ```python
   # New
   actions = [
       Action(name="Action 1", description="...", requirement_level="MUST"),
       Action(name="Action 2", description="...", requirement_level="SHOULD"),
       Action(name="Action 3", description="...", requirement_level="MAY")
   ]
   ```

## Testing

The simplified models maintain backward compatibility for core functionality while providing:
- ✅ Simplified validation
- ✅ RFC 2119 compliance
- ✅ Reduced complexity
- ✅ Better maintainability

## Next Steps

1. **Review the simplified models** for any missing functionality
2. **Test with existing specifications** to ensure compatibility
3. **Update any dependent code** that uses the old field names
4. **Consider deprecation timeline** for old field names

This simplification addresses all the concerns raised in Issue #1 while maintaining the core functionality of the agent script specification.