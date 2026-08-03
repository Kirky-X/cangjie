# Template Selection Guide

## Decision Order

1. Has the user explicitly specified a template or section?
2. Does the user want to "learn something" or "report something"?
3. Is the input a single source material or a synthesis of multiple sources?
4. Are there strong signals like decisions, action items, metrics, or trade-offs?
5. When uncertain, fall back to the default template of the corresponding family.

## One-Line Decision Method

- If the goal is "learning" and "review," choose `learning/*`
- If the goal is "content recap" and "highlight sharing," choose `media/*`
- If the goal is "recording discussions" and "tracking accountability," choose `meeting/*`
- If the goal is "reporting upward" or "tracking progress," choose `business/*`
- If the goal is "synthesizing multi-source information to support judgment," choose `analysis/*`
- If the goal is "understanding a paper," prefer `analysis/paper-summary`
- If the goal is "summarizing a book," first decide between `learning/nonfiction-book-summary` and `learning/fiction-book-summary`
- If the goal is "writing product documentation" or "creating a business plan," choose `product/*`
- If the goal is "writing a technical specification" or "designing architecture," choose `product/trd` or `product/architecture`
- If the goal is "formally archived detailed meeting minutes" (with ACTION numbers, Parking Lot), choose `product/meeting-minutes-detailed`
- If the goal is "literature review that builds an evaluative framework" (with PRISMA, scenario-based recommendations), choose `product/literature-review`

## Common Ambiguities

### Course Video vs Product Demo

- Goal is for the reader to master knowledge: `learning/course-notes`
- Goal is for the reader to follow along and perform tasks: `learning/tutorial-playbook`
- Goal is to recap program content, not to teach: `media/video-program-summary`

### Course Notes vs Book Summary

- Focus is on courses, bootcamps, or lecture content: `learning/course-notes`
- Focus is on the structure, arguments, and chapter-by-chapter content of a non-fiction book: `learning/nonfiction-book-summary`
- Focus is on the characters, plot, and themes of a novel or narrative work: `learning/fiction-book-summary`

### Podcast Interview vs Interview Record

- Aimed at content consumption and viewpoint extraction: `media/podcast-summary`
- Aimed at research input and Q&A organization: `meeting/interview-record`

### Meeting Minutes vs Project Report

- Focus is on discussion process, decisions, and action items: `meeting/decision-minutes`
- Focus is on phase progress, metrics, and risks: `business/project-status-report`

### Multi-Source Synthesis

- Focus is on common themes: `analysis/theme-synthesis`
- Focus is on making a choice: `analysis/decision-memo`
- Focus is on industry and factual scanning: `analysis/research-brief`

### Paper Reading

- Want to know research topic, method, formulas, experiments, and limitations: `analysis/paper-summary`
- If the paper is just one component among multiple evidence sources, consider switching to `analysis/research-brief` or `analysis/theme-synthesis`

### Book Summary

- Non-fiction, methodology, business, psychology, history, popular science: `learning/nonfiction-book-summary`
- Novels, literature, narrative works: `learning/fiction-book-summary`
- Default output should include "chapter-by-chapter summary + full-book summary," unless the user explicitly requests only one layer
- Default output format is "full-book file + standalone chapter files directory," unless the user explicitly requests a single merged file
- If the input only covers selected chapters or excerpts, the summary must state coverage scope at the beginning
- If the original book has a "parts/sections/volumes" structure, the summary preserves this layer by default rather than flattening into a long chapter list
- When there are many chapters, equal-length treatment is not required; prioritize making key chapters more detailed and appendix-like chapters more concise

### Paper Subtype Selection

- If the core is theorems, proofs, convergence, upper/lower bounds: `analysis/theoretical-paper-summary`
- If the core is datasets, experimental metrics, benchmarks, ablations: `analysis/experimental-paper-summary`
- If the core is system architecture, throughput, latency, scalability, deployment: `analysis/systems-paper-summary`
- If the core is classification frameworks, literature review, research threads, gaps: `analysis/survey-paper-summary`
- If no clear subtype is apparent: `analysis/paper-summary`

### Product Documentation Sub-type Selection

- Business plan, fundraising pitch: `product/business-plan`
- Business model, value proposition, revenue path: `product/business-model`
- Business requirements, project initiation, strategic layer: `product/brd`
- Market research, industry analysis: `product/market-research`
- Market requirements, product planning: `product/mrd`
- Competitive analysis, competitive landscape, differentiation: `product/competitive-analysis`
- Project kickoff, charter: `product/charter`
- Product requirements, feature design: `product/prd`
- Feature requirements refinement: `product/frd`
- UI/UX specifications, color system: `product/uiux-spec`
- Technical specification, architecture selection: `product/trd`
- System architecture, module design: `product/architecture`
- Database design, table structure: `product/db-design`
- Core algorithm documentation: `product/algorithm-doc`
- Release plan, launch schedule: `product/release-plan`
- Test report, quality report: `product/test-report`
- Canary release, phased rollout: `product/canary-plan`
- Data dashboard, metrics framework: `product/dashboard`
- User manual, usage guide: `product/user-guide`
- Operations manual, operational procedures: `product/operation-guide`
- When uncertain about sub-type: `product/prd`

### Competitive Analysis vs Competitive Scan

- Aimed at product decisions, includes differentiation strategy and moats: `product/competitive-analysis`
- Aimed at research synthesis, lightweight peer comparison: `analysis/competitive-scan`

### Detailed Meeting Minutes vs Standard Decision Minutes

- Requires formal archiving, includes ACTION/RISK numbers, Parking Lot, FAR principle: `product/meeting-minutes-detailed`
- Quick recording of decisions and action items: `meeting/decision-minutes`

### Literature Review Report vs Survey Paper Summary

- Requires building an evaluative framework, includes PRISMA process, scenario-based recommendations: `product/literature-review`
- Summarizing a single survey paper's classification framework: `analysis/survey-paper-summary`

## What to Communicate When Confirming with the User

At minimum, explain three things:

1. The selected template ID
2. Core sections
3. Why it is a better fit than adjacent templates

Example:

> I recommend `meeting/decision-minutes` because your content has clear decisions, action owners, and deadlines. The core sections will include discussion summary, decisions, action items, and risks. If you'd prefer speaker-organized views, I can switch to `meeting/discussion-minutes`.
