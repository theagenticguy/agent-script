"""Simplified drivers for converting between JSON and Markdown formats.

This module provides conversion utilities for the simplified agent script specification
that uses a flattened structure and RFC 2119 language.
"""

import mistune
import re
from agent_script_spec.simplified_models import SimplifiedAgentScriptSpecification, Frontmatter, WorkflowStep, InteractionWorkflow, RequirementRule
from enum import StrEnum
from typing import cast


KV_RE = re.compile(r":\s*", 1)  # split "key: value" only once


class SimplifiedSection(StrEnum):
    """Simplified section names for markdown parsing."""
    NAME = "name"
    ROLE = "role"
    EXPERTISE = "expertise"
    MISSION = "mission"
    CAPABILITIES = "capabilities"
    MCP_INTEGRATION = "mcp integration"
    WORKFLOW = "workflow"
    REQUIREMENTS = "requirements"
    COMMUNICATION_STYLE = "communication style"
    DELIVERABLES = "deliverables"


def _slug(text: str) -> str:
    """Normalize a heading for comparison (case-insensitive, accent-safe)."""
    return re.sub(r"[^\w ]", "", text).casefold().strip()


def _txt(node: dict) -> str:
    """Return concatenated raw text from an AST node."""
    if node["type"] == "text":
        return node["raw"]
    return "".join(_txt(c) for c in node.get("children", []))


def _collect_paragraph(ast: list[dict], idx: int) -> tuple[str, int]:
    """Return joined paragraphs until next heading."""
    parts = []

    # Skip initial blank lines
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1

    while idx < len(ast) and ast[idx]["type"] != "heading":
        if ast[idx]["type"] == "paragraph":
            parts.append(_txt(ast[idx]).strip())
        idx += 1
    return " ".join(parts).strip(), idx


def _collect_list_dict(ast: list[dict], idx: int) -> tuple[dict[str, str], int]:
    """Parse a bullet list whose items look like 'Key: value' -> dict."""
    mapping: dict[str, str] = {}

    # Skip blank lines to find the actual list
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1

    if idx < len(ast) and ast[idx]["type"] == "list":
        for li in ast[idx]["children"]:
            raw = _txt(li).strip()
            if ":" in raw:
                k, v = KV_RE.split(raw)
                mapping[k.strip()] = v.strip()
        idx += 1
    return mapping, idx


def _collect_list_items(ast: list[dict], idx: int) -> tuple[list[str], int]:
    """Parse a bullet list and return items as list of strings."""
    items: list[str] = []

    # Skip blank lines to find the actual list
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1

    if idx < len(ast) and ast[idx]["type"] == "list":
        items = [_txt(li).strip() for li in ast[idx]["children"]]
        idx += 1
    return items, idx


def _parse_workflow_steps(ast: list[dict], idx: int) -> tuple[list[WorkflowStep], int]:
    """Parse workflow steps from markdown AST."""
    steps: list[WorkflowStep] = []
    
    # Skip blank lines
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1
    
    # Look for numbered list or bullet list
    if idx < len(ast) and ast[idx]["type"] == "list":
        for li in ast[idx]["children"]:
            # Get the main description from the first child (paragraph)
            if li["children"] and li["children"][0]["type"] == "paragraph":
                description = _txt(li["children"][0]).strip()
                
                # Look for nested requirements list
                requirements = []
                if len(li["children"]) > 1:
                    for child in li["children"][1:]:
                        if child["type"] == "list":
                            for req_li in child["children"]:
                                req_text = _txt(req_li).strip()
                                if req_text:
                                    requirements.append(req_text)
                
                steps.append(WorkflowStep(
                    description=description,
                    requirements=requirements if requirements else None
                ))
        idx += 1
    
    return steps, idx


def _parse_workflow(ast: list[dict], idx: int) -> tuple[InteractionWorkflow, int]:
    """Parse the simplified workflow from markdown AST."""
    # Get workflow description
    description, idx = _collect_paragraph(ast, idx)
    
    # Look for "Steps" or "Workflow Steps" heading
    steps = []
    completion_criteria = None
    
    while idx < len(ast):
        if ast[idx]["type"] == "heading":
            heading_text = _slug(_txt(ast[idx]))
            level = ast[idx]["attrs"]["level"]
            
            if level == 3 and ("step" in heading_text or "workflow" in heading_text):
                idx += 1
                steps, idx = _parse_workflow_steps(ast, idx)
            elif level == 3 and "completion" in heading_text:
                idx += 1
                completion_criteria, idx = _collect_paragraph(ast, idx)
            else:
                break
        else:
            break
    
    return InteractionWorkflow(
        description=description,
        steps=steps,
        completion_criteria=completion_criteria
    ), idx


def _parse_requirements(ast: list[dict], idx: int) -> tuple[list[RequirementRule], int]:
    """Parse requirements from markdown AST."""
    requirements = []
    
    # Skip blank lines
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1
    
    if idx < len(ast) and ast[idx]["type"] == "list":
        for li in ast[idx]["children"]:
            req_text = _txt(li).strip()
            if req_text:
                requirements.append(RequirementRule(requirement=req_text))
        idx += 1
    
    return requirements, idx


def get_frontmatter_markdown(src_frontmatter: Frontmatter) -> str:
    """Get the frontmatter markdown."""
    frontmatter_dict = src_frontmatter.model_dump()
    
    # Remove the mcp_server_names from the frontmatter
    frontmatter_dict.pop("mcp_server_names", None)
    # Convert tools to comma separated string
    if frontmatter_dict.get("tools"):
        frontmatter_dict["tools"] = ", ".join(frontmatter_dict["tools"])
    
    return f"""---
name: {frontmatter_dict["name"]}
description: {frontmatter_dict["description"]}
tools: {frontmatter_dict.get("tools", "")}
model: {frontmatter_dict.get("model", "")}
---
"""


def to_markdown(spec: SimplifiedAgentScriptSpecification) -> str:
    """Convert the simplified agent script specification to markdown."""
    
    frontmatter_markdown = get_frontmatter_markdown(spec.frontmatter)
    
    # Build markdown content
    content = []
    
    # Title and basic info
    content.append(f"# {spec.name}")
    content.append("")
    content.append("## Role")
    content.append("")
    content.append(spec.role)
    content.append("")
    content.append("## Expertise")
    content.append("")
    content.append(spec.expertise)
    content.append("")
    content.append("## Mission")
    content.append("")
    content.append(spec.mission)
    content.append("")
    
    # Capabilities
    if spec.capabilities:
        content.append("### Capabilities")
        content.append("")
        for capability, description in spec.capabilities.items():
            content.append(f"* {capability}: {description}")
        content.append("")
    
    # MCP Integration
    if spec.mcp_integration:
        content.append("### MCP Integration")
        content.append("")
        for server_name, description in spec.mcp_integration.items():
            content.append(f"* {server_name}: {description}")
        content.append("")
    
    # Workflow
    content.append("## Workflow")
    content.append("")
    content.append(spec.workflow.description)
    content.append("")
    
    if spec.workflow.steps:
        content.append("### Workflow Steps")
        content.append("")
        for i, step in enumerate(spec.workflow.steps, 1):
            content.append(f"{i}. {step.description}")
            if step.requirements:
                content.append("")
                for req in step.requirements:
                    content.append(f"   * {req}")
            content.append("")
    
    if spec.workflow.completion_criteria:
        content.append("### Completion Criteria")
        content.append("")
        content.append(spec.workflow.completion_criteria)
        content.append("")
    
    # Requirements
    if spec.requirements:
        content.append("## Requirements")
        content.append("")
        for req in spec.requirements:
            content.append(f"* {req.requirement}")
            if req.rationale:
                content.append(f"  - Rationale: {req.rationale}")
        content.append("")
    
    # Communication Style
    if spec.communication_style:
        content.append("## Communication Style")
        content.append("")
        content.append(spec.communication_style)
        content.append("")
    
    # Deliverables
    if spec.deliverables:
        content.append("## Deliverables")
        content.append("")
        for deliverable, description in spec.deliverables.items():
            content.append(f"* {deliverable}: {description}")
        content.append("")
    
    # Combine frontmatter and content
    body_markdown = "\n".join(content)
    return frontmatter_markdown + "\n" + body_markdown


def from_markdown(markdown: str) -> SimplifiedAgentScriptSpecification:
    """Convert the markdown to a simplified agent script specification."""
    
    # Extract frontmatter
    _, frontmatter_markdown, body_markdown = re.split(r"^--- *\n(.*?)\n--- *\n", markdown, flags=re.DOTALL)
    
    # Extract frontmatter fields
    name_match = re.search(r"^name: (.*?)$", frontmatter_markdown, re.MULTILINE)
    description_match = re.search(r"^description: (.*?)$", frontmatter_markdown, re.MULTILINE)
    tools_match = re.search(r"^tools: (.*?)$", frontmatter_markdown, re.MULTILINE)
    model_match = re.search(r"^model: (.*?)$", frontmatter_markdown, re.MULTILINE)
    
    frontmatter_dict = {
        "name": name_match.group(1) if name_match else "",
        "description": description_match.group(1) if description_match else "",
        "tools": tools_match.group(1) if tools_match else "",
        "model": model_match.group(1) if model_match else "",
    }
    
    # Parse body markdown to AST
    md = mistune.create_markdown(renderer="ast")
    ast = md(body_markdown)
    
    frontmatter_model = Frontmatter(
        name=str(frontmatter_dict["name"]),
        description=str(frontmatter_dict["description"]),
        tools=set(str(frontmatter_dict["tools"]).split(", ")) if frontmatter_dict["tools"] else None,
        model=str(frontmatter_dict["model"]) if frontmatter_dict["model"] else None,
    )
    
    data: dict[str, object] = {
        "name": "",
        "role": "",
        "expertise": "",
        "mission": "",
        "capabilities": {},
        "mcp_integration": None,
        "workflow": None,
        "requirements": None,
        "communication_style": None,
        "deliverables": None,
    }
    
    # Type cast ast to proper type for processing
    ast_nodes = list(ast) if isinstance(ast, list) else []
    
    idx = 0
    while idx < len(ast_nodes):
        node = ast_nodes[idx]
        if not isinstance(node, dict) or node.get("type") != "heading":
            idx += 1
            continue
        
        attrs = node.get("attrs", {})
        if not isinstance(attrs, dict):
            idx += 1
            continue
        
        lvl = attrs.get("level", 0)
        heading = _slug(_txt(node))
        
        match lvl, heading:
            # H1 sections
            case 1, _:  # Any H1 is treated as the name
                data["name"] = _txt(node).strip()
                idx += 1
            # H2 sections
            case 2, SimplifiedSection.ROLE:
                data["role"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, SimplifiedSection.EXPERTISE:
                data["expertise"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, SimplifiedSection.MISSION:
                data["mission"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, SimplifiedSection.WORKFLOW:
                data["workflow"], idx = _parse_workflow(ast_nodes, idx + 1)
            case 2, SimplifiedSection.REQUIREMENTS:
                data["requirements"], idx = _parse_requirements(ast_nodes, idx + 1)
            case 2, SimplifiedSection.COMMUNICATION_STYLE:
                data["communication_style"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, SimplifiedSection.DELIVERABLES:
                data["deliverables"], idx = _collect_list_dict(ast_nodes, idx + 1)
            # H3 sections
            case 3, SimplifiedSection.CAPABILITIES:
                data["capabilities"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, SimplifiedSection.MCP_INTEGRATION:
                data["mcp_integration"], idx = _collect_list_dict(ast_nodes, idx + 1)
            # fallback
            case _:
                idx += 1
    
    # Create default workflow if not found
    if not data["workflow"]:
        data["workflow"] = InteractionWorkflow(
            description="Standard workflow for completing tasks",
            steps=[]
        )
    
    spec = SimplifiedAgentScriptSpecification(
        frontmatter=frontmatter_model,
        name=str(data["name"]) if data["name"] else frontmatter_model.name,
        role=str(data["role"]) if data["role"] else "",
        expertise=str(data["expertise"]) if data["expertise"] else "",
        mission=str(data["mission"]) if data["mission"] else "",
        capabilities=data["capabilities"] if isinstance(data["capabilities"], dict) else {},
        mcp_integration=data["mcp_integration"] if isinstance(data["mcp_integration"], dict) else None,
        workflow=data["workflow"] if isinstance(data["workflow"], InteractionWorkflow) else InteractionWorkflow(description="", steps=[]),
        requirements=data["requirements"] if isinstance(data["requirements"], list) else None,
        communication_style=str(data["communication_style"]) if data["communication_style"] else None,
        deliverables=data["deliverables"] if isinstance(data["deliverables"], dict) else None,
    )
    
    return spec