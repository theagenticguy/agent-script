import json
import rich_click as click
from agent_script_spec.models import AgentScriptSpecification, ComplexStep, Frontmatter, InteractionModel, Phase
from agent_script_tools.drivers import from_markdown, to_markdown
from pathlib import Path
from rich.console import Console
from rich.json import JSON


tools_list = [
    "Read",
    "Write",
    "Edit",
    "MultiEdit",
    "Grep",
    "Glob",
    "Bash",
    "LS",
    "WebSearch",
    "WebFetch",
    "Task",
    "mcp__context7__resolve-library-id",
    "mcp__context7__get-library-docs",
    "mcp__sequential-thinking__sequentialthinking",
]

spec = AgentScriptSpecification(
    frontmatter=Frontmatter(
        name="ai-engineer",
        description="A highly specialized AI agent for designing, building, and optimizing LLM-powered applications, RAG systems, and complex prompt pipelines.",
        tools=set(tools_list),
        model="sonnet",
    ),
    name="AI Engineer",
    role="Senior AI Engineer specializing in LLM-powered applications, RAG systems, and complex prompt pipelines. Focuses on production-ready AI solutions with vector search, agentic workflows, and multi-modal AI integrations.",
    expertise="LLM integration (OpenAI, Anthropic, open-source models), RAG architecture, vector databases (Pinecone, Weaviate, Chroma), prompt engineering, agentic workflows, LangChain/LlamaIndex, embedding models, fine-tuning, AI safety.",
    mission="To build the most advanced AI application, RAG system, and prompt pipeline for the user's needs.",
    key_capabilities={
        "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
        "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
    },
    rules={
        "DO": [
            "Always use structured data formats like JSON or YAML for configurations and function calling, ensuring predictability and ease of integration.",
        ],
        "DO-NOT": [
            "Never expose sensitive information. Sanitize inputs and outputs to prevent security vulnerabilities.",
        ],
    },
    mcp_integration={
        "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
        "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
    },
    interaction_model=InteractionModel(
        description="The interaction model of the agent script",
        phases={
            "Phase 1": Phase(
                description="The description of the phase",
                steps={
                    "Step 1": "The description of the step",
                    "Step 2": ComplexStep(
                        description="The description of the step",
                        steps={
                            "Important Step": "The description of the step",
                        },
                    ),
                },
            ),
            "Phase 2": Phase(
                description="The description of the phase",
                steps={
                    "Step 1": "The description of the step",
                },
            ),
            "Phase 3": Phase(
                description="The description of the phase",
                steps={
                    "Step 1": "The description of the step",
                },
                end_of_phase_instructions="The end of the phase instructions",
            ),
        },
    ),
    deliverables={
        "Production-Ready Code": "Fully functional code for LLM integration, RAG pipelines, or agent orchestration, complete with error handling and logging.",
    },
    core_competencies={
        "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
        "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
    },
    guiding_principles={
        "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
        "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
    },
    tool_usages={
        "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
        "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
    },
    approach={
        "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
        "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
    },
    communication_protocols="The communication protocols of the agent script",
)

console = Console()
cli = click.Group()


@cli.command(name="pretty-print-spec")
@click.option("--output", is_flag=True, help="Print the spec to a file")
def pretty_print_spec(output: bool):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    if output:
        with open(output_dir / "example.json", "w") as f:
            f.write(spec.model_dump_json(indent=2))
    else:
        console.print(JSON(spec.model_dump_json(indent=2)))


@cli.command(name="dump-markdown-schema")
def dump_markdown_schema():
    console.print(to_markdown(spec))


@cli.command(name="dump-json-schema")
def dump_json_schema():
    # make output dir if not exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "schema.json", "w") as f:
        # overwrite the whole file
        f.write(json.dumps(AgentScriptSpecification.model_json_schema(), indent=2))


@cli.command(name="convert-to-markdown")
@click.argument("json_file", type=click.Path(exists=True, path_type=Path))
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path (optional)")
@click.option("--print-raw", is_flag=True, help="Print raw markdown instead of rendered")
def convert_to_markdown(json_file: Path, output: Path | None, print_raw: bool):
    """Convert JSON agent specification to markdown format.

    Args:
        json_file: Path to the JSON specification file
        output: Optional output file path to save the markdown
        print_raw: If set, prints raw markdown instead of rendered
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
        if print_raw:
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
            console.print(spec.model_dump_json(indent=2))

    except FileNotFoundError:
        console.print(f"❌ Error: File '{markdown_file}' not found", style="red")
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")


if __name__ == "__main__":
    cli()
