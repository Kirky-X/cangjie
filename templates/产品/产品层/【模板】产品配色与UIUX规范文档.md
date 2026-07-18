# [Product/System Name (English)] - Product Color and UI/UX Specification Document

> **Document Status:** 🟡 Under Review / 🟢 Approved / 🔴 Rejected
>
> **Confidentiality Level:** Confidential / Internal Public / Public
>
> **Version:** v0.1.0
>
> **Date:** YYYY-MM-DD
>
> **Author:** [Name/Role]
>
> **Reviewer:** [Name/Role]
>
> **Audience:** [Role List]
>
> **Applicable Scope:** Web / iOS / Android / Desktop
>
> **Related Documents:** [Product Requirements Document PRD], [Brand Guidelines]

---

## 0. Document Guide

### 0.1 Document Purpose and Scope

[Explain the purpose, applicable scenarios, and non-applicable scenarios of this document]

### 0.2 Related Documents

| Document Type | Filename | Related Sections |
|---------|--------|---------|
| [Type] | [Filename] [Line Range] | [Section Description] |

> **Reference Format Note**: Related documents use the `filename line range` format (e.g., `【Template】Technical Requirements Document(TRD).md 3-17`). Line numbers may change as documents are updated; please refer to actual content.

### 0.3 Change Log

| Version | Date | Reviser | Change Content | Reviewer |
| :--- | :--- | :--- | :--- | :--- |
| v0.1.0 | YYYY-MM-DD | [Name] | Initial release | [Reviewer] |

---

## 1. Design Principles and Overview

### 1.1 Design Vision

Describe the visual character of the product in 1-2 sentences. For example:
> With "professional, trustworthy, lightweight" as the core, through restrained color hierarchy and clear interaction feedback, help users efficiently complete complex tasks.

### 1.2 Core Principles

| Principle | Description | Design Manifestation |
|------|------|----------|
| **Consistency** | Same visual language for same scenarios | Token naming, component states, interaction animations globally unified |
| **Hierarchy** | Distinguish information priority through color and shadow | Layering Model defines page depth |
| **Accessibility** | All users can use without barriers | Comply with WCAG 2.1 AA contrast standards, dual coding principle |
| **Responsive** | Adapt to multi-platform and theme switching | Support Light / Dark / High-Contrast modes |
| **Evidence-driven** | Design decisions based on evidence not intuition | Color quantity, type scale ratio, spacing baseline all supported by industry consensus |
| **Touch-friendly** | Minimum click target >= 44x44px | Mobile button height 48-52px, ensure comfortable finger tapping |
| **Breathing space** | Reasonable use of spacing to avoid crowding | 4/8/12/16/24px spacing system, clear information hierarchy |
| **Restrained coloring** | Primary color selected by industry, functional colors unified | Brand color coverage area <= 10%, neutral colors build text hierarchy |

> **Mobile Design Core Conclusion**: Good typography comes from clear information hierarchy, not fancy fonts. Consistency, clear hierarchy, adaptation first, touch-friendly, breathing space, and restrained coloring are the 6 core principles of APP design.

### 1.3 Design Token Architecture Overview

This specification adopts a **three-layer Token architecture**, following DTCG (W3C Design Tokens Community Group) specification:

| Layer | Naming Pattern | Example | Description |
|------|---------|------|------|
| **Primitive** | `{color}-{scale}` | `ink-green-700` | Platform-agnostic raw color values, not directly used in components |
| **Semantic** | `{purpose}[-variant][-{state}]` | `text-primary`, `bg-surface-hover` | Theme-bound semantic roles, support Light/Dark switching |
| **Component** | `{component}-{property}[-{state}]` | `btn-primary-bg-hover` | Framework-specific component-level Tokens |

> **State as the fourth dimension**: Each semantic Token must define at least 6 states (Default, Hover, Active, Focus, Selected, Disabled), otherwise color consistency across different interaction states cannot be guaranteed.

**Token Naming Rules**:
- Use lowercase letters + dots/hyphens as separators
- Semantic Token names describe **purpose** not **value** (e.g., `color.text.primary` not `color.text.black`)
- Total Token count recommended to be within 200, management cost increases exponentially beyond that

---

## 2. Color System

> **Core Idea**: Adopt three-layer Token system, all colors not directly using Hex values but called through semantic Tokens. Token naming pattern: `{category}.{property}.{variant}.{state}`
> Example: `color.background.primary.default`, `color.text.inverse`, `color.border.danger.hovered`

### 2.1 Brand Palette

Adopt **single brand color** strategy: only define 1 primary brand color, expand through gradient scale to cover all usage scenarios. Single color strategy advantages: focused visual focus, low development and maintenance cost, high cross-platform consistency.

| Token Name | Light Mode Value | Dark Mode Value | Usage Scenario |
|------------|--------------|-------------|----------|
| `color.brand` | [Primary Hex] | [Primary Dark Hex] | Primary buttons, Logo, navigation active state, links, icon emphasis |

> **Design Constraint**: Secondary emphasis and chart series colors are obtained from semantic palette (§2.3) and neutral palette (§2.5), no additional brand colors defined.

**Industry Brand Color Recommendations**:

| Industry Type | Recommended Color | Description |
|---------|---------|------|
| Retail/Consumer/E-commerce | `#3B82F6` (Blue) | Trust, professionalism, stability |
| Live/Social/Content | `#8B5CF6` (Purple) | Creativity, vitality, youth |
| Health/Sports/Travel | `#10B981` (Green) | Health, nature, vitality |
| Tools/Efficiency/Tech | `#14B8A6` (Teal) | Technology, efficiency, freshness |

> **Brand Color Selection Suggestion**: Choose primary color based on product industry attributes, ensure brand color aligns with product positioning. Brand color coverage area <= 10%.

**Brand Color Gradient Scale**:
Define 9 gradient levels (50-900), with **600 shade as the base color**. 600 shade typically achieves 4.5:1-7:1 contrast on white background, meeting WCAG AA-AAA standards.

| Gradient | Color Value (Light) | Color Value (Dark) | Purpose |
|------|---------------|--------------|------|
| `brand-50` | [Hex] | [Hex] | Very light background, hover base |
| `brand-100` | [Hex] | [Hex] | Light background, selected state base |
| `brand-200` | [Hex] | [Hex] | Light decorative elements |
| `brand-300` | [Hex] | [Hex] | Secondary icons, auxiliary text |
| `brand-400` | [Hex] | [Hex] | Medium emphasis |
| `brand-500` | [Hex] | [Hex] | Hover state, chart auxiliary colors |
| `brand-600` | [Hex] | [Hex] | **Base color (default)** |
| `brand-700` | [Hex] | [Hex] | Pressed/Active state |
| `brand-800` | [Hex] | [Hex] | Dark text (on-light) |
| `brand-900` | [Hex] | [Hex] | Very dark decoration, dark background emphasis |

> **Hidden Rule**: Don't use 400 or 500 as base color, as their contrast often cannot cover all usage scenarios.

### 2.2 Color Area Rules (60-30-10)

| Ratio | Role | Description |
|------|------|------|
| 60% | Primary/Base color | Page background, large area filling |
| 30% | Secondary color | Cards, sidebars, secondary areas |
| 10% | Accent color | CTA buttons, key icons, focus elements |

**Color Area Audit Checklist**:

- [ ] Page background color coverage area >= 60%
- [ ] Card/panel color coverage area ~30%
- [ ] Brand accent color coverage area <= 10%
- [ ] Brand color CTA buttons per screen <= 1
- [ ] Brand color only used for interactive elements (buttons, links, icons), not for large area backgrounds

### 2.3 Semantic/Functional Palette

Used to convey state, feedback, and urgency level, independent of brand color. Industry consensus: 4 core semantic colors (Success/Warning/Error/Info).

| Semantic | Token | Light | Dark | Usage Scenario |
|------|-------|-------|------|----------|
| **Success** | `color.semantic.success` | `#22C58B` | `#34D399` | Success prompts, completed state, positive indicators |
| **Warning** | `color.semantic.warning` | `#FFB020` | `#FBBF24` | Warning prompts, items requiring attention |
| **Error** | `color.semantic.error` | `#FF5A6B` | `#F87171` | Error prompts, delete confirmation, form validation failure |
| **Info** | `color.semantic.info` | `color.brand-600` | `color.brand-400` | Information prompts, neutral notifications (reuse brand color) |

**Semantic Color Light Background Variants**:

| Semantic | Light Background Token | Light Background Value | Purpose |
|------|--------------|-----------|------|
| **Success** | `color.semantic.success.subtle` | `#CFF5E7` | Success prompt background |
| **Warning** | `color.semantic.warning.subtle` | `#FFE8B5` | Warning prompt background |
| **Error** | `color.semantic.error.subtle` | `#FFD7DC` | Error prompt background |
| **Info** | `color.semantic.info.subtle` | `#D9E7FF` | Information prompt background |

> **Semantic Color Reuse Under Single Brand Color Strategy**: Info semantic color directly reuses brand color gradient, no additional definition. Brand color 600 (Light) and 400 (Dark) serve as default values for information prompts respectively.

**Semantic Color Extension Rules**: Each semantic color must include at least 5 variants:

| Variant | Naming Suffix | Purpose |
|------|---------|------|
| `default` | `color.semantic.error` | Default state |
| `hovered` | `color.semantic.error.hovered` | Mouse hover |
| `pressed` | `color.semantic.error.pressed` | Press/Active |
| `subtle` | `color.semantic.error.subtle` | Light background (e.g., error input field background) |
| `contrast` | `color.semantic.error.contrast` | Text/Icon color (ensure readability on subtle background) |

### 2.4 Color Semantics and Psychological Considerations

> Fill in the psychological meaning and cultural considerations of brand color selection. Color semantics are not universal but deeply influenced by cultural construction. **Attention is physiological, meaning is cultural** — red attracts attention in all cultures (wavelength determines), but the meaning red conveys varies by culture. See `UI Design Specification Systematic Research Report.md` §5.1 for details.

[Fill in this product brand color's psychological meaning, cultural difference considerations, saturation/brightness strategy]

**Key Principle**: Never let color be the sole carrier of semantics. If error state only conveys "error" through red, it will fail in cross-cultural scenarios. Must be supplemented with dual coding of icons, text, shapes, etc.

### 2.5 Neutral Palette

Builds interface skeleton, text, borders, dividers. Use blue-gray or warm gray, avoid pure black `#000000`.

| Token | Light Mode | Dark Mode | Usage Scenario |
|-------|-----------|-----------|----------|
| `color.neutral-50` | `#F3F6FB` | [Hex] | Page global background |
| `color.neutral-100` | [Hex] | [Hex] | Card background, input field background |
| `color.neutral-200` | `#E5E7EB` | [Hex] | Hover background, dividers |
| `color.neutral-300` | `#D1D5DB` | [Hex] | Disabled borders, secondary dividers |
| `color.neutral-400` | `#9CA3AF` | [Hex] | Placeholder text, disabled text |
| `color.neutral-500` | `#6B7280` | [Hex] | Body text (secondary), icon default state |
| `color.neutral-600` | `#374151` | [Hex] | Auxiliary text (dark body) |
| `color.neutral-700` | `#1A1B27` | [Hex] | Heading text, primary icons |
| `color.neutral-800` | [Hex] | [Hex] | Secondary headings |
| `color.neutral-900` | [Hex] | [Hex] | Heading text, primary icons |

**Neutral Color Text Hierarchy Specification**:

| Purpose | Color Value | Description |
|------|------|------|
| Headings | `#1A1B27` | Darkest, for page core topics |
| Dark body | `#374151` | Important paragraph body |
| Body | `#6B7280` | Page main information content |
| Auxiliary text | `#9CA3AF` | Supplementary notes, secondary information |
| Dividers | `#D1D5DB` | Content separation |
| Borders | `#E5E7EB` | Component borders |
| Page background | `#F3F6FB` | Page base color (not pure white, reduce visual fatigue) |

### 2.6 Layering Model

Defines the "depth" and "stacking logic" of interface elements, ensuring clear visual hierarchy in complex pages.

**Light Mode Layering**:
- **Layer 0 (Base)**: `neutral-50` — Deepest page background
- **Layer 1 (Surface)**: `neutral-100` — Cards, popups, sidebars
- **Layer 2 (Raised)**: `neutral-0` (pure white) — Dropdown menus, floating layers, Tooltips
- **Layer 3 (Overlay)**: Black mask with transparency `rgba(0,0,0,0.45)` — Modal background

**Dark Mode Layering** (Asymmetric mapping, not simple inversion):
- **Layer 0**: `neutral-50` (darkest)
- **Layer 1**: `neutral-100` — Slightly lighter than base layer (raised feeling)
- **Layer 2**: `neutral-200` — Floating layer continues to brighten
- **Layer 3**: `rgba(0,0,0,0.75)` — Deeper mask

> **Core Principle**: Dark Mode is not Light Mode's "inverted colors", but an independent color space. Each Token's Dark value needs independent design and verification, cannot be inverted through algorithms.

### 2.7 Color Role Mapping

Maps Tokens to specific UI elements, ensuring "background-text-icon" contrast compliance.

| Role | Background Token | Text/Icon Token | Purpose |
|------|-----------|----------------|------|
| **Primary** | `color.brand-600` | `color.text.on-brand` | Primary buttons, FAB, key action points |
| **Secondary** | Transparent | `color.brand-600` | Secondary buttons, filter tags |
| **Surface** | `color.background.surface` | `color.text.primary` | Cards, panels |
| **Inverse** | `color.background.inverse` | `color.text.inverse` | Dark banners, Toast |
| **Danger** | `color.semantic.error` | `color.text.on-danger` | Delete buttons, strong warnings |
| **Disabled** | `color.background.disabled` | `color.text.disabled` | Disabled state elements |

### 2.8 Dark/Light Mode Mapping Table

| Token | Light | Dark | Mapping Logic |
|-------|-------|------|---------|
| `color.background.default` | [Hex] | [Hex] | Page base color, dark mode not pure black retains depth feeling |
| `color.background.surface` | [Hex] | [Hex] | Card base color, dark mode Elevated brighter |
| `color.brand-600` | [Primary Hex] | [Primary Dark Hex] | Primary button background, dark mode brightened to 400 shade |
| `color.text.primary` | [Hex] | [Hex] | Primary heading/body, dark mode not pure white reduces Halation glare |
| `color.text.secondary` | [Hex] | [Hex] | Secondary description text |
| `color.text.disabled` | [Hex] | [Hex] | Disabled state text |
| `color.border.default` | [Hex] | [Hex] | Default border |
| `color.border.focus` | `color.brand-600` | `color.brand-400` | Focus state border (2px) |

> **Dark Mode Brand Color Mapping**: Light mode uses 600 shade, dark mode brightened to 400 shade, ensuring sufficient contrast on dark background.

### 2.9 Color Contrast Standards

#### 2.9.1 WCAG 2.1 Contrast Requirements

| Level | Normal Text (<18px / non-bold <14px) | Large Text (>=18px / bold >=14px) | UI Components / Graphics |
|------|------|------|------|
| **AA (Minimum)** | >= 4.5:1 | >= 3:1 | >= 3:1 |
| **AAA (Enhanced)** | >= 7:1 | >= 4.5:1 | Not defined |

#### 2.9.2 APCA Contrast Algorithm (WCAG 3.0 Candidate)

APCA is the successor to WCAG 2.x contrast algorithm, considering directionality of text and background colors, and interactive effects of font size and weight:

| Contrast Level | APCA Minimum (Lc) | Purpose |
|-----------|-------------------|------|
| Body text | Lc >= 60 | Body readability |
| Large text | Lc >= 45 | Headings, large font sizes |
| Minimum perceptible | Lc >= 15 | Decorative text |
| Best readability | Lc >= 75 | Long-form reading body |

#### 2.9.3 Dark Mode Contrast Strategy

| Strategy | Industry Suggestion | Theoretical Basis |
|------|---------|---------|
| Base color not pure black | Use `#121212` or tinted dark gray | Warm gray base more visually comfortable than pure black |
| Text not cool white | Use `#E0E0E0` or warm white | Halation effect: high brightness text produces glow diffusion on dark background |
| Brand color brightening | Dark mode brighten 1-2 shades | Maintain consistent visual weight |
| Status color brightening | Dark mode use 400 shade | 400 shade has better contrast on dark background |
| Shadow enhancement | Dark mode replace shadows with borders | Shadow effects weakened in dark mode |

### 2.10 Color Vision Deficiency (CVD) Accessibility

About 8% of males and 0.5% of females have color vision deficiency. Key specifications:

- Semantic colors cannot be distinguished by color alone, must be supplemented with icons, text, shapes (WCAG SC 1.4.1)
- Error (red) and Success (green) may be confused in Deuteranopia mode, must ensure icon+text assistance
- Color palette should be verified through CVD simulation: Protanopia / Deuteranopia / Tritanopia three modes
- Recommended tools: Sim Daltonism (macOS), Color Oracle (cross-platform), Chrome DevTools simulation

### 2.11 High Contrast Mode

- In high contrast mode shadows completely fail, must rely on **borders** and **outlines** to distinguish hierarchy
- Focus color on dark background may need customization
- All state changes cannot rely solely on color, must be supplemented with **icons, text labels or shape changes**
- Adapt to `prefers-contrast: more` media query

---

## 3. Typography System

> All text managed through Tokens: `font.family`, `font.size`, `font.weight`, `line.height`, `letter.spacing`

### 3.1 Font Stack

| Scenario | Font Stack | Token |
|------|--------|-------|
| Western/Numbers | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto` | `font.family.base` |
| Chinese | `"PingFang SC", "Microsoft YaHei", "Noto Sans SC"` | `font.family.chinese` |
| Code | `"SF Mono", "Fira Code", Consolas` | `font.family.code` |

**Font Loading Strategy**:

- Use `font-display: swap` to avoid FOIT (Flash of Invisible Text), ensure text immediately visible
- Key font preloading: `<link rel="preload" as="font" crossorigin href="...">`
- Chinese fonts loaded on demand (`unicode-range` sharding), reduce first load size
- Fall back to system font stack on font loading failure, don't block rendering

**Font Pairing Rules**:
1. Maximum 2 font families: 1 heading font + 1 body font, 3rd only for code
2. Contrast principle: Serif + Sans-serif pairing is most classic (e.g., Noto Serif SC + Noto Sans SC)
3. x-height matching: Paired fonts should have similar x-height
4. Chinese pairing: Headings use Song/Serif (cultural feel), body uses Hei/Sans-serif (readability)

### 3.2 Type Scale Ratio System

| Ratio Name | Value | Applicable Scenario |
|----------|------|----------|
| Minor Second | 1.067 | Compact information architecture, data-intensive |
| Major Second | 1.125 | Subtle hierarchy, enterprise backend |
| **Minor Third** | **1.2** | **Mobile, compact layout** |
| **Major Third** | **1.25** | **General, balanced (recommended)** |
| Perfect Fourth | 1.333 | Loose hierarchy, brand display |
| Augmented Fourth | 1.414 | Dramatic contrast, creative |
| Perfect Fifth | 1.5 | Extreme contrast, large screen display |

> **Recommendation**: 1.25x (Major Third) ratio aligns with IBM Carbon, belongs to industry general balanced choice.

### 3.3 Type Scale

| Token | Font Size | Line Height | Font Weight | Purpose |
|-------|------|------|------|------|
| `font.heading.xxl` | 28-32px | 1.2 | 700 | Page large heading (mobile H1) |
| `font.heading.xl` | 22-24px | 1.3 | 600 | Module heading (mobile H2) |
| `font.heading.lg` | 18-20px | 1.35 | 600 | Card heading |
| `font.body.large` | 16px | 1.5 | 400 | Body (mobile default, line length 25-35 characters) |
| `font.body.base` | 14px | 1.5 | 400 | **Default body (desktop)** |
| `font.body.small` | 12px | 1.4 | 400 | Auxiliary text, timestamps, notes |
| `font.label` | 14px | 1.2 | 500 | Button text, labels |

> **Mobile Font Size Specification**: Main heading and body must have clear distinction; body and auxiliary text must have at least 2px difference; don't rely on fancy fonts to replace information hierarchy. Core conclusion: good typography comes from clear information hierarchy.

### 3.4 Chinese Typography Specifics

| Specification Item | Recommended Value | Description |
|--------|--------|------|
| Body font size | 14-16px | 14px suitable for information-dense, 16px suitable for reading |
| Minimum font size | 12px | Below 12px reading speed significantly decreases |
| Line height (Chinese body) | 1.6-1.8 | Chinese characters have no ascenders/descenders, visual density between lines higher |
| letter-spacing | 0 | Chinese monospaced, no additional spacing needed |
| Heading letter-spacing | 0-0.05em | Can slightly increase breathing space |
| Chinese-English mixed typesetting | Western font size 1-2px smaller than Chinese | Western letter x-height typically smaller than Chinese character face |
| Chinese font weight | Minimum use Regular (400) | Light (300) extremely poor readability in Chinese scenarios |

### 3.5 Line Height Recommendations

| Font Size Range | Recommended Line Height Multiplier | Description |
|----------|-------------|------|
| 32px+ | 1.1-1.25 | Large headings, compact line spacing |
| 24-31px | 1.25-1.35 | Medium headings |
| 18-23px | 1.35-1.45 | Small headings |
| 14-17px | 1.5-1.7 | Body (Chinese on higher side) |
| 10-13px | 1.4-1.6 | Auxiliary text |

### 3.6 Cross-Platform Typography Mapping

Same semantic Token's specific mapping on different platforms needs independent definition, cannot simply equate px=pt=sp:

| Token | iOS | Android | Web |
|-------|-----|---------|-----|
| `font.body.large` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |
| `font.body.base` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |
| `font.label` | [N]pt / [N] / [N]pt line height | [N]sp / [N] / [N]sp line height | [N]px / [N] / [N] line height |

### 3.7 Responsive Typography Scaling

| Breakpoint | Heading Scaling | Body Scaling | Description |
|------|---------|---------|------|
| Mobile (<640px) | -2px | No change | Only headings shrink |
| Tablet (640-1024px) | -1px | No change | Transition |
| Desktop (>1024px) | Base | Base | Full size |
| Large (>1440px) | +2-4px | +1-2px | Large screen enlargement |

Recommend using CSS `clamp()` for fluid heading scaling: `font-size: clamp(1.5rem, 1.5rem + 0.5vw, 2.5rem)`.

### 3.8 Dynamic Type Stepped Scaling

Mobile needs to support system-level font size scaling (Apple Dynamic Type / Android Font Size). Scaling is not simple linear enlargement but **stepped scaling**:

| Accessibility Size | Scaling Ratio | Design Constraint |
|-------------------|---------|---------|
| XS (Default) | 1.0x | Base layout |
| L | 1.35x | Test if layout overflows |
| XL | 1.65x | Text may need truncation |
| XXXL | 2.35x | All UI layouts must support text truncation or auto-wrapping |
| AX5 (Maximum) | 4.59x | Touch targets must still be usable |

> **Key Rule**: After exceeding AX3, all UI layouts must support **text truncation** or **auto-wrapping**.

---

## 4. Spacing and Grid System

> Based on 4px / 8px base units, industry consensus: 4px minimum unit + 8px common baseline.

### 4.1 Spacing Scale

| Token | Value | Purpose |
|-------|-----|------|
| `space.0` | 0px | No spacing |
| `space.1` | 4px | Icon-text gap, label internal padding |
| `space.2` | 8px | Compact internal padding, list item spacing |
| `space.3` | 12px | Button internal horizontal padding, same-group secondary separation |
| `space.4` | 16px | Card internal padding, form spacing, independent module separation |
| `space.5` | 20px | Module spacing |
| `space.6` | 24px | Paragraph spacing, page large section separation |
| `space.8` | 32px | Section spacing |
| `space.10` | 40px | Large section spacing |
| `space.12` | 48px | Page-level spacing |
| `space.16` | 64px | Large module separation |

**Mobile Spacing Specification**:

| Spacing Value | Applicable Scenario |
|--------|---------|
| 4px | Fine internal spacing adjustment between icons, labels, numbers and text |
| 8px | Standard spacing between common components like list items, button groups, information rows |
| 12px | Secondary separation within same-group content, make content switching smoother |
| 16px | Regular separation between independent modules, balance clarity and page density |
| 24px | Between page large sections,拉开 primary-secondary hierarchy, stronger information breathing space |

> **Breathing Space Principle**: Reasonable use of spacing (4/8/12/16/24px), avoid page crowding. When spacing ratio >= 3:1, grouping perception significantly enhances.

### 4.2 Spacing Semantic Layering

Nathan Curtis's three-layer spacing strategy has become industry best practice:

| Layer | Spacing Range | Purpose | Example |
|------|---------|------|------|
| **Intra-component** | 4/8/12px | Internal element spacing | Button internal padding, icon-text spacing |
| **Inter-component** | 16/24px | Same-group component spacing | Form field spacing, list item spacing |
| **Layout-level** | 32/48/64px | Section/Page-level spacing | Card spacing, section spacing |

### 4.3 Spacing Semantic Naming Strategy

Numerical naming suitable for Primitive layer, semantic naming suitable for Semantic layer (recommended):

| Semantic Token | Compact Mode | Default Mode | Comfortable Mode | Purpose |
|-----------|-------------|-------------|-----------------|------|
| `space.compact` | 4px | 8px | 12px | Compact mode |
| `space.default` | 12px | 16px | 20px | Default mode |
| `space.comfortable` | 20px | 24px | 32px | Comfortable mode |
| `space.loose` | 28px | 32px | 40px | Loose mode |

> **Density is a scenario attribute not platform attribute**: Different pages on the same platform can use different densities (e.g., Dashboard uses Compact, detail page uses Comfortable).

### 4.4 Gestalt Proximity Quantification

| Element Spacing | Perceived Grouping | Application Scenario |
|---------|---------|---------|
| < 8px | Same group | Icon+text, label+value |
| 8-16px | Related group | Form fields, list items |
| > 24px | Independent group | Section separation, card spacing |

> When spacing ratio >= 3:1, grouping perception significantly enhances.

### 4.5 Responsive Breakpoint Standards

| Breakpoint Name | Width Range | Columns | Gutter | Margin | Touch Target |
|----------|---------|------|--------|--------|---------|
| **xs** | < 480px | 4 | 16px | 16px | 44-48px |
| **sm** | 480-639px | 4 | 16px | 16px | 44-48px |
| **md** | 640-767px | 8 | 16-24px | 24px | 44-48px |
| **lg** | 768-1023px | 8 | 24px | 24px | 36-44px |
| **xl** | 1024-1439px | 12 | 24px | 32px | 36-44px |
| **2xl** | >= 1440px | 12 | 24-32px | 32px | 36-44px |

> **768px (lg) is the consensus breakpoint for all systems**, corresponding to iPad portrait. Academic research supports 3-5 breakpoints as optimal.

### 4.6 Layout Pattern Classification

Component arrangement in grid system follows 6 basic layout patterns:

| Pattern | Description | Applicable Scenario | Representative Component |
|------|------|---------|---------|
| **Stack** | Vertical/equal-distance horizontal arrangement | Lists, button groups | VStack / HStack |
| **Inline** | Horizontal arrangement, auto-wrapping | Tags, filters | Tag Group / Breadcrumb |
| **Grid** | Two-dimensional grid layout | Card lists, galleries | Data Table / Gallery |
| **Box** | Fixed aspect ratio container | Images, videos | Aspect Ratio Box |
| **Center** | Horizontal and vertical centering | Empty states, loading pages | Empty State / Spinner |
| **Bleed** | Break container margins | Full-width banners, hero images | Hero Banner / Full-width CTA |

### 4.7 Asymmetric Margins and Maximum Width Constraints

| Breakpoint | Left/Right Margin | Actual Behavior |
|------|----------|---------|
| Mobile | 16px | Fixed margin |
| Tablet | 24px | Fixed margin |
| Desktop | 32px | Fixed margin |
| Large Desktop | 32px | Fixed margin |
| Max (>1440px) | Auto center | Content area max width [e.g., 1200px], auto margins on both sides |

> **Key Rule**: Maximum width constraint is an implicit constraint of grid system, content stops expanding beyond it. This is **"Constrained Responsive"**.

### 4.8 Page Layout Psychology Guidelines

> The following is a summary of psychological evidence for layout design, detailed discussion in `UI Design Specification Systematic Research Report.md` §4.8.

| Psychology Principle | Layout Inspiration |
|-----------|---------|
| Cognitive load theory | Progressive disclosure, chunking (4-7 items per group), consistency reduces extraneous load |
| F-shaped reading pattern | Core information in top-left and first two lines; keywords at line beginnings |
| Z-shaped reading pattern | Logo top-left, CTA top-right, core visual center, secondary CTA bottom-right |
| Hick's Law | Main navigation limited to 3-5 items, only 1 primary CTA per screen |
| Fitts's Law | Mobile touch targets >= 44x44pt, high-frequency operations near natural finger position |
| Von Restorff effect | Important elements contrast with surroundings through color/size/position to stand out |

---

## 5. Component Specifications and Interaction Logic

> Each component must define: **Anatomy**, **All States**, **Behavior**, **Tokens Used**, **Do & Don't**

### 5.1 Component State Machine Specification

Every interactive component must define a complete state machine, ensuring behavioral determinism and testability.

**Standard State Matrix**:

| State | Visual Performance | Trigger Condition | Exit Condition | Accessibility Requirement |
|------|---------|---------|---------|-----------|
| **Default** | Base style | Initial state | Any interaction | Focusable |
| **Hover** | Background overlay 5% (Light) / 5% (Dark) | Mouse enter | Mouse leave | Desktop only |
| **Pressed** | Background overlay 10% (Light) / 10% (Dark) | Press | Release | — |
| **Focus** | 2px focus ring | Tab/Click | Tab out/Escape | Must be visible, contrast >= 3:1 |
| **Disabled** | 38% transparency | `disabled=true` | `disabled=false` | `aria-disabled="true"` |
| **Loading** | Spinner + disable interaction | `isLoading=true` | Request complete/fail | `aria-busy="true"` |
| **Error** | Red border + error message | Validation fail | Correct input | `aria-invalid="true"` |
| **Success** | Green border/icon | Operation success | Auto-recover after 2s | `aria-live="polite"` |

**Global Interaction Overlay**:

All components' hover/active states use unified transparency overlay, ensuring visual consistency:

| State | Light Mode | Dark Mode | CSS Implementation |
|------|-----------|----------|---------|
| **Hover** | `rgba(0,0,0,0.05)` | `rgba(255,255,255,0.05)` | `background-color: color-mix(in srgb, currentColor 5%, transparent)` |
| **Active** | `rgba(0,0,0,0.1)` | `rgba(255,255,255,0.1)` | `background-color: color-mix(in srgb, currentColor 10%, transparent)` |
| **Focus** | `2px solid var(--color-border-focus)` | Same as left | Outline line, not background overlay |

> **Instant Feedback Rule**: Hover response delay 0ms (no `transition-delay`), Focus ring display 0ms. Only displacement/scale animations allow 150-200ms transitions.

**State Transition Rules**:
- Disabled state only allows `Disabled → Default` transition, other interactions prohibited
- Loading state prohibits Hover/Pressed transitions
- Error state must provide specific error message, prohibit only showing "Operation failed"
- State transitions must have corresponding visual feedback, no silent transitions

### 5.2 Button

#### Anatomy
```
[Icon (optional)] + [Text label] + [Loading icon (optional)]
```
- Height specification: `size.sm` = 32-36px (text buttons), `size.md` = 40-44px (secondary buttons), `size.lg` = 48-52px (primary buttons)
- Border radius: `radius.md` = 8px (most common on mobile), determined by brand character, can also be 4px/6px/999px
- Minimum click target: >= 44 x 44px (mandatory for touch devices)

**Button Size Specification**:

| Button Type | Height | Border Radius | Purpose |
|---------|------|------|------|
| **Primary** | 48-52px | 8px | Page core CTA, max 1 per page |
| **Secondary** | 40-44px | 8px | Secondary operations, cancel |
| **Text** | 32-36px | 0-4px | Low priority, toolbar |

> **Mobile Button Specification**: Primary button height 48-52px, ensure comfortable finger tapping; secondary button 40-44px, text button 32-36px. All buttons minimum click target >= 44x44px.

#### Type Variants
| Type | Background Token | Text Token | Border Token | Usage Scenario |
|------|-----------|-----------|-----------|----------|
| **Primary (Solid)** | `color.brand-600` | `color.text.on-brand` | None | Page primary action point, max 1 per page |
| **Secondary (Outlined)** | Transparent | `color.brand-600` | `color.brand-600` | Secondary operations, cancel |
| **Tertiary (Ghost)** | Transparent | `color.brand-600` | None | Low priority, toolbar |
| **Danger** | `color.semantic.error` | `color.text.on-danger` | None | Delete, irreversible operations |
| **Text (Pure text)** | Transparent | `color.brand-600` | None | Links, table operations |

#### Interaction States
All buttons must define the following 7 states:

| State | Visual Performance | Token Change | Trigger Condition |
|------|----------|-----------|----------|
| **Default** | Default style | `color.brand-600` | No interaction |
| **Hover** | Background overlay 5% (use global overlay) | `color.brand-500` | Mouse hover |
| **Pressed / Active** | Background overlay 10% (use global overlay), Y-axis offset 1px | `color.brand-700` | Mouse press/Touch press |
| **Focus** | Outer frame 2px focus ring, offset 2px | `color.border.focus` | Keyboard Tab focus |
| **Disabled** | Background lightened gray, text becomes `text.disabled`, no Hover effect | `color.background.disabled` | Not clickable |
| **Loading** | Background maintained, text hidden, shows Spinner (does not respond to clicks) | — | Async request in progress |
| **Success** | Briefly changes to green background + checkmark icon, recovers or redirects after 1.5s | `color.semantic.success` | Operation success feedback |

#### Interaction Details
- **Hover delay**: No delay, instant response (0ms)
- **Pressed feedback**: Provide `transform: translateY(1px)` physical press feeling
- **Focus visibility**: Must meet 3:1 contrast, hiding outline prohibited
- **Loading state**: Button width unchanged, prevent layout jitter; Spinner size = text height x 0.8
- **Debounce**: Continuous clicks, only first triggers, until state change

---

### 5.3 Input Field

#### State Definition
| State | Border | Background | Placeholder Text |
|------|------|------|----------|
| **Default** | `color.border.default` | `color.background.surface` | `color.text.placeholder` |
| **Hover** | `color.border.hover` (darkened) | No change | No change |
| **Focus** | `color.brand-600` (2px, brand color) | `color.background.default` | No change |
| **Filled** | `color.border.default` | No change | Moves up/shrinks as Label (Floating Label mode) |
| **Error** | `color.semantic.error` | `color.semantic.error.subtle` | Shows error icon + error text |
| **Disabled** | `color.border.disabled` | `color.background.disabled` | `color.text.disabled` |
| **Read-only** | Dashed border `border-dashed` | No change | No change |

#### Interaction Logic
- **Focus animation**: Border color transition `transition: border-color 200ms ease-out`
- **Error state**: Triggers validation on blur; error text appears below input field, font size `font.body.small`, color `color.semantic.error`
- **Clear button**: When hovering input field, clear icon appears on right side (only when has content and not Disabled state)
- **Password visibility toggle**: Click eye icon toggles `type="password/text"`, icon color becomes `color.brand-600` on Active

---

### 5.4 Card

#### Layering and Shadow
| Layer | Background Token | Shadow Token | Purpose |
|------|-----------|-----------|------|
| **Rest** | `color.background.surface` | `shadow.sm` (`0 1px 2px rgba(0,0,0,0.05)`) | Default display |
| **Hover** | No change | `shadow.md` (`0 4px 12px rgba(0,0,0,0.1)`) | Clickable card hover |
| **Pressed** | No change | `shadow.sm` + downward offset 1px | Press |
| **Selected** | `color.background.selected` | `shadow.md` + border `color.brand-600` | Selected state |

#### Interaction Logic
- **Hover lift**: Shadow deepens + slight enlargement `scale(1.01)`, transition 200ms ease-out
- **Click area**: When entire card is click target, must include clear focus ring
- **Internal operations**: If card has independent buttons (e.g., "edit"), must use `z-index` to ensure events don't bubble

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
- **Background**: `color.background.surface` (one layer deeper than page background, follows Layering Model)
- **Selected item**: Background `color.background.selected`, text `color.text.primary`, left 3px vertical bar `color.brand-600`
- **Hover**: Background `color.background.hover`, no left vertical bar
- **Collapse animation**: Width change `transition: width 250ms cubic-bezier(0.4, 0, 0.2, 1)`

---

### 5.6 Feedback Components

#### Toast / Notification
| Type | Background | Left Vertical Bar/Icon | Display Duration |
|------|------|--------------|----------|
| **Info** | `color.background.surface` | `color.semantic.info` | 3s |
| **Success** | `color.background.surface` | `color.semantic.success` | 3s |
| **Warning** | `color.background.surface` | `color.semantic.warning` | 5s (needs user attention) |
| **Error** | `color.background.surface` | `color.semantic.error` | Does not auto-dismiss (requires manual close) |

#### Interaction Logic
- **Enter**: Slide in from right (`translateX(100%) → 0`), 300ms, `cubic-bezier(0.4, 0, 0.2, 1)`
- **Exit**: Fade out upward (`translateY(-10px) + opacity 0`), 200ms
- **Hover pause**: When mouse hovers, countdown pauses; continues after mouse leaves
- **Stacking**: Maximum 3 displayed, new Toast pushes old Toast upward, spacing `space.3`

---

## 6. Iconography System

### 6.1 Icon Specifications

| Specification Item | Standard | Description |
|--------|------|------|
| Icon style | [Outline / Filled] | Same function icon provides Outline + Filled variants |
| Default size | 24px | Icon grid 24dp bounding box |
| Stroke width | 2dp | Material Design standard |
| Naming rule | `{category}-{name}-{variant}` | e.g., `nav-arrow-left-filled` |
| Implementation | SVG sprite preferred over icon font | Performance/Accessibility/Maintainability |

### 6.2 Icon Size Tokens

| Token | Value | Purpose |
|-------|-----|------|
| `icon.size.xs` | 12px | Compact inline icons |
| `icon.size.sm` | 16px | Table icons, auxiliary icons |
| `icon.size.md` | 20px | Button icons |
| `icon.size.lg` | 24px | Default icons (navigation bar, lists) |
| `icon.size.xl` | 32px | Empty state icons |
| `icon.size.2xl` | 48px | Onboarding page icons |
| `icon.size.3xl` | 64px | Large display icons |

> **Mobile Icon Specification**: Common sizes 16/20/24/32/48/64px, can be flexibly used in navigation bars, lists, buttons and prompts based on actual scenarios.

### 6.3 Drawing Grid

- Determine grid and safe area before drawing icons
- Recommend using outer frame, center lines and circular baselines to assist drawing
- Maintain graphic proportion and visual balance, reduce center of gravity offset
- Ensure clarity and stability at different sizes

### 6.3 Live Area and Trim Area

| Canvas Size | Live Area | Trim Area | Description |
|---------|-----------|-----------|------|
| 16x16px | 14x14px | 1px | High-density icons |
| 20x20px | 16x16px | 2px | Font Awesome 7 |
| 24x24px | 20x20px | 2px | Material Design |
| 32x32px | 28x28px | 2px | IBM |

- **Live Area** is the actual drawing area of icon content
- **Trim Area** is the safe margin, preventing icon from being cropped
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
- Functional icons: Need `aria-label` to describe function
- Icon button minimum size: 24x24px (WCAG 2.2 AA), recommended 32x32px

---

## 7. Shadow and Elevation System

### 7.1 Elevation Levels

| Elevation Level | Shadow Value | Purpose |
|----------------|--------|------|
| 0dp | No shadow | Page background, flat content |
| 1dp | `0 1px 2px rgba(0,0,0,0.1)` | Cards (default state) |
| 3dp | `0 2px 4px rgba(0,0,0,0.1)` | Cards (hover state), input fields |
| 8dp | `0 4px 8px rgba(0,0,0,0.12)` | Popup menus, dropdowns |
| 12dp | `0 6px 12px rgba(0,0,0,0.15)` | Floating action buttons |
| 24dp | `0 12px 24px rgba(0,0,0,0.2)` | Modals, dialogs |

### 7.2 Shadow + Surface Dual Expression

Shadow and Surface must be used in pairs, cannot mix different levels of Shadow and Surface:

| Elevation Level | Surface Token | Shadow Token | Purpose |
|-------------|--------------|-------------|------|
| **Sunken** | `elevation.surface.sunken` | None | Lowest layer, e.g., Kanban column background |
| **Default** | `elevation.surface` | None | Base layer, e.g., page content |
| **Raised** | `elevation.surface.raised` | `elevation.shadow.raised` | Movable cards |
| **Overlay** | `elevation.surface.overlay` | `elevation.shadow.overlay` | Modals, dropdown menus |

> **Dark Mode**: Shadow is almost invisible, so **Surface color must brighten with level** to compensate.

### 7.3 Z-index Token System

| Token | Value | Purpose |
|-------|-----|------|
| `--z-base` | 0 | Default content |
| `--z-dropdown` | 100 | Dropdown menus |
| `--z-sticky` | 200 | Sticky headers |
| `--z-overlay` | 300 | Mask layers |
| `--z-modal` | 400 | Modals |
| `--z-toast` | 500 | Toast notifications |

> **Key Rule**: Z-index values should increase in jumps (at least +50 or +100 each time), reserving space for intermediate levels.

---

## 8. Shape and Border Radius System

### 8.1 Border Radius Tokens

| Token | Value | Purpose |
|-------|-----|------|
| `--radius-none` | 0 | Tables, divided containers, strong-order information areas |
| `--radius-xs` | 2px | Small elements |
| `--radius-sm` | 4px | Input fields, labels, lightweight buttons and other small components |
| `--radius-md` | 8px | Buttons, cards, small popovers (**most common on mobile**) |
| `--radius-lg` | 12px | Content cards, floating panels, information module containers |
| `--radius-xl` | 16px | Large cards, bottom sheets, emphasis display areas |
| `--radius-full` | 9999px | Circular avatars, capsule buttons |
| `--radius-pill` | 9999px | Capsule buttons (alias of `--radius-full`) |

> **Mobile Border Radius Specification**: 8px is the most common border radius on mobile, suitable for buttons, cards, small popovers. 12px for content cards and floating panels, 16px for large cards and bottom sheets.

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

> **Key Rule**: If calculation result is negative, child element should maintain its own border radius Token, don't force apply formula.

---

## 9. Micro-interactions and Motion Specifications

### 9.1 Easing Curves

#### Productive vs Expressive Dual-Track System

| Scenario | Productive Easing (Functional) | Expressive Easing (Emotional) |
|------|--------------------------|---------------------------|
| Standard | `cubic-bezier(0.2, 0, 0.38, 0.9)` | `cubic-bezier(0.4, 0.14, 0.3, 1)` |
| Entrance | `cubic-bezier(0, 0, 0.38, 0.9)` | `cubic-bezier(0, 0, 0.3, 1)` |
| Exit | `cubic-bezier(0.2, 0, 1, 0.9)` | `cubic-bezier(0.4, 0.14, 1, 1)` |

- **Productive** for functional animations (fast, direct, non-distracting)
- **Expressive** for emotional animations (fluid, brand personality)
- Same component's "entrance" and "exit" should use different Easing: entrance uses Expressive, exit uses Productive

### 9.2 Duration Specifications

| Token | Value | Purpose |
|-------|-----|------|
| `duration.fast-01` | 70ms | Micro-interactions (buttons, switches) |
| `duration.fast-02` | 110ms | Micro-interactions (fade in/out) |
| `duration.moderate-01` | 150ms | Small expansion, short-distance movement |
| `duration.moderate-02` | 240ms | Expansion, system notifications, Toast |
| `duration.slow-01` | 400ms | Large expansion, important system notifications |
| `duration.slow-02` | 700ms | Background darkening |

### 9.3 Duration Scalar Global Speed Control

All Duration Tokens must be multiplied by `duration-scalar`, this is the only correct way to implement `prefers-reduced-motion`:

```css
:root {
  --duration-scalar: 1; /* Normal speed */
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-scalar: 0; /* Completely disable */
  }
}
```

> Components that manually set fixed durations without using scalar will not respond to users' reduced motion preferences.

### 9.4 Response Time Thresholds

| Threshold | User Perception | Design Strategy |
|------|---------|---------|
| < 100ms | Instant | No wait indicator needed |
| 100-300ms | Smooth | Micro-animation feedback |
| 300ms-1s | Acceptable delay | Spinner / Progress indicator |
| 1-5s | Noticeable wait | Skeleton screen + Progress bar |
| > 5s | Long wait | Percentage progress + Estimated time |

### 9.5 Skeleton Screen vs Spinner Decision Tree

| Wait Time | Strategy |
|---------|------|
| 0-300ms | No wait indicator |
| 300ms-1s | Button internal Spinner / Micro progress indicator |
| 1s-5s | Skeleton screen + Top progress bar |
| > 5s | Skeleton screen + Percentage progress + Estimated time |

### 9.6 Haptic Feedback Standards (Mobile)

| Scenario | Duration | Type |
|------|------|------|
| Button confirmation | 10-15ms | Impact Light |
| Selection change | 5-10ms | Selection |
| Long press trigger | 15-20ms | Impact Medium |
| Success notification | 50-100ms | Notification Success |
| Error notification | 100-200ms | Notification Error |

### 9.7 Common Motion Patterns

| Pattern | Rule | Example |
|------|------|------|
| **Fade** | Opacity 0 → 1, combined with Enter/Exit easing | Toast entrance, Tooltip |
| **Slide** | TranslateY/X ±8-16px | Dropdown menu, drawer expansion |
| **Scale** | Scale 0.95 → 1.0, combined with Fade | Modal popup, menu |
| **Ripple** | Water ripple diffusion at click position, primary color 20% transparency | Material style buttons (optional) |

### 9.8 Animation Parameter Supplement

| Property | Recommended Value | Description |
|------|-------|------|
| Displacement distance | 4-8px | Slight movement feedback |
| Scale ratio | 0.95-1.05 | Press/release effect |
| Spring animation | Spring (damping: 0.7-0.9) | Pull-to-refresh, drag release |
| Performance constraint | Only animate `transform` and `opacity` | Avoid layout thrashing |

---

## 10. Accessibility Specifications

### 10.1 Contrast Standards

- **Body text (< 18px or non-bold)**: Background contrast >= 4.5:1 (WCAG AA)
- **Large text (>= 18px or bold >= 14px)**: Background contrast >= 3:1
- **UI components/icons**: Adjacent color contrast >= 3:1
- **Focus ring**: Background contrast >= 3:1, thickness >= 2px

### 10.2 Dual Coding Principle (Mandatory)

All state changes must use at least **two coding methods** (color+icon, color+text, color+shape). This is a **Level A compliance mandatory requirement**, not an optional best practice.

| Scenario | Wrong Approach | Correct Approach |
|------|---------|---------|
| Error state | Only red border | Red border + Error icon + Error text |
| Success state | Only green background | Green background + Checkmark icon + Success text |
| Disabled state | Only gray | Gray + Reduced transparency + Disabled cursor |
| Links | Only blue | Blue + Underline + Hover state |

### 10.3 Focus Management

- All interactive elements must have visible focus indicators
- Focus ring style: `2px solid color.brand-600` (Light) / `color.brand-400` (Dark), `offset: 2px`, border radius follows component
- **Prohibited**: Using only color change to indicate focus, must be supplemented with outline
- On dark background, default Focus color may be invisible, need to switch to white Focus
- Modal opens with focus trap, closes with focus returning to triggering element

### 10.4 Halation Effect Handling

Users with astigmatism reading white text on dark background experience "halation", making text appear bolder and blurrier. Solutions:

- Use **non-pure-white text color** (`#E0E0E0` not `#FFFFFF`)
- Increase **font weight** (from 400 to 500)
- Increase **line height** (from 1.5 to 1.6-1.7)

### 10.5 Keyboard Navigation

- All interactive elements operable via Tab / Enter / Space / Esc
- Dynamic content uses `aria-live="polite"` or `"assertive"`
- Custom components use `role` + `aria-*` attributes
- All images have `alt`, icons have `aria-label`, forms have `<label>`

### 10.6 Reduced Motion Preference

- Adapt to `prefers-reduced-motion: reduce` media query
- Implemented through Duration Scalar mechanism (see §9.3)
- High contrast mode adapts to `prefers-contrast: more` media query

### 10.7 Touch Targets

| Platform | Minimum Touch Area | Adjacent Spacing |
|------|------------|---------|
| iOS | 44 x 44pt | >= 8px |
| Android | 48 x 48dp | >= 8px |
| Web (Mobile) | 44 x 44px | >= 8px |
| Web (Desktop) | 24-32px | >= 4px |

### 10.8 Text Scaling

- Support 200% text scaling without content loss (WCAG 2.1 SC 1.4.4)
- Test Dynamic Type maximum font size layout still usable

---

## 11. Cross-Platform Adaptation Specifications

### 11.1 Cross-Platform Strategy

Recommend **"Brand Consistent + Interaction Native"** hybrid strategy:

1. **Brand layer consistent**: Colors, fonts, icon styles, spacing ratios unified across platforms
2. **Interaction layer native**: Navigation paradigms, gesture operations, popup forms, back logic follow each platform's specifications
3. **Component layer adaptive**: Same component maintains visual consistency across platforms but interaction adapts to platform

### 11.2 Design Draft Base Sizes

| Platform | Canvas Width | Description |
|------|---------|------|
| **iOS** | 375px (iPhone standard) | @1x baseline, @2x/@3x adaptation |
| **Android** | 360px (mainstream models) | mdpi baseline, xxxhdpi adaptation |
| **Web** | 1440px (desktop) | Responsive baseline, adapt down to mobile |

> **Core Principle**: One set of drafts adapts to multiple platforms, prioritize layout adaptation capability. iOS and Android canvas width difference is only 15px, automatically adapted through fluid layout (Flex/Grid).

**Fixed Component Height Specification**:

| Component | iOS Height | Android Height | Description |
|------|---------|-------------|------|
| Status bar | 44pt | 24dp | Top system status bar |
| Navigation bar | 44pt | 56dp | Page navigation title bar |
| Bottom Tab bar | 50pt | 56dp | Bottom tab navigation |
| Bottom safe area | 34pt | 48dp | Home Indicator / Gesture navigation area |

### 11.3 Mobile vs Desktop Size Specifications

| Dimension | Mobile | Desktop | Description |
|------|-------|--------|------|
| Minimum touch target | 44-48px | 24-32px | Mouse precision higher than finger |
| Element spacing | 8-16px | 4-8px | Mobile needs to prevent accidental touch |
| Button height | 48-56px | 32-40px | Mobile needs larger touch area |
| Input field height | 48-56px | 36-44px | Mobile needs larger click area |
| List item height | 56-72px | 40-48px | Mobile needs larger line height |
| Navigation depth | Within 3 layers | Multi-layer nesting | Mobile cognitive load limitation |
| Content display | Single column, vertical scroll | Multi-column, grid, sidebar | Screen space difference |
| Operation exposure | Hidden (menu, more) | Direct exposure (toolbar) | Space constraint difference |
| Form design | Step-by-step, single page few fields | Long form, multi-column layout | Mobile input cost high |
| Modal usage | Full-screen modal mainly | Centered popup, side drawer | Screen space difference |

### 11.4 Interaction Differences

| Dimension | iOS | Android | Web |
|------|-----|---------|-----|
| Hover state | None (touch device) | None (touch device) | Yes (mouse hover) |
| Press feedback | Highlight faded 70% | Ripple water wave | Background darkened + Y offset |
| Haptic feedback | Taptic Engine | HapticFeedback | Vibration API (limited) |
| Back gesture | Edge right swipe (system-wide) | Predictive back (Android 14+) | Browser back (no gesture) |
| Long press feedback | Context menu + haptic | Context menu + Ripple | Right-click menu (no haptic) |

> **Key Rule**: Touch devices have no Hover state, so **all functions cannot rely on Hover exposure**. DS must provide **equivalent operation paths** for each input mode.

### 11.5 Safe Area Constraints

| Platform | Top Safe Area | Bottom Safe Area | Side Safe Area |
|------|-----------|-----------|-----------|
| iOS (Notch) | 44pt | 34pt (Home Indicator) | 0pt |
| iOS (Dynamic Island) | 59pt | 34pt | 0pt |
| Android (Full screen) | 24dp | 48dp (Gesture navigation) | 0dp |
| Android (Three-button navigation) | 24dp | 0dp | 0dp |

> Bottom fixed buttons must be located **above the safe area**. Web's `env(safe-area-inset-*)` CSS variables can handle this automatically.

### 11.6 Density Token Control

| Density Mode | Mobile | Desktop | Applicable Scenario |
|---------|-------|--------|---------|
| **Compact** | Not recommended | Data-intensive backend | Recommended for keyboard/mouse devices |
| **Default** | Recommended | General scenario | General recommendation |
| **Comfortable** | Reading apps | Display pages | Recommended for touch devices |

> Density changes affect **spacing, font size, component size** three dimensions, cannot only change spacing.

---

## 12. Brand Token Mapping

> This section is a project mandatory requirement, defining the mapping relationship from brand color system to Design Tokens. Adopts single brand color strategy.

### 12.1 Brand Color System Definition

| Brand Color | Hex Value | Semantic | Usage Scenario |
|--------|--------|------|---------|
| [Brand primary color name] | [Hex] | Brand identity, call to action | Primary buttons, Logo, navigation active state, links, icon emphasis |