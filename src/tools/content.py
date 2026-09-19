"""
Content retrieval tools — syllabus, bibliography, exams.

These are the foundational tools present in every subject MCP.
"""

from __future__ import annotations

from mcp import types

from ..resources.loader import ContentLoader


def register_content_tools(
    tools: list[types.Tool],
    handlers: dict,
    loader: ContentLoader,
    config: dict,
) -> None:

    # --- get_syllabus ---
    tools.append(
        types.Tool(
            name="get_syllabus",
            description="Return the full course syllabus, including topics, timeline, and assessment criteria.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    )

    async def handle_get_syllabus(_args: dict) -> str:
        items = loader.get_section("syllabus")
        if not items:
            return "No syllabus content loaded yet. Add files to content/syllabus/."
        return "\n\n---\n\n".join(f"# {item['name']}\n\n{item['text']}" for item in items)

    handlers["get_syllabus"] = handle_get_syllabus

    # --- get_bibliography ---
    tools.append(
        types.Tool(
            name="get_bibliography",
            description="Return the recommended bibliography and reading materials for this subject.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    )

    async def handle_get_bibliography(_args: dict) -> str:
        items = loader.get_section("bibliography")
        if not items:
            return "No bibliography content loaded yet. Add files to content/bibliography/."
        return "\n\n---\n\n".join(f"# {item['name']}\n\n{item['text']}" for item in items)

    handlers["get_bibliography"] = handle_get_bibliography

    # --- get_past_exams ---
    tools.append(
        types.Tool(
            name="get_past_exams",
            description="Retrieve past exam papers, optionally filtered by topic or year.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "description": "Optional keyword to filter exams by topic, year, or type.",
                    }
                },
                "required": [],
            },
        )
    )

    async def handle_get_past_exams(args: dict) -> str:
        keyword = args.get("filter", "").strip()
        if keyword:
            results = loader.search(keyword, section="exams")
            if not results:
                return f"No exams found matching '{keyword}'."
            return "\n\n---\n\n".join(r["snippet"] for r in results)
        items = loader.get_section("exams")
        if not items:
            return "No exam content loaded yet. Add files to content/exams/."
        return "\n\n---\n\n".join(f"# {item['name']}\n\n{item['text']}" for item in items)

    handlers["get_past_exams"] = handle_get_past_exams

    # --- search_content ---
    tools.append(
        types.Tool(
            name="search_content",
            description="Full-text search across all loaded content (notes, syllabus, exams, exercises, bibliography).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The term or phrase to search for.",
                    },
                    "section": {
                        "type": "string",
                        "description": "Optional: restrict search to a section — 'syllabus', 'bibliography', 'exams', 'exercises', 'notes', 'media'.",
                    },
                },
                "required": ["query"],
            },
        )
    )

    async def handle_search_content(args: dict) -> str:
        query = args.get("query", "").strip()
        section = args.get("section", None)
        if not query:
            return "Please provide a search query."
        results = loader.search(query, section=section)
        if not results:
            return f"No results found for '{query}'" + (f" in section '{section}'" if section else "") + "."
        parts = []
        for r in results[:10]:  # cap at 10 results
            parts.append(f"**Source:** {r['uri']}\n{r['snippet']}")
        return "\n\n---\n\n".join(parts)

    handlers["search_content"] = handle_search_content

    # --- get_notes ---
    tools.append(
        types.Tool(
            name="get_notes",
            description="Retrieve lecture notes or summaries, optionally filtered by topic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Optional topic or keyword to filter notes.",
                    }
                },
                "required": [],
            },
        )
    )

    async def handle_get_notes(args: dict) -> str:
        topic = args.get("topic", "").strip()
        if topic:
            results = loader.search(topic, section="notes")
            if not results:
                return f"No notes found for topic '{topic}'."
            return "\n\n---\n\n".join(r["snippet"] for r in results)
        items = loader.get_section("notes")
        if not items:
            return "No notes loaded yet. Add files to content/notes/."
        return "\n\n---\n\n".join(f"# {item['name']}\n\n{item['text']}" for item in items)

    handlers["get_notes"] = handle_get_notes
