# Template Authoring Guide

When adding or modifying templates, follow these constraints.

## Required Fields

- `id`
- `family`
- `label`
- `best_for`
- `input_modalities`
- `detection_signals`
- `anti_signals`
- `required_sections`
- `optional_sections`

## Authoring Rules

1. First check whether existing templates can be reused; do not add new ones lightly.
2. New templates must belong to a clearly defined template family.
3. Repeated sections should be placed in `section_library` rather than duplicating the same descriptions across multiple templates.
4. `required_sections` should only include sections that must appear in that template.
5. `optional_sections` should include sections that depend on the content; do not pad them just for completeness.
6. `detection_signals` should use user language and content signals, not just abstract labels.
7. `anti_signals` are used to exclude adjacent templates that could be easily misidentified.
8. When modifying a template, simultaneously check `registry.yaml`, `taxonomy.yaml`, and `SKILL.md`.

## Pre-Addition Self-Check

- Is the distinction from existing templates sufficiently clear?
- Are there stable identification signals?
- Is there a clear fallback or adjacent alternative template?
- Is a new template truly needed, rather than just adding optional sections to an existing one?
