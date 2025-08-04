import mistune
import re
from agent_script_spec.models import AgentScriptSpecification, ComplexStep, Frontmatter, InteractionModel, Phase
from enum import StrEnum
from typing import Literal, cast


STEP_RE = re.compile(r"^(Step \d+):\s*(.+)$")
KV_RE = re.compile(r":\s*", 1)  # split “key: value” only once


class Section(StrEnum):
    NAME = "name"
    ROLE = "role"
    EXPERTISE = "expertise"
    MISSION = "mission"
    KEY_CAPABILITIES = "key capabilities"
    MCP_INTEGRATION = "mcp integration"
    TOOL_USAGE = "tool usage"
    COMM_PROTOCOL = "communication protocol"
    INTERACTION_MODEL = "interaction model"
    CORE_COMPETENCIES = "core competencies"
    GUIDING_PRINCIPLES = "guiding principles"
    RULES = "rules"
    APPROACH = "approach"
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
    items: list[str] = []

    # Skip blank lines to find the actual list
    while idx < len(ast) and ast[idx]["type"] == "blank_line":
        idx += 1

    if idx < len(ast) and ast[idx]["type"] == "list":
        items = [_txt(li).strip() for li in ast[idx]["children"]]
        idx += 1
    return items, idx


# ───────────── interaction-model parsing ─────────────


def _parse_steps(ast: list[dict], idx: int) -> tuple[dict[str, str | ComplexStep], int]:
    steps: dict[str, str | ComplexStep] = {}

    while idx < len(ast) and ast[idx]["type"] != "heading":
        match ast[idx]:
            case {"type": "blank_line"}:
                # Skip blank lines
                pass
            case {"type": "paragraph"}:
                if m := STEP_RE.match(_txt(ast[idx])):
                    steps[m.group(1)] = m.group(2).strip()
            case {"type": "list"}:
                for li in ast[idx]["children"]:
                    head = _txt(li["children"][0]).strip()
                    if ":" in head:
                        k, desc = KV_RE.split(head)
                        k = k.strip()

                        # Only include steps that match the "Step N" pattern
                        if re.match(r"^Step \d+$", k):
                            # nested sub-steps?
                            nested = {}
                            if len(li["children"]) > 1 and li["children"][1]["type"] == "list":
                                for sub in li["children"][1]["children"]:
                                    sub_head = _txt(sub).strip()
                                    if ":" in sub_head:
                                        sk, sv = KV_RE.split(sub_head)
                                        nested[sk.strip()] = sv.strip()
                            steps[k] = ComplexStep(description=desc.strip(), steps=nested) if nested else desc.strip()
        idx += 1
    return steps, idx


def _parse_interaction_model(ast: list[dict], idx: int) -> tuple[InteractionModel, int]:
    description, idx = _collect_paragraph(ast, idx)
    phases: dict[str, Phase] = {}

    while idx < len(ast):
        if not (node := ast[idx])["type"] == "heading" or node["attrs"]["level"] != 3:
            break
        phase_key = _txt(node).strip()
        idx += 1

        # Collect only the first paragraph as phase description, not all paragraphs
        phase_parts = []
        # Skip blank lines
        while idx < len(ast) and ast[idx]["type"] == "blank_line":
            idx += 1
        # Get first paragraph only
        if idx < len(ast) and ast[idx]["type"] == "paragraph":
            phase_parts.append(_txt(ast[idx]).strip())
            idx += 1
        phase_desc = " ".join(phase_parts).strip()

        # Now parse steps from remaining content
        step_map, idx = _parse_steps(ast, idx)

        # optional H4 "End of Phase Instructions"
        end_instr = None
        if (
            idx < len(ast)
            and (ep := ast[idx])["type"] == "heading"
            and ep["attrs"]["level"] == 4
            and _slug(_txt(ep)) == "end of phase instructions"
        ):
            idx += 1
            end_instr, idx = _collect_paragraph(ast, idx)

        phases[phase_key] = Phase(
            description=phase_desc,
            steps=step_map,
            end_of_phase_instructions=end_instr,
        )

    return InteractionModel(description=description, phases=phases), idx


def get_frontmatter_markdown(src_frontmatter: Frontmatter) -> str:
    """Get the frontmatter markdown."""

    # convert frontmatter to markdown
    frontmatter_dict = src_frontmatter.model_dump()

    # remove the mcp_server_names from the frontmatter
    frontmatter_dict.pop("mcp_server_names", None)
    # convert tools to comma separated string
    frontmatter_dict["tools"] = ", ".join(frontmatter_dict["tools"])

    # convert frontmatter to markdown
    frontmatter_markdown = f"""---
name: {frontmatter_dict["name"]}
description: {frontmatter_dict["description"]}
tools: {frontmatter_dict["tools"]}
model: {frontmatter_dict["model"]}
---
"""

    return frontmatter_markdown


def to_markdown(spec: AgentScriptSpecification) -> str:
    """Convert the agent script specification to markdown."""

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

    # Key Capabilities
    if spec.key_capabilities:
        content.append("### Key Capabilities")
        content.append("")
        for key, description in spec.key_capabilities.items():
            content.append(f"* {key}: {description}")
        content.append("")

    # MCP Integration
    if spec.mcp_integration:
        content.append("### MCP Integration")
        content.append("")
        for server_name, description in spec.mcp_integration.items():
            content.append(f"* {server_name}: {description}")
        content.append("")

    # Tool Usage
    if spec.tool_usages:
        content.append("### Tool Usage")
        content.append("")
        for tool_category, description in spec.tool_usages.items():
            content.append(f"* {tool_category}: {description}")
        content.append("")

    # Communication Protocol
    if spec.communication_protocols:
        content.append("### Communication Protocol")
        content.append("")
        content.append(spec.communication_protocols)
        content.append("")

    # Interaction Model
    content.append("## Interaction Model")
    content.append("")
    content.append(spec.interaction_model.description)
    content.append("")

    for phase_key, phase in spec.interaction_model.phases.items():
        content.append(f"### {phase_key}")
        content.append("")
        content.append(phase.description)
        content.append("")

        # Steps
        for step_key, step in phase.steps.items():
            if isinstance(step, str):
                content.append(f"{step_key}: {step}")
            else:  # ComplexStep
                content.append(f"{step_key}: {step.description}")
                content.append("")
                if step.steps:
                    for sub_step_key, sub_step_desc in step.steps.items():
                        content.append(f"* {sub_step_key}: {sub_step_desc}")
        if phase.end_of_phase_instructions:
            content.append("")
            content.append("#### End of Phase Instructions")
            content.append("")
            content.append(phase.end_of_phase_instructions)

        content.append("")

    content.append("## Final Instructions")
    content.append("")

    # Core Competencies
    if spec.core_competencies:
        content.append("### Core Competencies")
        content.append("")
        for competency, description in spec.core_competencies.items():
            content.append(f"* {competency}: {description}")
        content.append("")

    # Guiding Principles
    if spec.guiding_principles:
        content.append("### Guiding Principles")
        content.append("")
        for principle, description in spec.guiding_principles.items():
            content.append(f"* {principle}: {description}")
        content.append("")

    # Rules
    if spec.rules:
        content.append("### Rules")
        content.append("")
        if "DO" in spec.rules:
            content.append("#### DO")
            content.append("")
            for rule in spec.rules["DO"]:
                content.append(f"* {rule}")
            content.append("")
        if "DO-NOT" in spec.rules:
            content.append("#### DO NOT")
            content.append("")
            for rule in spec.rules["DO-NOT"]:
                content.append(f"* {rule}")
            content.append("")

    # Approach
    if spec.approach:
        content.append("### Approach")
        content.append("")
        for approach_key, approach_desc in spec.approach.items():
            content.append(f"* {approach_key}: {approach_desc}")
        content.append("")

    # Deliverables
    if spec.deliverables:
        content.append("## Deliverables")
        content.append("")
        content.append(
            "It is essential that your outputs are comprehensive and include all the relevant information according to the task and the deliverables below:"
        )
        content.append("")
        for deliverable, description in spec.deliverables.items():
            content.append(f"* {deliverable}: {description}")
        content.append("")

    # Combine frontmatter and content
    body_markdown = "\n".join(content)
    return frontmatter_markdown + "\n" + body_markdown


def from_markdown(markdown: str) -> AgentScriptSpecification:
    """Convert the markdown to an agent script specification."""

    # extract frontmatter as Frontmatter
    _, frontmatter_markdown, body_markdown = re.split(r"^--- *\n(.*?)\n--- *\n", markdown, flags=re.DOTALL)

    # extract name, description, tools, model from frontmatter
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
    # parse body markdown to ast
    md = mistune.create_markdown(renderer="ast")
    ast = md(body_markdown)

    frontmatter_model = Frontmatter(
        name=str(frontmatter_dict["name"]),
        description=str(frontmatter_dict["description"]),
        tools=set(str(frontmatter_dict["tools"]).split(", ")),
        model=str(frontmatter_dict["model"]),
    )

    data: dict[str, object] = {
        "role": "",
        "expertise": "",
        "mission": "",
        "key_capabilities": {},
        "mcp_integration": None,
        "tool_usages": None,
        "communication_protocols": None,
        "interaction_model": None,
        "core_competencies": None,
        "guiding_principles": None,
        "rules": None,
        "approach": None,
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
            # ───── H1 sections ─────
            case 1, _:  # Any H1 is treated as the name
                data["name"] = _txt(node).strip()
                idx += 1
            # ───── H2 sections ─────
            case 2, Section.ROLE:
                data["role"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, Section.EXPERTISE:
                data["expertise"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, Section.MISSION:
                data["mission"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 2, Section.INTERACTION_MODEL:
                data["interaction_model"], idx = _parse_interaction_model(ast_nodes, idx + 1)
            case 2, Section.DELIVERABLES:
                # Skip initial blank lines
                j = idx + 1
                while j < len(ast_nodes) and ast_nodes[j]["type"] == "blank_line":
                    j += 1
                # Skip the explanatory paragraph (first paragraph only)
                if j < len(ast_nodes) and ast_nodes[j]["type"] == "paragraph":
                    j += 1
                data["deliverables"], idx = _collect_list_dict(ast_nodes, j)
            # ───── H3 sections ─────
            case 3, Section.KEY_CAPABILITIES:
                data["key_capabilities"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.MCP_INTEGRATION:
                data["mcp_integration"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.TOOL_USAGE:
                data["tool_usages"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.COMM_PROTOCOL:
                data["communication_protocols"], idx = _collect_paragraph(ast_nodes, idx + 1)
            case 3, Section.CORE_COMPETENCIES:
                data["core_competencies"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.GUIDING_PRINCIPLES:
                data["guiding_principles"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.APPROACH:
                data["approach"], idx = _collect_list_dict(ast_nodes, idx + 1)
            case 3, Section.RULES:
                idx += 1
                rules: dict[str, list[str]] = {}

                # Skip blank lines to get to H4 headings
                while idx < len(ast_nodes) and ast_nodes[idx].get("type") == "blank_line":
                    idx += 1

                while (
                    idx < len(ast_nodes)
                    and isinstance(ast_nodes[idx], dict)
                    and ast_nodes[idx].get("type") == "heading"
                    and isinstance(ast_nodes[idx].get("attrs"), dict)
                    and ast_nodes[idx]["attrs"].get("level") == 4
                ):
                    sub = _slug(_txt(ast_nodes[idx]))
                    key = "DO" if sub == "do" else "DO-NOT"
                    rules[key], idx = _collect_list_items(ast_nodes, idx + 1)
                data["rules"] = rules or None
            # fallback
            case _:
                idx += 1

    spec = AgentScriptSpecification(
        frontmatter=frontmatter_model,
        name=str(data["name"]),
        role=str(data["role"]) if data["role"] else "",
        expertise=str(data["expertise"]) if data["expertise"] else "",
        mission=str(data["mission"]) if data["mission"] else "",
        key_capabilities=data["key_capabilities"] if isinstance(data["key_capabilities"], dict) else {},
        mcp_integration=data["mcp_integration"] if isinstance(data["mcp_integration"], dict) else None,
        tool_usages=data["tool_usages"] if isinstance(data["tool_usages"], dict) else None,
        communication_protocols=str(data["communication_protocols"]) if data["communication_protocols"] else None,
        interaction_model=data["interaction_model"]
        if isinstance(data["interaction_model"], InteractionModel)
        else InteractionModel(description="", phases={}),
        core_competencies=data["core_competencies"] if isinstance(data["core_competencies"], dict) else None,
        guiding_principles=data["guiding_principles"] if isinstance(data["guiding_principles"], dict) else None,
        rules=cast(
            dict[Literal["DO", "DO-NOT"], list[str]] | None,
            data["rules"]
            if (isinstance(data["rules"], dict) and all(k in ["DO", "DO-NOT"] for k in data["rules"].keys()))
            else None,
        ),
        approach=data["approach"] if isinstance(data["approach"], dict) else None,
        deliverables=data["deliverables"] if isinstance(data["deliverables"], dict) else None,
    )
    return spec
