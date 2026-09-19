"""
Teaching tools — concept explanation, topic breakdown, knowledge checks.

These tools guide the AI in teaching subject matter rather than just retrieving it.
They rely on the loaded content but add pedagogical structure.
"""

from __future__ import annotations

from mcp import types

from ..resources.loader import ContentLoader


def register_teaching_tools(
    tools: list[types.Tool],
    handlers: dict,
    loader: ContentLoader,
    config: dict,
) -> None:

    subject_name = config.get("subject_name", "this subject")

    # --- explain_concept ---
    tools.append(
        types.Tool(
            name="explain_concept",
            description=(
                f"Explain a concept from {subject_name}. "
                "Searches loaded content for relevant material and returns a structured explanation."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "concept": {
                        "type": "string",
                        "description": "The concept or topic to explain.",
                    },
                    "depth": {
                        "type": "string",
                        "enum": ["introductory", "intermediate", "advanced"],
                        "description": "Depth of explanation. Defaults to 'intermediate'.",
                    },
                },
                "required": ["concept"],
            },
        )
    )

    async def handle_explain_concept(args: dict) -> str:
        concept = args.get("concept", "").strip()
        depth = args.get("depth", "intermediate")
        if not concept:
            return "Please provide a concept to explain."

        # Pull relevant content to ground the explanation
        results = loader.search(concept)
        context_block = ""
        if results:
            snippets = "\n\n".join(r["snippet"] for r in results[:5])
            context_block = f"\n\n## Relevant content from course materials\n\n{snippets}"

        return (
            f"## Concept: {concept}\n"
            f"**Depth:** {depth}\n"
            f"**Subject:** {subject_name}\n"
            f"{context_block}\n\n"
            f"[The AI should now produce a {depth}-level explanation of '{concept}' "
            f"grounded in the course material above and its own knowledge of {subject_name}.]"
        )

    handlers["explain_concept"] = handle_explain_concept

    # --- get_topic_outline ---
    tools.append(
        types.Tool(
            name="get_topic_outline",
            description="Return a structured outline of all topics in the syllabus, useful for planning study sessions.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    )

    async def handle_get_topic_outline(_args: dict) -> str:
        items = loader.get_section("syllabus")
        if not items:
            return (
                "No syllabus loaded. Add syllabus content to content/syllabus/ to generate an outline."
            )
        combined = "\n\n".join(item["text"] for item in items)
        return (
            f"## Topic Outline — {subject_name}\n\n"
            f"[Extracted from syllabus]\n\n"
            f"{combined}"
        )

    handlers["get_topic_outline"] = handle_get_topic_outline

    # --- generate_study_plan ---
    tools.append(
        types.Tool(
            name="generate_study_plan",
            description="Generate a suggested study plan for an upcoming exam or for the full course.",
            inputSchema={
                "type": "object",
                "properties": {
                    "days_available": {
                        "type": "integer",
                        "description": "Number of days available to study.",
                    },
                    "focus_topics": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of topics to prioritize.",
                    },
                },
                "required": ["days_available"],
            },
        )
    )

    async def handle_generate_study_plan(args: dict) -> str:
        days = args.get("days_available", 7)
        focus = args.get("focus_topics", [])
        focus_note = f"\nPriority topics: {', '.join(focus)}" if focus else ""
        syllabus_items = loader.get_section("syllabus")
        syllabus_text = (
            "\n\n".join(item["text"] for item in syllabus_items)
            if syllabus_items
            else "No syllabus loaded."
        )
        return (
            f"## Study Plan Request\n"
            f"**Subject:** {subject_name}\n"
            f"**Days available:** {days}{focus_note}\n\n"
            f"## Syllabus reference\n\n{syllabus_text}\n\n"
            f"[The AI should produce a day-by-day study plan distributing the topics above "
            f"across {days} days, prioritizing focus topics if listed.]"
        )

    handlers["generate_study_plan"] = handle_generate_study_plan
