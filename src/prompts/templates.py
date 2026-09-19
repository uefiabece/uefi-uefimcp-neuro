"""Loads prompt fragments from the /prompts directory."""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def load_prompt(name: str) -> str:
    """Load a prompt file by name (without .md extension)."""
    path = PROMPTS_DIR / f"{name}.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return f"[Prompt '{name}' not found. Add it to prompts/{name}.md]"
