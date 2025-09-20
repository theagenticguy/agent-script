"""Simplified Agent Script Specification Models

This module provides a simplified version of the agent script specification
that reduces hierarchical complexity and enforces RFC 2119 language for
requirements clarity.

Key improvements:
1. Flattened interaction model (removed phases/steps hierarchy)
2. Eliminated redundant fields
3. Enforced RFC 2119 terminology (MUST, SHOULD, MAY)
4. Streamlined structure for better usability
"""

import re
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer, field_validator, model_validator
from typing import Annotated, Literal, Self


class Frontmatter(BaseModel):
    """Frontmatter specification for agent scripts.
    
    This section MUST contain the essential metadata for the agent.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    name: str = Field(description="The name of the agent script. This MUST be unique and descriptive.")
    description: str = Field(description="A concise description of the agent script. This SHOULD be 1-2 sentences.")
    tools: set[Annotated[str, Field(description="The name of the tool")]] | None = Field(
        None, description="A list of tools that the agent script MAY use. MCP tools MUST follow the pattern 'mcp__server-name__tool-name'."
    )
    model: str | None = Field(None, description="The model that the agent script SHOULD use. MAY be omitted for model-agnostic agents.")

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


class WorkflowStep(BaseModel):
    """A single workflow step with clear requirements.
    
    Each step MUST have a clear description and MAY include specific requirements.
    """
    
    description: str = Field(description="Description of what this step accomplishes. This MUST be action-oriented.")
    requirements: list[str] | None = Field(
        None, 
        description="Specific requirements for this step using RFC 2119 language. Each requirement SHOULD start with MUST, SHOULD, or MAY."
    )


class InteractionWorkflow(BaseModel):
    """Simplified interaction workflow without hierarchical phases.
    
    This replaces the complex phase/step/sub-step hierarchy with a flat list of workflow steps.
    """

    description: str = Field(description="Overview of the interaction workflow. This SHOULD describe the overall approach.")
    steps: list[WorkflowStep] = Field(description="Sequential list of workflow steps. Each step MUST be clearly defined.")
    completion_criteria: str | None = Field(
        None, 
        description="Criteria that MUST be met for the workflow to be considered complete."
    )


class RequirementRule(BaseModel):
    """A single requirement rule using RFC 2119 language.
    
    Requirements MUST use RFC 2119 keywords to specify obligation levels:
    - MUST: Absolute requirement (mandatory)
    - MUST NOT: Absolute prohibition (forbidden)  
    - SHOULD: Strong recommendation (preferred)
    - SHOULD NOT: Strong recommendation against (discouraged)
    - MAY: Optional or permissible (allowed)
    - MAY NOT: Optional prohibition (not required to avoid)
    """
    
    requirement: str = Field(description="The requirement statement. This MUST start with MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, or MAY NOT.")
    rationale: str | None = Field(None, description="Optional explanation of why this requirement exists.")


class SimplifiedAgentScriptSpecification(BaseModel):
    """Simplified Agent Script Specification.
    
    This model reduces complexity by:
    1. Flattening the interaction model
    2. Consolidating redundant fields
    3. Enforcing RFC 2119 language
    4. Streamlining the overall structure
    """

    model_config = ConfigDict(
        validate_default=True,
        use_attribute_docstrings=True,
        extra="forbid",
        str_to_lower=False,
        str_to_upper=False,
        str_strip_whitespace=True,
    )

    frontmatter: Frontmatter
    """The frontmatter metadata. This MUST be provided."""

    name: str
    """The display name of the agent. This MUST match the frontmatter name."""

    role: str
    """The primary role of the agent. This MUST clearly define the agent's function."""

    expertise: str
    """Domain expertise and knowledge areas. This SHOULD be comprehensive but concise."""

    mission: str
    """The agent's mission statement. This MUST clearly state the agent's purpose."""

    capabilities: dict[str, str]
    """Core capabilities of the agent. Keys MUST be capability names, values MUST describe the specific skills.
    
    This consolidates the previous key_capabilities and core_competencies fields.
    """

    mcp_integration: dict[str, str] | None = None
    """MCP server integration descriptions. Keys MUST match mcp_server_names from frontmatter."""

    workflow: InteractionWorkflow
    """The simplified interaction workflow. This MUST define how the agent operates."""

    requirements: list[RequirementRule] | None = None
    """Behavioral requirements using RFC 2119 language. Each rule MUST use RFC 2119 keywords.
    
    Supported keywords: MUST, MUST NOT, SHOULD, SHOULD NOT, MAY, MAY NOT.
    Use negative forms (MUST NOT, SHOULD NOT) to specify prohibited behaviors and constraints.
    
    This consolidates the previous rules, guiding_principles, and approach fields.
    """

    communication_style: str | None = None
    """How the agent SHOULD communicate with users. MAY include tone, format, and interaction preferences."""

    deliverables: dict[str, str] | None = None
    """Expected outputs and their specifications. Keys MUST be deliverable names, values MUST describe requirements."""

    @field_validator("name")
    @classmethod
    def validate_name_matches_frontmatter(cls, v: str, info) -> str:
        """Validate that name matches frontmatter name."""
        if hasattr(info.data, 'frontmatter') and info.data['frontmatter'].name != v:
            raise ValueError(f"Name '{v}' must match frontmatter name '{info.data['frontmatter'].name}'")
        return v

    @field_validator("requirements")
    @classmethod
    def validate_rfc2119_requirements(cls, v: list[RequirementRule] | None) -> list[RequirementRule] | None:
        """Validate that requirements use RFC 2119 language."""
        if not v:
            return v
            
        rfc2119_keywords = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY", "MAY NOT"]
        
        for rule in v:
            requirement_upper = rule.requirement.upper()
            if not any(keyword in requirement_upper for keyword in rfc2119_keywords):
                logger.warning(f"Requirement does not use RFC 2119 language: {rule.requirement}")
        
        return v

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
                if spec_mcp_integration_keys != set(frontmatter_mcp_server_names):
                    extra_in_spec = spec_mcp_integration_keys - set(frontmatter_mcp_server_names)
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