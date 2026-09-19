"""
Exercise tools — retrieval, solving, and generation.

These tools handle practice problems: fetching from the content library,
walking through solutions step by step, and generating new exercises on demand.
"""

from __future__ import annotations

from mcp import types

from ..resources.loader import ContentLoader


def register_exercise_tools(
    tools: list[types.Tool],
    handlers: dict,
    loader: ContentLoader,
    config: dict,
) -> None:

    subject_name = config.get("subject_name", "this subject")

    # --- get_exercises ---
    tools.append(
        types.Tool(
            name="get_exercises",
            description="Retrieve practice exercises from the content library, optionally filtered by topic or difficulty.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Optional topic keyword to filter exercises.",
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                        "description": "Optional difficulty filter.",
                    },
                },
                "required": [],
            },
        )
    )

    async def handle_get_exercises(args: dict) -> str:
        topic = args.get("topic", "").strip()
        difficulty = args.get("difficulty", "").strip()

        query = " ".join(filter(None, [topic, difficulty]))
        if query:
            results = loader.search(query, section="exercises")
            if not results:
                return f"No exercises found for query '{query}'."
            return "\n\n---\n\n".join(r["snippet"] for r in results)

        items = loader.get_section("exercises")
        if not items:
            return "No exercises loaded yet. Add files to content/exercises/."
        return "\n\n---\n\n".join(f"# {item['name']}\n\n{item['text']}" for item in items)

    handlers["get_exercises"] = handle_get_exercises

    # --- solve_exercise ---
    tools.append(
        types.Tool(
            name="solve_exercise",
            description=(
                "Walk through the solution of an exercise step by step. "
                "Provide the exercise text and optionally the topic for better context retrieval."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "exercise": {
                        "type": "string",
                        "description": "The full text of the exercise to solve.",
                    },
                    "topic": {
                        "type": "string",
                        "description": "Optional topic hint to pull relevant theory from notes.",
                    },
                    "show_work": {
                        "type": "boolean",
                        "description": "If true, show all intermediate steps. Defaults to true.",
                    },
                },
                "required": ["exercise"],
            },
        )
    )

    async def handle_solve_exercise(args: dict) -> str:
        exercise = args.get("exercise", "").strip()
        topic = args.get("topic", "").strip()
        show_work = args.get("show_work", True)

        if not exercise:
            return "Please provide the exercise text."

        context_block = ""
        if topic:
            results = loader.search(topic, section="notes")
            if results:
                snippets = "\n\n".join(r["snippet"] for r in results[:3])
                context_block = f"\n\n## Related theory from notes\n\n{snippets}"

        return (
            f"## Exercise\n\n{exercise}\n"
            f"{context_block}\n\n"
            f"## Instructions for solver\n"
            f"Subject: {subject_name}\n"
            f"Show all intermediate steps: {show_work}\n\n"
            f"[The AI should now solve the exercise above, using the theory context if provided, "
            f"showing {'all intermediate steps' if show_work else 'only the final answer'}.]"
        )

    handlers["solve_exercise"] = handle_solve_exercise

    # --- generate_exercise ---
    tools.append(
        types.Tool(
            name="generate_exercise",
            description="Generate a new practice exercise on a given topic and difficulty level.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic for the exercise.",
                    },
                    "difficulty": {
                        "type": "string",
                        "enum": ["easy", "medium", "hard"],
                        "description": "Desired difficulty. Defaults to 'medium'.",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["multiple_choice", "open_answer", "proof", "practical"],
                        "description": "Exercise format. Defaults to 'open_answer'.",
                    },
                    "include_solution": {
                        "type": "boolean",
                        "description": "Whether to generate the solution alongside the exercise.",
                    },
                },
                "required": ["topic"],
            },
        )
    )

    async def handle_generate_exercise(args: dict) -> str:
        topic = args.get("topic", "").strip()
        difficulty = args.get("difficulty", "medium")
        style = args.get("style", "open_answer")
        include_solution = args.get("include_solution", False)

        # Pull reference material to ground generation
        results = loader.search(topic)
        context_block = ""
        if results:
            snippets = "\n\n".join(r["snippet"] for r in results[:3])
            context_block = f"\n\n## Reference material\n\n{snippets}"

        return (
            f"## Exercise Generation Request\n"
            f"**Subject:** {subject_name}\n"
            f"**Topic:** {topic}\n"
            f"**Difficulty:** {difficulty}\n"
            f"**Style:** {style}\n"
            f"**Include solution:** {include_solution}\n"
            f"{context_block}\n\n"
            f"[The AI should now generate a {difficulty} {style.replace('_', ' ')} exercise "
            f"about '{topic}' for {subject_name}, grounded in the reference material above. "
            f"{'Include a full solution.' if include_solution else 'Do not reveal the solution.'}]"
        )

    handlers["generate_exercise"] = handle_generate_exercise
