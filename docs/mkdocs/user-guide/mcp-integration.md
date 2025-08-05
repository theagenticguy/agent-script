# MCP Integration

<i data-feather="link" style="color: var(--md-primary-fg-color);"></i> Learn how to integrate Model Context Protocol (MCP) servers into your agent specifications.

---

Model Context Protocol (MCP) enables agents to connect to external data sources and services through standardized server integrations. Agent Script Tools provides built-in support for defining and validating MCP integrations.

## <i data-feather="server" style="color: var(--md-primary-fg-color);"></i> MCP Server Declaration

### Frontmatter Tools

Declare MCP tools in the frontmatter using the naming pattern `mcp__server-name__tool-name`:

```yaml
---
name: research-agent
description: AI agent with research capabilities
tools: read, write, mcp__context7__get-library-docs, mcp__sequential-thinking__analyze
model: claude-3-5-sonnet
---
```

### Automatic Server Detection

The system automatically extracts MCP server names from tool patterns:

```python
from agent_script_spec.models import Frontmatter

frontmatter = Frontmatter(
    name="research-agent",
    description="AI agent with research capabilities",
    tools={
        "read", "write", 
        "mcp__context7__get-library-docs",
        "mcp__context7__resolve-library-id", 
        "mcp__sequential-thinking__analyze"
    },
    model="claude-3-5-sonnet"
)

# Automatically extracted server names
print(frontmatter.mcp_server_names)
# Output: ["context7", "sequential-thinking"]
```

---

## <i data-feather="settings" style="color: var(--md-primary-fg-color);"></i> MCP Integration Section

Define how each MCP server is used in the specification:

```markdown
### MCP Integration

* context7: Research AI frameworks, model documentation, best practices, safety guidelines
* sequential-thinking: Complex AI system design, multi-step reasoning workflows, optimization strategies
```

### Validation Requirements

!!! warning "Server Consistency"
    MCP integration keys must match the servers extracted from frontmatter tools. The system validates this automatically:
    
    - ✅ **Valid**: Integration keys match extracted servers
    - ❌ **Error**: Extra servers not present in tools
    - ⚠️ **Warning**: Missing servers present in tools but not in integration

---

## <i data-feather="database" style="color: var(--md-primary-fg-color);"></i> Common MCP Servers

### Research & Documentation

=== "context7"

    **Purpose**: Access to library documentation and AI frameworks
    
    **Tools**:
    ```
    mcp__context7__get-library-docs
    mcp__context7__resolve-library-id
    ```
    
    **Usage**:
    ```markdown
    * context7: Research AI frameworks, model documentation, best practices
    ```

=== "deepwiki"

    **Purpose**: GitHub repository documentation and analysis
    
    **Tools**:
    ```
    mcp__deepwiki__read-wiki-structure
    mcp__deepwiki__read-wiki-contents
    mcp__deepwiki__ask-question
    ```

### Reasoning & Analysis

=== "sequential-thinking"

    **Purpose**: Complex multi-step reasoning workflows
    
    **Tools**:
    ```
    mcp__sequential-thinking__sequentialthinking
    ```
    
    **Usage**:
    ```markdown
    * sequential-thinking: Complex AI system design, multi-step reasoning workflows
    ```

### Web & Search

=== "brave-search"

    **Purpose**: Web search and content retrieval
    
    **Tools**:
    ```
    mcp__brave-search__web-search
    mcp__brave-search__local-search
    mcp__brave-search__news-search
    ```

---

## <i data-feather="check-square" style="color: var(--md-primary-fg-color);"></i> Integration Examples

### Research Assistant

```yaml
---
name: ai-research-assistant
description: Advanced AI research and analysis agent
tools: read, write, mcp__context7__get-library-docs, mcp__sequential-thinking__analyze
model: claude-3-5-sonnet
---
```

```markdown
### MCP Integration

* context7: Access latest AI research papers and framework documentation
* sequential-thinking: Multi-step analysis for complex research questions
```

### Data Analysis Agent

```yaml
---
name: data-analyst
description: Specialized data analysis and visualization agent
tools: pandas, matplotlib, mcp__context7__resolve-library-id, mcp__brave-search__web-search
model: claude-3-5-sonnet
---
```

```markdown
### MCP Integration

* context7: Python data science library documentation and best practices
* brave-search: Research industry trends and external datasets
```

---

## <i data-feather="alert-triangle" style="color: var(--md-primary-fg-color);"></i> Best Practices

### Tool Naming

!!! tip "Consistent Naming"
    Use clear, descriptive server names in the MCP tool pattern:
    
    ```
    # Good
    mcp__context7__get-library-docs
    mcp__research-db__query-papers
    
    # Avoid
    mcp__ctx__docs
    mcp__db1__query
    ```

### Integration Descriptions

Provide clear descriptions of how each MCP server enhances the agent:

```markdown
# Good - Specific and actionable
* context7: Access comprehensive documentation for Python ML libraries including scikit-learn, TensorFlow, and PyTorch

# Less helpful - Too vague  
* context7: Get documentation
```

### Server Dependencies

Document when MCP servers work together:

```markdown
### MCP Integration

* context7: Primary documentation source for AI frameworks and libraries
* sequential-thinking: Complex reasoning workflows that leverage context7 research findings
* brave-search: External validation and supplementary research for context7 findings
```

---

## <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> Next Steps

<div class="grid cards" markdown>

-   <i data-feather="edit" style="color: var(--md-primary-fg-color);"></i> **[Create Specifications](spec-anatomy.md)**

    ---

    Learn the complete agent specification format with MCP integration

-   <i data-feather="activity" style="color: var(--md-primary-fg-color);"></i> **[View Examples](../examples/)**

    ---

    See real agent specifications with MCP server integrations

-   <i data-feather="code" style="color: var(--md-primary-fg-color);"></i> **[API Reference](../api-reference/)**

    ---

    Technical documentation for MCP validation and models

</div>
