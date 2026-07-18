# Template Authoring Guide

Follow these constraints when adding or modifying templates.

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

1. First check whether an existing template can be reused; do not add new ones hastily.
2. New templates must belong to a clearly defined template family.
3. Repeated sections should be placed in `section_library` rather than duplicating the same descriptions across multiple templates.
4. `required_sections` should only contain sections that must appear in that template.
5. `optional_sections` should contain sections that are "content-dependent"; do not pad for completeness.
6. `detection_signals` should use user language and content signals, not just abstract labels.
7. `anti_signals` are used to exclude adjacent templates that could be easily misidentified.
8. When modifying a template, also check `registry.yaml`, `taxonomy.yaml`, and `SKILL.md`.

## Pre-addition Self-check

- Is the distinction between this template and existing templates sufficiently clear?
- Are there stable identification signals?
- Is there a clear fallback or adjacent alternative template?
- Is a new template truly needed, rather than just adding optional sections to an existing one?
