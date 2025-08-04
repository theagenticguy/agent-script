import json
import rich_click as click
from .drivers import from_markdown, to_markdown
from agent_script_spec.models import AgentScriptSpecification
from pathlib import Path
from rich.console import Console
from rich.json import JSON


example_agent_script = AgentScriptSpecification.model_validate_json(Path("examples/ai-engineer.json").read_text())

console = Console(width=120)
cli = click.Group()


@cli.command(name="agent-script-json")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
def agent_script_json(output: Path | None):
    """Show the JSON for the example agent script.

    Args:
        output: Optional output file path to save the JSON, can contain a full path and filename
    """
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            f.write(example_agent_script.model_dump_json(indent=2))
    else:
        console.print(JSON(example_agent_script.model_dump_json(indent=2)))


@cli.command(name="agent-script-markdown")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
def agent_script_markdown(output: Path | None):
    """Show the markdown for the example agent script.

    Args:
        output: Optional output file path to save the markdown, can contain a full path and filename
    """
    markdown_output = to_markdown(example_agent_script)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            f.write(markdown_output)
    else:
        console.print(markdown_output)


@cli.command(name="show-spec-json")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
def show_spec_json(output: Path | None):
    """Show the JSON schema for the agent script specification.

    Args:
        output: Optional output file path to save the JSON, can contain a full path and filename
    """
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            # overwrite the whole file
            f.write(json.dumps(AgentScriptSpecification.model_json_schema(), indent=2))
    else:
        console.print(JSON(json.dumps(AgentScriptSpecification.model_json_schema(), indent=2)))


@cli.command(name="convert-to-markdown")
@click.argument("json_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
def convert_to_markdown(json_file: Path, output: Path | None):
    """Convert JSON agent specification to markdown format.

    Args:
        json_file: Path to the JSON specification file
        output: Optional output file path to save the markdown, can contain a full path and filename
    """
    try:
        # Load the JSON file
        with open(json_file) as f:
            data = json.load(f)

        # Create the specification object
        spec = AgentScriptSpecification(**data)

        # Convert to markdown
        markdown_output = to_markdown(spec)

        # Print the result
        console.print(markdown_output)

        # Save to file if output path is provided
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w") as f:
                f.write(markdown_output)
            console.print(f"\n✅ Conversion complete! Output saved to {output}")

    except FileNotFoundError:
        console.print(f"❌ Error: File '{json_file}' not found", style="red")
    except json.JSONDecodeError as e:
        console.print(f"❌ Error: Invalid JSON in '{json_file}': {e}", style="red")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")


@cli.command(name="convert-to-json")
@click.argument("markdown_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
def convert_to_json(markdown_file: Path, output: Path | None):
    """Convert markdown agent specification to JSON format.

    Args:
        markdown_file: Path to the markdown specification file
        output: Optional output file path to save the JSON
    """
    try:
        # Load the markdown file
        with open(markdown_file) as f:
            markdown = f.read()

        # Convert to JSON
        spec = from_markdown(markdown)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            with open(output, "w") as f:
                f.write(spec.model_dump_json(indent=2))
        else:
            console.print(JSON(spec.model_dump_json(indent=2)))

    except FileNotFoundError:
        console.print(f"❌ Error: File '{markdown_file}' not found", style="red")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")


if __name__ == "__main__":
    cli()
