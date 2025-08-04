import pytest
from pydantic import ValidationError
from src.agent_script_spec.models import AgentScriptSpecification, Frontmatter, InteractionModel, Phase
from typing import Any
from unittest.mock import patch


@pytest.fixture
def tools_list() -> list[str]:
    return [
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


@pytest.fixture
def frontmatter(tools_list: list[str]) -> Frontmatter:
    return Frontmatter(
        name="ai-engineer",
        description="A highly specialized AI agent for designing, building, and optimizing LLM-powered applications, RAG systems, and complex prompt pipelines.",
        tools=set(tools_list),
        model="sonnet",
    )


@pytest.fixture
def frontmatter_no_mcp_server_names() -> Frontmatter:
    return Frontmatter(
        name="test-agent",
        description="Test agent",
        tools={"Read", "Write"},
        model="sonnet",
    )


@pytest.fixture
def partial_valid_spec() -> dict[str, Any]:
    return {
        "name": "AI Engineer",
        "role": "Senior AI Engineer specializing in LLM-powered applications, RAG systems, and complex prompt pipelines. Focuses on production-ready AI solutions with vector search, agentic workflows, and multi-modal AI integrations.",
        "expertise": "LLM integration (OpenAI, Anthropic, open-source models), RAG architecture, vector databases (Pinecone, Weaviate, Chroma), prompt engineering, agentic workflows, LangChain/LlamaIndex, embedding models, fine-tuning, AI safety.",
        "mission": "To build the most advanced AI application, RAG system, and prompt pipeline for the user's needs.",
        "rules": {
            "DO": [
                "Always use structured data formats like JSON or YAML for configurations and function calling, ensuring predictability and ease of integration.",
            ],
            "DO-NOT": [
                "Never expose sensitive information. Sanitize inputs and outputs to prevent security vulnerabilities.",
            ],
        },
        "deliverables": {
            "Production-Ready Code": "Fully functional code for LLM integration, RAG pipelines, or agent orchestration, complete with error handling and logging.",
        },
        "mcp_integration": {
            "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
            "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
        },
        "key_capabilities": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
            "AI Workflow Orchestration": "Agentic systems, multi-step reasoning, tool integration",
            "Production Deployment": "Scalable AI systems, cost optimization, monitoring, safety measures",
        },
        "core_competencies": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
        },
        "guiding_principles": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
        },
        "approach": {
            "LLM Application Development": "Production-ready AI applications, API integrations, error handling",
            "RAG System Architecture": "Vector search, knowledge retrieval, context optimization, multi-modal RAG",
            "Prompt Engineering": "Advanced prompting techniques, chain-of-thought, few-shot learning",
        },
        "tool_usages": {
            "Bash": "Use Bash to execute shell commands",
            "Read/Grep": "Use Read/Grep to read and grep files",
        },
        "communication_protocols": "The communication protocols of the agent script",
        "interaction_model": {
            "description": "The interaction model of the agent script",
            "phases": {
                "Phase 1": {
                    "description": "The description of the phase",
                    "steps": {
                        "Step 1": "The description of the step",
                        "Step 2": {
                            "description": "The description of the step",
                            "steps": {
                                "Learning": "The description of the learning step",
                                "Reasoning": "The description of the reasoning step",
                                "Planning": "The description of the planning step",
                                "Execution": "The description of the execution step",
                            },
                        },
                    },
                },
                "Phase 2": {
                    "description": "Another phase description",
                    "steps": {
                        "Step 1": "The description of the step",
                    },
                },
                "Phase 3": {
                    "description": "The description of the phase",
                    "steps": {
                        "Step 1": "The description of the step",
                    },
                    "end_of_phase_instructions": "The end of the phase instructions",
                },
            },
        },
    }


def test_agent_script_spec(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test creating a valid AgentScriptSpecification matching the structure in scripts.py"""

    spec = AgentScriptSpecification(
        frontmatter=frontmatter,
        **partial_valid_spec,
    )

    assert spec
    assert spec.frontmatter.name == "ai-engineer"
    assert spec.name == "AI Engineer"
    assert len(spec.interaction_model.phases) == 3


def test_phase_validation_error_non_sequential(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for non-sequential phase numbers."""

    partial_valid_spec["interaction_model"]["phases"] = {
        "Phase 1": Phase(
            description="First phase",
            steps={"Step 1": "First step"},
        ),
        "Phase 3": Phase(
            description="Third phase",
            steps={"Step 1": "First step"},
        ),
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

    # Check that the error message mentions the phase validation issue
    assert "Phase numbers must be monotonically increasing starting from 1" in str(exc_info.value)


def test_step_validation_error_non_sequential(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for non-sequential step numbers."""

    partial_valid_spec["interaction_model"]["phases"]["Phase 1"]["steps"] = {
        "Step 1": "First step",
        "Step 3": "Third step",  # Skipping Step 2 - should cause validation error
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

    # Check that the error message mentions the step validation issue
    assert "Step numbers must be monotonically increasing starting from 1" in str(exc_info.value)


def test_invalid_phase_naming_pattern(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for invalid phase naming patterns."""

    partial_valid_spec["interaction_model"]["phases"] = {
        "Phase One": Phase(
            description="First phase",
            steps={"Step 1": "First step"},
        ),
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

    # Check that the error message mentions the phase key pattern issue
    assert "must match pattern 'Phase N' where N is a number" in str(exc_info.value)


def test_invalid_step_naming_pattern(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for invalid step naming patterns."""

    partial_valid_spec["interaction_model"]["phases"]["Phase 1"]["steps"] = {
        "Step One": "First step",
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

    # Check that the error message mentions the step key pattern issue
    assert "must match pattern 'Step N' where N is a number" in str(exc_info.value)


def test_no_mcp_server_names(frontmatter_no_mcp_server_names: Frontmatter, partial_valid_spec: dict):
    partial_valid_spec["mcp_integration"] = {
        "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
        "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
    }
    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter_no_mcp_server_names,
            **partial_valid_spec,
        )
        assert (
            "No MCP servers found in tools, but mcp_integration contains: {'context7', 'sequential-thinking'}"
            in str(exc_info.value)
        )


def test_invalid_mcp_integration_keys(frontmatter_no_mcp_server_names: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for invalid MCP integration keys."""

    partial_valid_spec["mcp_integration"] = {
        "invalid-mcp": "Test MCP integration",
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter_no_mcp_server_names,
            **partial_valid_spec,
        )

        assert "Extra MCP servers in mcp_integration: {'invalid-mcp'}" in str(exc_info.value)


def test_valid_mcp_integration_keys(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for invalid MCP integration keys."""

    partial_valid_spec["mcp_integration"] = None

    # capture STDIO for logger.warning
    with patch("src.agent_script_spec.models.logger.warning") as mock_warning:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

        assert mock_warning.call_count == 1
        assert "Missing MCP servers in mcp_integration:" in str(mock_warning.call_args[0][0])


def test_no_tools_in_frontmatter(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test that the BaseModel raises a validation error for no tools in the frontmatter."""

    frontmatter.tools = None
    partial_valid_spec["mcp_integration"] = None

    spec = AgentScriptSpecification(
        frontmatter=frontmatter,
        **partial_valid_spec,
    )

    assert spec
    assert spec.frontmatter.tools is None
    assert spec.mcp_integration is None


def test_mcp_integration_perfect_match(frontmatter: Frontmatter):
    """Test successful validation when mcp_integration keys exactly match frontmatter MCP servers."""

    # Create minimal spec that will hit the perfect match path
    spec = AgentScriptSpecification(
        frontmatter=frontmatter,
        name="Test Agent",
        role="Test role",
        expertise="Test expertise",
        mission="Test mission",
        key_capabilities={"test": "capability"},
        mcp_integration={
            "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
            "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
        },
        interaction_model=InteractionModel(
            description="Test interaction model",
            phases={"Phase 1": Phase(description="Test phase", steps={"Step 1": "Test step"})},
        ),
    )

    # This should succeed without warnings or errors and hit the final return self
    assert spec
    assert spec.mcp_integration is not None
    assert len(spec.mcp_integration) == 2
    assert "context7" in spec.mcp_integration
    assert "sequential-thinking" in spec.mcp_integration


def test_missing_some_mcp_servers_in_integration(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test warning when frontmatter has MCP servers but mcp_integration only mentions some."""

    partial_valid_spec["mcp_integration"] = {
        "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
        # Missing "sequential-thinking" - should trigger warning
    }

    with patch("src.agent_script_spec.models.logger.warning") as mock_warning:
        spec = AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

        assert spec
        assert mock_warning.call_count == 1
        assert "Missing MCP servers in mcp_integration: {'sequential-thinking'}" in str(mock_warning.call_args[0][0])


def test_extra_mcp_servers_in_integration(frontmatter: Frontmatter, partial_valid_spec: dict):
    """Test error when mcp_integration has extra MCP servers not in frontmatter tools."""

    partial_valid_spec["mcp_integration"] = {
        "context7": "Research AI frameworks, model documentation, best practices, safety guidelines",
        "sequential-thinking": "Complex AI system design, multi-step reasoning workflows, optimization strategies",
        "extra-server": "This server is not in the frontmatter tools - should cause error",
    }

    with pytest.raises(ValidationError) as exc_info:
        AgentScriptSpecification(
            frontmatter=frontmatter,
            **partial_valid_spec,
        )

    # Check that the error message mentions the extra MCP server
    assert "Extra MCP servers in mcp_integration: {'extra-server'}" in str(exc_info.value)
