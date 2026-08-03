# [Team/Individual Name] - Weekly / Monthly Report

> **Document Status:** 🟢 Published / 🟡 Draft
>
> **Confidentiality Level:** Confidential / Internal / Public
>
> **Version:** vX.X
>
> **Report Period:** {YYYY-W## / YYYY-MM}
>
> **Report Type:** 🟢 Weekly / 🟡 Monthly
>
> **Author:** [Name / Role]
>
> **Team:** [Team Name / Department]
>
> **Reporting To:** [Direct Manager / Team / Cross-team Sync]
>
> **Submission Time:** YYYY-MM-DD HH:MM
>
> **Related Documents:** [Previous Week/Month Report](./Previous Report Link) / [OKR](./OKR Link) / [Project Board](./Board Link)

---

## 0. Document Guide

### 0.1 Document Purpose & Scope

**Weekly/Monthly Report answers:** "What was done this period, how's the progress, what are the blockers, and what's planned next" — a regular sync tool for teams and individuals.

**Applicable Scenarios:**

- ✅ Individual weekly / monthly reports
- ✅ Team weekly / monthly reports
- ✅ Department regular reporting
- ✅ Cross-team progress sync
- ❌ Project retrospective (use Retrospective Report)
- ❌ Performance summary (use performance process)
- ❌ Detailed technical design (use TRD)

### 0.2 Writing Principles

| Principle | Description |
| :--- | :--- |
| **Results-Oriented** | Describe deliverables and impact, not a daily log |
| **Data-Driven** | Use numbers, avoid "roughly done" |
| **Risks Visible** | Blockers and risks must be explicitly exposed, not hidden |
| **Conciseness First** | Single weekly report ≤ 1 page, monthly report ≤ 2 pages |
| **Traceable** | Link to OKR / Project / Issue for future reference |

### 0.3 Report Structure Alignment

> This template's chapter structure aligns with the `business/weekly-monthly-report` definition in `cangjie/references/registry.yaml`:
>
> - **Required Sections**: report_info / summary / completed_work / in_progress / blockers / next_period_plan
> - **Optional Sections**: metrics / asks / reflections

| Template Section | Registry Field | Required |
| :--- | :--- | :--- |
| §1 Report Info | `report_info` | ✅ |
| §2 Period Summary | `summary` | ✅ |
| §3 Completed Work | `completed_work` | ✅ |
| §4 Work In Progress | `in_progress` | ✅ |
| §5 Blockers & Risks | `blockers` | ✅ |
| §6 Next Period Plan | `next_period_plan` | ✅ |
| §7 Data Metrics | `metrics` | ⚪ Optional |
| §8 Support Needed | `asks` | ⚪ Optional |
| §9 Reflections | `reflections` | ⚪ Optional |

### 0.4 Change Log

| Version | Date | Author | Changes | Reviewer |
| :--- | :--------- | :--- | :--- | :--- |
| v0.1 | YYYY-MM-DD | [Name] | Initial draft: basic structure | [Name] |
| v0.2 | YYYY-MM-DD | [Name] | Aligned with registry required_sections | [Name] |
| v1.0 | YYYY-MM-DD | [Name] | Review passed | [Owner] |

---

## 1. Report Info

| Element | Content |
| :--- | :--- |
| **Report Period** | {2026-W27 / 2026-07} |
| **Date Range** | {2026-07-01 ~ 2026-07-05} |
| **Report Type** | 🟢 Weekly / 🟡 Monthly |
| **Author** | [Name / Role] |
| **Team** | [Team / Department] |
| **Reporting To** | [Manager / Cross-team] |
| **Core Objectives** | [e.g., Q3 OKR progress + User Center v2.0 launch] |
| **Overall Status** | 🟢 On Track / 🟡 At Risk / 🔴 Significantly Behind |

---

## 2. Period Summary

> **30-Second Read:** The top 3 things this period + overall progress + biggest risk. **A manager can grasp the full picture by reading only this section.**

### 2.1 Key Results (Top 3)

1. **{Key Result 1}**: [e.g., User Center v2.0 canary released to 30%, core metrics stable]
2. **{Key Result 2}**: [e.g., Performance optimization P99 from 800ms to 200ms]
3. **{Key Result 3}**: [e.g., Completed onboarding for 2 new hires]

### 2.2 Overall Progress

| Objective | Progress | Status | Notes |
| :--- | :--- | :--- | :--- |
| OKR-1: Conversion Rate Improvement | 75% | 🟢 On Track | [One-line note] |
| OKR-2: SLO Compliance | 60% | 🟡 At Risk | [One-line note] |
| OKR-3: Team Building | 90% | 🟢 Ahead | [One-line note] |

### 2.3 Biggest Risks

| Risk | Level | Mitigation |
| :--- | :--- | :--- |
| {Risk 1} | 🔴 High | [Mitigation measure] |
| {Risk 2} | 🟡 Medium | [Mitigation measure] |

---

## 3. Completed Work

> **Methodology**: Categorized by project / theme. Each item includes "deliverable + quantified result + related link". **Not a daily log.**

### 3.1 Project Deliveries

| Work Item | Type | Deliverable | Quantified Result | Related Link |
| :--- | :--- | :--- | :--- | :--- |
| {Work Item 1} | Development | [e.g., User Center v2.0 module] | [e.g., 5k lines of code / 85% test coverage] | [PR/Issue] |
| {Work Item 2} | Review | [e.g., Architecture design review] | [e.g., Passed + 2 improvements] | [Document Link] |
| {Work Item 3} | Documentation | [e.g., API documentation] | [e.g., 12 endpoints] | [Document Link] |

### 3.2 Technical Contributions

- **{Contribution 1}**: [e.g., Fixed 5 production bugs, including 1 P1]
- **{Contribution 2}**: [e.g., Performance optimization, QPS +30%]
- **{Contribution 3}**: [e.g., Code Review 8 times, 12 actionable suggestions]

### 3.3 Collaboration & Meetings

| Meeting / Collaboration | Role | Output | Duration |
| :--- | :--- | :--- | :--- |
| {Meeting 1} | Facilitator / Participant | [e.g., Decision minutes] | 1h |
| {Meeting 2} | Participant | [e.g., Plan alignment] | 30min |

### 3.4 Learning & Growth

- **{Learning 1}**: [e.g., Completed Rust async programming training]
- **{Learning 2}**: [e.g., Read Chapter 5 of "Designing Data-Intensive Applications"]
- **{Sharing 1}**: [e.g., Team sharing on "Canary Release Best Practices"]

---

## 4. Work In Progress

> **Methodology**: Each item includes "current progress + estimated completion date + blocker".

| Work Item | Current Progress | Estimated Completion | Blocker | Owner |
| :--- | :--- | :--- | :--- | :--- |
| {Work Item 1} | 80% | YYYY-MM-DD | [e.g., Waiting for third-party API] | [Name] |
| {Work Item 2} | 50% | YYYY-MM-DD | — | [Name] |
| {Work Item 3} | 30% | YYYY-MM-DD | [e.g., Test environment unavailable] | [Name] |

---

## 5. Blockers & Risks

> **Methodology**: Blockers must be explicitly exposed. **Hidden blockers always become incidents.**

### 5.1 Blockers

| # | Blocker Description | Affected Work | Impact | Attempted Solutions | Support Needed |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | [e.g., Third-party API test environment unavailable] | [e.g., Order module integration] | 🔴 High | [e.g., Contacted them 3 times] | [e.g., Manager help] |
| 2 | [e.g., Test environment DB quota insufficient] | [e.g., Performance testing] | 🟡 Medium | [e.g., Request submitted] | [e.g., DBA expedite] |

### 5.2 Risk Alerts

| # | Risk Description | Probability | Impact | Response Plan | Owner |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | [e.g., Launch may be delayed 1 week] | 🟡 Medium | 🔴 High | [e.g., Compress test cycle / Add manpower] | [Name] |
| 2 | [e.g., Third-party dependency stability declining] | 🟢 Low | 🟡 Medium | [e.g., Fallback + monitoring] | [Name] |

---

## 6. Next Period Plan

> **Methodology**: Each item includes "objective + expected deliverable + linked OKR".

### 6.1 Key Objectives

| Work Item | Objective | Expected Deliverable | Linked OKR | Priority |
| :--- | :--- | :--- | :--- | :--- |
| {Work Item 1} | [e.g., Launch] | [e.g., User Center v2.0 100% canary] | OKR-1 | P0 |
| {Work Item 2} | [e.g., Development] | [e.g., Order module 80%] | OKR-2 | P0 |
| {Work Item 3} | [e.g., Research] | [e.g., Tech selection report] | OKR-3 | P1 |

### 6.2 Key Milestones

| Date | Milestone | Acceptance Criteria |
| :--- | :--- | :--- |
| YYYY-MM-DD | [e.g., User Center v2.0 launch] | [e.g., 100% canary + no alerts] |
| YYYY-MM-DD | [e.g., Performance optimization complete] | [e.g., P99 ≤ 200ms] |

---

## 7. Data Metrics ⚪ Optional

> **Methodology**: Use data, compare with previous period, annotate trends.

### 7.1 Business Metrics

| Metric | Previous Period | Current Period | Change | Target | Achievement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| DAU | 12,000 | 13,500 | +12.5% | 15,000 | 🟡 90% |
| Conversion Rate | 5.2% | 6.1% | +0.9pp | 8% | 🟡 76% |
| Retention (Next-day) | 35% | 38% | +3pp | 45% | 🟡 84% |

### 7.2 Technical Metrics

| Metric | Previous Period | Current Period | Change | Target | Achievement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SLO | 99.85% | 99.92% | +0.07pp | 99.95% | 🟡 99.97% |
| P99 Latency | 350ms | 220ms | -37% | 200ms | 🟡 91% |
| Error Rate | 0.05% | 0.02% | -60% | 0.01% | 🟡 50% |

### 7.3 Team Metrics

| Metric | Previous Period | Current Period | Change | Target |
| :--- | :--- | :--- | :--- | :--- |
| PR Merges | 25 | 32 | +28% | — |
| Test Coverage | 78% | 82% | +4pp | 80% |
| Code Review Count | 45 | 52 | +16% | — |
| Bugs (Production) | 8 | 5 | -38% | ≤ 5 |

---

## 8. Support Needed ⚪ Optional

> **Methodology**: Clearly state requests for quick response from managers and collaborators.

| # | Request Description | Target | Expected Time | Urgency | Current Status |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | [e.g., Coordinate DBA to expedite quota handling] | [Manager] | YYYY-MM-DD | 🔴 Urgent | ⚪ Pending |
| 2 | [e.g., Invite architect for design review] | [Architect] | YYYY-MM-DD | 🟡 High | ⚪ Pending |
| 3 | [e.g., Add 1 person for testing support] | [Manager] | YYYY-MM-DD | 🟡 High | 🟢 Confirmed |

---

## 9. Reflections ⚪ Optional

> **Methodology**: What was learned, what went wrong, and how to improve next time. **Unrecorded repetitive work = waste.**

### 9.1 Lessons Learned

- **{Lesson 1}**: [e.g., Canary releases must follow SOP; skipping steps amplifies anomalies]
- **{Lesson 2}**: [e.g., Third-party dependencies must be coordinated 1 week in advance to avoid last-minute blockers]

### 9.2 What Went Wrong

- **{Issue 1}**: [e.g., Estimation was significantly off; planned 5 days actually took 8]
- **{Issue 2}**: [e.g., Communication not timely enough, causing downstream team to wait]

### 9.3 Improvements for Next Time

- **{Improvement 1}**: [e.g., Apply 1.3x historical deviation factor during estimation]
- **{Improvement 2}**: [e.g., Daily progress sync to avoid downstream blockers]

### 9.4 Knowledge Capture

| Item | Type | Location |
| :--- | :--- | :--- |
| [e.g., Canary SOP v1.0] | SOP | [Knowledge Base Link] |
| [e.g., Third-party Integration Checklist] | Checklist | [Knowledge Base Link] |

---

## 10. Appendix

### 10.1 Detailed Work Log

> Complete work log (if needed) can be placed in the appendix. Omitted in regular weekly reports.

| Date | Work Content | Duration | Output |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD | {Content} | 4h | {Output} |
| YYYY-MM-DD | {Content} | 6h | {Output} |

### 10.2 Related Documents

- [Previous Week/Month Report](./Previous Report Link)
- [OKR Progress](./OKR Link)
- [Project Board](./Board Link)
- [Retrospective Report](./Retrospective Report Link)

---

## 📌 Weekly/Monthly Report Writing Checklist

- [ ] §1 Report Info: Period / Type / Author / Overall Status
- [ ] §2 Period Summary: Top 3 Key Results + Overall Progress + Biggest Risk
- [ ] §3 Completed Work: Categorized by project, with deliverables and quantified results
- [ ] §4 Work In Progress: With progress / estimated completion / blockers
- [ ] §5 Blockers & Risks: Blockers explicitly exposed + risk alerts
- [ ] §6 Next Period Plan: With objectives / expected deliverables / linked OKR
- [ ] §7 Data Metrics (Optional): Business / Technical / Team, with previous period comparison
- [ ] §8 Support Needed (Optional): Clear request + target + expected time
- [ ] §9 Reflections (Optional): Lessons / Improvements / Knowledge capture
- [ ] Single weekly report ≤ 1 page, monthly report ≤ 2 pages
- [ ] Data-driven, avoid "roughly" / "approximately"
- [ ] OKR / Project / Issue links complete
- [ ] Blockers are visible, not hidden
- [ ] Chapter structure aligns with registry `business/weekly-monthly-report` definition
