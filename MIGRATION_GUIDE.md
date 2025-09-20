# Migration Guide: Simplified Agent Script Specification

This guide explains the changes made to simplify the agent script specification and provides instructions for migrating existing specifications.

## Overview of Changes

The simplified specification addresses the suggestions in [Issue #1](https://github.com/theagenticguy/agent-script/issues/1) by:

1. **Flattening hierarchical structures** - Eliminated complex phase/step/sub-step hierarchy
2. **Removing redundant fields** - Consolidated overlapping sections
3. **Enforcing RFC 2119 language** - Added clear requirement levels using MUST/SHOULD/MAY

## Key Changes

### 1. Flattened Interaction Model

**Before (Complex Hierarchy):**
```json
{
  "interaction_model": {
    "description": "...",
    "phases": {
      "Phase 1": {
        "description": "...",
        "steps": {
          "Step 1": "...",
          "Step 2": {
            "description": "...",
            "steps": {
              "Sub-step": "..."
            }
          }
        }
      }
    }
  }
}
```

**After (Simplified Workflow):**
```json
{
  "workflow": {
    "description": "...",
    "steps": [
      {
        "description": "Analyze requirements",
        "requirements": [
          "MUST gather complete requirements",
          "SHOULD identify challenges early"
        ]
      }
    ],
    "completion_criteria": "Solution MUST be functional and tested"
  }
}
```

### 2. Consolidated Redundant Fields

**Before (Multiple Overlapping Fields):**
- `key_capabilities` + `core_competencies` 
- `guiding_principles` + `approach` + `rules`
- `tool_usages` (redundant with frontmatter `tools`)

**After (Consolidated Fields):**
- `capabilities` (single field for all capabilities)
- `requirements` (single field for all behavioral rules using RFC 2119)
- Removed `tool_usages` (use frontmatter `tools` instead)

### 3. RFC 2119 Compliance

**Before (Ambiguous Language):**
```json
{
  "rules": {
    "DO": ["Always use structured data formats"],
    "DO-NOT": ["Never expose sensitive information"]
  }
}
```

**After (RFC 2119 Language):**
```json
{
  "requirements": [
    {
      "requirement": "MUST use structured data formats like JSON or YAML for configurations"
    },
    {
      "requirement": "MUST NOT expose sensitive information and MUST sanitize inputs"
    }
  ]
}
```

## Migration Steps

### Step 1: Update Your Model Imports

```python
# Old import
from agent_script_spec.models import AgentScriptSpecification

# New import
from agent_script_spec.simplified_models import SimplifiedAgentScriptSpecification
```

### Step 2: Update Conversion Tools

```python
# Old drivers
from agent_script_tools.drivers import to_markdown, from_markdown

# New drivers
from agent_script_tools.simplified_drivers import to_markdown, from_markdown
```

### Step 3: Transform Your Specification

Use this mapping to convert your existing specification:

| Old Field | New Field | Notes |
|-----------|-----------|-------|
| `key_capabilities` | `capabilities` | Merge with `core_competencies` |
| `core_competencies` | `capabilities` | Merge with `key_capabilities` |
| `interaction_model` | `workflow` | Flatten phases/steps into simple step list |
| `rules` | `requirements` | Convert to RFC 2119 language |
| `guiding_principles` | `requirements` | Convert to RFC 2119 language |
| `approach` | `requirements` | Convert to RFC 2119 language |
| `tool_usages` | *(removed)* | Use frontmatter `tools` instead |
| `communication_protocols` | `communication_style` | Renamed for clarity |

### Step 4: Convert Rules to RFC 2119 Format

Transform your existing rules using these patterns:

- **"Always do X"** → **"MUST do X"**
- **"Should do Y"** → **"SHOULD do Y"**  
- **"Can do Z"** → **"MAY do Z"**
- **"Never do A"** → **"MUST NOT do A"**

## Example Migration

### Before (Original Format)
```json
{
  "key_capabilities": {
    "Development": "Build applications"
  },
  "core_competencies": {
    "Architecture": "Design systems"
  },
  "interaction_model": {
    "phases": {
      "Phase 1": {
        "steps": {
          "Step 1": "Analyze requirements"
        }
      }
    }
  },
  "rules": {
    "DO": ["Use best practices"],
    "DO-NOT": ["Expose secrets"]
  }
}
```

### After (Simplified Format)
```json
{
  "capabilities": {
    "Development": "Build applications",
    "Architecture": "Design systems"
  },
  "workflow": {
    "steps": [
      {
        "description": "Analyze requirements",
        "requirements": ["MUST gather complete requirements"]
      }
    ]
  },
  "requirements": [
    {
      "requirement": "MUST use best practices for development"
    },
    {
      "requirement": "MUST NOT expose secrets or sensitive information"
    }
  ]
}
```

## Validation

After migration, validate your specification:

```python
from agent_script_spec.simplified_models import SimplifiedAgentScriptSpecification

# Load and validate
spec = SimplifiedAgentScriptSpecification.model_validate(your_data)

# Check RFC 2119 compliance
rfc_keywords = ["MUST", "SHOULD", "MAY"]
for req in spec.requirements or []:
    has_rfc = any(keyword in req.requirement.upper() for keyword in rfc_keywords)
    if not has_rfc:
        print(f"Warning: Non-RFC 2119 requirement: {req.requirement}")
```

## Benefits of Migration

1. **Reduced Complexity**: Simpler structure is easier to understand and maintain
2. **Clear Requirements**: RFC 2119 language eliminates ambiguity
3. **Better Validation**: Stricter validation catches errors early
4. **Improved Usability**: Flatter structure reduces cognitive load
5. **Standards Compliance**: Follows established RFC conventions

## Backward Compatibility

The original models and drivers remain available for backward compatibility:

- `agent_script_spec.models` - Original complex models
- `agent_script_tools.drivers` - Original conversion tools

However, we recommend migrating to the simplified format for new projects and updating existing ones when possible.

## Support

If you encounter issues during migration:

1. Check the validation error messages for specific guidance
2. Review the example specifications in `examples/`
3. Run the test suite to verify your changes
4. Open an issue if you need assistance

The simplified specification maintains all the power of the original while being much easier to use and understand.