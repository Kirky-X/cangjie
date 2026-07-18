# Reference Template System

This directory defines the template system for the content summarization skill. The goal is not to store a large collection of isolated Markdown files, but to provide a structured template library that supports automatic selection, manual overrides, and continuous extensibility.

## Directory Overview

```text
references/
  README.md
  registry.yaml             # Template registry (all template IDs + required_sections + detection_signals)
  taxonomy.yaml             # Template taxonomy (goals + signal_words + default_family)
  families/                 # 6 major template family definitions (default template per family + sub-template list + selection_rules)
    learning.yaml
    media.yaml
    meeting.yaml
    business.yaml
    analysis.yaml
    product.yaml
  guides/                   # Template selection / authoring / output skeleton guides
    template-selection.md   # Template selection decision tree
    template-authoring.md   # Template authoring guidelines
    output-skeletons.md     # Output skeleton index (split by family)
    skeletons-learning.md   # Learning family skeletons
    skeletons-media.md      # Media family skeletons
    skeletons-meeting.md    # Meeting family skeletons
    skeletons-business.md   # Business family skeletons
    skeletons-analysis.md   # Analysis family skeletons
    detail-policy.md        # Output density policy
    examples.md             # Complete example set
    api-docs.md             # chub tool usage and API documentation retrieval
  templates-index.md        # Template index (points to ../templates/)
```

> Complete Markdown document templates have been migrated to `../templates/` (product layer / strategy layer / delivery layer / operations layer / technology layer / general). See [templates-index.md](templates-index.md) for the index.

## Design Principles

1. User specification takes priority over automatic selection.
2. Templates are grouped by "output goal," not by input medium.
3. Repeated sections within a template family are consolidated via `required_sections` and `optional_sections` declarations.
4. A template definition must be usable by both agents and humans.

## Template Family Overview

| Template Family | Covered Content | Default Fallback |
| ---------- | ---------------------------------------- | -------------------------------- |
| `learning` | Courses, lectures, book study, tutorial compilation | `learning/course-notes` |
| `media` | Podcasts, shows, livestreams, public video reviews | `media/podcast-summary` |
| `meeting` | Meetings, discussions, interviews, 1:1s, workshops | `meeting/discussion-minutes` |
| `business` | Weekly reports, monthly reports, project status, management briefings | `business/project-status-report` |
| `analysis` | Research synthesis, paper reading, theme synthesis, decision support | `analysis/research-brief` |
| `product` | Product documentation, business plans, technical design, delivery operations | `product/prd` |

## Current Template Principles

- No backward compatibility with old template names.
- Only the new template families and template IDs are used externally.
- When adding new templates, continue naming by "output goal" and do not revert to the old input-medium naming convention.

## Paper Template Types

Paper-related templates are now divided into 5 types:

- `analysis/paper-summary`
- `analysis/theoretical-paper-summary`
- `analysis/experimental-paper-summary`
- `analysis/systems-paper-summary`
- `analysis/survey-paper-summary`

When auto-selecting, if the paper type can be identified from the content, the specific sub-template should be used. If identification is ambiguous, fall back to `analysis/paper-summary`.

## Book Template Types

Book-related templates are now divided into 2 types:

- `learning/nonfiction-book-summary`
- `learning/fiction-book-summary`

When auto-selecting, first determine whether the book is nonfiction or a narrative work. Both default to outputting "chapter summaries + whole-book summary"; if the input only covers selected chapters or excerpts, the coverage scope must be explicitly noted.
