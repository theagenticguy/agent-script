# Agent Specification Format

<i data-feather="file-text" style="color: var(--md-primary-fg-color);"></i> Learn the complete structure for defining AI agents with comprehensive capabilities and interaction models.

---

The Agent Script Specification defines a structured format for describing AI agents using Pydantic models. This format ensures type safety, validation, and compatibility across different environments.

## <i data-feather="layers" style="color: var(--md-primary-fg-color);"></i> Specification Overview

An agent specification consists of several interconnected components:

```mermaid
graph TD
    A[AgentScriptSpecification] --> B[Frontmatter]
    A --> C[Core Identity]
    A --> D[Capabilities]
    A --> E[Interaction Model]
    A --> F[Rules & Guidelines]
    
    B --> B1[Name & Description]
    B --> B2[Tools & Model]
    B --> B3[MCP Servers]
    
    C --> C1[Role & Expertise]
    C --> C2[Mission Statement]
    
    D --> D1[Key Capabilities]
    D --> D2[MCP Integration]
    D --> D3[Tool Usages]
    
    E --> E1[Phases]
    E --> E2[Steps]
    E --> E3[Instructions]
    
    F --> F1[DO Rules]
    F --> F2[DO-NOT Rules]
    F --> F3[Approach]
    F --> F4[Deliverables]
```

---

## <i data-feather="info" style="color: var(--md-primary-fg-color);"></i> Frontmatter

The frontmatter contains metadata compatible with Claude Code subagents:

```python
from agent_script_spec.models import Frontmatter

frontmatter = Frontmatter(
    name="data-scientist",
    description="AI agent specialized in data analysis and machine learning",
    tools={
        "read", "write", "execute",
        "mcp__context7__get-library-docs",
        "mcp__sequential-thinking__sequentialthinking"
    },
    model="claude-3-5-sonnet"
)
```

### Properties

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Unique identifier for the agent |
| `description` | `str` | Brief description of the agent's purpose |
| `tools` | `set[str]` | Available tools and MCP integrations |
| `model` | `str \| None` | Preferred language model |

!!! info "MCP Server Detection"
    The frontmatter automatically extracts MCP server names from tool patterns like `mcp__server-name__tool-name`. Access via `frontmatter.mcp_server_names`.

---

## <i data-feather="user" style="color: var(--md-primary-fg-color);"></i> Core Identity

Define the agent's fundamental characteristics:

### Role & Expertise

```python
spec = AgentScriptSpecification(
    name="AI Research Assistant",
    role="Senior AI researcher specializing in natural language processing",
    expertise="Transformer architectures, fine-tuning, evaluation metrics, research methodologies",
    mission="Accelerate AI research by providing expert analysis and implementation guidance"
)
```

### Key Capabilities

Structure specific skills with detailed descriptions:

```python
key_capabilities = {
    "Literature Review": "Comprehensive analysis of recent papers, identifying trends and gaps",
    "Model Architecture": "Design and optimization of transformer-based models",
    "Experimental Design": "Statistical methodology for robust AI experiments",
    "Code Implementation": "PyTorch/TensorFlow implementations with best practices"
}
```

---

## <i data-feather="link" style="color: var(--md-primary-fg-color);"></i> MCP Integration

Define Model Context Protocol server integrations:

```python
mcp_integration = {
    "context7": "Access latest AI research papers and documentation",
    "sequential-thinking": "Complex reasoning workflows for research analysis",
    "arxiv-search": "Search and retrieve academic papers from ArXiv"
}
```

!!! warning "Validation Requirement"
    MCP integration keys must match server names extracted from tools in frontmatter. The system validates this consistency automatically.

---

## <i data-feather="git-commit" style="color: var(--md-primary-fg-color);"></i> Interaction Model

The interaction model defines multi-phase workflows with structured steps:

### Basic Structure

```python
from agent_script_spec.models import InteractionModel, Phase, ComplexStep

interaction_model = InteractionModel(
    description="Three-phase research methodology",
    phases={
        "Phase 1": Phase(
            description="Literature review and problem definition",
            steps={
                "Step 1": "Identify research question and scope",
                "Step 2": "Search relevant literature databases",
                "Step 3": ComplexStep(
                    description="Comprehensive literature analysis",
                    steps={
                        "Categorization": "Group papers by methodology and findings",
                        "Gap Analysis": "Identify limitations in current research",
                        "Synthesis": "Summarize state-of-the-art approaches"
                    }
                )
            },
            end_of_phase_instructions="Present literature review summary for approval"
        )
    }
)
```

### Phase Validation

Phases must follow these rules:

- **Sequential numbering**: "Phase 1", "Phase 2", "Phase 3", etc.
- **Monotonic ordering**: No gaps in numbering
- **Starting from 1**: First phase must be "Phase 1"

### Step Validation

Steps within each phase must follow:

- **Sequential numbering**: "Step 1", "Step 2", "Step 3", etc.
- **Monotonic ordering**: No gaps in numbering
- **Starting from 1**: First step must be "Step 1"

### Complex Steps

Use `ComplexStep` for multi-part operations:

```python
complex_step = ComplexStep(
    description="Data preprocessing and feature engineering",
    steps={
        "Data Cleaning": "Handle missing values and outliers",
        "Feature Selection": "Identify most relevant variables",
        "Scaling": "Normalize features for model training"
    }
)
```

---

## <i data-feather="shield" style="color: var(--md-primary-fg-color);"></i> Rules & Guidelines

### Behavioral Rules

Define what the agent should and should not do:

```python
rules = {
    "DO": [
        "Always cite sources when referencing research",
        "Validate statistical significance before making claims",
        "Provide confidence intervals for quantitative results"
    ],
    "DO-NOT": [
        "Never make claims without empirical support",
        "Don't ignore contradictory evidence",
        "Avoid overgeneralizing from limited datasets"
    ]
}
```

### Approach Guidelines

Define methodological preferences:

```python
approach = {
    "Statistical Rigor": "Use appropriate statistical tests and confidence intervals",
    "Reproducibility": "Ensure all experiments are documented and reproducible",
    "Ethical Considerations": "Address potential biases and fairness concerns"
}
```

---

## <i data-feather="target" style="color: var(--md-primary-fg-color);"></i> Deliverables

Specify expected outputs and formats:

```python
deliverables = {
    "Research Summary": "Comprehensive analysis document with findings and recommendations",
    "Code Implementation": "Well-documented, tested code following best practices",
    "Methodology Report": "Detailed explanation of experimental design and validation",
    "Results Dashboard": "Interactive visualization of key findings and metrics"
}
```

---

## <i data-feather="check-square" style="color: var(--md-primary-fg-color);"></i> Complete Example

Here's a full specification for an AI research assistant:

=== "Python Code"

    ```python
    from agent_script_spec.models import *

    # Create comprehensive AI research assistant
    research_assistant = AgentScriptSpecification(
        frontmatter=Frontmatter(
            name="ai-research-assistant",
            description="Advanced AI agent for research analysis and implementation",
            tools={
                "read", "write", "execute", "search",
                "mcp__context7__get-library-docs",
                "mcp__arxiv__search-papers"
            },
            model="claude-3-5-sonnet"
        ),
        name="AI Research Assistant",
        role="Senior AI researcher specializing in NLP and machine learning",
        expertise="Transformer architectures, fine-tuning, evaluation, research methodology",
        mission="Accelerate AI research through expert analysis and implementation",
        key_capabilities={
            "Literature Review": "Systematic analysis of recent papers and trends",
            "Model Design": "Architecture optimization for specific tasks",
            "Experimental Setup": "Rigorous experimental design and validation"
        },
        mcp_integration={
            "context7": "Access latest AI framework documentation",
            "arxiv": "Search and analyze academic papers"
        },
        interaction_model=InteractionModel(
            description="Systematic research methodology with iterative refinement",
            phases={
                "Phase 1": Phase(
                    description="Problem definition and literature review",
                    steps={
                        "Step 1": "Define research question and objectives",
                        "Step 2": "Conduct comprehensive literature search",
                        "Step 3": "Analyze and synthesize existing approaches"
                    }
                ),
                "Phase 2": Phase(
                    description="Design and implementation",
                    steps={
                        "Step 1": "Design experimental methodology",
                        "Step 2": "Implement solution with best practices",
                        "Step 3": "Validate approach with appropriate metrics"
                    },
                    end_of_phase_instructions="Review implementation before final analysis"
                )
            }
        ),
        rules={
            "DO": [
                "Always validate claims with empirical evidence",
                "Use appropriate statistical methods and confidence intervals",
                "Document all experimental procedures for reproducibility"
            ],
            "DO-NOT": [
                "Never make unsupported claims about model performance",
                "Don't ignore contradictory evidence or limitations",
                "Avoid using inappropriate evaluation metrics"
            ]
        },
        deliverables={
            "Research Analysis": "Comprehensive report with literature review and findings",
            "Implementation": "Production-ready code with documentation and tests",
            "Methodology": "Detailed experimental design and validation approach"
        }
    )
    ```

=== "JSON Output"

    ```json
    {
      "frontmatter": {
        "name": "ai-research-assistant",
        "description": "Advanced AI agent for research analysis and implementation",
        "tools": ["read", "write", "execute", "search", "mcp__context7__get-library-docs", "mcp__arxiv__search-papers"],
        "model": "claude-3-5-sonnet"
      },
      "name": "AI Research Assistant",
      "role": "Senior AI researcher specializing in NLP and machine learning",
      "expertise": "Transformer architectures, fine-tuning, evaluation, research methodology",
      "mission": "Accelerate AI research through expert analysis and implementation",
      "key_capabilities": {
        "Literature Review": "Systematic analysis of recent papers and trends",
        "Model Design": "Architecture optimization for specific tasks",
        "Experimental Setup": "Rigorous experimental design and validation"
      },
      "interaction_model": {
        "description": "Systematic research methodology with iterative refinement",
        "phases": {
          "Phase 1": {
            "description": "Problem definition and literature review",
            "steps": {
              "Step 1": "Define research question and objectives",
              "Step 2": "Conduct comprehensive literature search",
              "Step 3": "Analyze and synthesize existing approaches"
            }
          }
        }
      }
    }
    ```

---

## <i data-feather="alert-circle" style="color: var(--md-primary-fg-color);"></i> Validation Rules

The specification enforces several validation rules:

### Required Fields

!!! error "Missing Required Fields"
    These fields are mandatory for all specifications:
    
    - `frontmatter` with valid name, description
    - `name`, `role`, `expertise` 
    - `interaction_model` with at least one phase

### Format Constraints

!!! warning "Format Requirements"
    - Phase keys must match pattern: `Phase \d+` (e.g., "Phase 1")
    - Step keys must match pattern: `Step \d+` (e.g., "Step 1") 
    - Numbers must be sequential starting from 1
    - MCP integration keys must match extracted server names

### Type Safety

All fields are strictly typed with Pydantic validation:

```python
# This will raise a validation error
invalid_spec = AgentScriptSpecification(
    frontmatter=Frontmatter(name="", description=""),  # Empty name not allowed
    name=123,  # Must be string
    interaction_model="invalid"  # Must be InteractionModel object
)
```

---

## <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> Next Steps

<div class="grid cards" markdown>

-   <i data-feather="repeat" style="color: var(--md-primary-fg-color);"></i> **[Format Conversion](conversion.md)**

    ---

    Learn to convert between JSON and Markdown formats

-   <i data-feather="activity" style="color: var(--md-primary-fg-color);"></i> **[View Examples](../examples/)**

    ---

    Explore real-world agent specifications

</div>
