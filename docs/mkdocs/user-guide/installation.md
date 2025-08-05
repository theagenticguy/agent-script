# Installation Guide

<i data-feather="download" style="color: var(--md-primary-fg-color);"></i> Get started with Agent Script Tools in your development environment.

---

## <i data-feather="settings" style="color: var(--md-primary-fg-color);"></i> Prerequisites

Before installing Agent Script Tools, ensure you have the following requirements:

!!! info "System Requirements"
    - **Python 3.13+** - Leveraging modern Python features
    - **[uv](https://docs.astral.sh/uv/)** - Fast, reliable package manager
    - **Git** - For cloning the repository

### Installing uv

If you don't have `uv` installed, get it with:

=== "Linux/macOS"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```bash
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "Alternative Methods"

    ```bash
    # Via pip
    pip install uv
    
    # Via conda
    conda install -c conda-forge uv
    
    # Via homebrew (macOS)
    brew install uv
    ```

---

## <i data-feather="git-branch" style="color: var(--md-primary-fg-color);"></i> Installation Methods

### From Source (Recommended)

Clone the repository and install in development mode:

```bash
# Clone the repository
git clone https://github.com/theagenticguy/agent-script.git
cd agent-script

# Install all dependencies including development tools
uv sync --all-groups

# Activate virtual environment (optional with uv)
source .venv/bin/activate
```

### Production Installation

For production use, install without development dependencies:

```bash
# Clone and install production dependencies only
git clone https://github.com/theagenticguy/agent-script.git
cd agent-script
uv sync
```

### Package Installation

Install individual packages:

=== "agent-script-tools"

    ```bash
    # Install from workspace root
    uv add agent-script-tools
    ```

=== "agent-script-spec"

    ```bash
    # Install specification models only
    uv add agent-script-spec
    ```

---

## <i data-feather="check-circle" style="color: var(--md-primary-fg-color);"></i> Verification

Verify your installation works correctly:

```bash
# Test CLI commands
uv run agent-script-json
uv run agent-script-markdown

# Run the test suite
uv run poe test

# Check code quality
uv run poe code-quality
```

!!! success "Expected Output"
    If installation is successful, you should see:
    
    - JSON and Markdown output from the CLI commands
    - All tests passing
    - No linting or type errors

---

## <i data-feather="tool" style="color: var(--md-primary-fg-color);"></i> Development Setup

For contributing to Agent Script Tools:

### 1. Clone and Install

```bash
git clone https://github.com/theagenticguy/agent-script.git
cd agent-script
uv sync --all-groups
```

### 2. Install Pre-commit Hooks

```bash
# Install git hooks for code quality
pre-commit install
```

### 3. Configure Your Editor

=== "VS Code"

    Install recommended extensions:
    
    ```json
    {
      "recommendations": [
        "ms-python.python",
        "ms-python.mypy-type-checker",
        "charliermarsh.ruff",
        "ms-python.black-formatter"
      ]
    }
    ```

=== "PyCharm"

    Configure the Python interpreter:
    
    1. **File → Settings → Project → Python Interpreter**
    2. **Add → Existing Environment**
    3. **Point to `.venv/bin/python`**

---

## <i data-feather="package" style="color: var(--md-primary-fg-color);"></i> Project Structure

After installation, your project structure will look like:

```
agent-script/
├── pyproject.toml                    # Main project configuration
├── uv.lock                          # Dependency lock file
├── src/
│   └── agent_script_tools/          # CLI tools package
│       ├── __init__.py
│       ├── scripts.py               # Command implementations
│       └── drivers.py               # Conversion logic
├── packages/
│   └── agent-script-spec/           # Specification models
│       ├── pyproject.toml
│       └── src/
│           └── agent_script_spec/
│               ├── models.py        # Pydantic models
│               └── generate.py      # Schema generation
├── examples/                        # Example specifications
├── tests/                          # Test suite
├── docs/                           # Documentation
└── .venv/                          # Virtual environment
```

---

## <i data-feather="zap" style="color: var(--md-primary-fg-color);"></i> Quick Commands Reference

Common commands for daily development:

| Command | Description |
|---------|-------------|
| `uv sync --all-groups` | Install/update all dependencies |
| `uv run poe format` | Format code with Ruff |
| `uv run poe lint` | Lint code |
| `uv run poe typecheck` | Type check with MyPy |
| `uv run poe code-quality` | Run all quality checks |
| `uv run poe test` | Run tests |
| `uv run poe cov` | Run tests with coverage |
| `uv run poe docs` | Serve documentation locally |

---

## <i data-feather="alert-triangle" style="color: #ff9800;"></i> Troubleshooting

### Common Issues

!!! warning "Python Version"
    **Issue**: `python: command not found` or wrong Python version
    
    **Solution**: 
    ```bash
    # Check Python version
    python --version  # Should be 3.13+
    
    # Install Python 3.13 if needed
    # On macOS with homebrew:
    brew install python@3.13
    
    # On Ubuntu/Debian:
    sudo apt install python3.13 python3.13-venv
    ```

!!! warning "uv Installation"
    **Issue**: `uv: command not found`
    
    **Solution**: 
    ```bash
    # Reinstall uv
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Restart your shell or source profile
    source ~/.bashrc  # or ~/.zshrc
    ```

!!! warning "Permission Errors"
    **Issue**: Permission denied when installing
    
    **Solution**: 
    ```bash
    # Don't use sudo with uv
    # Create virtual environment explicitly
    uv venv
    source .venv/bin/activate
    uv sync --all-groups
    ```

### Getting Help

If you encounter issues:

1. **Check the logs**: Most uv commands provide verbose output with `-v`
2. **Search GitHub Issues**: [github.com/theagenticguy/agent-script/issues](https://github.com/theagenticguy/agent-script/issues)
3. **Create an Issue**: Include your OS, Python version, and error messages

---

## <i data-feather="arrow-right" style="color: var(--md-primary-fg-color);"></i> Next Steps

Now that you have Agent Script Tools installed:

<div class="grid cards" markdown>

-   <i data-feather="file-text" style="color: var(--md-primary-fg-color);"></i> **[Learn the Specification Format](specifications.md)**

    ---

    Understand how to define agent capabilities, tools, and interaction models

-   <i data-feather="refresh-cw" style="color: var(--md-primary-fg-color);"></i> **[Try Format Conversion](conversion.md)**

    ---

    Convert between JSON and Markdown formats with practical examples

</div>
