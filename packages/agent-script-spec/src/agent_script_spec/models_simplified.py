import re
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer, field_validator, model_validator
from typing import Annotated, Literal, Self


class Frontmatter(BaseModel):
    """Frontmatter specification for agent scripts.

    MUST conform with Claude Code subagents format."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    name: str = Field(description="The name of the agent script. MUST be unique and non-empty.")
    description: str = Field(description="A short description of the agent script. MUST be non-empty.")
    tools: set[Annotated[str, Field(description="The name of the tool")]] | None = Field(
        None, description="A list of tools that the agent script can use. MAY be empty if no tools are required."
    )
    model: str | None = Field(None, description="The model that the agent script will use. SHOULD be specified for consistency.")

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


class Action(BaseModel):
    """A single action in the interaction workflow.
    
    Actions MUST be executed sequentially and SHOULD be self-contained."""
    
    name: str = Field(description="The name of the action. MUST be descriptive and unique within the workflow.")
    description: str = Field(description="Detailed description of what this action accomplishes. MUST be non-empty.")
    requirement_level: Literal["MUST", "SHOULD", "MAY"] = Field(
        default="MUST", 
        description="RFC 2119 requirement level. MUST indicates critical actions, SHOULD indicates recommended actions, MAY indicates optional actions."
    )


class InteractionWorkflow(BaseModel):
    """Simplified interaction workflow with sequential actions.
    
    This replaces the complex Phase/Step/Sub-step hierarchy with a flat list of actions."""

    description: str = Field(description="High-level description of the interaction approach. MUST be non-empty.")
    actions: list[Action] = Field(description="Sequential list of actions to execute. MUST contain at least one action.")
    
    @field_validator("actions")
    @classmethod
    def validate_actions_not_empty(cls, v: list[Action]) -> list[Action]:
        """Validate that actions list is not empty."""
        if not v:
            raise ValueError("Actions list MUST contain at least one action")
        return v


class AgentScriptSpecification(BaseModel):
    """Simplified agent script specification with RFC 2119 language.

    This specification MUST be used for all agent definitions and SHOULD be validated
    before deployment."""

    model_config = ConfigDict(
        validate_default=True,
        use_attribute_docstrings=True,
        extra="forbid",
        str_to_lower=False,
        str_to_upper=False,
        str_strip_whitespace=True,
    )

    frontmatter: Frontmatter
    """The frontmatter of the agent script. MUST be present and valid."""

    name: str
    """The name of the agent script. MUST be human-readable and descriptive."""

    role: str
    """The role of the agent script. MUST clearly define the agent's primary function."""

    expertise: str
    """The expertise of the agent script. MUST specify domain knowledge and technical skills."""

    mission: str
    """The mission of the agent script. MUST define the agent's primary objective."""

    capabilities: dict[str, str]
    """The capabilities of the agent script. MUST define specific skills and competencies.

    This field consolidates the previous key_capabilities, core_competencies, and tool_usages.
    
    Example:
    ```json
    {
        "capabilities": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
        }
    }
    ```
    """

    mcp_integration: dict[str, str] | None = None
    """The MCP integration of the agent script. SHOULD be present if MCP tools are used.

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

    interaction_workflow: InteractionWorkflow
    """The interaction workflow of the agent script. MUST define the execution sequence."""

    approach: dict[str, str] | None = None
    """The approach of the agent script. MAY define methodological preferences.

    This field consolidates the previous guiding_principles and approach fields.
    
    Example:
    ```json
    {
        "approach": {
            "Statistical Rigor": "Use appropriate statistical tests and confidence intervals",
            "Reproducibility": "Ensure all experiments are documented and reproducible",
            "Ethical Considerations": "Address potential biases and fairness concerns"
        }
    }
    ```
    """

    rules: dict[Literal["DO"] | Literal["DO-NOT"], list[str]] | None = None
    """The rules of the agent script. SHOULD define behavioral constraints.

    Example:
    ```json
    {
        "rules": {
            "DO": [
                "Always use structured data formats like JSON or YAML for configurations",
                "Validate all inputs before processing"
            ],
            "DO-NOT": [
                "Never expose sensitive information",
                "Don't ignore error conditions"
            ]
        }
    }
    ```
    """

    deliverables: dict[str, str] | None = None
    """The deliverables of the agent script. SHOULD specify expected outputs and formats.

    Example:
    ```json
    {
        "deliverables": {
            "Production-Ready Code": "Fully functional code with error handling and logging",
            "Documentation": "Comprehensive user and technical documentation"
        }
    }
    ```
    """

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