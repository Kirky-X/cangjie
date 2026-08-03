# Output Skeletons

Output skeletons (section structure + field hints) for each template family. When generating the final output, populate according to the selected template's `required_sections`.

> The original single file has been split by family (the single file previously exceeded 500 lines). Load the corresponding family as needed.

## Family Index

- **[Learning Family](skeletons-learning.md)** — Course notes, tutorial playbooks, book summaries (non-fiction/fiction), lecture summaries, concept explainers
- **[Media Family](skeletons-media.md)** — Podcast interviews, video programs, event recaps, content highlights, speech summaries
- **[Meeting Family](skeletons-meeting.md)** — Decision minutes, discussion minutes, interview records, 1-on-1 notes, co-creation workshop summaries
- **[Business Family](skeletons-business.md)** — Project status reports, weekly/monthly reports, executive briefs, risk/issue reports, action trackers
- **[Analysis Family](skeletons-analysis.md)** — Research briefs, paper summaries (general/theoretical/experimental/systems/survey), decision memos, theme synthesis, competitive scans

> Product documentation family: skeletons are directly in `../../templates/Product/` under each artifact template document (artifact templates, not guiding skeletons). Index at [templates-index.md](../templates-index.md).

## Usage

1. Look up the template's `required_sections` in `references/registry.yaml`
2. Open the corresponding family file and locate the `### <template ID>` section
3. Fill in according to the skeleton sections, following SKILL.md's Output Rules and [detail-policy.md](detail-policy.md)
