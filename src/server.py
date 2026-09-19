"""
MCP server entry point for a UFABC subject.

This is the template server. When specializing for a subject:
- Update config/subject.json with subject metadata
- Fill content/ with subject-specific material
- Adjust tool list below based on subject needs
- Update prompts/system.md with subject identity
"""

from __future__ import annotations

import json
from pathlib import Path

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from .resources.loader import ContentLoader
from .tools.content import register_content_tools
from .tools.teaching import register_teaching_tools
from .tools.exercises import register_exercise_tools
from .prompts.templates import load_prompt

ROOT = Path(__file__).parent.parent
CONFIG_PATH = ROOT / "config" / "subject.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def build_server(config: dict, loader: ContentLoader) -> Server:
    subject_name = config.get("subject_name", "Unknown Subject")
    server = Server(config.get("server_name", "uefi-mcp"))

    system_prompt = load_prompt("system")

    # --- Resources ---
    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        return loader.list_resources()

    @server.read_resource()
    async def read_resource(uri: types.AnyUrl) -> str:
        return loader.read_resource(str(uri))

    # --- Prompts ---
    @server.list_prompts()
    async def list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="teach",
                description=f"Enter teaching mode for {subject_name}",
                arguments=[
                    types.PromptArgument(name="topic", description="Topic to teach", required=True)
                ],
            ),
            types.Prompt(
                name="solve",
                description="Walk through an exercise step by step",
                arguments=[
                    types.PromptArgument(
                        name="exercise", description="Exercise text or description", required=True
                    )
                ],
            ),
        ]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        args = arguments or {}
        if name == "teach":
            topic = args.get("topic", "")
            teaching_prompt = load_prompt("teaching")
            return types.GetPromptResult(
                description=f"Teaching: {topic}",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"{system_prompt}\n\n{teaching_prompt}\n\nTeach me about: {topic}",
                        ),
                    )
                ],
            )
        if name == "solve":
            exercise = args.get("exercise", "")
            solver_prompt = load_prompt("solver")
            return types.GetPromptResult(
                description=f"Solving exercise",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(
                            type="text",
                            text=f"{system_prompt}\n\n{solver_prompt}\n\nExercise: {exercise}",
                        ),
                    )
                ],
            )
        raise ValueError(f"Unknown prompt: {name}")

    # --- Tools ---
    all_tools: list[types.Tool] = []
    tool_handlers: dict = {}

    register_content_tools(all_tools, tool_handlers, loader, config)
    register_teaching_tools(all_tools, tool_handlers, loader, config)
    register_exercise_tools(all_tools, tool_handlers, loader, config)

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return all_tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        handler = tool_handlers.get(name)
        if handler is None:
            raise ValueError(f"Unknown tool: {name}")
        result = await handler(arguments)
        return [types.TextContent(type="text", text=str(result))]

    return server


async def run():
    config = load_config()
    loader = ContentLoader(ROOT / "content")
    server = build_server(config, loader)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    anyio.run(run)


if __name__ == "__main__":
    main()
