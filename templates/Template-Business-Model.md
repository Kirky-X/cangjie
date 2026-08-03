# [Product/System Name (English Name)] - Business Model Document

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
>
> **Core Objective**: Clearly articulate the complete loop of "how to create, deliver, and capture value"

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

## 2. Business Model Overview

### 2.1 One-liner Business Model

> **We** provide **[Value Proposition]** to **[Target Customers]** through **[Core Capabilities/Resources]**, solving **[Core Pain Points]**, and derive **[Revenue Streams]** from this.

### 2.2 Business Model Canvas

```mermaid
graph TB
    subgraph Value Proposition
        VP[Value Propositions]
    end

    subgraph Customer Side
        CS[Customer Segments]
        CR[Customer Relationships]
        CH[Channels]
    end

    subgraph Infrastructure
        KA[Key Activities]
        KR[Key Resources]
        KP[Key Partnerships]
    end

    subgraph Financial
        C[Cost Structure]
        R[Revenue Streams]
    end

    VP --> CS
    CR --> CS
    CH --> CS
    KA --> VP
    KR --> VP
    KP --> KA
    KP --> KR
    C --> KA
    C --> KR
    C --> KP
    R --> CS

    style VP fill:#e3f2fd,stroke:#1565c0,stroke-width:3px
    style R fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style C fill:#ffebee,stroke:#c62828,stroke-width:2px
```

### 2.3 Business Model Flywheel

```mermaid
graph LR
    A[Acquisition] --> B[Activation]
    B --> C[Revenue]
    C --> D[Retention]
    D --> E[Referral]
    E --> A

    style A fill:#bbdefb,stroke:#1565c0
    style B fill:#c8e6c9,stroke:#2e7d32
    style C fill:#fff9c4,stroke:#f57f17
    style D fill:#ffccbc,stroke:#d84315
    style E fill:#e1bee7,stroke:#6a1b9a
```

---

## 3. Value Proposition Design

### 3.1 Value Proposition Canvas

```mermaid
graph TB
    subgraph Customer Profile
        J1[Jobs to be done]
        J2[Pains]
        J3[Gains]
    end

    subgraph Value Map
        V1[Products & Services]
        V2[Pain Relievers]
        V3[Gain Creators]
    end

    V1 --> J1
    V2 --> J2
    V3 --> J3

    style J1 fill:#fff3e0,stroke:#e65100
    style J2 fill:#ffebee,stroke:#c62828
    style J3 fill:#e8f5e9,stroke:#2e7d32
    style V1 fill:#e3f2fd,stroke:#1565c0
    style V2 fill:#fce4ec,stroke:#ad1457
    style V3 fill:#f3e5f5,stroke:#7b1fa2
```

### 3.2 Value Proposition Layering

| Layer | Value Type | Specific Description | Customer Perception |
|------|---------|---------|---------|
| **Functional Value** | Solve Problems | Provides [specific function], replaces [traditional method] | Efficiency improvement X-fold |
| **Economic Value** | Reduce Costs | Saves [XX]% cost compared to competitors | ROI quantifiable |
| **Emotional Value** | Experience Upgrade | Usage process [enjoyable/professional/reassuring] | NPS > 40 |
| **Social Value** | Identity | Helps customers build [professional/leading] image | Brand premium |

---

## 4. Customer Segmentation and Relationships

### 4.1 Customer Segmentation Pyramid

```mermaid
graph TB
    subgraph Customer Tiers
        T1[Lighthouse Customers / 5% / Industry benchmarks/Strategic endorsements]
        T2[Core Paying Customers / 25% / High ARPU/High retention]
        T3[Growth Customers / 40% / Potential to be unlocked]
        T4[Long-tail Free/Low-payment / 30% / Word-of-mouth/Data contribution]
    end

    T1 --> T2
    T2 --> T3
    T3 --> T4

    style T1 fill:#ffd700,stroke:#b8860b,stroke-width:2px
    style T2 fill:#c0c0c0,stroke:#808080,stroke-width:2px
    style T3 fill:#cd7f32,stroke:#8b4513,stroke-width:2px
    style T4 fill:#e0e0e0,stroke:#757575,stroke-width:1px
```

### 4.2 Customer Personas

| Dimension | Customer A (Decision Maker) | Customer B (User) | Customer C (Influencer) |
|------|----------------|----------------|----------------|
| **Role** | CEO/VP | Department Manager/Executive | IT/Procurement/Consultant |
| **Age** | 35-50 | 25-35 | 30-45 |
| **Core Needs** | Cost reduction, business growth | Easy to operate, error-free | Secure, stable, compliant |
| **Decision Weight** | High (Budget approval) | Medium (Usage feedback) | Medium (Technical evaluation) |
| **Touchpoints** | Industry summits, private boards | Product community, training | Tech forums, POC |

### 4.3 Customer Relationship Strategy

```mermaid
journey
    title Customer Relationship Depth Evolution
    section Acquisition Phase
      Content Outreach: 3: Marketing
      Trial Experience: 4: Product
      Sales Follow-up: 3: Sales
    section Growth Phase
       Onboarding: 5: Customer Success
      Value Delivery: 5: Product
      Regular Follow-ups: 4: Customer Success
    section Maturity Phase
      Upsell/Upgrade: 5: Sales
      Ecosystem Co-building: 4: Executives
      Case Study Endorsement: 5: Marketing
    section Renewal Phase
      Renewal Negotiation: 4: Sales
      Churn Warning: 3: Customer Success
      Referral: 5: Customer
```

---

## 5. Channel Design

### 5.1 Omnichannel Funnel

```mermaid
graph LR
    subgraph Awareness Layer
        A1[SEO/Content Marketing]
        A2[Social Media]
        A3[Industry Summits]
        A4[Word-of-Mouth Referral]
    end

    subgraph Consideration Layer
        B1[Website/Mini Program]
        B2[Product Demo]
        B3[Case Study White Papers]
        B4[Free Trial]
    end

    subgraph Purchase Layer
        C1[Direct Sales Team]
        C2[Channel Partners]
        C3[Self-service Ordering]
        C4[Ecosystem Cooperation]
    end

    subgraph Delivery Layer
        D1[Customer Success Team]
        D2[Online Help Center]
        D3[Community Forum]
        D4[API Documentation]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    B1 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C4 --> D4

    style A1 fill:#e3f2fd,stroke:#1565c0
    style B1 fill:#e8f5e9,stroke:#2e7d32
    style C1 fill:#fff3e0,stroke:#e65100
    style D1 fill:#f3e5f5,stroke:#7b1fa2
```

### 5.2 Channel Efficiency Matrix

| Channel | CAC | Conversion Rate | Customer Quality | Scalability Potential | Priority |
|------|-----|--------|---------|-----------|--------|
| Direct Sales Team | High | High | Very High | Medium | P1 |
| Channel Partners | Medium | Medium | High | High | P2 |
| Content Marketing | Low | Low | Medium | Very High | P1 |
| Product-Led Growth | Very Low | Medium | Medium | Very High | P0 |
| Ecosystem Cooperation | Medium | High | High | Medium | P2 |

---

## 6. Revenue Streams and Pricing

### 6.1 Revenue Structure

```mermaid
pie showData
    title Target Revenue Composition
    "Subscription Revenue (SaaS)" : 50
    "Usage-based Billing (PAYG)" : 20
    "Value-added Services" : 15
    "Solutions/Customization" : 10
    "Ecosystem/Platform Commission" : 5
```

### 6.2 Pricing Strategy

```mermaid
graph TB
    subgraph Pricing Anchors
        P1[Free Version / Freemium / Customer Acquisition/Education]
        P2[Basic Version / ¥X/month / Individual/Small Team]
        P3[Professional Version / ¥Y/month / SMB Core]
        P4[Enterprise Version / Custom Pricing / Large Customer Exclusive]
    end

    P1 --> P2
    P2 --> P3
    P3 --> P4

    P1 -.->|Feature Limitations| P2
    P2 -.->|Seats/Premium Features| P3
    P3 -.->|Exclusive Services/Private Deployment| P4

    style P1 fill:#e0e0e0,stroke:#9e9e9e
    style P2 fill:#bbdefb,stroke:#1565c0
    style P3 fill:#64b5f6,stroke:#1565c0,stroke-width:2px
    style P4 fill:#ffd700,stroke:#b8860b,stroke-width:2px
```

### 6.3 Pricing Dimension Design

| Version | Price | Core Features | Target Customer | Conversion Strategy |
|------|------|---------|---------|---------|
| **Free** | ¥0 | Basic features + usage limits | Individual/Student | Entry point for experience |
| **Basic** | ¥99/person/month | Core features + standard support | Small Team | Feature unlock |
| **Professional** | ¥299/person/month | Advanced features + priority support | Growing Enterprise | ROI justification |
| **Enterprise** | Custom | Full features + private deployment + dedicated CSM | Large Corporation | Executive dialogue |

---

## 7. Core Resources and Capabilities

### 7.1 Resource Capability Pyramid

```mermaid
graph TB
    subgraph Strategic Layer
        S1[Data Assets / Industry Know-how]
        S2[Brand Awareness / Trust Endorsement]
    end

    subgraph Capability Layer
        C1[Technical Capability / Algorithms/Architecture]
        C2[Operational Capability / Acquisition/Retention]
        C3[Commercialization Capability / Pricing/Sales]
    end

    subgraph Resource Layer
        R1[Talent Team / Core Backbone]
        R2[Capital Reserves / Financing/Cash Flow]
        R3[Intellectual Property / Patents/Software Copyrights]
    end

    R1 --> C1
    R1 --> C2
    R1 --> C3
    C1 --> S1
    C2 --> S2
    C3 --> S2
    R2 --> C1
    R2 --> C2
    R3 --> C1

    style S1 fill:#ffd700,stroke:#b8860b,stroke-width:2px
    style S2 fill:#ffd700,stroke:#b8860b,stroke-width:2px
```

### 7.2 Core Capability Assessment

| Capability Dimension | Self-assessment Level | Industry Benchmark | Development Status | Investment Plan |
|---------|---------|---------|---------|---------|
| Technology R&D | ⭐⭐⭐⭐⭐ | Leading | Established | Continuous investment |
| Product Experience | ⭐⭐⭐⭐ | Excellent | Iterating | Increased investment |
| Customer Acquisition Efficiency | ⭐⭐⭐ | Average | Building | Key breakthrough focus |
| Customer Success | ⭐⭐⭐⭐ | Excellent | Established | Systematization |
| Supply Chain/Delivery | ⭐⭐ | Behind | Starting | Talent acquisition |

---

## 8. Key Business Activities

### 8.1 Value Chain Analysis

```mermaid
graph LR
    subgraph Primary Value Chain
        A1[Insight Discovery] --> A2[Product R&D]
        A2 --> A3[Market Acquisition]
        A3 --> A4[Sales Conversion]
        A4 --> A5[Delivery Implementation]
        A5 --> A6[Customer Success]
        A6 --> A7[Renewal & Upsell]
    end

    subgraph Support Activities
        B1[Infrastructure / Cloud/Security/Compliance]
        B2[Human Resources / Recruitment/Training]
        B3[Financial Management / Budget/Financing]
        B4[Ecosystem Cooperation / Channels/Alliances]
    end

    B1 --> A2
    B2 --> A1
    B3 --> A3
    B4 --> A4

    style A1 fill:#e3f2fd,stroke:#1565c0
    style A2 fill:#e3f2fd,stroke:#1565c0
    style A3 fill:#e8f5e9,stroke:#2e7d32
    style A4 fill:#e8f5e9,stroke:#2e7d32
    style A5 fill:#fff3e0,stroke:#e65100
    style A6 fill:#fff3e0,stroke:#e65100
    style A7 fill:#f3e5f5,stroke:#7b1fa2
```

### 8.2 Key Business Processes

| Business Area | Core Metric | Current Level | Target Level | Key Actions |
|---------|---------|---------|---------|---------|
| Insight Discovery | Requirement Accuracy | 60% | 85% | Establish Customer Advisory Board |
| Product R&D | Time to Launch | 6 weeks | 2 weeks | Agile Transformation + DevOps |
| Market Acquisition | MQL Cost | ¥500 | ¥200 | Content Marketing + PLG |
| Sales Conversion | Win Rate | 15% | 30% | Sales Methodology + Tools |
| Customer Success | Health Score | 70 pts | 90 pts | CSM Systematization |
| Renewal & Upsell | NRR | 100% | 120% | Value Operations |

---

## 9. Partner Network

### 9.1 Ecosystem Cooperation Map

```mermaid
graph TB
    subgraph Core Layer
        US[Our Platform]
    end

    subgraph Technology Layer
        T1[Cloud Providers / AWS/Alibaba Cloud]
        T2[AI Models / OpenAI/Self-developed]
        T3[Security Providers / Compliance/ISO]
    end

    subgraph Channel Layer
        D1[Industry ISVs / Vertical Solutions]
        D2[System Integrators / SI]
        D3[Consulting Firms / MBB/Big Four]
    end

    subgraph Customer Layer
        C1[Lighthouse Customers / Joint Innovation]
        C2[Scale Customers / Standard Service]
    end

    T1 --> US
    T2 --> US
    T3 --> US
    US --> D1
    US --> D2
    US --> D3
    D1 --> C1
    D2 --> C2
    D3 --> C1

    style US fill:#ffd700,stroke:#b8860b,stroke-width:3px
    style T1 fill:#e3f2fd,stroke:#1565c0
    style D1 fill:#e8f5e9,stroke:#2e7d32
    style C1 fill:#f3e5f5,stroke:#7b1fa2
```

### 9.2 Cooperation Model Design

| Cooperation Type | Partner Role | Our Value | Partner Value | Cooperation Depth |
|---------|---------|---------|---------|---------|
| **Strategic Alliance** | Cloud providers/platforms | Solution richness | Increased customer stickiness | Joint products + Joint sales |
| **Channel Distribution** | Regional agents/ISVs | Market coverage expansion | Profit margin + Product supplement | Training certification + Rebates |
| **Technical Integration** | API/Data partners | Enhanced product capability | Traffic/Data feedback | Technical integration + Co-branding |
| **Content Co-creation** | Media/Consulting | Industry influence | Exclusive content source | White papers + Summits |

---

## 10. Cost Structure and Unit Economics

### 10.1 Cost Structure Analysis

```mermaid
pie showData
    title Operating Cost Composition
    "Personnel Costs (R&D/Sales/CS)" : 55
    "Cloud Resources/Infrastructure" : 15
    "Marketing & Sales Expenses" : 18
    "Administration & Management" : 8
    "Other" : 4
```

### 10.2 Unit Economics Model

```mermaid
graph LR
    subgraph Revenue Side
        ARPU[ARPU / ¥X/month]
        LTV[LTV / ¥Y / Lifetime Value]
    end

    subgraph Cost Side
        CAC[CAC / Customer Acquisition Cost]
        CRC[CRC / Service Cost]
        COGS[COGS / Direct Cost]
    end

    subgraph Health Metrics
        R1[LTV/CAC > 3]
        R2[Payback Period < 12 months]
        R3[Gross Margin > 70%]
        R4[NRR > 110%]
    end

    ARPU --> LTV
    CAC --> R1
    LTV --> R1
    CRC --> R2
    COGS --> R3
    ARPU --> R4

    style LTV fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style CAC fill:#ffebee,stroke:#c62828,stroke-width:2px
    style R1 fill:#e8f5e9,stroke:#2e7d32
    style R2 fill:#e8f5e9,stroke:#2e7d32
    style R3 fill:#e8f5e9,stroke:#2e7d32
    style R4 fill:#e8f5e9,stroke:#2e7d32
```

### 10.3 Key Financial Metrics

| Metric | Definition | Current Value | Health Standard | Optimization Direction |
|------|------|--------|---------|---------|
| **CAC** | Per-customer Acquisition Cost | ¥[XX] | < LTV/3 | Optimize channel structure |
| **LTV** | Customer Lifetime Value | ¥[XX] | > 3×CAC | Improve retention/upsell |
| **LTV/CAC** | Return on Investment Ratio | [X]:1 | > 3:1 | Bidirectional optimization |
| **Payback Period** | CAC Recovery Time | [X] months | < 12 months | Increase first-order value |
| **Gross Margin** | (Revenue - Direct Cost)/Revenue | [X]% | SaaS>70% | Infrastructure optimization |
| **NRR** | Net Revenue Retention | [X]% | > 110% | Upsell + Expansion |
| **Rule of 40** | Growth Rate% + Profit Margin% | [X]% | > 40% | Balance growth and profitability |

---

## 11. Business Model Evolution Roadmap

### 11.1 Three-Stage Evolution

> **Note**: Gantt charts are incompatible with Feishu; replaced with table descriptions.

| Stage | Task | Start Date | End Date | Duration | Status |
|------|------|----------|----------|------|------|
| Phase 1: Point Tool | MVP Validation | 2024-01 | 2024-06 | 6 months | Completed |
| Phase 1: Point Tool | PMF Confirmation | 2024-07 | 2024-12 | 6 months | Completed |
| Phase 1: Point Tool | Single-point Monetization | 2024-10 | 2025-03 | 6 months | Completed |
| Phase 2: Platform | Feature Expansion | 2025-01 | 2025-06 | 6 months | In Progress |
| Phase 2: Platform | Multi-tenant Architecture | 2025-04 | 2025-09 | 6 months | In Progress |
| Phase 2: Platform | Ecosystem Opening | 2025-07 | 2025-12 | 6 months | Not Started |
| Phase 3: Ecosystem Network | Data Flywheel | 2026-01 | 2026-06 | 6 months | Not Started |
| Phase 3: Ecosystem Network | Platform Commission | 2026-04 | 2026-09 | 6 months | Not Started |
| Phase 3: Ecosystem Network | Industry Standard | 2026-07 | 2026-12 | 6 months | Not Started |

### 11.2 Business Model Characteristics per Stage

| Stage | Period | Core Model | Revenue Characteristics | Key Resources | Moat |
|------|------|---------|---------|---------|--------|
| **Point Tool** | Current | Product Selling | Linear growth, sales-dependent | Product Capability | Feature Leadership |
| **Platform** | 12-18 months | Subscription + Value-added | Compound growth, emerging network effects | Customer Data | Switching Costs |
| **Ecosystem Network** | 24-36 months | Platform Commission + Data | Exponential growth, ecosystem synergy | Industry Standards | Network Effects |

---

## 12. Risk and Sustainability Analysis

### 12.1 Business Model Vulnerability Assessment

```mermaid
graph TB
    subgraph risk[Risk Impact Matrix: Probability vs Impact]
        subgraph high[High Probability]
            GI[Big Tech Entry / High Impact · High Probability]
            DP[Pricing Pressure / Medium Impact · High Probability]
        end
        subgraph low[Low Probability]
            TI[Technology Iteration / Medium Impact · Medium Probability]
            CC[Customer Concentration / High Impact · Low Probability]
            TL[Talent Loss / Medium Impact · Medium Probability]
            PC[Policy Changes / High Impact · Low Probability]
            ED[Economic Downturn / Medium Impact · Low Probability]
        end
    end
```

### 12.2 Sustainability Safeguard Mechanisms

| Risk Type | Vulnerability | Mitigation Strategy | Monitoring Metric |
|---------|--------|---------|---------|
| **Competitive Risk** | Big Tech Replication | Deep vertical focus + Data barrier | Market share changes |
| **Technology Risk** | Wrong technology path | Dual-track R&D + Rapid iteration | Technical debt ratio |
| **Customer Risk** | Large customer loss | Customer diversification + Multi-industry | Customer concentration |
| **Financial Risk** | Cash flow disruption | Controlled burn rate + Diversified revenue | Runway months |
| **Compliance Risk** | Data regulation | Compliance-first + Localization | Compliance audit results |

### 12.3 ESG and Long-term Value

```mermaid
graph TB
    subgraph ESG Value
        E[Environment / Green Computing/Carbon Neutrality]
        S[Social / Digital Inclusion/Employment]
        G[Governance / Data Privacy/Compliance]
    end

    subgraph Business Value
        B1[Brand Premium]
        B2[Customer Trust]
        B3[Policy Dividends]
        B4[Capital Favor]
    end

    E --> B1
    S --> B2
    G --> B3
    E --> B4
    S --> B4
    G --> B4

    style E fill:#c8e6c9,stroke:#2e7d32
    style S fill:#bbdefb,stroke:#1565c0
    style G fill:#fff9c4,stroke:#f57f17
    style B4 fill:#ffd700,stroke:#b8860b,stroke-width:2px
```

---

## Appendices

### A. Glossary

| Term | English | Definition |
|------|------|------|
| CAC | Customer Acquisition Cost | Per-customer acquisition cost |
| LTV | Lifetime Value | Customer lifetime value |
| NRR | Net Revenue Retention | Net revenue retention rate |
| PMF | Product-Market Fit | Product-market fit |
| PLG | Product-Led Growth | Product-led growth |
| ARR | Annual Recurring Revenue | Annual recurring revenue |
| MRR | Monthly Recurring Revenue | Monthly recurring revenue |
| ARPU | Average Revenue Per User | Average revenue per user |

### B. Reference Frameworks

- Osterwalder, A. & Pigneur, Y. *Business Model Generation*
- Maurya, A. *Running Lean*
- Ellis, S. & Brown, M. *Hacking Growth*
- McKinsey 7S Model / Porter Value Chain / Bain Profit System

---

> **Document Maintenance**: Recommended to review and update quarterly, with immediate revisions during major strategic adjustments.
>
> **Distribution Scope**: Core management team, board of directors, strategic investors (after signing NDA).
