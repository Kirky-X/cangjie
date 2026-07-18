# Template Selection Guide

## Decision Sequence

1. Has the user explicitly specified a template or sections?
2. Is the user trying to "learn something" or "report something"?
3. Is the input a single material or a synthesis of multiple materials?
4. Are there strong signals such as decisions, action items, metrics, or trade-offs?
5. When uncertain, fall back to the default template of the corresponding family.

## Quick One-Liner Rules

- If the goal is "learning" and "review," choose `learning/*`
- If the goal is "content review" and "highlight dissemination," choose `media/*`
- If the goal is "record discussion" and "track accountability," choose `meeting/*`
- If the goal is "report upward" or "track progress," choose `business/*`
- If the goal is "synthesize multi-source information to support judgment," choose `analysis/*`
- If the goal is "understand a paper," prefer `analysis/paper-summary`
- If the goal is "summarize a book," first choose between `learning/nonfiction-book-summary` and `learning/fiction-book-summary`
- If the goal is "write product documentation" or "create a business plan," choose `product/*`
- If the goal is "write a technical proposal" or "design architecture," choose `product/trd` or `product/architecture`
- If the goal is "formally archived detailed meeting minutes" (with ACTION numbers, Parking Lot), choose `product/meeting-minutes-detailed`
- If the goal is "literature review for building an evaluative framework" (with PRISMA, scenario-based recommendations), choose `product/literature-review`

## Common Ambiguities

### Course Video vs Product Demo

- Want readers to master knowledge: `learning/course-notes`
- Want readers to follow along operationally: `learning/tutorial-playbook`
- Want to review show content rather than teach: `media/video-program-summary`

### Course Notes vs Book Summary

- Focus is on courses, bootcamps, instructional content: `learning/course-notes`
- Focus is on an entire nonfiction book's structure, arguments, chapter-by-chapter content: `learning/nonfiction-book-summary`
- Focus is on an entire novel or narrative work's characters, plot, themes: `learning/fiction-book-summary`

### Podcast Interview vs Interview Record

- For content consumption and viewpoint extraction: `media/podcast-summary`
- For research input and Q&A organization: `meeting/interview-record`

### Meeting Minutes vs Project Report

- Focus is on discussion process, decisions, action items: `meeting/decision-minutes`
- Focus is on phase progress, metrics, risks: `business/project-status-report`

### Multi-Material Summary

- Focus is on common themes: `analysis/theme-synthesis`
- Focus is on making a choice: `analysis/decision-memo`
- Focus is on industry and factual scanning: `analysis/research-brief`

### Paper Reading

- Want to know research topic, methods, formulas, experiments, and limitations: `analysis/paper-summary`
- If the paper is just one component among multiple evidence materials, consider switching to `analysis/research-brief` or `analysis/theme-synthesis`

### Book Summary

- Nonfiction, methodology, business, psychology, history, popular science: `learning/nonfiction-book-summary`
- Novels, literature, narrative works: `learning/fiction-book-summary`
- Default output includes "chapter summaries + whole-book summary" unless the user explicitly requests only one level
- Default output format is "whole-book file + chapter directory" unless the user explicitly requests a single merged file
- If the input only covers selected chapters or excerpts, the coverage scope must be noted at the beginning
- If the original book has "parts/volumes" structures, the summary preserves this layer by default and does not flatten into a long chapter list
- When chapters are numerous, do not require equal length for each; prioritize making key chapters more detailed and supplementary chapters more concise

### Paper Sub-Type Selection

- Core is theorems, proofs, convergence, bounds: `analysis/theoretical-paper-summary`
- Core is datasets, experimental metrics, benchmarks, ablation: `analysis/experimental-paper-summary`
- Core is system architecture, throughput, latency, scalability, deployment: `analysis/systems-paper-summary`
- Core is classification frameworks, literature review, research threads, gaps: `analysis/survey-paper-summary`
- If no clear sub-type is identifiable: `analysis/paper-summary`

### Product Documentation Sub-Layer Selection

- Business plan, fundraising pitch: `product/business-plan`
- Business model, value proposition, monetization path: `product/business-model`
- Business requirements, project initiation, strategy layer: `product/brd`
- Market research, industry analysis: `product/market-research`
- Market requirements, product planning: `product/mrd`
- Competitive analysis, competitive landscape, differentiation: `product/competitive-analysis`
- Project kickoff, charter: `product/charter`
- Product requirements, feature design: `product/prd`
- Functional requirements detail: `product/frd`
- UIUX specification, color system: `product/uiux-spec`
- Technical proposal, architecture selection: `product/trd`
- System architecture, module design: `product/architecture`
- Database design, table structure: `product/db-design`
- Core algorithm documentation: `product/algorithm-doc`
- Release plan, go-live schedule: `product/release-plan`
- Test report, quality report: `product/test-report`
- Canary release, phased rollout: `product/canary-plan`
- Data dashboard, metrics system: `product/dashboard`
- User manual, usage guide: `product/user-guide`
- Operations manual, operations process: `product/operation-guide`
- When uncertain about sub-layer: `product/prd`

### Competitive Analysis vs Competitive Scan

- For product decisions, including differentiation strategy and moat: `product/competitive-analysis`
- For research synthesis, lightweight peer comparison: `analysis/competitive-scan`

### Detailed Meeting Minutes vs Standard Decision Minutes

- Requires formal archiving, with ACTION/RISK numbers, Parking Lot, FAR principles: `product/meeting-minutes-detailed`
- Quick recording of decisions and action items: `meeting/decision-minutes`

### Literature Review Report vs Survey Paper Summary

- Requires building an evaluative framework, with PRISMA process, scenario-based recommendations: `product/literature-review`
- Summarizing the classification framework of a single survey paper: `analysis/survey-paper-summary`

## When Confirming with the User

At minimum, explain three things:

1. The selected template ID
2. Core sections
3. Why it is more appropriate than adjacent templates

Example:

> I recommend `meeting/decision-minutes` because your content has clear decisions, responsible persons, and deadlines. Core sections will include discussion summary, decisions, action items, and risks. If you'd prefer to see it organized by speaker, I can switch to `meeting/discussion-minutes`.
