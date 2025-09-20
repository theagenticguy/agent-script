"""Tests for the simplified agent script models."""

import json
import pytest
from pathlib import Path
import sys

# Add package paths for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "packages/agent-script-spec/src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_script_spec.simplified_models import SimplifiedAgentScriptSpecification, WorkflowStep, InteractionWorkflow, RequirementRule
from agent_script_tools.simplified_drivers import to_markdown, from_markdown


class TestSimplifiedModels:
    """Test the simplified agent script models."""
    
    def test_workflow_step_validation(self):
        """Test WorkflowStep model validation."""
        step = WorkflowStep(
            description="Test step",
            requirements=["MUST do something", "SHOULD do something else"]
        )
        assert step.description == "Test step"
        assert len(step.requirements) == 2
    
    def test_requirement_rule_validation(self):
        """Test RequirementRule model validation."""
        rule = RequirementRule(
            requirement="MUST use proper formatting",
            rationale="For consistency and clarity"
        )
        assert rule.requirement == "MUST use proper formatting"
        assert rule.rationale == "For consistency and clarity"
    
    def test_simplified_spec_validation(self):
        """Test SimplifiedAgentScriptSpecification validation."""
        example_path = Path(__file__).parent.parent / "examples/ai-engineer-simplified.json"
        
        if example_path.exists():
            with open(example_path) as f:
                data = json.load(f)
            
            spec = SimplifiedAgentScriptSpecification.model_validate(data)
            
            assert spec.name == "ai-engineer"
            assert "LLM" in spec.role
            assert len(spec.capabilities) == 4
            assert len(spec.workflow.steps) == 4
            assert len(spec.requirements) == 7
            
            # Test RFC 2119 compliance
            rfc_keywords = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY", "MAY NOT"]
            for req in spec.requirements:
                has_rfc_keyword = any(keyword in req.requirement.upper() for keyword in rfc_keywords)
                assert has_rfc_keyword, f"Requirement should use RFC 2119 language: {req.requirement}"
            
            # Test that we have both positive and negative requirements
            has_must_not = any("MUST NOT" in req.requirement.upper() for req in spec.requirements)
            has_should_not = any("SHOULD NOT" in req.requirement.upper() for req in spec.requirements)
            assert has_must_not, "Specification should include MUST NOT requirements for prohibited behaviors"
            assert has_should_not, "Specification should include SHOULD NOT requirements for discouraged behaviors"
    
    def test_markdown_conversion(self):
        """Test conversion between JSON and Markdown."""
        example_path = Path(__file__).parent.parent / "examples/ai-engineer-simplified.json"
        
        if example_path.exists():
            with open(example_path) as f:
                data = json.load(f)
            
            spec = SimplifiedAgentScriptSpecification.model_validate(data)
            
            # Convert to markdown
            markdown = to_markdown(spec)
            assert "# ai-engineer" in markdown
            assert "## Role" in markdown
            assert "## Workflow" in markdown
            assert "## Requirements" in markdown
            
            # Test round-trip conversion
            spec_from_md = from_markdown(markdown)
            
            assert spec.name == spec_from_md.name
            assert spec.role == spec_from_md.role
            assert spec.mission == spec_from_md.mission
            assert len(spec.capabilities) == len(spec_from_md.capabilities)
    
    def test_mcp_integration_validation(self):
        """Test MCP integration validation."""
        from agent_script_spec.simplified_models import Frontmatter
        
        # Test with valid MCP tools and integration
        frontmatter = Frontmatter(
            name="test-agent",
            description="Test agent",
            tools={"mcp__test-server__tool1", "regular_tool"},
            model="test-model"
        )
        
        spec_data = {
            "frontmatter": frontmatter,
            "name": "test-agent",
            "role": "Test role",
            "expertise": "Test expertise",
            "mission": "Test mission",
            "capabilities": {"test": "capability"},
            "mcp_integration": {"test-server": "Test integration"},
            "workflow": InteractionWorkflow(
                description="Test workflow",
                steps=[WorkflowStep(description="Test step")]
            )
        }
        
        spec = SimplifiedAgentScriptSpecification(**spec_data)
        assert spec.mcp_integration["test-server"] == "Test integration"
        
        # Test with mismatched MCP integration (should raise error)
        spec_data["mcp_integration"] = {"wrong-server": "Wrong integration"}
        
        with pytest.raises(ValueError, match="Extra MCP servers"):
            SimplifiedAgentScriptSpecification(**spec_data)