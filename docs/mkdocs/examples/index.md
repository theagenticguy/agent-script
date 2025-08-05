# Examples

<i data-feather="activity" style="color: var(--md-primary-fg-color);"></i> Real-world agent specifications demonstrating different use cases and patterns.

---

## <i data-feather="cpu" style="color: var(--md-primary-fg-color);"></i> AI Engineer Agent

The included AI Engineer example demonstrates a comprehensive agent specification with MCP integrations.

### View the Specification

=== "Markdown Format"

    ```bash
    # View the Markdown specification
    uv run agent-script-markdown
    
    # Or view the file directly
    cat examples/ai-engineer.md
    ```

=== "JSON Format"

    ```bash
    # View the JSON specification
    uv run agent-script-json
    
    # Or view the file directly
    cat examples/ai-engineer.json
    ```

### Key Features Demonstrated

<div class="grid cards" markdown>

-   <i data-feather="layers" style="color: var(--md-primary-fg-color);"></i> **Multi-Phase Interaction**

    ---
    
    Three-phase workflow from requirements to implementation with structured steps
    
-   <i data-feather="link" style="color: var(--md-primary-fg-color);"></i> **MCP Integration**

    ---
    
    Context7 and sequential-thinking servers for research and complex reasoning

-   <i data-feather="shield" style="color: var(--md-primary-fg-color);"></i> **Behavioral Rules**

    ---
    
    Clear DO and DO-NOT guidelines for secure, production-ready development

-   <i data-feather="target" style="color: var(--md-primary-fg-color);"></i> **Deliverables**

    ---
    
    Specific output requirements including code, tests, and documentation

</div>

---

## <i data-feather="play" style="color: var(--md-primary-fg-color);"></i> Try the Examples

### Convert Between Formats

```bash
# Convert JSON to Markdown
uv run convert-to-markdown examples/ai-engineer.json -o my-agent.md

# Convert Markdown to JSON  
uv run convert-to-json examples/ai-engineer.md -o my-agent.json
```

### Validate and Test

```bash
# Generate JSON schema
uv run generate-schema

# View the schema
uv run show-spec-json
```

---

## <i data-feather="edit" style="color: var(--md-primary-fg-color);"></i> Creating Your Own

Use the AI Engineer specification as a template:

1. **Copy the structure** from `examples/ai-engineer.md`
2. **Customize the identity** (name, role, expertise)
3. **Define your capabilities** and MCP integrations
4. **Design your interaction model** phases and steps
5. **Set behavioral rules** and expected deliverables
6. **Validate** with the conversion tools

---

## <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> Next Steps

<div class="grid cards" markdown>

-   <i data-feather="layers" style="color: var(--md-primary-fg-color);"></i> **[Spec Anatomy](../user-guide/spec-anatomy.md)**

    ---
    
    Understand every section of the specification format

-   <i data-feather="repeat" style="color: var(--md-primary-fg-color);"></i> **[Format Conversion](../user-guide/conversion.md)**

    ---
    
    Learn to work with JSON and Markdown formats

-   <i data-feather="code" style="color: var(--md-primary-fg-color);"></i> **[API Reference](../api-reference/)**

    ---
    
    Technical documentation for developers

</div>
