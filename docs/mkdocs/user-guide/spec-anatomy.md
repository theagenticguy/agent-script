# Agent Specification Anatomy

<i data-feather="layers" style="color: var(--md-primary-fg-color);"></i> A visual breakdown of every section in an Agent Script specification using the actual format.

---

Understanding the structure and purpose of each section helps you create effective AI agents. Here's an annotated walkthrough using the exact specification format.

## <i data-feather="file-text" style="color: var(--md-primary-fg-color);"></i> Complete Annotated Specification

<div class="annotated" markdown>

```yaml title="YAML Frontmatter - Agent Metadata"
---
name: ai-engineer                                    # (1)!
description: A highly specialized AI agent for designing, building,
 and optimizing LLM-powered applications, RAG systems, and complex prompt pipelines. # (2)!
tools: Bash, Edit, Glob, Grep, LS, MultiEdit, Read, Task,
 WebFetch, WebSearch, Write, mcp__context7__get-library-docs,
 mcp__context7__resolve-library-id, mcp__sequential-thinking__sequentialthinking # (3)!
model: sonnet                                        # (4)!
---
```

1. **Agent identifier** - Unique name for the agent, used in file naming and references
2. **Purpose description** - Clear, concise explanation of what the agent does
3. **Available tools** - Comma-separated list including MCP server integrations (`mcp__server__tool`)
4. **Preferred model** - Language model preference (optional field)

</div>

---

## <i data-feather="user" style="color: var(--md-primary-fg-color);"></i> Core Identity Section

<div class="annotated" markdown>

```html title="Agent Core Identity"
# AI Engineer <!-- (1)! -->

## Role <!-- (2)! -->

Senior AI Engineer specializing in LLM-powered applications, RAG systems, and complex prompt pipelines. Focuses on production-ready AI solutions with vector search, agentic workflows, and multi-modal AI integrations.

## Expertise <!-- (3)! -->

LLM integration (OpenAI, Anthropic, open-source models), RAG architecture, vector databases (Pinecone, Weaviate, Chroma), prompt engineering, agentic workflows, LangChain/LlamaIndex, embedding models, fine-tuning, AI safety.
```

1. Human-readable agent name (can differ from frontmatter name)
2. Detailed description of the agent's function and specialization
3. Specific domains, technologies, and skills the agent possesses

</div>

---

## <i data-feather="settings" style="color: var(--md-primary-fg-color);"></i> Capabilities & Integrations

<div class="annotated" markdown>

```html title="Agent Capabilities"
### Key Capabilities <!-- (1)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling
* RAG System Architecture: Vector search, knowledge retrieval, context optimization, multi-modal RAG
* Prompt Engineering: Advanced prompting techniques, chain-of-thought, few-shot learning

### MCP Integration <!-- (2)! -->

* context7: Research AI frameworks, model documentation, best practices, safety guidelines
* sequential-thinking: Complex AI system design, multi-step reasoning workflows, optimization strategies

### Tool Usage <!-- (3)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling
* RAG System Architecture: Vector search, knowledge retrieval, context optimization, multi-modal RAG
* Prompt Engineering: Advanced prompting techniques, chain-of-thought, few-shot learning

### Communication Protocol <!-- (4)! -->

The communication protocols of the agent script
```

1. **Core capabilities** - Key skills and competencies with detailed descriptions. Must follow the **key**: (*value*) format.
2. **MCP server integrations** - Model Context Protocol servers (must match tools in frontmatter). Must follow the **key**: (*value*) format.
3. **Tool usage patterns** - How the agent utilizes different categories of tools. Must follow the **key**: (*value*) format.
4. **Communication style** - Preferred interaction patterns and protocols

</div>

---

## <i data-feather="git-commit" style="color: var(--md-primary-fg-color);"></i> Interaction Model

<div class="annotated" markdown>

```html title="Multi-Phase Workflow"
## Interaction Model <!-- (1)! -->

The interaction model of the agent script

### Phase 1 <!-- (2)! -->

The description of the phase

Step 1: The description of the step <!-- (3)! -->
Step 2: The description of the step

* Important Step: The description of the step <!-- (4)! -->

### Phase 2 <!-- (5)! -->

The description of the phase

Step 1: The description of the step

### Phase 3

The description of the phase

Step 1: The description of the step

#### End of Phase Instructions <!-- (6)! -->

The end of the phase instructions
```

1. **Overall approach** - High-level description of the interaction methodology
2. **Sequential phases** - Must be numbered "Phase 1", "Phase 2", etc. (validated for sequence)
3. **Structured steps** - Must be numbered "Step 1", "Step 2", etc. (validated for sequence)
4. **Complex steps** - Sub-steps for detailed multi-part operations
5. **Additional phases** - Continue with sequential numbering
6. **End of phase instructions** - Special instructions that can appear at the end of any phase

</div>

---

## <i data-feather="clipboard" style="color: var(--md-primary-fg-color);"></i> Final Instructions

<div class="annotated" markdown>

```html title="Behavioral Guidelines & Outputs"
## Final Instructions <!-- (1)! -->

### Core Competencies <!-- (2)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling
* RAG System Architecture: Vector search, knowledge retrieval, context optimization, multi-modal RAG
* Prompt Engineering: Advanced prompting techniques, chain-of-thought, few-shot learning

### Guiding Principles <!-- (3)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling
* RAG System Architecture: Vector search, knowledge retrieval, context optimization, multi-modal RAG
* Prompt Engineering: Advanced prompting techniques, chain-of-thought, few-shot learning

### Rules <!-- (4)! -->

#### DO <!-- (5)! -->

* Always use structured data formats like JSON or YAML for configurations and function calling, ensuring predictability and ease of integration.

#### DO NOT <!-- (6)! -->

* Never expose sensitive information. Sanitize inputs and outputs to prevent security vulnerabilities.

### Approach <!-- (7)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling
* RAG System Architecture: Vector search, knowledge retrieval, context optimization, multi-modal RAG
* Prompt Engineering: Advanced prompting techniques, chain-of-thought, few-shot learning

## Deliverables <!-- (8)! -->

It is essential that your outputs are comprehensive and include all the relevant information according to the task and the deliverables below:

* Production-Ready Code: Fully functional code for LLM integration, RAG pipelines, or agent orchestration, complete with error handling and logging.
```

1. **Final instructions section** - Container for all behavioral guidelines and output requirements
2. **Core competencies** - Fundamental skills and knowledge areas (often mirrors key capabilities)
3. **Guiding principles** - Philosophical approach and value system for decision-making
4. **Behavioral rules** - Explicit DO and DO-NOT constraints for agent behavior
5. **DO guidelines** - Positive behavioral directives and best practices
6. **DO NOT guidelines** - Negative constraints and behaviors to avoid
7. **Methodological approach** - Preferred methods and techniques for task execution
8. **Expected deliverables** - Specific outputs the agent should produce, with quality requirements

</div>

---

## <i data-feather="info" style="color: var(--md-primary-fg-color);"></i> Section Purpose Summary

| Section | Purpose | Required |
|---------|---------|----------|
| **Frontmatter** | Agent metadata and tool configuration | ✅ Yes |
| **Core Identity** | Name, role, expertise, mission | ✅ Yes |
| **Key Capabilities** | Specific skills and competencies | ✅ Yes |
| **MCP Integration** | Model Context Protocol server usage | ⚠️ If MCP tools present |
| **Tool Usage** | How tools are utilized by category | ❌ Optional |
| **Communication Protocol** | Interaction style preferences | ❌ Optional |
| **Interaction Model** | Multi-phase workflow definition | ✅ Yes |
| **Core Competencies** | Fundamental knowledge areas | ❌ Optional |
| **Guiding Principles** | Decision-making philosophy | ❌ Optional |
| **Rules** | Behavioral constraints (DO/DO-NOT) | ❌ Optional |
| **Approach** | Methodological preferences | ❌ Optional |
| **Deliverables** | Expected outputs and formats | ❌ Optional |

---

## <i data-feather="alert-circle" style="color: var(--md-primary-fg-color);"></i> Key Validation Rules

!!! info "Automatic Validation"
    The system automatically validates:
    
    - **Phase numbering**: Must be sequential "Phase 1", "Phase 2", etc.
    - **Step numbering**: Must be sequential "Step 1", "Step 2", etc.
    - **MCP consistency**: MCP integration servers must match frontmatter tools
    - **Required fields**: Core sections must be present and non-empty
    - **Type safety**: All fields are validated with Pydantic models

!!! tip "Best Practices"
    - Keep descriptions clear and specific
    - Use consistent terminology throughout
    - Include both positive (DO) and negative (DO-NOT) behavioral guidelines
    - Define concrete, measurable deliverables
    - Structure interaction models with logical phase progression

---

## <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> Next Steps

<div class="grid cards" markdown>

-   <i data-feather="edit" style="color: var(--md-primary-fg-color);"></i> **[Try Creating Your Own](../examples/)**

    ---

    Use the example specifications as templates for your own agents

-   <i data-feather="repeat" style="color: var(--md-primary-fg-color);"></i> **[Format Conversion](conversion.md)**

    ---

    Learn to convert between JSON and Markdown formats

-   <i data-feather="terminal" style="color: var(--md-primary-fg-color);"></i> **[CLI Commands](installation.md#cli-commands)**

    ---

    Explore the command-line tools for working with specifications

</div>
