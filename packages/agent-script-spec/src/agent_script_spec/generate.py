import json
import os
from agent_script_spec.models import AgentScriptSpecification
from pathlib import Path


def generate_schemas():
    """Generate JSON schemas from Pydantic models."""
    package_dir = Path(__file__).parent.parent.parent
    output_dir = package_dir / "dist"
    output_dir.mkdir(exist_ok=True)

    # Get version from environment or default
    version = os.environ.get("SCHEMA_VERSION", "0.1.0")

    # Generate schema for main model
    schema = AgentScriptSpecification.model_json_schema()

    # Add metadata with version
    schema["$id"] = (
        f"https://github.com/theagenticguy/agent-script-spec/releases/download/schema-v{version}/agent_script_spec.json"
    )
    schema["title"] = "Agent Script Specification Schema"
    schema["version"] = version

    output_file = output_dir / "agent_script_spec.json"
    with open(output_file, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Generated schema: {output_file} (version: {version})")
    return
