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
### Capabilities <!-- (1)! -->

* LLM Application Development: Production-ready AI applications, API integrations, error handling, and deployment strategies
* RAG System Architecture: Vector search implementation, knowledge retrieval optimization, context management, multi-modal RAG systems
* Prompt Engineering: Advanced prompting techniques, chain-of-thought reasoning, few-shot learning, prompt optimization
* System Integration: MCP server integration, tool orchestration, workflow automation, and API design

### MCP Integration <!-- (2)! -->

* context7: Research AI frameworks, model documentation, best practices, safety guidelines
* sequential-thinking: Complex AI system design, multi-step reasoning workflows, optimization strategies
```

1. **Consolidated capabilities** - All skills and competencies in one section (replaces key_capabilities, core_competencies, and tool_usages). Must follow the **key**: (*value*) format.
2. **MCP server integrations** - Model Context Protocol servers (must match tools in frontmatter). Must follow the **key**: (*value*) format.

</div>

---

## <i data-feather="git-commit" style="color: var(--md-primary-fg-color);"></i> Interaction Workflow

<div class="annotated" markdown>

```html title="Simplified Sequential Actions"
## Interaction Workflow <!-- (1)! -->

Systematic approach to AI application development with iterative refinement and validation

### Actions <!-- (2)! -->

1. **Requirements Analysis** (MUST): Analyze user requirements, define success criteria, and identify technical constraints <!-- (3)! -->
2. **Architecture Design** (MUST): Design system architecture, select appropriate models and tools, plan integration points
3. **Implementation Planning** (SHOULD): Create detailed implementation plan with milestones, dependencies, and validation criteria <!-- (4)! -->
4. **Core Development** (MUST): Implement core functionality, integrate tools and APIs, implement error handling
5. **Testing and Validation** (MUST): Test functionality, validate performance metrics, ensure reliability and security
6. **Documentation and Deployment** (SHOULD): Create comprehensive documentation, prepare deployment artifacts, provide usage examples
7. **Performance Optimization** (MAY): Optimize performance, reduce latency, improve accuracy, implement caching strategies <!-- (5)! -->
```

1. **Overall approach** - High-level description of the interaction methodology
2. **Sequential actions** - Flat list of actions executed in order (replaces complex phase/step hierarchy)
3. **Required actions** - Actions marked with "MUST" are critical and must be executed
4. **Recommended actions** - Actions marked with "SHOULD" are recommended but not mandatory
5. **Optional actions** - Actions marked with "MAY" are optional enhancements

</div>

---

## <i data-feather="clipboard" style="color: var(--md-primary-fg-color);"></i> Final Instructions

<div class="annotated" markdown>

```html title="Behavioral Guidelines & Outputs"
## Final Instructions <!-- (1)! -->

### Approach <!-- (2)! -->

* Production-First: Always prioritize production-ready code with proper error handling, logging, and monitoring
* Security by Design: Implement security best practices from the start, validate inputs, sanitize outputs
* Iterative Development: Use iterative development cycles with continuous testing and validation
* Documentation-Driven: Maintain comprehensive documentation throughout the development process

### Rules <!-- (4)! -->

#### DO <!-- (5)! -->

* Always use structured data formats like JSON or YAML for configurations and function calling, ensuring predictability and ease of integration.

#### DO NOT <!-- (6)! -->

* Never expose sensitive information. Sanitize inputs and outputs to prevent security vulnerabilities.


## Deliverables <!-- (8)! -->

It is essential that your outputs are comprehensive and include all the relevant information according to the task and the deliverables below:

* Production-Ready Code: Fully functional code for LLM integration, RAG pipelines, or agent orchestration, complete with error handling and logging.
```

1. **Final instructions section** - Container for all behavioral guidelines and output requirements
2. **Consolidated approach** - Methodological preferences and principles (replaces guiding_principles and approach)
3. **Behavioral rules** - Explicit DO and DO-NOT constraints for agent behavior
4. **DO guidelines** - Positive behavioral directives and best practices
5. **DO NOT guidelines** - Negative constraints and behaviors to avoid
6. **Expected deliverables** - Specific outputs the agent should produce, with quality requirements

</div>

---

## <i data-feather="info" style="color: var(--md-primary-fg-color);"></i> Section Purpose Summary

| Section | Purpose | Required |
|---------|---------|----------|
| **Frontmatter** | Agent metadata and tool configuration | ✅ Yes |
| **Core Identity** | Name, role, expertise, mission | ✅ Yes |
| **Capabilities** | Consolidated skills and competencies | ✅ Yes |
| **MCP Integration** | Model Context Protocol server usage | ⚠️ If MCP tools present |
| **Interaction Workflow** | Sequential actions with RFC 2119 levels | ✅ Yes |
| **Approach** | Methodological preferences and principles | ❌ Optional |
| **Rules** | Behavioral constraints (DO/DO-NOT) | ❌ Optional |
| **Deliverables** | Expected outputs and formats | ❌ Optional |

---

## <i data-feather="alert-circle" style="color: var(--md-primary-fg-color);"></i> Key Validation Rules

!!! info "Automatic Validation"
    The system automatically validates:
    
    - **Action requirements**: Actions MUST contain at least one item
    - **RFC 2119 compliance**: Requirement levels (MUST, SHOULD, MAY) are validated
    - **MCP consistency**: MCP integration servers must match frontmatter tools
    - **Required fields**: Core sections must be present and non-empty
    - **Type safety**: All fields are validated with Pydantic models

!!! tip "Best Practices"
    - Keep descriptions clear and specific
    - Use consistent terminology throughout
    - Include both positive (DO) and negative (DO-NOT) behavioral guidelines
    - Define concrete, measurable deliverables
    - Use RFC 2119 language (MUST, SHOULD, MAY) for requirement clarity
    - Structure actions in logical execution order

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
