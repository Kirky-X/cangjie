# Output Density Policy

> Output density control strategy and compression boundaries. Extracted from SKILL.md; use this to control information density when generating final output.

## Three Density Levels

Use `standard-detailed` by default, unless the user explicitly requests shorter:

- `brief`: Keep only conclusions, a few key points, and minimal necessary action items. Use only when the user explicitly asks for a quick-read version.
- `standard-detailed`: Default mode. Cover all required sections, retaining sufficient facts and evidence for each section.
- `deep-dive`: Use when the user explicitly requests "detailed breakdown / complete notes / as comprehensive as possible / preserve formulas and experimental details." Increase section depth and evidence density.

## Default Retention Policies by Content Type

- **Learning**: Preserve causal relationships between knowledge points, examples, terminology definitions, and practice suggestions — not just topic lists.
- **Book**: By default, produce hierarchical summaries; at minimum cover both "chapter-by-chapter summary" and "full-book summary." The full-book summary must not be a simple concatenation of chapter summaries — it must additionally distill the book's main thread and structural relationships.
- **Book**: Chapter summaries default to standalone files; the full-book file is responsible only for book-level distillation, structural relationships, key arguments, and synthesized judgments.
- **Media**: Preserve how topics develop, guest disagreements, highlight arguments, and key quotes — not just "what was discussed."
- **Meeting**: Preserve who proposed what, how the discussion converged to decisions, open issues, action owners, and deadlines.
- **Business**: Preserve the impact behind progress, root causes of risks, metric changes, and the priority of next actions.
- **Paper**: Preserve research questions, method details, formulas/models, experimental setup, result evidence, and limitations — do not just rewrite the abstract.

## Compression Boundaries

What can and cannot be compressed during execution:

- Can compress repetitive expressions, but cannot compress different viewpoints, different experimental results, or different decision items.
- Can omit decorative sentences, but cannot omit key evidence that conclusions depend on.
- Can skip some fine-grained details, but cannot compress "method, evidence, results, limitations" into a single vague generalization.

## Book Hierarchical Compression Strategy

Book summaries follow these hierarchical compression rules by default:

- Output format is by default:
  - `BookTitle-FullSummary.md`: Book-level distillation, no embedded chapter summaries.
  - `ChapterSummaries/NN_ChapterName-Summary.md`: Standalone file per chapter.
- Unless the user specifically requests otherwise, do not repeat full chapter summary text in the full-book file; the full-book file should retain at most chapter navigation, part overviews, or key chapter indices.
- Determine the structural hierarchy first: `Book → Parts/Sections → Chapters → Subsections`. If the original book has a mid-level structure like "Part 1/Part 2/Sections/Volumes," the summary should preserve this layer rather than flattening all chapters into a single long list.
- Write "book-level distillation" first, then "part/chapter-level summaries." Never use chapter summaries as a substitute for the book-level summary.
- When there are many chapters, do not require equal length per chapter. Core chapters, pivotal chapters, and method chapters should be more detailed than setup chapters; appendices, acknowledgments, and endorsements are downgraded to "brief mention" or excluded from the main summary, but note the treatment.
- When the chapter count is `> 12`, enable `hierarchical-compression` by default:
  - Each part gets `2–4` part-level summary bullets.
  - Each chapter's standalone file gets `4–8` high-information bullets.
  - Book-level chapter entries remain standalone and must not be compressed away.
- When the chapter count is `> 20` and the user has not requested ultra-detailed output, chapter summaries should prioritize: this chapter's core question, key arguments/events, and relationship to the book's main thread. Do not evenly expand all fields in every chapter.
- If the input is a long book but only excerpts are provided, the output must be changed to "hierarchical summary based on available chapters" and must not pretend to be a complete book reading result.
- For non-fiction long works, prioritize: the chapter's function in the argumentative chain; for narrative long works, prioritize: the chapter's function in plot progression and character development.
