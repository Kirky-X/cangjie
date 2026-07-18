# Output Skeletons

Output skeletons for each template family (section structure + field prompts). When generating the final output, populate according to the selected template's `required_sections`.

> The original single file has been split by family (the single file previously exceeded 500 lines). Load the relevant family as needed.

## Index by Family

- **[Learning Family](skeletons-learning.md)** — Course notes, tutorial playbooks, book summaries (nonfiction/fiction), lecture summaries, concept explainers
- **[Media Family](skeletons-media.md)** — Podcast interviews, video programs, event recaps, content highlights, speech summaries
- **[Meeting Family](skeletons-meeting.md)** — Decision minutes, discussion minutes, interview records, 1-on-1 notes, co-creation workshops
- **[Business Family](skeletons-business.md)** — Project status, weekly reports, executive briefs, incident reports, action trackers
- **[Analysis Family](skeletons-analysis.md)** — Research briefs, paper summaries (general/theoretical/experimental/systems/survey), decision memos, theme synthesis, competitive scans

> Product documentation family: skeletons can be found directly in the artifact template documents under `../../templates/Product/` (artifact templates, not guidance skeletons). See [templates-index.md](../templates-index.md) for the index.

## Usage

1. Look up the template's `required_sections` in `references/registry.yaml`
2. Open the corresponding family file and locate the `### <Template ID>` section
3. Populate according to the skeleton sections, following SKILL.md's Output Rules and [detail-policy.md](detail-policy.md)
