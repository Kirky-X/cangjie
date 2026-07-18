# Output Density Policy

> Output density control strategy and compression boundaries. Extracted from SKILL.md to control information density when generating final output.

## Three Density Levels

Default is `standard-detailed` unless the user explicitly requests a shorter version:

- `brief`: Keep only conclusions, a few key points, and minimal necessary action items. Use only when the user explicitly requests a quick-read version.
- `standard-detailed`: Default mode. Covers all required sections with sufficient facts and evidence for each.
- `deep-dive`: Use when the user explicitly requests "detailed breakdown / complete notes / as comprehensive as possible / preserve formulas and experiment details." Increases in-section depth and evidence density.

## Default Retention Strategy by Content Type

- **Learning**: Preserve causal relationships between concepts, examples, terminology definitions, and practice suggestions — not just topic lists.
- **Books**: Default to hierarchical summaries covering both "chapter summaries" and "whole-book summary"; the whole-book summary must not merely concatenate chapter digests but must additionally distill the overarching thesis and structural relationships.
- **Books**: Chapter digests default to individual files; the whole-book file is responsible only for book-level distillation, structural relationships, key arguments, and synthesizing judgments.
- **Media**: Preserve how topics develop, guest disagreements, highlight arguments, and key quotes — not just "what was discussed."
- **Meetings**: Preserve who proposed what, how decisions were reached, unresolved issues, responsible persons, and deadlines.
- **Business**: Preserve the impact behind progress, root causes of risks, metric changes, and priority of next steps.
- **Papers**: Preserve research questions, method details, formulas/models, experiment setup, results evidence, and limitations — do not just rewrite the abstract.

## Compression Boundaries

What can and cannot be compressed during execution:

- Can compress repetitive expressions; cannot compress different viewpoints, different experimental results, or different decision items.
- Can omit decorative statements; cannot omit key evidence that conclusions depend on.
- Can skip minor details; cannot compress "methods, evidence, results, limitations" into a single vague generalization.

## Book Hierarchical Compression Strategy

Book summaries follow these hierarchical compression rules by default:

- Default output format is:
  - `BookTitle-whole-book-summary.md`: Book-level distillation, does not embed complete chapter digests
  - `Chapter-Summaries/NN_ChapterName-Summary.md`: One independent file per chapter
- Unless the user explicitly requests otherwise, do not duplicate "full chapter digest text" into the whole-book file; the whole-book file may contain at most chapter navigation, section overviews, or key chapter index.
- First determine the structural hierarchy: `Whole Book -> Parts/Volumes -> Chapters -> Sections`. If the original book has "Part 1/Part 2/Volumes" mid-level structures, the summary should preserve this layer and not flatten all chapters into a single long list.
- Write "whole-book distillation" first, then "part/chapter-level summaries." Do not substitute chapter digests for the whole-book summary.
- When chapters are numerous, do not require equal length for each. Core chapters, pivotal chapters, and methodology chapters should be more detailed than setup chapters; appendices, acknowledgments, recommendations, and other non-core content should be downgraded to "brief treatment" or excluded from the main summary, but the handling approach must be noted.
- When the chapter count is `> 12`, enable `hierarchical-compression` by default:
  - Each part gets 2-4 bullet point summaries first
  - Each chapter file gets 4-8 high-information-density bullets
  - Whole-book-level chapters remain independent and must not be compressed away
- When the chapter count is `> 20` and the user has not requested ultra-detail, chapter digests should prioritize: core question of the chapter, key arguments/events, and relationship to the whole-book thesis. Do not equally expand all fields in every chapter.
- If the input is a long book but only excerpts are provided, the output must be changed to "hierarchical summary based on provided chapters" and must not masquerade as a complete reading.
- For nonfiction long books, prioritize: the chapter's function in the argument chain; for narrative long books, prioritize: the chapter's function in plot progression and character development.
