import re
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer, field_validator, model_validator
from typing import Annotated, Literal, Self


class Frontmatter(BaseModel):
    """Frontmatter specification for agent scripts.

    Mostly conforms with Claude Code subagents."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    name: str = Field(description="The name of the agent script")
    description: str = Field(description="A short description of the agent script")
    tools: set[Annotated[str, Field(description="The name of the tool")]] | None = Field(
        None, description="A list of tools that the agent script can use"
    )
    model: str | None = Field(None, description="The model that the agent script will use")

    @field_serializer("tools")
    def serialize_tools(self, v: set[Annotated[str, Field(description="The name of the tool")]]) -> list[str]:
        """Serialize the tools to a list of strings."""
        return sorted(v)

    @computed_field
    @property
    def mcp_server_names(self) -> list[str] | None:
        """The set of MCP server names from tools."""
        if not self.tools:
            return None

        server_names: set[str] = set()
        mcp_pattern = re.compile(r"^mcp__([^_]+(?:-[^_]+)*)__")

        for tool in self.tools:
            match = mcp_pattern.match(tool)
            if match:
                server_names.add(match.group(1))

        return None if not server_names else sorted(server_names)


class ComplexStep(BaseModel):
    """Step in the interaction model with optional nested sub-steps."""

    description: str
    steps: dict[str, str] | None = None  # For nested sub-steps (unconstrained keys)


class Phase(BaseModel):
    """Phase in the interaction model containing ordered steps."""

    description: str
    steps: dict[str, str | ComplexStep]
    end_of_phase_instructions: str | None = None

    @field_validator("steps")
    @classmethod
    def validate_step_keys(cls, v: dict[str, str | ComplexStep]) -> dict[str, str | ComplexStep]:
        """Validate that step keys follow the pattern 'Step N' where N is monotonically increasing."""
        step_numbers = []

        for key in v.keys():
            match = re.match(r"^Step (\d+)$", key)
            if not match:
                raise ValueError(f"Step key '{key}' must match pattern 'Step N' where N is a number")
            step_numbers.append(int(match.group(1)))

        # Check monotonically increasing starting from 1
        step_numbers.sort()
        expected = list(range(1, len(step_numbers) + 1))
        if step_numbers != expected:
            raise ValueError(
                f"Step numbers must be monotonically increasing starting from 1. "
                f"Got {step_numbers}, expected {expected}"
            )

        return v


class InteractionModel(BaseModel):
    """Defines the interaction model with phases and steps."""

    description: str
    phases: dict[str, Phase]

    @field_validator("phases")
    @classmethod
    def validate_phase_keys(cls, v: dict[str, Phase]) -> dict[str, Phase]:
        """Validate that phase keys follow the pattern 'Phase N' where N is monotonically increasing."""
        phase_numbers = []

        for key in v.keys():
            match = re.match(r"^Phase (\d+)$", key)
            if not match:
                raise ValueError(f"Phase key '{key}' must match pattern 'Phase N' where N is a number")
            phase_numbers.append(int(match.group(1)))

        # Check monotonically increasing starting from 1
        phase_numbers.sort()
        expected = list(range(1, len(phase_numbers) + 1))
        if phase_numbers != expected:
            raise ValueError(
                f"Phase numbers must be monotonically increasing starting from 1. "
                f"Got {phase_numbers}, expected {expected}"
            )

        return v


class AgentScriptSpecification(BaseModel):
    """Agent script specification."""

    model_config = ConfigDict(
        validate_default=True,
        use_attribute_docstrings=True,
        extra="forbid",
        str_to_lower=False,
        str_to_upper=False,
        str_strip_whitespace=True,
    )

    frontmatter: Frontmatter
    """The frontmatter of the agent script."""

    name: str
    """The name of the agent script."""

    role: str
    """The role of the agent script."""

    expertise: str
    """The expertise of the agent script."""

    mission: str
    """The mission of the agent script."""

    key_capabilities: dict[str, str]
    """The key capabilities of the agent script.

    Example:
    ```json
    {
        "key_capabilities": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
        }
    }
    ```
    """

    mcp_integration: dict[str, str] | None = None
    """The MCP integration of the agent script.

    Example:
    ```json
    {
        "mcp_integration": {
            "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
            "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
        }
    }
    ```
    """

    interaction_model: InteractionModel
    """The interaction model of the agent script."""

    core_competencies: dict[str, str] | None = None
    """The core competencies of the agent script.

    Example:
    ```json
    {
        "core_competencies": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
        }
    }
    ```
    """

    guiding_principles: dict[str, str] | None = None
    """The guiding principles of the agent script."""

    tool_usages: dict[str, str] | None = None
    """The tool usages of the agent script."""

    rules: dict[Literal["DO"] | Literal["DO-NOT"], list[str]] | None = None
    """The rules of the agent script."""

    communication_protocols: str | None = None
    """The communication protocols of the agent script."""

    approach: dict[str, str] | None = None
    """The approach of the agent script."""

    deliverables: dict[str, str] | None = None
    """The deliverables of the agent script."""

    @model_validator(mode="after")
    def validate_mcp_integration_keys(self) -> Self:
        """Validate that mcp_integration keys match mcp_server_names from frontmatter."""
        frontmatter_mcp_server_names = self.frontmatter.mcp_server_names
        spec_mcp_integration_keys = set(self.mcp_integration.keys()) if self.mcp_integration else None

        match frontmatter_mcp_server_names, spec_mcp_integration_keys:
            case None, None:
                return self
            case None, _:
                raise ValueError(
                    f"No MCP servers found in tools, but mcp_integration contains: {spec_mcp_integration_keys}"
                )
            case _, None:
                logger.warning(f"Missing MCP servers in mcp_integration: {frontmatter_mcp_server_names}")
                return self
            case _, _:
                if spec_mcp_integration_keys != frontmatter_mcp_server_names:
                    # this is an error state, the agent can't do anything with mcp servers not in the frontmatter
                    extra_in_spec = spec_mcp_integration_keys - set(frontmatter_mcp_server_names)

                    # this is a warning state, the agent can do something with mcp servers
                    # not in the spec but it's better to be explicit
                    missing_in_spec = set(frontmatter_mcp_server_names) - spec_mcp_integration_keys
                    if extra_in_spec:
                        raise ValueError(
                            f"Extra MCP servers in mcp_integration: {extra_in_spec}. "
                            "These MCP servers are not in the tools list in the frontmatter."
                        )
                    if missing_in_spec:
                        logger.warning(
                            f"Missing MCP servers in mcp_integration: {missing_in_spec}. "
                            "These MCP servers are in the tools list in the frontmatter. "
                            "This is just a warning, but it's better to be explicit."
                        )

        return self
