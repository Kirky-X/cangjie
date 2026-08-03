# [Product/System Name (English Name)] - Business Plan (BP)

> **Document Status:** 🟡 Under Review / 🟢 Approved / 🔴 Rejected
>
> **Confidentiality Level:** Confidential / Internal / Public
>
> **Version:** vX.X
>
> **Date:** YYYY-MM-DD
>
> **Author:** [Name/Role]
>
> **Reviewer:** [Name/Role]
>
> **Audience:** [Role List]

---

## 0. Document Guide

### 0.1 Document Purpose and Scope

[Describe the purpose, applicable scenarios, and non-applicable scenarios of this document]

### 0.2 Related Documents

| Document Type | Filename | Related Sections |
|---------|--------|---------|
| [Type] | [Filename] [Line Range] | [Section Description] |

> **Reference Format Note**: Related documents use the `Filename Line Range` format (e.g., `【Template】Technical Requirements Document(TRD).md 3-17`). Line numbers may change as documents are updated; please refer to the actual content.

### 0.3 Change Log

| Version | Date | Reviser | Changes | Reviewer |
| :--- | :--- | :--- | :--- | :--- |
| v0.1 | YYYY-MM-DD | [Name] | Initial draft | [Reviewer] |

---

## 2. Executive Summary

> ⚠️ **Core Principle**: This is the most critical section of the entire BP. Investors use 3-5 minutes to decide whether to continue reading. Keep it to **1-2 pages**, with no more than 3 lines per paragraph.

### 2.1 Investment Highlights
- **Track**: Operating in the [XX] industry, market size of [XX] billion RMB, CAGR of [XX]%
- **Product**: [Product Name], PMF validated, core metrics [XX]
- **Team**: Founders from [top company/prestigious university], previously managed [XX]-scale business
- **Fundraising**: Seeking [XX] million RMB / [XX] million USD in this round, offering [XX]% equity

### 2.2 Project Overview

```mermaid
mindmap
  root((Project Overview))
    Company Info
      Founded:YYYY-MM
      Location:City
      Stage:Angel/Pre-A/Series A
    Core Data
      Users:XX K
      Revenue:XX K/month
      Growth Rate:XX% MoM
    Current Round
      Amount:XX K
      Use of Funds:Product R&D 40% Market Expansion 35% Operations Reserve 25%
```

---

## 3. Pain Points and Market Opportunity

### 3.1 Core Pain Point Analysis

> 💡 **Writing Tip**: Describe pain points using "user's own words," not self-congratulatory descriptions. Prove these are **real needs, high-frequency, with strong willingness to pay**.

| Pain Dimension | Current State | User Cost | Market Gap |
|---------|---------|---------|---------|
| **Low Efficiency** | Traditional methods require [X] hours to complete | Labor cost [XX] RMB/order | No automation tools |
| **Information Silos** | Data scattered across [N] systems | Decision delay [X] days | No unified platform |
| **High Cost** | Existing solutions priced at [XX] K/year | Unaffordable for SMBs | No affordable products |

### 3.2 Market Size and Trends

| Category | Bar Value | Line Value |
|:---|:---:|:---:|
| 2024 | 120 | 120 |
| 2025 | 180 | 180 |
| 2026 | 260 | 260 |
| 2027 | 350 | 350 |
| 2028 | 480 | 480 |

> **Note**: xychart-beta is an incompatible Mermaid type for Feishu; replaced with table descriptions (template sample data).

**Market Data Support**:
- **TAM (Total Addressable Market)**: [XX] billion RMB
- **SAM (Serviceable Addressable Market)**: [XX] billion RMB
- **SOM (Serviceable Obtainable Market)**: [XX] billion RMB (3-year target)

---

## 4. Product and Service Solutions

### 4.1 Product Architecture

```mermaid
graph TB
    subgraph User End
        A[Web Console] --> B[Mobile App]
        A --> C[Mini Program/Lite App]
    end

    subgraph Core Engine
        D[AI Decision Engine] --> E[Real-time Computing Layer]
        E --> F[Data Middle Platform]
    end

    subgraph Infrastructure
        G[Cloud-native Architecture] --> H[Security & Compliance Layer]
        H --> I[Multi-tenant Isolation]
    end

    User End --> Core Engine
    Core Engine --> Infrastructure

    style D fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style E fill:#e1f5fe,stroke:#01579b,stroke-width:2px
```

### 4.2 Product Value Matrix

| Feature Module | Pain Point Solved | Core Advantage | Technical Barrier |
|---------|---------|---------|---------|
| Intelligent Analysis | Slow manual processing | 10x efficiency improvement | Proprietary NLP algorithms |
| Automated Orchestration | Tedious processes | Zero-code configuration | Patented workflow engine |
| Real-time Alerts | Post-hoc remediation | 24h advance alerts | Time-series prediction models |

### 4.3 User Journey and Aha Moment

```mermaid
journey
    title User Experience Journey Map
    section Awareness Phase
      Discover Need: 5: User
      Search Solutions: 4: User
      Compare Competitors: 3: User
    section Experience Phase
      Register Trial: 4: User, Product
      Complete First Order: 5: User, Product
      Realize Value: 5: User, Product
    section Payment Phase
      Choose Plan: 4: User
      Team Expansion: 5: User, Sales
      Renewal/Upgrade: 5: User, Product
```

---

## 5. Business Model and Monetization Path

### 5.1 Business Model Canvas

```mermaid
graph LR
    subgraph bmc[Business Model Canvas]
        KP[Key Partners / Cloud Providers · Channel Partners · ISVs] --> KA[Key Activities / Product R&D · Customer Success · Data Training]
        KR[Key Resources / Tech Team · Data Assets · Brand Trust] --> VP[Value Proposition / Cost Reduction · Intelligent Decisions · Rapid Deployment]
        VP --> CR[Customer Relationships / 1v1 Dedicated · Self-service · Community]
        VP --> CH[Channels / Direct Sales · Online · Ecosystem Cooperation]
        CR --> CS[Customer Segments / SMBs · Mid-to-Large Enterprises]
        CH --> CS
    end
    COST[Cost Structure / R&D 40% · Marketing 35% · Operations 25%] --- REV[Revenue Streams / SaaS Subscription · Value-added Services · Enterprise Customization · Ecosystem Commission]
```

### 5.2 Revenue Model

```mermaid
pie showData
    title Revenue Composition (Target State)
    "SaaS Subscription Fees" : 45
    "Value-added Services/Premium Features" : 25
    "Enterprise Custom Solutions" : 20
    "Ecosystem Commission/Monetization" : 10
```

### 5.3 Unit Economics Model

| Metric | Value | Industry Benchmark | Description |
|-----|------|---------|------|
| **CAC (Customer Acquisition Cost)** | ¥[XX] | ¥[XX] | Including sales + marketing costs |
| **LTV (User Lifetime Value)** | ¥[XX] | ¥[XX] | Calculated over 36 months |
| **LTV/CAC** | [X]:1 | >3:1 Healthy | Return on investment ratio |
| **Monthly Churn Rate** | [X]% | <5% Healthy | Including paid downgrades |
| **Payback Period** | [X] months | <12 months ideal | CAC recovery cycle |

---

## 6. Market Competition and Moat

### 6.1 Competitive Landscape Map

```mermaid
graph TB
    subgraph matrix[Competitive Positioning Matrix: Feature Completeness vs Cost-effectiveness]
        subgraph complete[Feature Complete]
            WE[Us / High cost-effectiveness · Feature complete]
            TA[Traditional Vendor A / Low cost-effectiveness · Feature complete]
        end
        subgraph incomplete[Feature Incomplete]
            LB[Low-price Competitor B / High cost-effectiveness · Feature incomplete]
            NC[Emerging Competitor C / Low cost-effectiveness · Feature incomplete]
        end
        WE --- TA
        LB --- NC
    end
```

### 6.2 Competitive Comparison Analysis

| Comparison Dimension | Us | Competitor A (Traditional) | Competitor B (Emerging) | Competitor C (International) |
|---------|------|---------------|---------------|---------------|
| **Pricing Model** | On-demand Subscription | High annual fees | Free + Premium | Usage-based |
| **Deployment** | 5-minute onboarding | 2-week implementation required | SaaS only | Hybrid cloud |
| **Core Algorithm** | Proprietary/Patented | Open-source | Third-party API | Proprietary |
| **Customer Success** | 1v1 Dedicated | Ticket-based | Community support | Email support |
| **Data Security** | Level 3 Compliance | Level 2 Compliance | No certification | SOC2 |

### 6.3 Moat Construction

```mermaid
graph LR
    subgraph Moat System
        A[Network Effects] --> B[Switching Costs]
        B --> C[Economies of Scale]
        C --> D[Brand Awareness]
        D --> E[Technical Patents]
    end

    subgraph Current Stage
        F[Data Flywheel / More users → Better data → More accurate product]
    end

    Moat System --> F
    style A fill:#c8e6c9,stroke:#2e7d32
    style E fill:#c8e6c9,stroke:#2e7d32
```

---

## 7. Operations Plan and Milestones

### 7.1 Development Stage Roadmap

> **Note**: Gantt charts are incompatible with Feishu; replaced with table descriptions.

| Stage | Task | Start Date | End Date | Duration | Status |
|------|------|----------|----------|------|------|
| Product R&D | MVP Validation | 2024-01 | 2024-06 | 6 months | Completed |
| Product R&D | Core Features V1.0 | 2024-07 | 2024-12 | 6 months | Completed |
| Product R&D | Platform V2.0 | 2025-01 | 2025-06 | 6 months | In Progress |
| Product R&D | Ecosystem V3.0 | 2025-07 | 2025-12 | 6 months | Not Started |
| Market Expansion | Seed Users 100 | 2024-01 | 2024-06 | 6 months | Completed |
| Market Expansion | Industry Benchmarks 10 | 2024-07 | 2024-12 | 6 months | Completed |
| Market Expansion | Scale to 1000 | 2025-01 | 2025-06 | 6 months | In Progress |
| Market Expansion | Overseas/New Industries | 2025-07 | 2025-12 | 6 months | Not Started |
| Team Building | Core Team 10 | 2024-01 | 2024-06 | 6 months | Completed |
| Team Building | Expand to 30 | 2024-07 | 2024-12 | 6 months | Completed |
| Team Building | Expand to 80 | 2025-01 | 2025-06 | 6 months | In Progress |
| Team Building | Expand to 150 | 2025-07 | 2025-12 | 6 months | Not Started |

### 7.2 Key Milestones and KPIs

| Stage | Period | Core Objective | Key Metrics |
|-----|------|---------|---------|
| **Validation** | Completed | PMF Validation | NPS > 40, Retention > 60% |
| **Growth** | Current | Scalable Customer Acquisition | ARR exceeding [XX] K |
| **Expansion** | Next 12 months | Market Penetration | [XX] paying customers |
| **Profitability** | Next 24 months | Positive Cash Flow | Monthly breakeven |

---

## 8. Core Management Team

> 💡 **Investor Perspective**: Early-stage projects are judged by the team, growth-stage by data. Team introduction must be **specific and verifiable**—avoid empty phrases like "10 years of industry experience."

### 8.1 Founding Team

```mermaid
graph TD
    subgraph Core Team
        CEO[CEO/Founder / Name:XXX / Former XX Company VP / Serial Entrepreneur / Managed 100M+ user products]
        CTO[CTO/Co-founder / Name:XXX / Former XX Tech Giant Architect / 10 years distributed systems experience / X technical patents]
        COO[COO/Co-founder / Name:XXX / Former XX Consulting Partner / Expert in B2B scaling / Led XX billion annual revenue business]
    end

    subgraph Advisory Team
        ADV1[Strategic Advisor / XX Fund Partner]
        ADV2[Technical Advisor / XX University Professor/Academician]
    end

    CEO --> CTO
    CEO --> COO
    ADV1 --> CEO
    ADV2 --> CTO

    style CEO fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style CTO fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style COO fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

### 8.2 Team Background and Responsibilities

| Position | Name | Core Resume | Responsibilities | Full-time/Part-time |
|-----|------|---------|---------|----------|
| CEO | [Name] | [Top Company] [X] years, [Specific Achievements] | Strategy/Fundraising/Product | Full-time |
| CTO | [Name] | [Prestigious University] [Major], [Patents/Publications] | Technology/R&D | Full-time |
| CMO | [Name] | [Notable Cases], [Channel Resources] | Marketing/Brand | Full-time |
| Sales VP | [Name] | [Industry Customer Resources], [Track Record] | Commercialization/Customer Success | Full-time |

---

## 9. Financial Projections and Fundraising Needs

### 9.1 Historical and Projected Financial Data

**Revenue Projections**:

| Category | Bar Value | Line Value |
|:---|:---:|:---:|
| 2023 | 50 | 50 |
| 2024 | 300 | 300 |
| 2025E | 1,200 | 1,200 |
| 2026E | 3,500 | 3,500 |
| 2027E | 8,000 | 8,000 |

**Net Profit Projections**:

| Category | Bar Value | Line Value |
|:---|:---:|:---:|
| 2023 | -200 | -200 |
| 2024 | -500 | -500 |
| 2025E | -300 | -300 |
| 2026E | 500 | 500 |
| 2027E | 2,000 | 2,000 |

> **Note**: xychart-beta is an incompatible Mermaid type for Feishu; replaced with table descriptions (template sample data).

### 9.2 Financial Projection Table (Next 3-5 Years)

| Metric (10K RMB) | 2024 Actual | 2025 Projected | 2026 Projected | 2027 Projected |
|------------|----------|----------|----------|----------|
| **Operating Revenue** | [XX] | [XX] | [XX] | [XX] |
| **Gross Profit** | [XX] | [XX] | [XX] | [XX] |
| **Gross Margin** | [XX]% | [XX]% | [XX]% | [XX]% |
| **Operating Expenses** | [XX] | [XX] | [XX] | [XX] |
| **Net Profit** | [XX] | [XX] | [XX] | [XX] |
| **Net Margin** | [XX]% | [XX]% | [XX]% | [XX]% |

### 9.3 Fundraising Needs and Use of Funds

```mermaid
pie showData
    title This Round [XX] K RMB Fund Allocation
    "Product R&D (40%)" : 40
    "Marketing & Sales (35%)" : 35
    "Operations & Infrastructure (15%)" : 15
    "Talent & Reserve (10%)" : 10
```

**Fundraising Details**:
- **Round**: [Angel/Pre-A/Series A/B] Round
- **Amount**: [XX] million RMB / [XX] million USD
- **Equity Offered**: [XX]%
- **Pre-money Valuation**: [XX] million RMB (based on [XX]x ARR or [XX]x PS)
- **Use of Funds**:
  - Product R&D: [XX] K (40%) — Core algorithm optimization, V2.0 platform development
  - Market Expansion: [XX] K (35%) — Sales team building, brand advertising, channel development
  - Operations Reserve: [XX] K (15%) — Cloud resources, compliance certification, office space
  - Talent Acquisition: [XX] K (10%) — Key position recruitment, option pool replenishment

---

## 10. Risk Analysis and Mitigation Strategies

### 10.1 SWOT Analysis

```mermaid
graph TB
    subgraph swot[SWOT Strategic Analysis]
        subgraph positive[Positive Factors]
            S[Strengths / Technology leadership · Complete team]
            O[Opportunities / Policy tailwinds · Market growth]
        end
        subgraph negative[Negative Factors]
            W[Weaknesses / Brand newly established · Limited capital]
            T[Threats / Big Tech entry · Economic downturn]
        end
        S --- W
        O --- T
    end
```

### 10.2 Core Risks and Mitigation Plans

| Risk Type | Specific Description | Probability | Impact | Mitigation Strategy |
|---------|---------|---------|---------|---------|
| **Market Risk** | Big Tech rapid follow-up, price war | Medium | High | Deep vertical focus, build data barrier |
| **Technology Risk** | Core algorithm underperformance | Low | High | Dual technology routes, prepare Plan B |
| **Operational Risk** | Key talent loss | Medium | Medium | Comprehensive equity incentives, knowledge documentation |
| **Financial Risk** | Fundraising environment deterioration | Medium | High | Control burn rate, maintain 18-month runway |
| **Compliance Risk** | Data regulation policy changes | Low | Medium | Proactive compliance/ISO applications, legal first |

---

## Appendix

> The following can be organized as separate appendix documents for deep due diligence review.

1. **Detailed Financial Model** (Excel): 3-5 year complete three-statement projections and assumptions
2. **Product Demo Video/Demo**: Core feature operation flow
3. **Customer Testimonials/Case Studies**: [Benchmark customer] before/after comparison data
4. **Intellectual Property List**: Patents, software copyrights, trademarks
5. **Detailed Team Resumes**: Complete backgrounds of core members
6. **Industry Research Reports**: Third-party authoritative data sources

---

## Writing Checklist (Pre-submission Self-Check)

| Check Item | Status | Description |
|-------|------|------|
| Is the one-liner value proposition clear? | ☐ | Understandable to non-industry people |
| Are pain points described in user's own words? | ☐ | Avoid self-congratulatory expressions |
| Are market data from authoritative sources? | ☐ | Cite iResearch/IDC/Government reports |
| Is the business model clear on how it makes money? | ☐ | Revenue sources, pricing, cost structure |
| Is the competitive analysis objective? | ☐ | Don't disparage competitors, highlight differentiation |
| Are financial projections reasonable? | ☐ | Avoid "1 billion profit in one year" |
| Is the fundraising amount and use of funds clear? | ☐ | 33% of BPs fail here |
| Is contact information complete? | ☐ | Founder's phone + WeChat + email |

---

> 📧 **Contact Information**
> - Founder: [Name]
> - Phone: [Number]
> - WeChat: [WeChat ID]
> - Email: [email@company.com]
> - Company Website: [www.company.com]

---

### 💡 Usage Suggestions

1. **Version Management**: Prepare three versions
   - **1-page Executive Summary** (PDF, for initial email outreach)
   - **12-15 page Presentation Version** (PPT/Markdown, for roadshows)
   - **30-50 page Full Version** (Word/Markdown, for deep due diligence)

2. **Charts First**: Every page must have at least 1 chart or data point, with no more than 100 words of text.

3. **Data Authenticity**: All projections based on verifiable assumptions. Prepare Excel workbooks for follow-up questions.

4. **Customized Modifications**: Adjust emphasis for different investor types—financial VCs look at growth data, strategic investors look at synergy value.
