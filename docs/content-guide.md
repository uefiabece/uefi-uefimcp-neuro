# Content Guide

This guide explains how to add and organize educational content in the `content/` directory.

## Directory layout

```
content/
├── syllabus/       Official course syllabus and topic lists
├── bibliography/   Books, papers, and reference links
├── exams/          Past exams and answer keys
├── exercises/      Practice problems (organized by topic)
├── notes/          Lecture notes, summaries, and concept sheets
└── media/          Images, diagrams, and other visual content
```

## Supported file formats

The server indexes **text-based files** automatically:

| Extension | Use for |
|---|---|
| `.md` | Notes, explanations, formatted content (preferred) |
| `.txt` | Plain text content |
| `.tex` | LaTeX source files |
| `.csv` | Tabular data |
| `.json` / `.yaml` | Structured data |

Binary files (PDFs, images) are not indexed for search, but images in `content/media/` can be referenced by tools for subjects with `image_interpretation: true`.

## Naming conventions

- Use `kebab-case` for all filenames
- Include the topic in the filename: `derivatives-exercises.md`, not `exercises1.md`
- For exams: `MM-YYYY-exam-type.md` (e.g. `06-2023-midterm.md`)
- For exercises by topic: `<topic>-<level>.md` (e.g. `limits-medium.md`)

## Adding syllabus content

Create one or more `.md` files in `content/syllabus/`. Recommended structure:

```markdown
# Course Syllabus — [Subject Name]

## Topics
1. Topic A
2. Topic B
...

## Assessment
- Midterm: 40%
- Final exam: 60%

## Schedule
Week 1: Topic A
Week 2: Topic B
...
```

## Adding exercises

Exercises are plain markdown. Use the following structure to enable filtering by difficulty:

```markdown
# [Topic] Exercises — [Difficulty]

<!-- difficulty: medium -->
<!-- topic: limits -->

## Exercise 1
[Problem statement]

### Solution
[Full solution, if this is an answer key file]
```

## Adding past exams

Place exam files in `content/exams/`. Include the answer key in the same file or a companion file named `<exam>-answers.md`.

## Tips

- More content = better search results. Add as much as you can.
- Keep each file focused on one topic for cleaner search snippets.
- Use headers (`##`, `###`) liberally — they help the AI structure its answers.
