# Agent Script Specification

A Pydantic-based specification library for defining AI agent configurations, capabilities, and interaction models. This package provides the core data models and validation logic for agent specifications that can be serialized to JSON or converted to/from Markdown.

## Overview

The Agent Script Specification defines a structured format for describing AI agents, including their:

- **Capabilities and expertise**
- **Tool integrations and MCP server connections**  
- **Multi-phase interaction workflows**
- **Behavioral rules and guidelines**
- **Expected deliverables**

## Installation

This package is designed to be used as part of the agent-script workspace, but can be installed independently:

```bash
# As part of the workspace
uv sync --all-groups

# Or install independently
pip install agent-script-spec
```

## Core Models

### AgentScriptSpecification

The main specification model that defines an AI agent:

```python
from agent_script_spec.models import AgentScriptSpecification

# Example structure
spec = AgentScriptSpecification(
    frontmatter=Frontmatter(
        name="example-agent",
        description="An example AI agent",
        tools={"tool1", "tool2"},
        model="gpt-4"
    ),
    name="Example Agent",
    role="Assistant for specific tasks",
    expertise="Domain-specific knowledge",
    mission="Primary objective",
    key_capabilities={"capability": "description"},
    interaction_model=InteractionModel(
        description="How the agent interacts",
        phases={"Phase 1": Phase(...)}
    ),
    # ... additional fields
)
```

### Frontmatter

Metadata for the agent specification, compatible with Claude Code subagents:

```python
from agent_script_spec.models import Frontmatter

frontmatter = Frontmatter(
    name="ai-engineer",
    description="AI development specialist", 
    tools={"read", "write", "execute", "mcp__context7__get-library-docs"},
    model="sonnet"
)

# Automatically extracts MCP server names
print(frontmatter.mcp_server_names)  # ["context7"]
```

### InteractionModel

Defines multi-phase interaction workflows with structured steps:

```python
from agent_script_spec.models import InteractionModel, Phase, ComplexStep

interaction = InteractionModel(
    description="Three-phase development process",
    phases={
        "Phase 1": Phase(
            description="Analysis and planning",
            steps={
                "Step 1": "Analyze requirements",
                "Step 2": ComplexStep(
                    description="Create detailed plan",
                    steps={
                        "Research": "Gather information",
                        "Design": "Create architecture"
                    }
                )
            },
            end_of_phase_instructions="Review with user before proceeding"
        )
    }
)
```

## Validation Features

The specification includes comprehensive validation:

### Step and Phase Validation

- **Monotonic numbering**: Steps must be numbered consecutively (Step 1, Step 2, etc.)
- **Phase ordering**: Phases must follow sequential numbering (Phase 1, Phase 2, etc.)

### MCP Integration Validation

- **Tool consistency**: MCP servers referenced in specifications must match tools in frontmatter
- **Server extraction**: Automatically extracts MCP server names from tool patterns like `mcp__server-name__tool`

### Type Safety

- **Strict typing**: Full MyPy compatibility with strict type checking
- **Pydantic validation**: Runtime validation of all fields and structures
- **Serialization support**: JSON serialization with proper handling of sets and complex types

## JSON Schema Generation

Generate JSON schemas for external tooling:

```python
from agent_script_spec.generate import generate_schemas
from agent_script_spec.models import AgentScriptSpecification

# Generate schema programmatically
schema = AgentScriptSpecification.model_json_schema()

# Or use the CLI command
generate_schemas()  # Creates dist/agent_script_spec.json
```

The generated schema includes:

- Full model validation rules
- Proper JSON Schema Draft 7 format
- Versioned schema URLs for stability
- Comprehensive field documentation

## CLI Integration

When used with the main `agent-script-tools` package, provides:

```bash
# Generate JSON schemas
uv run generate-schema

# Validate specifications (via conversion tools)
uv run convert-to-json spec.md  # Validates during conversion
```

## Example Usage

### Loading and Validating Specifications

```python
import json
from agent_script_spec.models import AgentScriptSpecification

# Load from JSON
with open("agent-spec.json") as f:
    data = json.load(f)
    spec = AgentScriptSpecification(**data)

# Direct JSON loading
with open("agent-spec.json") as f:
    spec = AgentScriptSpecification.model_validate_json(f.read())

# Serialize back to JSON
json_output = spec.model_dump_json(indent=2)
```

### Working with Complex Specifications

```python
from agent_script_spec.models import *

# Create a comprehensive agent specification
spec = AgentScriptSpecification(
    frontmatter=Frontmatter(
        name="data-analyst",
        description="Specialized data analysis agent",
        tools={"pandas", "matplotlib", "mcp__context7__resolve-library-id"},
        model="claude-3-5-sonnet"
    ),
    name="Data Analysis Expert", 
    role="Senior Data Analyst specializing in statistical analysis",
    expertise="Python data stack, statistical modeling, visualization",
    mission="Transform raw data into actionable insights",
    key_capabilities={
        "Statistical Analysis": "Advanced statistical methods and hypothesis testing",
        "Data Visualization": "Creating compelling charts and dashboards", 
        "Machine Learning": "Predictive modeling and pattern recognition"
    },
    mcp_integration={
        "context7": "Access to latest data science library documentation"
    },
    interaction_model=InteractionModel(
        description="Systematic approach to data analysis projects",
        phases={
            "Phase 1": Phase(
                description="Data exploration and understanding",
                steps={
                    "Step 1": "Load and examine data structure",
                    "Step 2": "Identify data quality issues",
                    "Step 3": ComplexStep(
                        description="Exploratory data analysis",
                        steps={
                            "Summary Statistics": "Calculate basic descriptive statistics",
                            "Distribution Analysis": "Examine data distributions",
                            "Correlation Analysis": "Identify relationships between variables"
                        }
                    )
                }
            ),
            "Phase 2": Phase(
                description="Analysis and modeling",
                steps={
                    "Step 1": "Apply appropriate analytical methods",
                    "Step 2": "Create visualizations and insights"
                },
                end_of_phase_instructions="Present findings and get feedback"
            )
        }
    ),
    rules={
        "DO": [
            "Always validate data quality before analysis",
            "Provide clear explanations of methodology",
            "Use appropriate statistical tests and confidence intervals"
        ],
        "DO-NOT": [
            "Never make claims without statistical backing",
            "Don't ignore missing data or outliers without justification"
        ]
    },
    deliverables={
        "Analysis Report": "Comprehensive report with findings and recommendations",
        "Visualizations": "Publication-ready charts and graphs", 
        "Code Documentation": "Well-documented analysis code with explanations"
    }
)

# Validation happens automatically
print(f"Agent: {spec.name}")
print(f"MCP Servers: {spec.frontmatter.mcp_server_names}")
```

## Dependencies

- **pydantic** (>=2.11.7): Core validation and serialization
- **loguru** (>=0.7.3): Structured logging for validation warnings

## Development

This package follows strict development practices:

- **Type Safety**: Full MyPy strict mode compliance
- **Testing**: Comprehensive test coverage with pytest
- **Documentation**: Google-style docstrings for all public APIs
- **Validation**: Runtime validation with clear error messages

## License

Licensed under the Apache License 2.0. See the main project LICENSE file for details.
