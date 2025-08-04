# Agent Script Tools

A comprehensive toolkit for defining, validating, and converting AI agent specifications between JSON and Markdown formats. This project provides structured specifications for AI agents, including their capabilities, interaction models, MCP integrations, and behavioral rules.

## Features

### Core Functionality

- **Agent Specification Format**: Structured Pydantic models for defining AI agent capabilities and behavior
- **Bi-directional Conversion**: Convert between JSON and Markdown formats seamlessly
- **JSON Schema Generation**: Automatic generation of JSON schemas from Pydantic models
- **MCP Integration Support**: Built-in support for Model Context Protocol (MCP) server integration
- **Interaction Model Framework**: Define multi-phase interaction workflows with validation
- **CLI Tools**: Rich command-line interface for working with agent specifications

### Development Stack

- **Python 3.13+**: Leveraging modern Python features
- **[uv](https://docs.astral.sh/uv/)**: Fast, reliable package management
- **Pydantic**: Data validation and settings management using Python type annotations
- **Rich Click**: Beautiful command-line interfaces with rich formatting
- **Mistune**: Fast, flexible Markdown parser for conversion operations
- **Ruff**: All-in-one Python linter and formatter
- **MyPy**: Static type checking with strict mode enabled
- **Pytest**: Testing framework with coverage reporting
- **Task Automation**: Using poethepoet (poe) for common development tasks
- **Conventional Commits**: Enforced via commitizen
- **Coverage Requirements**: 85% code coverage minimum

## Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager

## Getting Started

### Setup

```bash
# Navigate to your project directory
cd agent-script

# start git
git init

# Install dependencies
uv sync --all-groups

# Activate virtual environment (optional with uv)
source .venv/bin/activate

# Install pre-commit hooks
pre-commit install
```

### CLI Commands

The project provides several CLI commands for working with agent specifications:

```bash
# Show example agent script in JSON format
uv run agent-script-json

# Show example agent script in Markdown format
uv run agent-script-markdown

# Show the JSON schema for agent specifications
uv run show-spec-json

# Convert JSON specification to Markdown
uv run convert-to-markdown path/to/spec.json

# Convert Markdown specification to JSON
uv run convert-to-json path/to/spec.md

# Generate JSON schemas from Pydantic models
uv run generate-schema
```

### Development Commands

The project uses [poethepoet](https://github.com/nat-n/poethepoet) to manage common tasks:

```bash
# Format code
uv run poe format

# Lint code
uv run poe lint

# Type check
uv run poe typecheck

# Run all quality checks
uv run poe code-quality

# Run tests
uv run poe test

# Run tests with coverage reporting
uv run poe cov

# Security scanning
uv run poe scan

# Generate documentation locally
uv run poe docs

# Generate JSON schemas
uv run poe generate-schema
```

### Commiting

```bash
# Commit changes
git commit -m "(feat|fix|chore|ci|docs|refactor|test): imperitive present tense message, consise, all lower case, no period at the end"
```

## Project Structure

This is a workspace project with two main packages:

```bash
.
├── pyproject.toml                    # Main project configuration
├── uv.lock                          # Lock file for dependencies
├── src/
│   └── agent_script_tools/          # Main CLI tools package
│       ├── __init__.py
│       ├── scripts.py               # CLI command implementations
│       └── drivers.py               # Conversion logic (JSON ↔ Markdown)
├── packages/
│   └── agent-script-spec/           # Agent specification models package
│       ├── pyproject.toml           # Spec package configuration
│       ├── README.md                # Spec package documentation
│       └── src/
│           └── agent_script_spec/
│               ├── __init__.py
│               ├── models.py        # Pydantic models for agent specs
│               └── generate.py      # JSON schema generation
├── examples/
│   ├── ai-engineer.json             # Example agent specification (JSON)
│   └── ai-engineer.md               # Example agent specification (Markdown)
├── tests/                           # Test files
├── docs/                            # Documentation
└── .venv/                           # Virtual environment (created by uv)
```

## Next Steps

After creating your project from this template:

1. Initialize git repository: `git init`
2. Make your first commit: `git add . && git commit -m "feat: initial project setup"`
3. Create a remote repository and push your code
4. Start building your amazing Python project!

## Agent Specification Format

The project defines a comprehensive specification for AI agents with the following components:

### Core Elements

- **Frontmatter**: Metadata including name, description, tools, and model
- **Role & Expertise**: Agent's primary function and domain knowledge
- **Key Capabilities**: Specific skills and competencies
- **MCP Integration**: Model Context Protocol server configurations
- **Interaction Model**: Multi-phase workflows with structured steps
- **Rules**: DO and DO-NOT behavioral guidelines
- **Deliverables**: Expected outputs and formats

### Example Usage

```python
from agent_script_spec.models import AgentScriptSpecification
from agent_script_tools.drivers import to_markdown, from_markdown

# Load from JSON
with open("examples/ai-engineer.json") as f:
    spec = AgentScriptSpecification.model_validate_json(f.read())

# Convert to Markdown
markdown = to_markdown(spec)

# Convert back to spec
spec_from_md = from_markdown(markdown)
```

## Dependencies

### Core Libraries

- **loguru**: Modern logging with rich formatting
- **pydantic**: Data validation and settings management
- **mistune**: Fast, flexible Markdown parser
- **python-frontmatter**: YAML frontmatter parsing
- **rich-click**: Beautiful command-line interfaces

### Development Tools

- **commitizen**: Conventional commit enforcement
- **mypy**: Static type checking
- **poethepoet**: Task runner and command automation
- **pre-commit**: Git hooks for code quality
- **pytest**: Testing framework with asyncio and coverage support
- **ruff**: Fast Python linter and formatter

### Security & Quality

- **bandit**: Security vulnerability scanner
- **pip-audit**: Package vulnerability auditing

## Building and Publishing

```bash
# Build both packages
uv build

# Build specific package
cd packages/agent-script-spec && uv build

# Install locally for development
uv sync --all-groups
```

## Documentation

```bash
# Start documentation server
uv run poe docs

# Build documentation
uv run poe docs-build

# Deploy to GitHub Pages
uv run poe docs-deploy
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
