# Agent Script Specification & Tools

**A comprehensive toolkit for defining, validating, and converting AI agent specifications between JSON and Markdown formats.**

Agent Script Tools provides structured specifications for AI agents, including their capabilities, interaction models, MCP integrations, and behavioral rules. Build production-ready AI agent configurations with type-safe validation and seamless format conversion.

---

## <i data-feather="zap" style="color: var(--md-primary-fg-color);"></i> Quick Start

Get up and running with Agent Script Tools in minutes:

```bash
# Clone the repository
git clone https://github.com/theagenticguy/agent-script.git
cd agent-script

# Install dependencies
uv sync --all-groups

# Try the example commands
uv run agent-script-json
uv run agent-script-markdown
```

## <i data-feather="star" style="color: var(--md-primary-fg-color);"></i> Key Features

<div class="grid cards" markdown>

-   <i data-feather="code" style="color: var(--md-primary-fg-color);"></i> **Structured Specifications**

    ---

    Define AI agents with comprehensive Pydantic models including capabilities, tools, and interaction workflows

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [Learn more](user-guide/specifications.md)

-   <i data-feather="repeat" style="color: var(--md-primary-fg-color);"></i> **Bi-directional Conversion** 

    ---

    Seamlessly convert between JSON and Markdown formats with full fidelity preservation

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [See examples](user-guide/conversion.md)

-   <i data-feather="link" style="color: var(--md-primary-fg-color);"></i> **MCP Integration**

    ---

    Native support for Model Context Protocol server integration and tool management

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [MCP guide](user-guide/mcp-integration.md)

</div>

## <i data-feather="terminal" style="color: var(--md-primary-fg-color);"></i> Command Line Interface

The toolkit provides rich CLI commands for working with agent specifications:

=== "View Specifications"

    ```bash
    # Show example agent in JSON format
    uv run agent-script-json
    
    # Show example agent in Markdown format  
    uv run agent-script-markdown
    
    # Show the JSON schema
    uv run show-spec-json
    ```

=== "Convert Formats"

    ```bash
    # Convert JSON to Markdown
    uv run convert-to-markdown examples/ai-engineer.json
    
    # Convert Markdown to JSON
    uv run convert-to-json examples/ai-engineer.md
    ```

=== "Schema Generation"

    ```bash
    # Generate JSON schemas from models
    uv run generate-schema
    ```

## <i data-feather="layers" style="color: var(--md-primary-fg-color);"></i> Project Architecture

This workspace contains two complementary packages:

<div class="grid cards" markdown>

-   <i data-feather="tool" style="color: var(--md-primary-fg-color);"></i> **agent-script-tools**

    ---

    CLI toolkit with conversion drivers and command implementations
    
    * Rich command-line interface
    * JSON ↔ Markdown conversion logic
    * Example specifications and templates

-   <i data-feather="package" style="color: var(--md-primary-fg-color);"></i> **agent-script-spec**

    ---

    Pydantic models defining the agent specification structure
    
    * Type-safe data models
    * Validation and serialization
    * JSON schema generation

</div>

## <i data-feather="code" style="color: var(--md-primary-fg-color);"></i> Example Usage

Here's a simple example of working with agent specifications:

```python
from agent_script_spec.models import AgentScriptSpecification
from agent_script_tools.drivers import to_markdown, from_markdown

# Load specification from JSON
with open("examples/ai-engineer.json") as f:
    spec = AgentScriptSpecification.model_validate_json(f.read())

# Convert to Markdown
markdown = to_markdown(spec)
print(f"Agent: {spec.name}")
print(f"Tools: {len(spec.frontmatter.tools)}")

# Convert back from Markdown
spec_from_md = from_markdown(markdown)
assert spec == spec_from_md  # Round-trip conversion preserves data
```

## <i data-feather="book-open" style="color: var(--md-primary-fg-color);"></i> What's Next?

<div class="grid cards" markdown>

-   <i data-feather="download" style="color: var(--md-primary-fg-color);"></i> **Installation Guide**

    ---

    Detailed setup instructions and development environment configuration

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [Get started](user-guide/installation.md)

-   <i data-feather="file-text" style="color: var(--md-primary-fg-color);"></i> **Specification Format**

    ---

    Complete reference for the agent specification format and all available fields

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [Learn format](user-guide/specifications.md)

-   <i data-feather="code" style="color: var(--md-primary-fg-color);"></i> **API Reference**

    ---

    Full API documentation for all classes, functions, and modules

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [Browse API](api-reference/)

-   <i data-feather="activity" style="color: var(--md-primary-fg-color);"></i> **Examples**

    ---

    Real-world examples and use cases for different types of AI agents

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [View examples](examples/)

-   <i data-feather="git-pull-request" style="color: var(--md-primary-fg-color);"></i> **RFC: Spec Simplification**

    ---

    Draft proposal to simplify the spec and use RFC 2119 terms

    <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> [Read the RFC](user-guide/rfc-simplify-spec.md)

</div>

---

<div style="text-align: center; margin: 2em 0; color: var(--md-default-fg-color--light);">
  <i data-feather="heart" style="color: #e91e63;"></i> 
  Built with <strong>Python 3.13+</strong>, <strong>Pydantic</strong>, and <strong>uv</strong>
</div>
