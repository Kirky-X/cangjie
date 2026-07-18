# Reference Template System

This directory defines the template system for the content summarization skill. The goal is not to store a large collection of isolated Markdown files, but to provide a structured template library that supports auto-selection, manual override, and continuous expansion.

## Directory Overview

```text
references/
  README.md
  registry.yaml             # Template registry (all template IDs + required_sections + detection_signals)
  taxonomy.yaml             # Template taxonomy (goals + signal_words + default_family)
  families/                 # 6 major template family definitions (each with default template + sub-template list + selection_rules)
    learning.yaml
    media.yaml
    meeting.yaml
    business.yaml
    analysis.yaml
    product.yaml
  guides/                   # Template selection / authoring / output skeleton guides
    template-selection.md   # Template selection decision tree
    template-authoring.md   # Template authoring specification
    output-skeletons.md     # Output skeleton index (split by family)
    skeletons-learning.md   # Learning family skeleton
    skeletons-media.md      # Media family skeleton
    skeletons-meeting.md    # Meeting family skeleton
    skeletons-business.md   # Business family skeleton
    skeletons-analysis.md   # Analysis family skeleton
    detail-policy.md        # Output density policy
    examples.md             # Complete example collection
    api-docs.md             # chub tool usage and API documentation fetching
  templates-index.md        # Template index (points to ../templates/)
```

> Complete Markdown document templates have been migrated to `../templates/` (Product layer/Strategy layer/Delivery layer/Operations layer/Technical layer/General), with the index at [templates-index.md](templates-index.md).

## Design Principles

1. User specification takes priority over auto-selection.
2. Templates are grouped by "output goal" rather than by input medium.
3. Duplicate sections within a template family are consolidated, with trimming via `required_sections` and `optional_sections` declarations.
4. A template definition must be usable by both agents and humans.

## Template Family Overview

| Family | Coverage | Default Fallback |
| --- | --- | --- |
| `learning` | Courses, lectures, book learning, tutorials | `learning/course-notes` |
| `media` | Podcasts, programs, livestreams, public video reviews | `media/podcast-summary` |
| `meeting` | Meetings, discussions, interviews, 1:1s, workshops | `meeting/discussion-minutes` |
| `business` | Weekly/monthly reports, project status, management reporting | `business/project-status-report` |
| `analysis` | Research synthesis, paper reading, theme synthesis, decision support | `analysis/research-brief` |
| `product` | Product docs, business plans, technical design, delivery & operations | `product/prd` |

## Current Template Principles

- No backward compatibility with old template names.
- Only use the new template family and template IDs externally.
- When adding new templates, continue naming by "output goal", not reverting to old input-medium naming.

## Paper Template Subtypes

Paper-related templates are now split into 5 types:

- `analysis/paper-summary`
- `analysis/theoretical-paper-summary`
- `analysis/experimental-paper-summary`
- `analysis/systems-paper-summary`
- `analysis/survey-paper-summary`

When auto-selecting, if the paper type can be identified from the content, it should preferentially map to the specific subtype; when identification is unclear, fall back to `analysis/paper-summary`.

## Book Template Subtypes

Book-related templates are now split into 2 types:

- `learning/nonfiction-book-summary`
- `learning/fiction-book-summary`

When auto-selecting, first determine whether the book is non-fiction or narrative. Both default to producing "chapter-by-chapter summary + full book summary"; if the input only covers partial chapters or excerpts, the coverage scope must be explicitly noted.
