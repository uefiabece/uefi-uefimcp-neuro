# Customization Guide

How to specialize this template for a specific UFABC subject.

---

## Step 1 — Update `config/subject.json`

Fill in all fields:

```json
{
  "server_name": "uefi-mcp-precalculus",
  "subject_name": "Pré-Cálculo",
  "course_name": "Bacharelado em Ciência e Tecnologia",
  "institution": "UFABC",
  "language": "pt-BR",

  "features": {
    "image_interpretation": false,
    "symbolic_math": true,
    "circuit_editing": false,
    "code_execution": false
  },

  "metadata": {
    "credits": 4,
    "semester": "Q1",
    "professor": null,
    "year": 2025
  }
}
```

Enable only the features your subject actually needs. Each feature flag may require additional dependencies (see `pyproject.toml` optional groups).

---

## Step 2 — Update `prompts/system.md`

Replace all `[Subject Name]` placeholders with the real subject name and course. Adjust the scope section to match what topics are in/out of bounds.

---

## Step 3 — Populate `content/`

See [`content-guide.md`](./content-guide.md) for full instructions.

At minimum, add:
- [ ] Syllabus → `content/syllabus/`
- [ ] Bibliography → `content/bibliography/`
- [ ] At least a few past exams → `content/exams/`

---

## Step 4 — Add subject-specific tools (optional)

For subjects with unusual needs, add new tool files under `src/tools/` and register them in `src/server.py`.

### Example: adding a circuit interpreter tool

```python
# src/tools/circuits.py

def register_circuit_tools(tools, handlers, loader, config):
    if not config.get("features", {}).get("circuit_editing"):
        return  # skip if feature not enabled

    tools.append(types.Tool(
        name="interpret_circuit",
        description="Interpret a circuit diagram image and describe its components.",
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Path to the circuit image in content/media/"}
            },
            "required": ["image_path"]
        }
    ))

    async def handle_interpret_circuit(args):
        # implementation here
        ...

    handlers["interpret_circuit"] = handle_interpret_circuit
```

Then in `server.py`:
```python
from .tools.circuits import register_circuit_tools
register_circuit_tools(all_tools, tool_handlers, loader, config)
```

---

## Naming the repo

Follow the ecosystem convention:

```
uefi-<course-slug>       # course-level (e.g. uefi-science-and-technology)
uefi-<subject-slug>      # subject-level (e.g. uefi-precalculus)
```

Register the new repo in `uefi-context/projects/`.
