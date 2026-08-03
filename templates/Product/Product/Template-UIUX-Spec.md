# [Product/System Name (English Name)] - Product Color & UI/UX Specification Document

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
> **Scope:** Web / iOS / Android / Desktop
>
> **Related Documents:** [Product Requirements Document PRD], [Brand Guidelines]

---

## 0. Document Guide

### 0.1 Document Purpose and Scope

[Explain the purpose, applicable scenarios, and non-applicable scenarios of this document]

### 0.2 Related Documents

| Document Type | Filename | Related Sections |
|-------------|----------|-----------------|
| [Type] | [Filename] [Line Range] | [Section Description] |

> **Reference Format Note**: Related documents use the `filename line range` format (e.g., `【Template】Technical Requirements Document(TRD).md 3-17`). Line numbers may change as documents are updated. Please refer to the actual content.

### 0.3 Change Log

| Version | Date | Author | Changes | Reviewer |
| :--- | :--- | :--- | :--- | :--- |
| v0.1.0 | YYYY-MM-DD | [Name] | Initial Release | [Reviewer] |

---

## 1. Design Principles and Overview

### 1.1 Design Vision

Describe the product's visual temperament in 1-2 sentences. For example:
> Focusing on "professional, trustworthy, and lightweight," through restrained color hierarchy and clear interaction feedback, helping users efficiently complete complex tasks.

### 1.2 Core Principles

| Principle | Description | Design Implementation |
|-----------|-------------|----------------------|
| **Consistency** | Use the same visual language in the same scenarios | Token naming, component states, interaction effects unified globally |
| **Hierarchy** | Distinguish information priority through color and shadows | Layering Model defines page depth |
| **Accessibility** | All users can use without barriers | Comply with WCAG 2.1 AA contrast standards, dual encoding principle |
| **Responsive** | Adapt to multiple platforms and theme switching | Support Light / Dark / High-Contrast modes |
| **Evidence-based** | Design decisions based on evidence, not intuition | Color quantity, type scale ratio, spacing baseline have industry consensus support |
| **Touch-friendly** | Minimum tap target >= 44x44px | Mobile button height 48-52px, ensure comfortable finger tapping |
| **Breathing room** | Use spacing reasonably to avoid crowding | 4/8/12/16/24px spacing system, clear information hierarchy |
| **Restrained coloring** | Main color selected by industry, functional colors unified | Brand color coverage <= 10%, neutral colors build text hierarchy |

> **Mobile Design Core Conclusion**: Good typography comes from clear information hierarchy, not fancy fonts. Consistency, clear hierarchy, adaptation priority, touch-friendly, breathing room, and restrained coloring are the 6 core principles of APP design.

### 1.3 Design Token Architecture Overview

This specification uses a **three-layer Token architecture**, following the DTCG (W3C Design Tokens Community Group) specification:

| Layer | Naming Pattern | Example | Description |
|-------|---------------|---------|-------------|
| **Primitive** | `{color}-{scale}` | `ink-green-700` | Platform-agnostic original color values, not directly used in components |
| **Semantic** | `{purpose}[-variant][-{state}]` | `text-primary`, `bg-surface-hover` | Theme-bound semantic roles, supporting Light/Dark switching |
| **Component** | `{component}-{property}[-{state}]` | `btn-primary-bg-hover` | Framework-specific component-level Tokens |

> **State as the Fourth Dimension**: Each semantic Token must define at least 6 states (Default, Hover, Active, Focus, Selected, Disabled), otherwise color consistency across different interaction states cannot be guaranteed.

**Token Naming Rules**:
- Use lowercase letters + periods/hyphens as separators
- Semantic Token names describe **purpose** not **value** (e.g., `color.text.primary` not `color.text.black`)
- Recommended total Token count is under 200; beyond that, management costs grow exponentially

---

## 2. Color System

> **Core Idea**: Adopt a three-layer Token system where all colors are not used directly as Hex values but invoked through semantic Tokens. Token naming rule: `{category}.{property}.{variant}.{state}`
> Example: `color.background.primary.default`, `color.text.inverse`, `color.border.danger.hovered`

### 2.1 Brand Palette

Adopting a **single brand color** strategy: only define 1 primary brand color, covering all usage scenarios through gradient expansion. Advantages of single-color strategy: focused visual focus, low development and maintenance costs, high cross-platform consistency.

| Token Name | Light Mode Value | Dark Mode Value | Usage Scenarios |
|-----------|-----------------|-----------------|-----------------|
| `color.brand` | [Primary Hex] | [Primary Dark Hex] | Primary buttons, Logo, navigation active state, links, icon emphasis |

> **Design Constraint**: Auxiliary emphasis and chart series colors are sourced from the semantic palette (§2.3) and neutral palette (§2.5), with no additional brand colors defined.

**Industry Brand Color Recommendations**:

| Industry Type | Recommended Color | Description |
|--------------|-------------------|-------------|
| Retail/Consumer/E-commerce | `#3B82F6` (Blue) | Trust, professionalism, stability |
| Live Streaming/Social/Content | `#8B5CF6` (Purple) | Creativity, vitality, youth |
| Health/Sports/Travel | `#10B981` (Green) | Health, nature, vitality |
| Tools/Efficiency/Tech | `#14B8A6` (Teal) | Technology, efficiency, freshness |

> **Brand Color Selection Recommendation**: Choose primary color based on product industry attributes, ensuring brand color aligns with product positioning. Brand color coverage <= 10%.

**Brand Color Gradient Scale**:
Define 9 gradient levels (50-900), with **level 600 as the base color**. Level 600 on white backgrounds typically achieves 4.5:1-7:1 contrast, meeting WCAG AA-AAA standards.

| Gradient | Color Value (Light) | Color Value (Dark) | Purpose |
|----------|--------------------|--------------------|---------|
| `brand-50` | [Hex] | [Hex] | Very light background, hover base color |
| `brand-100` | [Hex] | [Hex] | Light background, selected state base color |
| `brand-200` | [Hex] | [Hex] | Light decorative elements |
| `brand-300` | [Hex] | [Hex] | Secondary icons, auxiliary text |
| `brand-400` | [Hex] | [Hex] | Medium emphasis |
| `brand-500` | [Hex] | [Hex] | Hover state, chart auxiliary colors |
| `brand-600` | [Hex] | [Hex] | **Base color (default)** |
| `brand-700` | [Hex] | [Hex] | Pressed/Active state |
| `brand-800` | [Hex] | [Hex] | Dark text (on-light) |
| `brand-900` | [Hex] | [Hex] | Very dark decoration, dark background emphasis |

> **Hidden Rule**: Do not use 400 or 500 as the base color, as their contrast often cannot cover all usage scenarios.

### 2.2 Color Area Rules (60-30-10)

| Ratio | Role | Description |
|-------|------|-------------|
| 60% | Primary/Base color | Page background, large area fill |
| 30% | Secondary color | Cards, sidebars, secondary areas |
| 10% | Accent color | CTA buttons, key icons, focus elements |

**Color Area Audit Checklist**:

- [ ] Page background color covers >= 60% area
- [ ] Card/panel color covers ~30% area
- [ ] Brand accent color covers <= 10% area
- [ ] Maximum 1 brand color CTA button per screen
- [ ] Brand color only used for interactive elements (buttons, links, icons), not for large background areas

### 2.3 Semantic/Functional Palette

Used to convey status, feedback, and urgency levels, independent of brand color. Industry consensus: 4 core semantic colors (Success/Warning/Error/Info).

| Semantic | Token | Light | Dark | Usage Scenarios |
|----------|-------|-------|------|-----------------|
| **Success** | `color.semantic.success` | `#22C58B` | `#34D399` | Success messages, completion status, positive indicators |
| **Warning** | `color.semantic.warning` | `#FFB020` | `#FBBF24` | Warning messages, items requiring attention |
| **Error** | `color.semantic.error` | `#FF5A6B` | `#F87171` | Error messages, deletion confirmation, form validation failures |
| **Info** | `color.semantic.info` | `color.brand-600` | `color.brand-400` | Information messages, neutral notifications (reusing brand color) |

**Semantic Color Light Background Variants**:

| Semantic | Light Background Token | Light Background Value | Purpose |
|----------|----------------------|------------------------|---------|
| **Success** | `color.semantic.success.subtle` | `#CFF5E7` | Success message background |
| **Warning** | `color.semantic.warning.subtle` | `#FFE8B5` | Warning message background |
| **Error** | `color.semantic.error.subtle` | `#FFD7DC` | Error message background |
| **Info** | `color.semantic.info.subtle` | `#D9E7FF` | Information message background |

> **Semantic Color Reuse under Single Brand Color Strategy**: Info semantic color directly reuses brand color gradient, with no additional definitions. Brand color 600 (Light) and 400 (Dark) serve as default values for information messages respectively.

**Semantic Color Extension Rules**: Each semantic color must contain at least 5 variants:

| Variant | Naming Suffix | Purpose |
|---------|---------------|---------|
| `default` | `color.semantic.error` | Default state |
| `hovered` | `color.semantic.error.hovered` | Mouse hover |
| `pressed` | `color.semantic.error.pressed` | Press/active |
| `subtle` | `color.semantic.error.subtle` | Light background (e.g., error input field background) |
| `contrast` | `color.semantic.error.contrast` | Text/icon color (ensure readability on subtle background) |

### 2.4 Color Semantics and Psychological Considerations

> Fill in the psychological meaning and cultural considerations of brand color selection. Color semantics are not universal but deeply influenced by cultural construction. **Attention is physiological, meaning is cultural** — red attracts attention in all cultures (determined by wavelength), but the meaning red conveys varies across cultures. See `UI Design Specification Systematic Research Report.md` §5.1.

[Fill in the psychological meaning, cultural difference considerations, saturation/brightness strategy of this product's brand color]

**Key Principle**: Never let color be the sole carrier of semantics. If error state only conveys "error" through red, it will fail in cross-cultural scenarios. Must be paired with dual encoding such as icons, text, and shapes.

### 2.5 Neutral Palette

Builds the interface skeleton, text, borders, and dividers. Use blue-gray or warm gray, avoiding pure black `#000000`.

| Token | Light Mode | Dark Mode | Usage Scenarios |
|-------|-----------|-----------|-----------------|
| `color.neutral-50` | `#F3F6FB` | [Hex] | Page global background |
| `color.neutral-100`| [Hex] | [Hex] | Card background, input field background |
| `color.neutral-200`| `#E5E7EB` | [Hex] | Hover background, dividers |
| `color.neutral-300`| `#D1D5DB` | [Hex] | Disabled borders, secondary dividers |
| `color.neutral-400`| `#9CA3AF` | [Hex] | Placeholder text, disabled text |
| `color.neutral-500`| `#6B7280` | [Hex] | Body text (secondary), icon default state |
| `color.neutral-600`| `#374151` | [Hex] | Auxiliary text (dark body text) |
| `color.neutral-700`| `#1A1B27` | [Hex] | Heading text, primary icons |
| `color.neutral-800`| [Hex] | [Hex] | Secondary headings |
| `color.neutral-900`| [Hex] | [Hex] | Heading text, primary icons |

**Neutral Color Text Hierarchy Specification**:

| Purpose | Color Value | Description |
|---------|-------------|-------------|
| Headings | `#1A1B27` | Deepest, for page core themes |
| Dark body text | `#374151` | Important paragraph body text |
| Body text | `#6B7280` | Page main information content |
| Auxiliary text | `#9CA3AF` | Supplementary explanations, secondary information |
| Dividers | `#D1D5DB` | Content separation |
| Borders | `#E5E7EB` | Component borders |
| Page background | `#F3F6FB` | Page base color (not pure white, reduces visual fatigue) |

### 2.6 Layering Model

Defines the "depth" and "stacking logic" of interface elements, ensuring clear visual hierarchy in complex pages.

**Light Mode Layering**:
- **Layer 0 (Base)**: `neutral-50` — Page bottom-most background
- **Layer 1 (Surface)**: `neutral-100` — Cards, popups, sidebars
- **Layer 2 (Raised)**: `neutral-0` (pure white) — Dropdown menus, floating layers, Tooltips
- **Layer 3 (Overlay)**: Black overlay with transparency `rgba(0,0,0,0.45)` — Modal background

**Dark Mode Layering** (asymmetric mapping, not simple inversion):
- **Layer 0**: `neutral-50` (deepest)
- **Layer 1**: `neutral-100` — Slightly lighter than bottom layer (raised feel)
- **Layer 2**: `neutral-200` — Floating layers continue to lighten
- **Layer 3**: `rgba(0,0,0,0.75)` — Deeper overlay

> **Core Principle**: Dark Mode is not a "color inversion" of Light Mode but an independent color space. Each Token's Dark value needs independent design and verification, not algorithmic inversion.

### 2.7 Color Role Mapping

Maps Tokens to specific UI elements, ensuring "background-text-icon" contrast compliance.

| Role | Background Token | Text/Icon Token | Purpose |
|------|-----------------|-----------------|---------|
| **Primary** | `color.brand-600` | `color.text.on-brand` | Primary buttons, FAB, key action points |
| **Secondary** | Transparent | `color.brand-600` | Secondary buttons, filter tags |
| **Surface** | `color.background.surface` | `color.text.primary` | Cards, panels |
| **Inverse** | `color.background.inverse` | `color.text.inverse` | Dark banners, Toast |
| **Danger** | `color.semantic.error` | `color.text.on-danger` | Delete buttons, strong warnings |
| **Disabled** | `color.background.disabled` | `color.text.disabled` | Disabled state elements |

### 2.8 Dark/Light Mode Mapping Table

| Token | Light | Dark | Mapping Logic |
|-------|-------|------|---------------|
| `color.background.default` | [Hex] | [Hex] | Page base color, dark mode not pure black to preserve depth |
| `color.background.surface` | [Hex] | [Hex] | Card base color, dark mode Elevated brighter |
| `color.brand-600` | [Primary Hex] | [Primary Dark Hex] | Primary button background, dark mode brightened to level 400 |
| `color.text.primary` | [Hex] | [Hex] | Primary heading/body text, dark mode not pure white to reduce Halation glare |
| `color.text.secondary`| [Hex] | [Hex] | Secondary description text |
| `color.text.disabled` | [Hex] | [Hex] | Disabled state text |
| `color.border.default` | [Hex] | [Hex] | Default borders |
| `color.border.focus` | `color.brand-600` | `color.brand-400` | Focus state border (2px) |

> **Dark Mode Brand Color Mapping**: Light mode uses level 600, dark mode brightened to level 400, ensuring sufficient contrast on dark backgrounds.

### 2.9 Color Contrast Standards

#### 2.9.1 WCAG 2.1 Contrast Requirements

| Level | Normal Text (<18px / non-bold <14px) | Large Text (>=18px / bold >=14px) | UI Components / Graphical Objects |
|-------|--------------------------------------|-----------------------------------|-----------------------------------|
| **AA (Minimum)** | >= 4.5:1 | >= 3:1 | >= 3:1 |
| **AAA (Enhanced)** | >= 7:1 | >= 4.5:1 | Not defined |

#### 2.9.2 APCA Contrast Algorithm (WCAG 3.0 Candidate)

APCA is the successor to the WCAG 2.x contrast algorithm, considering the directional interaction effects of text color and background color, font size and weight:

| Contrast Level | APCA Minimum Value (Lc) | Purpose |
|----------------|--------------------------|---------|
| Body text | Lc >= 60 | Body text readability |
| Large text | Lc >= 45 | Headings, large font sizes |
| Minimum perceivable | Lc >= 15 | Decorative text |
| Optimal readability | Lc >= 75 | Long-form reading body text |

#### 2.9.3 Dark Mode Contrast Strategy

| Strategy | Industry Recommendation | Theoretical Basis |
|----------|------------------------|-------------------|
| Base color not pure black | Use `#121212` or toned dark gray | Warm gray base is more visually comfortable than pure black |
| Text not cool white | Use `#E0E0E0` or warm white | Halation effect: high brightness text on dark backgrounds produces glow diffusion |
| Brand color brightening | Dark mode brightened by 1-2 levels | Maintain consistent visual weight |
| Status color brightening | Dark mode uses level 400 | Level 400 has better contrast on dark backgrounds |
| Shadow intensification | Dark mode replaces shadows with borders | Shadow effects weaken in dark mode |

### 2.10 Color Vision Deficiency (CVD) Accessibility

Approximately 8% of males and 0.5% of females have color vision deficiency. Key specifications:

- Semantic colors cannot be distinguished by color alone; must be supplemented with icons, text, shapes (WCAG SC 1.4.1)
- Error (red) and Success (green) may be confused in Deuteranopia mode; ensure icon + text assistance
- Color palette should be verified through CVD simulation: Protanopia / Deuteranopia / Tritanopia three modes
- Recommended tools: Sim Daltonism (macOS), Color Oracle (cross-platform), Chrome DevTools simulation

### 2.11 High Contrast Mode

- In high contrast mode, shadows are completely ineffective; must rely on **Border** and **Outline** to distinguish hierarchy
- Focus color on dark backgrounds may need customization
- All state changes cannot rely solely on color; must be paired with **icons, text labels, or shape changes**
- Adapt to `prefers-contrast: more` media query

---

## 3. Typography System

> All text uses Token management: `font.family`, `font.size`, `font.weight`, `line.height`, `letter.spacing`

### 3.1 Font Stack

| Scenario | Font Stack | Token |
|----------|-----------|-------|
| Western/Numbers | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto` | `font.family.base` |
| Chinese | `"PingFang SC", "Microsoft YaHei", "Noto Sans SC"` | `font.family.chinese` |
| Code | `"SF Mono", "Fira Code", Consolas` | `font.family.code` |

**Font Loading Strategy**:

- Use `font-display: swap` to avoid FOIT (Flash of Invisible Text), ensuring text is immediately visible
- Preload critical fonts: `<link rel="preload" as="font" crossorigin href="...">`
- Load Chinese fonts on demand (`unicode-range` sharding), reducing initial loading volume
- When font loading fails, fall back to system font stack without blocking rendering

**Font Pairing Rules**:
1. Maximum 2 font families: 1 heading font + 1 body font, third only for code
2. Contrast principle: Serif + Sans-serif pairing is most classic (e.g., Noto Serif SC + Noto Sans SC)
3. x-height matching: Paired fonts should have similar x-height
4. Chinese pairing: Headings use Song/Serif (cultural feel), body text uses Hei/Sans-serif (readability)

### 3.2 Type Scale Ratio System

| Ratio Name | Ratio | Applicable Scenarios |
|------------|-------|---------------------|
| Minor Second | 1.067 | Compact information architecture, data-intensive |
| Major Second | 1.125 | Subtle hierarchy, enterprise backends |
| **Minor Third** | **1.2** | **Mobile, compact layouts** |
| **Major Third** | **1.25** | **General, balanced (recommended)** |
| Perfect Fourth | 1.333 | Loose hierarchy, brand display |
| Augmented Fourth | 1.414 | Dramatic contrast, creative |
| Perfect Fifth | 1.5 | Extreme contrast, large screen display |

> **Recommendation**: 1.25x (Major Third) ratio aligns with IBM Carbon, belonging to industry general balanced choices.

### 3.3 Type Scale

| Token | Font Size | Line Height | Font Weight | Purpose |
|-------|-----------|-------------|-------------|---------|
| `font.heading.xxl` | 28-32px | 1.2 | 700 | Page large heading (mobile H1) |
| `font.heading.xl` | 22-24px | 1.3 | 600 | Module heading (mobile H2) |
| `font.heading.lg` | 18-20px | 1.35 | 600 | Card heading |
| `font.body.large` | 16px | 1.5 | 400 | Body text (mobile default, line width 25-35 characters) |
| `font.body.base` | 14px | 1.5 | 400 | **Default body text (desktop)** |
| `font.body.small`| 12px | 1.4 | 400 | Auxiliary text, timestamps, notes |
| `font.label` | 14px | 1.2 | 500 | Button text, labels |

> **Mobile Font Size Specification**: Main heading and body text should have clear distinction; body text and auxiliary text should have at least 2px difference; don't rely on fancy fonts to replace information hierarchy. Core conclusion: good typography comes from clear information hierarchy.

### 3.4 Chinese Typography Specificity

| Specification Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Body font size | 14-16px | 14px suitable for information-intensive, 16px suitable for reading-type |
| Minimum font size | 12px | Below 12px reading speed significantly decreases |
| Line height (Chinese body) | 1.6-1.8 | Chinese characters have no ascenders/descenders, higher visual density between lines |
| letter-spacing | 0 | Chinese characters are monospaced, no extra spacing needed |
| Heading letter-spacing | 0-0.05em | Can slightly increase breathing room |
| Chinese-English mixed typesetting | Western font size 1-2px smaller than Chinese | Western letter x-height is typically smaller than Chinese character face |
| Chinese font weight | Minimum use Regular (400) | Light (300) has extremely poor readability in Chinese scenarios |

### 3.5 Line Height Recommended Values

| Font Size Range | Recommended Line Height Multiplier | Description |
|-----------------|------------------------------------|-------------|
| 32px+ | 1.1-1.25 | Large headings, tight line spacing |
| 24-31px | 1.25-1.35 | Medium headings |
| 18-23px | 1.35-1.45 | Small headings |
| 14-17px | 1.5-1.7 | Body text (higher for Chinese) |
| 10-13px | 1.4-1.6 | Auxiliary text |

### 3.6 Cross-Platform Typography Mapping

Specific mapping of the same semantic Token on different platforms needs independent definition; cannot simply equate px=pt=sp:

| Token | iOS | Android | Web |
|-------|-----|---------|-----|
| `font.body.large` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |
| `font.body.base` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |
| `font.label` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |

### 3.7 Responsive Typography Scaling

| Breakpoint | Heading Scaling | Body Scaling | Description |
|------------|-----------------|--------------|-------------|
| Mobile (<640px) | -2px | No change | Only headings shrink |
| Tablet (640-1024px) | -1px | No change | Transition |
| Desktop (>1024px) | Base | Base | Full size |
| Large (>1440px) | +2-4px | +1-2px | Large screen enlargement |

Recommended to use CSS `clamp()` for fluid heading scaling: `font-size: clamp(1.5rem, 1.5rem + 0.5vw, 2.5rem)`.

### 3.8 Dynamic Type Stepped Scaling

Mobile needs to support system-level font size scaling (Apple Dynamic Type / Android Font Size). Scaling is not simple linear enlargement but **stepped scaling**:

| Accessibility Size | Scaling Ratio | Design Constraints |
|-------------------|---------------|-------------------|
| XS (default) | 1.0x | Base layout |
| L | 1.35x | Test if layout overflows |
| XL | 1.65x | Text may need truncation |
| XXXL | 2.35x | All UI layouts must support text truncation or automatic wrapping |
| AX5 (maximum) | 4.59x | Touch targets must still be usable |

> **Key Rule**: Beyond AX3, all UI layouts must support **text truncation** or **automatic wrapping**.

---

## 4. Spacing & Grid System

> Based on 4px / 8px base units, industry consensus: 4px minimum unit + 8px common baseline.

### 4.1 Spacing Scale

| Token | Value | Purpose |
|-------|-------|---------|
| `space.0` | 0px | No spacing |
| `space.1` | 4px | Icon and text gap, label internal spacing |
| `space.2` | 8px | Compact padding, list item spacing |
| `space.3` | 12px | Button internal horizontal padding, secondary separation of same-group content |
| `space.4` | 16px | Card padding, form spacing, independent module separation |
| `space.5` | 20px | Module spacing |
| `space.6` | 24px | Paragraph spacing, page large block separation |
| `space.8` | 32px | Block spacing |
| `space.10` | 40px | Large block spacing |
| `space.12`| 48px | Page-level spacing |
| `space.16`| 64px | Large module separation |

**Mobile Spacing Specification**:

| Spacing Value | Applicable Scenarios |
|---------------|---------------------|
| 4px | Fine internal spacing adjustments between icons, labels, numbers and text |
| 8px | Standard spacing between common components like list items, button groups, information rows |
| 12px | Secondary separation within same-group content, making content transitions smoother |
| 16px | Regular separation between independent modules, balancing clarity and page density |
| 24px | Between page large blocks, separating primary and secondary levels, giving information more breathing room |

> **Breathing Room Principle**: Use spacing reasonably (4/8/12/16/24px) to avoid page crowding. When spacing ratio >= 3:1, group perception significantly enhances.

### 4.2 Spacing Semantic Layering

Nathan Curtis's three-layer spacing strategy has become industry best practice:

| Layer | Spacing Range | Purpose | Examples |
|-------|---------------|---------|----------|
| **Intra-component** | 4/8/12px | Internal element spacing | Button internal padding, icon and text spacing |
| **Inter-component** | 16/24px | Same-group component spacing | Form field spacing, list item spacing |
| **Layout** | 32/48/64px | Block/page-level spacing | Card spacing, block spacing |

### 4.3 Spacing Semantic Naming Strategy

Numerical naming suits Primitive layer, semantic naming suits Semantic layer (recommended):

| Semantic Token | Compact Mode | Default Mode | Comfortable Mode | Purpose |
|----------------|-------------|--------------|------------------|---------|
| `space.compact` | 4px | 8px | 12px | Compact mode |
| `space.default` | 12px | 16px | 20px | Default mode |
| `space.comfortable` | 20px | 24px | 32px | Comfortable mode |
| `space.loose` | 28px | 32px | 40px | Loose mode |

> **Density is a scene attribute, not a platform attribute**: Different pages on the same platform can use different densities (e.g., Dashboard uses Compact, detail page uses Comfortable).

### 4.4 Gestalt Proximity Quantification

| Element Spacing | Perceived Grouping | Application Scenarios |
|-----------------|-------------------|----------------------|
| < 8px | Same group | Icon+text, label+value |
| 8-16px | Related group | Form fields, list items |
| > 24px | Independent group | Block separation, card spacing |

> When spacing ratio >= 3:1, group perception significantly enhances.

### 4.5 Responsive Breakpoint Standards

| Breakpoint Name | Width Range | Columns | Gutter | Margin | Touch Target |
|-----------------|-------------|---------|--------|--------|--------------|
| **xs** | < 480px | 4 | 16px | 16px | 44-48px |
| **sm** | 480-639px | 4 | 16px | 16px | 44-48px |
| **md** | 640-767px | 8 | 16-24px | 24px | 44-48px |
| **lg** | 768-1023px | 8 | 24px | 24px | 36-44px |
| **xl** | 1024-1439px | 12 | 24px | 32px | 36-44px |
| **2xl** | >= 1440px | 12 | 24-32px | 32px | 36-44px |

> **768px (lg) is the consensus breakpoint for all systems**, corresponding to iPad portrait. Academic research supports 3-5 breakpoints as optimal.

### 4.6 Layout Pattern Classification

Component arrangement in grid systems follows 6 basic layout patterns:

| Pattern | Description | Applicable Scenarios | Representative Components |
|---------|-------------|---------------------|--------------------------|
| **Stack** | Vertical/horizontal equal-distance arrangement | Lists, button groups | VStack / HStack |
| **Inline** | Horizontal arrangement, automatic wrapping | Tags, filters | Tag Group / Breadcrumb |
| **Grid** | Two-dimensional grid layout | Card lists, galleries | Data Table / Gallery |
| **Box** | Fixed aspect ratio container | Images, videos | Aspect Ratio Box |
| **Center** | Horizontal and vertical centering | Empty states, loading pages | Empty State / Spinner |
| **Bleed** | Breaking container margins | Full-width Banners, Hero images | Hero Banner / Full-width CTA |

### 4.7 Asymmetric Margins and Maximum Width Constraints

| Breakpoint | Left/Right Margin | Actual Behavior |
|------------|-------------------|-----------------|
| Mobile | 16px | Fixed margin |
| Tablet | 24px | Fixed margin |
| Desktop | 32px | Fixed margin |
| Large Desktop | 32px | Fixed margin |
| Max (>1440px) | Auto centering | Content area max width [e.g., 1200px], auto white space on both sides |

> **Key Rule**: Maximum width constraint is an implicit constraint of the grid system; beyond it, content no longer expands. This is **"Constrained Responsive"**.

### 4.8 Page Layout Psychology Guidelines

> The following is a summary of psychological foundations for layout design; detailed discussion see `UI Design Specification Systematic Research Report.md` §4.8.

| Psychological Principle | Layout Implications |
|------------------------|---------------------|
| Cognitive Load Theory | Progressive disclosure, chunking (4-7 items per group), consistency reduces extraneous load |
| F-shaped Reading Pattern | Core information in top-left and first two lines; keywords at beginning of each line |
| Z-shaped Reading Pattern | Logo top-left, CTA top-right, core visual center, secondary CTA bottom-right |
| Hick's Law | Main navigation items limited to 3-5, only 1 primary CTA per screen |
| Fitts's Law | Mobile touch targets >= 44x44pt, high-frequency operations near natural finger positions |
| Von Restorff Effect | Important elements stand out through contrast with surroundings via color/size/position

---

## 5. Components & Interaction

> Each component must define: **Anatomy**, **All States**, **Behavior**, **Tokens Used**, **Do & Don't**

### 5.1 Component State Machine Specification

Each interactive component must define a complete state machine to ensure deterministic and testable behavior.

**Standard State Matrix**:

| State | Visual Representation | Trigger Condition | Exit Condition | Accessibility Requirements |
|-------|----------------------|-------------------|----------------|---------------------------|
| **Default** | Base style | Initial state | Any interaction | Focusable |
| **Hover** | Background overlay 5% (Light) / 5% (Dark) | Mouse enter | Mouse leave | Desktop only |
| **Pressed** | Background overlay 10% (Light) / 10% (Dark) | Press | Release | — |
| **Focus** | 2px focus ring | Tab/click | Tab out/Escape | Must be visible, contrast >= 3:1 |
| **Disabled** | 38% opacity | `disabled=true` | `disabled=false` | `aria-disabled="true"` |
| **Loading** | Spinner + disabled interaction | `isLoading=true` | Request complete/failed | `aria-busy="true"` |
| **Error** | Red border + error message | Validation failed | Correct input | `aria-invalid="true"` |
| **Success** | Green border/icon | Operation success | Auto-recover after 2s | `aria-live="polite"` |

**Global Interaction Overlay**:

All components' hover/active states use unified opacity overlay to ensure visual consistency:

| State | Light Mode | Dark Mode | CSS Implementation |
|-------|------------|-----------|-------------------|
| **Hover** | `rgba(0,0,0,0.05)` | `rgba(255,255,255,0.05)` | `background-color: color-mix(in srgb, currentColor 5%, transparent)` |
| **Active** | `rgba(0,0,0,0.1)` | `rgba(255,255,255,0.1)` | `background-color: color-mix(in srgb, currentColor 10%, transparent)` |
| **Focus** | `2px solid var(--color-border-focus)` | Same as left | Outline, not background overlay |

> **Immediate Feedback Rule**: Hover response delay 0ms (no `transition-delay`), Focus ring display 0ms. Only displacement/scaling animations allow 150-200ms transitions.

**State Transition Rules**:
- Disabled state only allows `Disabled → Default` transition, other interactions prohibited
- Loading state prohibits Hover/Pressed transitions
- Error state must provide specific error messages, prohibiting only "operation failed" display
- State transitions must have corresponding visual feedback, no silent transitions

### 5.2 Button

#### Anatomy
```
[Icon (optional)] + [Text Label] + [Loading Icon (optional)]
```
- Height specification: `size.sm` = 32-36px (text buttons), `size.md` = 40-44px (secondary buttons), `size.lg` = 48-52px (primary buttons)
- Border radius: `radius.md` = 8px (most common on mobile), determined by brand tone, also 4px/6px/999px
- Minimum tap target: >= 44 x 44px (mandatory for touch devices)

**Button Size Specification**:

| Button Type | Height | Border Radius | Purpose |
|-------------|--------|---------------|---------|
| **Primary** | 48-52px | 8px | Page core CTA, maximum 1 per page |
| **Secondary** | 40-44px | 8px | Secondary actions, cancel |
| **Text** | 32-36px | 0-4px | Low priority, toolbar |

> **Mobile Button Specification**: Primary button height 48-52px, ensure comfortable finger tapping; secondary buttons 40-44px, text buttons 32-36px. All buttons minimum tap target >= 44x44px.

#### Type Variants
| Type | Background Token | Text Token | Border Token | Usage Scenarios |
|------|-----------------|------------|--------------|-----------------|
| **Primary (Solid)** | `color.brand-600` | `color.text.on-brand` | None | Page primary action, maximum 1 per page |
| **Secondary (Outline)**| Transparent | `color.brand-600` | `color.brand-600` | Secondary actions, cancel |
| **Tertiary (Ghost)** | Transparent | `color.brand-600` | None | Low priority, toolbar |
| **Danger** | `color.semantic.error` | `color.text.on-danger` | None | Delete, irreversible operations |
| **Text (Pure Text)** | Transparent | `color.brand-600` | None | Links, in-table operations |

#### Interaction States
All buttons must define the following 7 states:

| State | Visual Representation | Token Changes | Trigger Condition |
|-------|----------------------|---------------|-------------------|
| **Default** | Default style | `color.brand-600` | No interaction |
| **Hover** | Background overlay 5% (using global overlay) | `color.brand-500` | Mouse hover |
| **Pressed / Active** | Background overlay 10% (using global overlay), Y-axis offset down 1px | `color.brand-700` | Mouse press/touch press |
| **Focus** | Outer frame 2px focus ring, offset 2px | `color.border.focus` | Keyboard Tab focus |
| **Disabled** | Background light gray, text `text.disabled`, no Hover effect | `color.background.disabled` | When not clickable |
| **Loading** | Background maintained, text hidden, Spinner displayed (not responding to clicks)| — | During async request |
| **Success** | Briefly change to green background + checkmark icon, recover or redirect after 1.5s | `color.semantic.success` | Operation success feedback |

#### Interaction Details
- **Hover delay**: No delay, immediate response (0ms)
- **Pressed feedback**: Provides `transform: translateY(1px)` physical press feel
- **Focus visibility**: Must meet 3:1 contrast, hiding outline prohibited
- **Loading state**: Button width unchanged to prevent layout jitter; Spinner size = text height x 0.8
- **Debouncing**: On consecutive clicks, only first triggers until state changes

---

### 5.3 Input / TextField

#### State Definition
| State | Border | Background | Placeholder Text |
|-------|--------|------------|------------------|
| **Default** | `color.border.default` | `color.background.surface` | `color.text.placeholder` |
| **Hover** | `color.border.hover` (deepened) | No change | No change |
| **Focus** | `color.brand-600` (2px, brand color) | `color.background.default` | No change |
| **Filled** | `color.border.default` | No change | Move up/shrink as Label (Floating Label mode) |
| **Error** | `color.semantic.error` | `color.semantic.error.subtle` | Display error icon + error text |
| **Disabled**| `color.border.disabled` | `color.background.disabled` | `color.text.disabled` |
| **Read-only** | Dashed border `border-dashed` | No change | No change |

#### Interaction Logic
- **Focus animation**: Border color transition `transition: border-color 200ms ease-out`
- **Error state**: Triggers validation on blur; error text appears below input field, font size `font.body.small`, color `color.semantic.error`
- **Clear button**: When hovering input field, clear icon appears on right (only when content exists and not Disabled)
- **Password visibility toggle**: Click eye icon to toggle `type="password/text"`, icon color changes to `color.brand-600` on Active

---

### 5.4 Card

#### Layering and Shadows
| Layer | Background Token | Shadow Token | Purpose |
|-------|-----------------|--------------|---------|
| **Rest** | `color.background.surface` | `shadow.sm` (`0 1px 2px rgba(0,0,0,0.05)`) | Default display |
| **Hover** | No change | `shadow.md` (`0 4px 12px rgba(0,0,0,0.1)`) | Clickable card hover |
| **Pressed**| No change | `shadow.sm` + downward offset 1px | Press |
| **Selected** | `color.background.selected` | `shadow.md` + border `color.brand-600` | Selected state |

#### Interaction Logic
- **Hover elevation**: Shadow deepens + slight scale `scale(1.01)`, transition 200ms ease-out
- **Click area**: When entire card is tap target, must include clear focus ring
- **Internal operations**: If card has independent buttons (e.g., "Edit"), use `z-index` to ensure events don't bubble

---

### 5.5 Navigation

#### Top Navigation
- **Height**: 56px / 64px (desktop)
- **Background**: `color.background.surface` (Light) or `color.neutral-100` (Dark)
- **Logo area**: Left side, width `space.16` (64px)
- **Menu items**:
  - Default: `color.text.secondary`
  - Hover: `color.text.primary` + bottom 2px indicator bar (`color.brand-600`)
  - Active/Selected: `color.text.primary` + indicator bar persistent
  - Focus: Outer frame focus ring
- **Navigation item count**: Limited to 3-5 items (Hick's Law sweet spot)

#### Side Navigation
- **Width**: 200px (expanded) / 64px (collapsed)
- **Background**: `color.background.surface` (one level deeper than page background, following Layering Model)
- **Selected item**: Background `color.background.selected`, text `color.text.primary`, left 3px vertical bar `color.brand-600`
- **Hover**: Background `color.background.hover`, no left vertical bar
- **Collapse animation**: Width change `transition: width 250ms cubic-bezier(0.4, 0, 0.2, 1)`

---

### 5.6 Feedback Components

#### Toast / Notification
| Type | Background | Left Vertical Bar/Icon | Duration |
|------|------------|------------------------|----------|
| **Info** | `color.background.surface` | `color.semantic.info` | 3s |
| **Success** | `color.background.surface` | `color.semantic.success` | 3s |
| **Warning** | `color.background.surface` | `color.semantic.warning` | 5s (requires user attention) |
| **Error** | `color.background.surface` | `color.semantic.error` | No auto-dismiss (requires manual close) |

#### Interaction Logic
- **Entry**: Slide in from right (`translateX(100%) → 0`), 300ms, `cubic-bezier(0.4, 0, 0.2, 1)`
- **Exit**: Fade out upward (`translateY(-10px) + opacity 0`), 200ms
- **Hover pause**: When mouse hovers, countdown pauses; continues after leaving
- **Stacking**: Maximum 3 displayed, new Toast pushes old Toast upward, spacing `space.3`

---

## 6. Iconography

### 6.1 Icon Specification

| Specification Item | Standard | Description |
|-------------------|----------|-------------|
| Icon style | [Outline / Filled] | Provide Outline + Filled variants for same-function icons |
| Default size | 24px | Icon grid 24dp bounding box |
| Stroke width | 2dp | Material Design standard |
| Naming rule | `{category}-{name}-{variant}` | e.g., `nav-arrow-left-filled` |
| Implementation | SVG sprite preferred over icon font | Performance/accessibility/maintainability |

### 6.2 Icon Size Tokens

| Token | Value | Purpose |
|-------|-------|---------|
| `icon.size.xs` | 12px | Compact inline icons |
| `icon.size.sm` | 16px | In-table icons, auxiliary icons |
| `icon.size.md` | 20px | In-button icons |
| `icon.size.lg` | 24px | Default icons (navigation bar, lists) |
| `icon.size.xl` | 32px | Empty state icons |
| `icon.size.2xl` | 48px | Onboarding page icons |
| `icon.size.3xl` | 64px | Large display icons |

> **Mobile Icon Specification**: Common sizes 16/20/24/32/48/64px, can be flexibly used in navigation bars, lists, buttons and prompts according to actual scenarios.

### 6.3 Drawing Grid

- Determine grid and safe area before drawing icons
- Recommended to use frame, center line and circular baseline to assist drawing
- Maintain graphic proportions and visual balance, reduce center of gravity offset
- Ensure clarity and stability at different sizes

### 6.3 Live Area and Trim Area

| Canvas Size | Live Area | Trim Area | Description |
|-------------|-----------|-----------|-------------|
| 16x16px | 14x14px | 1px | High-density icons |
| 20x20px | 16x16px | 2px | Font Awesome 7 |
| 24x24px | 20x20px | 2px | Material Design |
| 32x32px | 28x28px | 2px | IBM |

- **Live Area** is the actual drawing area for icon content
- **Trim Area** is the safe margin to prevent icon clipping
- All icon elements must **align to pixel grid** (use integer coordinates)

### 6.4 currentColor Strategy

Icons should use `currentColor` or semantic Tokens for filling, not hardcoded colors:

```css
.icon {
  fill: var(--icon-color-primary, currentColor);
}
```

### 6.5 Icon Accessibility

- Decorative icons: `aria-hidden="true"`
- Functional icons: require `aria-label` to describe functionality
- Icon button minimum size: 24x24px (WCAG 2.2 AA), recommended 32x32px

---

## 7. Elevation System

### 7.1 Elevation Levels

| Elevation Level | Shadow Value | Purpose |
|-----------------|--------------|---------|
| 0dp | No shadow | Page base color, flat content |
| 1dp | `0 1px 2px rgba(0,0,0,0.1)` | Cards (default state) |
| 3dp | `0 2px 4px rgba(0,0,0,0.1)` | Cards (hover state), input fields |
| 8dp | `0 4px 8px rgba(0,0,0,0.12)` | Pop-up menus, dropdowns |
| 12dp | `0 6px 12px rgba(0,0,0,0.15)` | Floating buttons |
| 24dp | `0 12px 24px rgba(0,0,0,0.2)` | Modals, dialogs |

### 7.2 Shadow + Surface Dual Expression

Shadow and Surface must be used in pairs; cannot mix different levels of Shadow and Surface:

| Elevation Level | Surface Token | Shadow Token | Purpose |
|-----------------|---------------|--------------|---------|
| **Sunken** | `elevation.surface.sunken` | None | Lowest layer, e.g., Kanban column background |
| **Default** | `elevation.surface` | None | Baseline layer, e.g., page content |
| **Raised** | `elevation.surface.raised` | `elevation.shadow.raised` | Movable cards |
| **Overlay** | `elevation.surface.overlay` | `elevation.shadow.overlay` | Modals, dropdown menus |

> **Dark Mode**: Shadows are nearly invisible, so **Surface color must lighten with elevation level** to compensate.

### 7.3 Z-index Token System

| Token | Value | Purpose |
|-------|-------|---------|
| `--z-base` | 0 | Default content |
| `--z-dropdown` | 100 | Dropdown menus |
| `--z-sticky` | 200 | Sticky headers |
| `--z-overlay` | 300 | Overlay layers |
| `--z-modal` | 400 | Modals |
| `--z-toast` | 500 | Toast notifications |

> **Key Rule**: z-index values should increment in jumps (at least +50 or +100 each time) to reserve space for intermediate levels.

---

## 8. Shape System

### 8.1 Border Radius Tokens

| Token | Value | Purpose |
|-------|-------|---------|
| `--radius-none` | 0 | Tables, divided containers, strong order information areas |
| `--radius-xs` | 2px | Small elements |
| `--radius-sm` | 4px | Input fields, labels, lightweight buttons and other small components |
| `--radius-md` | 8px | Buttons, cards, small popovers (**most common on mobile**) |
| `--radius-lg` | 12px | Content cards, floating panels, information module containers |
| `--radius-xl` | 16px | Large cards, bottom sheets, emphasis display areas |
| `--radius-full` | 9999px | Circular avatars, capsule buttons |
| `--radius-pill` | 9999px | Capsule buttons (alias for `--radius-full`) |

> **Mobile Border Radius Specification**: 8px is the most common border radius on mobile, applicable to buttons, cards, small popovers. 12px for content cards and floating panels, 16px for large cards and bottom sheets.

### 8.2 Nested Border Radius Golden Formula

`Inner Radius = Outer Radius - Padding`

```css
.parent {
  --radius: 24px;
  --padding: 12px;
  border-radius: var(--radius);
  padding: var(--padding);
}

.child {
  border-radius: calc(var(--radius) - var(--padding)); /* = 12px */
}
```

> **Key Rule**: If the calculation result is negative, child elements should maintain their own border radius Token, not forcibly apply the formula.

---

## 9. Motion & Micro-interactions

### 9.1 Easing Curves

#### Productive vs Expressive Dual-track System

| Scenario | Productive Easing (Functional) | Expressive Easing (Emotional) |
|----------|-------------------------------|-------------------------------|
| Standard | `cubic-bezier(0.2, 0, 0.38, 0.9)` | `cubic-bezier(0.4, 0.14, 0.3, 1)` |
| Entrance | `cubic-bezier(0, 0, 0.38, 0.9)` | `cubic-bezier(0, 0, 0.3, 1)` |
| Exit | `cubic-bezier(0.2, 0, 1, 0.9)` | `cubic-bezier(0.4, 0.14, 1, 1)` |

- **Productive** for functional animations (fast, direct, not distracting)
- **Expressive** for emotional animations (smooth, with brand personality)
- Same component's "entrance" and "exit" should use different Easing: entrance uses Expressive, exit uses Productive

### 9.2 Duration Specification

| Token | Value | Purpose |
|-------|-------|---------|
| `duration.fast-01` | 70ms | Micro-interactions (buttons, toggles) |
| `duration.fast-02` | 110ms | Micro-interactions (fade in/out) |
| `duration.moderate-01` | 150ms | Small expansions, short-distance movements |
| `duration.moderate-02` | 240ms | Expansions, system notifications, Toast |
| `duration.slow-01` | 400ms | Large expansions, important system notifications |
| `duration.slow-02` | 700ms | Background dimming |

### 9.3 Duration Scalar Global Speed Control Mechanism

All Duration Tokens must be multiplied by `duration-scalar`, which is the only correct way to implement `prefers-reduced-motion`:

```css
:root {
  --duration-scalar: 1; /* Normal speed */
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-scalar: 0; /* Completely disabled */
  }
}
```

> Components that manually set fixed durations without using scalar will not respond to users' reduced motion preferences.

### 9.4 Response Time Thresholds

| Threshold | User Perception | Design Strategy |
|-----------|-----------------|-----------------|
| < 100ms | Instant | No wait indicator needed |
| 100-300ms | Smooth | Micro-animation feedback |
| 300ms-1s | Acceptable delay | Spinner / progress indicator |
| 1-5s | Noticeable wait | Skeleton screen + progress bar |
| > 5s | Long wait | Percentage progress + estimated time |

### 9.5 Skeleton Screen vs Spinner Decision Tree

| Wait Time | Strategy |
|-----------|----------|
| 0-300ms | No wait indicator |
| 300ms-1s | In-button Spinner / micro progress indicator |
| 1s-5s | Skeleton screen + top progress bar |
| > 5s | Skeleton screen + percentage progress + estimated time |

### 9.6 Haptic Feedback Standards (Mobile)

| Scenario | Duration | Type |
|----------|----------|------|
| Button confirmation | 10-15ms | Impact Light |
| Selection change | 5-10ms | Selection |
| Long press trigger | 15-20ms | Impact Medium |
| Success notification | 50-100ms | Notification Success |
| Error notification | 100-200ms | Notification Error |

### 9.7 Common Animation Patterns

| Pattern | Rules | Examples |
|---------|-------|----------|
| **Fade** | Opacity 0 → 1, paired with Enter/Exit easing | Toast entry, Tooltip |
| **Slide** | TranslateY/X ±8-16px | Dropdown menus, drawer expansion |
| **Scale** | Scale 0.95 → 1.0, paired with Fade | Modal pop-up, menus |
| **Ripple** | Water ripple expansion from click position, primary color 20% opacity | Material style buttons (optional) |

### 9.8 Animation Parameter Supplement

| Property | Recommended Value | Description |
|----------|-------------------|-------------|
| Displacement distance | 4-8px | Slight movement feedback |
| Scale ratio | 0.95-1.05 | Press/release effect |
| Spring animation | Spring (damping: 0.7-0.9) | Pull-to-refresh, drag release |
| Performance constraint | Only animate `transform` and `opacity` | Avoid layout thrashing |

---

## 10. Accessibility Specification

### 10.1 Contrast Standards

- **Body text (< 18px or non-bold)**: Contrast with background >= 4.5:1 (WCAG AA)
- **Large text (>= 18px or bold >= 14px)**: Contrast with background >= 3:1
- **UI components/icons**: Contrast with adjacent colors >= 3:1
- **Focus ring**: Contrast with background >= 3:1, thickness >= 2px

### 10.2 Dual Encoding Principle (Mandatory Requirement)

All state changes must use at least **two encoding methods** (color+icon, color+text, color+shape). This is a **Level A compliance mandatory requirement**, not an optional best practice.

| Scenario | Wrong Approach | Correct Approach |
|----------|---------------|------------------|
| Error state | Red border only | Red border + error icon + error text |
| Success state | Green background only | Green background + checkmark icon + success text |
| Disabled state | Gray only | Gray + reduced opacity + disabled cursor |
| Link | Blue only | Blue + underline + hover state |

### 10.3 Focus Management

- All interactive elements must have visible focus indicators
- Focus ring style: `2px solid color.brand-600` (Light) / `color.brand-400` (Dark), `offset: 2px`, border radius follows component
- **Prohibited**: Using only color changes to indicate focus; must be paired with outline
- On dark backgrounds, default Focus color may be invisible; need to switch to white Focus
- Focus trap when modal opens, focus returns to trigger element after closing

### 10.4 Halation Effect Handling

Astigmatic users reading white text on dark backgrounds experience "halos," making text appear thicker and blurrier. Solutions:

- Use **non-pure-white text color** (`#E0E0E0` instead of `#FFFFFF`)
- Increase **font weight** (from 400 to 500)
- Increase **line height** (from 1.5 to 1.6-1.7)

### 10.5 Keyboard Navigation

- All interactive elements can be operated via Tab / Enter / Space / Esc
- Dynamic content uses `aria-live="polite"` or `"assertive"`
- Custom components use `role` + `aria-*` annotations
- All images have `alt`, icons have `aria-label`, forms have `<label>`

### 10.6 Reduced Motion Preference

- Adapt to `prefers-reduced-motion: reduce` media query
- Implemented through Duration Scalar mechanism (see §9.3)
- High contrast mode adapts to `prefers-contrast: more` media query

### 10.7 Touch Target

| Platform | Minimum Touch Area | Adjacent Spacing |
|----------|-------------------|------------------|
| iOS | 44 x 44pt | >= 8px |
| Android | 48 x 48dp | >= 8px |
| Web (mobile) | 44 x 44px | >= 8px |
| Web (desktop) | 24-32px | >= 4px |

### 10.8 Text Scaling

- Support 200% text scaling without losing content (WCAG 2.1 SC 1.4.4)
- Test layout usability at Dynamic Type maximum font size

---

## 11. Cross-Platform Specification

### 11.1 Cross-Platform Strategy

Recommended **"Brand Consistent + Interaction Native"** hybrid strategy:

1. **Brand layer consistent**: Colors, fonts, icon styles, spacing ratios unified across platforms
2. **Interaction layer native**: Navigation paradigms, gesture operations, popup forms, back logic follow each platform's specifications
3. **Component layer adapted**: Same component maintains visual consistency across platforms but interaction methods adapt to platform

### 11.2 Design Base Dimensions

| Platform | Canvas Width | Description |
|----------|-------------|-------------|
| **iOS** | 375px (iPhone standard) | @1x baseline, @2x/@3x adaptation |
| **Android** | 360px (mainstream models) | mdpi baseline, xxxhdpi adaptation |
| **Web** | 1440px (desktop) | Responsive baseline, adapting down to mobile |

> **Core Principle**: One design adapts to multiple platforms, prioritizing layout adaptation capability. iOS and Android canvas width difference is only 15px, automatically adapted through fluid layout (Flex/Grid).

**Fixed Component Height Specification**:

| Component | iOS Height | Android Height | Description |
|-----------|------------|----------------|-------------|
| Status bar | 44pt | 24dp | Top system status bar |
| Navigation bar | 44pt | 56dp | Page navigation title bar |
| Bottom Tab bar | 50pt | 56dp | Bottom tab navigation |
| Bottom safe area | 34pt | 48dp | Home Indicator / gesture navigation area |

### 11.3 Mobile vs Desktop Size Specification

| Dimension | Mobile | Desktop | Description |
|-----------|--------|---------|-------------|
| Minimum touch target | 44-48px | 24-32px | Mouse precision higher than finger |
| Element spacing | 8-16px | 4-8px | Mobile needs to prevent accidental touches |
| Button height | 48-56px | 32-40px | Mobile needs larger touch area |
| Input field height | 48-56px | 36-44px | Mobile needs larger click area |
| List item height | 56-72px | 40-48px | Mobile needs larger line height |
| Navigation depth | Within 3 levels | Multiple nesting | Mobile cognitive load limitation |
| Content display | Single column, vertical scrolling | Multiple columns, grid, sidebar | Screen space difference |
| Operation exposure | Hidden (menu, more) | Directly exposed (toolbar) | Space constraint difference |
| Form design | Step-by-step, few fields per page | Long forms, multi-column layout | Mobile input cost high |
| Modal usage | Full-screen modals mainly | Centered popups, side drawers | Screen space difference |

### 11.4 Interaction Differences

| Dimension | iOS | Android | Web |
|-----------|-----|---------|-----|
| Hover state | None (touch device) | None (touch device) | Yes (mouse hover) |
| Press feedback | Highlight dimmed 70% | Ripple water ripple | Background darkened + Y offset |
| Haptic feedback | Taptic Engine | HapticFeedback | Vibration API (limited) |
| Back gesture | Edge swipe right (full system) | Predictive back (Android 14+) | Browser back (no gesture) |
| Long press feedback | Context menu + haptic | Context menu + Ripple | Right-click menu (no haptic) |

> **Key Rule**: Touch devices have no Hover state, so **all functionality cannot rely on Hover exposure**. DS must provide **equivalent operation paths** for each input mode.

### 11.5 Safe Area Constraints

| Platform | Top Safe Area | Bottom Safe Area | Side Safe Area |
|----------|---------------|------------------|----------------|
| iOS (Notch) | 44pt | 34pt (Home Indicator) | 0pt |
| iOS (Dynamic Island) | 59pt | 34pt | 0pt |
| Android (Full screen) | 24dp | 48dp (gesture navigation) | 0dp |
| Android (Three-button navigation) | 24dp | 0dp | 0dp |

> Bottom fixed buttons must be located **above the safe area**. Web's `env(safe-area-inset-*)` CSS variables can handle this automatically.

### 11.6 Density Token Control

| Density Mode | Mobile | Desktop | Applicable Scenarios |
|--------------|--------|---------|---------------------|
| **Compact** | Not recommended | Data-intensive backends | Recommended for keyboard/mouse devices |
| **Default** | Recommended | General scenarios | General recommendation |
| **Comfortable** | Reading apps | Display pages | Recommended for touch devices |

> Density changes affect **three dimensions: spacing, font size, component size**; cannot only change spacing.

---

## 12. Brand Token Mapping

> This section is a project mandatory requirement, defining the mapping relationship from brand color system to Design Tokens. Adopting single brand color strategy.

### 12.1 Brand Color System Definition

| Brand Color | Hex Value | Semantics | Usage Scenarios |
|-------------|-----------|-----------|-----------------|
| [Primary Brand Color Name] | [Hex] | Brand identification, call to action | Primary buttons, Logo, navigation active state, links, icon emphasis |

> **Single Brand Color Constraint**: Only define 1 brand color; auxiliary emphasis sourced from semantic and neutral palettes. Brand color coverage <= 10%.

### 12.2 Brand Color Gradient Expansion

> Define 9 gradient levels (50-900) for brand color, with level 600 as base color.

#### [Primary Brand Color Name] Gradient

| Gradient | Hex Value | Purpose |
|----------|-----------|---------|
| `[Primary]-50` | [Hex] | Very light background, hover base color |
| `[Primary]-100` | [Hex] | Light background, selected state base color |
| `[Primary]-200` | [Hex] | Light decorative elements |
| `[Primary]-300` | [Hex] | Secondary icons, auxiliary text |
| `[Primary]-400` | [Hex] | Medium emphasis |
| `[Primary]-500` | [Hex] | Hover state, chart auxiliary colors |
| `[Primary]-600` | [Hex] | **Base color (default)** |
| `[Primary]-700` | [Hex] | Pressed/Active state |
| `[Primary]-800` | [Hex] | Dark text (on-light) |
| `[Primary]-900` | [Hex] | Very dark decoration, dark background emphasis |

### 12.3 CSS Variable Mapping

Brand Tokens (`--sin-s-*`) map to component Tokens (`--sin-c-{module}-*`):

```css
:root {
  /* ===== Brand Tokens (Semantic Layer) ===== */
  --sin-s-brand: [Primary Hex];
  --sin-s-brand-hover: [Primary-500 Hex];
  --sin-s-brand-pressed: [Primary-700 Hex];
  --sin-s-brand-subtle: [Primary-50 Hex];
  --sin-s-brand-contrast: [Primary-800 Hex];

  /* ===== Component Tokens (Component Layer) ===== */
  /* --sin-c-{module}-* naming convention */

  /* Button */
  --sin-c-btn-primary-bg: var(--sin-s-brand);
  --sin-c-btn-primary-bg-hover: var(--sin-s-brand-hover);
  --sin-c-btn-primary-bg-pressed: var(--sin-s-brand-pressed);
  --sin-c-btn-primary-text: [on-brand Hex];
  --sin-c-btn-secondary-bg: transparent;
  --sin-c-btn-secondary-border: var(--sin-s-brand);
  --sin-c-btn-secondary-text: var(--sin-s-brand);
  --sin-c-btn-danger-bg: var(--sin-s-semantic-error);
  --sin-c-btn-danger-text: [on-danger Hex];

  /* Navigation */
  --sin-c-nav-active-indicator: var(--sin-s-brand);
  --sin-c-nav-bg: var(--sin-s-brand-subtle);

  /* Input */
  --sin-c-input-border-focus: var(--sin-s-brand);

  /* Card */
  --sin-c-card-bg: [Hex];
  --sin-c-card-bg-surface: var(--sin-s-brand-subtle);

  /* Text */
  --sin-c-text-primary: [Hex];
  --sin-c-text-secondary: [Hex];
  --sin-c-text-on-brand: [on-brand Hex];
  --sin-c-text-link: var(--sin-s-brand);

  /* Border */
  --sin-c-border-default: [Hex];
  --sin-c-border-focus: var(--sin-s-brand);

  /* Background */
  --sin-c-bg-default: [Hex];
  --sin-c-bg-surface: var(--sin-s-brand-subtle);
  --sin-c-bg-page: var(--sin-s-brand-subtle);

  /* Shadow */
  --sin-c-shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --sin-c-shadow-md: 0 4px 12px rgba(0,0,0,0.1);

  /* Spacing */
  --sin-c-space-1: 4px;
  --sin-c-space-2: 8px;
  --sin-c-space-4: 16px;
  --sin-c-space-6: 24px;

  /* Radius */
  --sin-c-radius-sm: 4px;
  --sin-c-radius-md: 8px;
  --sin-c-radius-full: 9999px;
  --sin-c-radius-pill: var(--sin-c-radius-full);
}

[data-theme="dark"] {
  --sin-s-brand: [Primary Dark Hex];
  --sin-s-brand-hover: [Primary-400 Dark Hex];
  --sin-s-brand-pressed: [Primary-600 Dark Hex];
  --sin-s-brand-subtle: [Primary-900 Dark Hex];
  --sin-s-brand-contrast: [Primary-200 Dark Hex];

  --sin-c-text-primary: [Hex];
  --sin-c-bg-default: [Hex];
  --sin-c-bg-surface: [Hex];
  --sin-c-bg-page: [Hex];
  --sin-c-border-default: [Hex];
  --sin-c-border-focus: var(--sin-s-brand);
  /* ... other Token overrides */
}

/* Dark mode auto-detection: follow system preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --sin-s-brand: [Primary Dark Hex];
    --sin-s-brand-hover: [Primary-400 Dark Hex];
    --sin-s-brand-pressed: [Primary-600 Dark Hex];
    --sin-s-brand-subtle: [Primary-900 Dark Hex];
    --sin-s-brand-contrast: [Primary-200 Dark Hex];

    --sin-c-text-primary: [Hex];
    --sin-c-bg-default: [Hex];
    --sin-c-bg-surface: [Hex];
    --sin-c-bg-page: [Hex];
    --sin-c-border-default: [Hex];
    --sin-c-border-focus: var(--sin-s-brand);
    /* ... other Token overrides */
  }
}
```

---

## 13. Visual Examples: Do & Don't

### 13.1 Color Usage

| Do | Don't |
|----|-------|
| Only 1 primary button per page, for the most critical CTA | More than 3 solid brand color buttons on same page |
| Error text paired with error icon + error text (dual encoding) | Only using red text to indicate error, no other prompts |
| Using `color.text.inverse` on dark backgrounds (not pure white, avoid Halation) | Continuing to use dark text or pure white `#FFFFFF` on dark backgrounds |
| Following Layering Model, cards use Surface color | Stacking pure white cards on white background, no hierarchy distinction |
| Brand color only for interactive elements (buttons, links, icons) | Brand color for large backgrounds or non-interactive decoration |
| Brand color coverage <= 10% | Brand color coverage > 10% causing visual heaviness |
| Using level 600 as base color | Using 400 or 500 as base color (insufficient contrast) |

### 13.2 Interaction Design

| Do | Don't |
|----|-------|
| Disabled buttons provide Tooltip explaining reason | Disabled buttons with no prompts, user confusion |
| Form errors provide immediate feedback on blur | Only exposing all errors at submission |
| Async operations provide Loading / Skeleton state | Button click with no feedback, user unsure if effective |
| Destructive operations require second confirmation (popup/re-click) | Delete button executes directly, no confirmation |
| Focus ring uses outline + contrast >= 3:1 | Only using color changes to indicate focus |
| All state changes use dual encoding (color+icon/text) | Only using color to convey state information |

### 13.3 Cross-Platform Design

| Do | Don't |
|----|-------|
| Brand layer consistent + interaction layer native | All platforms with identical interaction methods |
| Mobile touch targets >= 44px | Desktop dimensions directly used on mobile |
| Functionality not dependent on Hover exposure | Key operations only shown in Hover state |
| Bottom buttons located above safe area | Content flush against screen edges |

---

## 14. Appendix

### 14.1 Token Code Reference (CSS Variables)

```css
:root {
  /* Brand (Primitive Layer) */
  --[PrimaryName]-50: [Hex];
  --[PrimaryName]-100: [Hex];
  --[PrimaryName]-200: [Hex];
  --[PrimaryName]-300: [Hex];
  --[PrimaryName]-400: [Hex];
  --[PrimaryName]-500: [Hex];
  --[PrimaryName]-600: [Hex];
  --[PrimaryName]-700: [Hex];
  --[PrimaryName]-800: [Hex];
  --[PrimaryName]-900: [Hex];

  /* Semantic - Brand (Single Brand Color) */
  --color-brand: var(--[PrimaryName]-600);
  --color-brand-hovered: var(--[PrimaryName]-500);
  --color-brand-pressed: var(--[PrimaryName]-700);
  --color-brand-subtle: var(--[PrimaryName]-50);
  --color-brand-contrast: var(--[PrimaryName]-800);

  /* Semantic - Functional */
  --color-semantic-success: [Hex];
  --color-semantic-warning: [Hex];
  --color-semantic-error: [Hex];
  --color-semantic-info: var(--color-brand);

  /* Semantic - Neutral */
  --color-neutral-50: [Hex];
  --color-neutral-100: [Hex];
  --color-neutral-900: [Hex];

  /* Semantic - Text */
  --color-text-primary: [Hex];
  --color-text-secondary: [Hex];
  --color-text-disabled: [Hex];
  --color-text-inverse: [Hex];
  --color-text-on-brand: [Hex];

  /* Semantic - Background */
  --color-background-default: [Hex];
  --color-background-surface: [Hex];

  /* Semantic - Border */
  --color-border-default: [Hex];
  --color-border-focus: var(--color-brand);

  /* Elevation */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-4: 16px;
  --space-6: 24px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-full: 9999px;
  --radius-pill: var(--radius-full);

  /* Z-index */
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-overlay: 300;
  --z-modal: 400;
  --z-toast: 500;

  /* Motion */
  --duration-fast-01: 70ms;
  --duration-fast-02: 110ms;
  --duration-moderate-01: 150ms;
  --duration-moderate-02: 240ms;
  --duration-slow-01: 400ms;
  --duration-slow-02: 700ms;
  --duration-scalar: 1;

  --easing-productive: cubic-bezier(0.2, 0, 0.38, 0.9);
  --easing-expressive: cubic-bezier(0.4, 0.14, 0.3, 1);
  --easing-enter: cubic-bezier(0, 0, 0.2, 1);
  --easing-exit: cubic-bezier(0.4, 0, 1, 1);
}

[data-theme="dark"] {
  --color-brand: var(--[PrimaryName]-400);
  --color-brand-hovered: var(--[PrimaryName]-300);
  --color-brand-pressed: var(--[PrimaryName]-500);
  --color-brand-subtle: var(--[PrimaryName]-900);
  --color-brand-contrast: var(--[PrimaryName]-200);

  --color-text-primary: [Hex];
  --color-text-secondary: [Hex];
  --color-background-default: [Hex];
  --color-background-surface: [Hex];
  --color-border-default: [Hex];
  --color-border-focus: var(--color-brand);
  /* ... other Token overrides */
}

/* Dark mode auto-detection: follow system preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-brand: var(--[PrimaryName]-400);
    --color-brand-hovered: var(--[PrimaryName]-300);
    --color-brand-pressed: var(--[PrimaryName]-500);
    --color-brand-subtle: var(--[PrimaryName]-900);
    --color-brand-contrast: var(--[PrimaryName]-200);

    --color-text-primary: [Hex];
    --color-text-secondary: [Hex];
    --color-background-default: [Hex];
    --color-background-surface: [Hex];
    --color-border-default: [Hex];
    --color-border-focus: var(--color-brand);
    /* ... other Token overrides */
  }
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-scalar: 0;
  }
}
```

### 14.2 Reference Resources

- [Material Design 3 - Color](https://m3.material.io/styles/color/roles)
- [IBM Carbon - Color System](https://carbondesignsystem.com/elements/color/overview/)
- [Microsoft Fluent 2 - Color](https://fluent2.microsoft.design/color)
- [Atlassian Design Tokens](https://atlassian.design/tokens/design-tokens)
- [W3C DTCG Specification](https://design-tokens.github.io/community-group/format/)
- [WCAG 2.1 Contrast Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [APCA Contrast Algorithm](https://github.com/Myndex/apca-w3)
- [W3C Chinese Layout Requirements (clreq)](https://www.w3.org/TR/clreq/)
- [Style Dictionary v4](https://amzn.github.io/style-dictionary/)