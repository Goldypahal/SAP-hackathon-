---
name: CareerIntel Professional
colors:
  surface: '#faf8ff'
  surface-dim: '#d7d9ec'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eef4ff'
  surface-container: '#ebedff'
  surface-container-high: '#dfe9fa'
  surface-container-highest: '#e0e1f4'
  on-surface: '#181b28'
  on-surface-variant: '#434655'
  inverse-surface: '#2d303e'
  inverse-on-surface: '#eff0ff'
  outline: '#737685'
  outline-variant: '#c3c6d7'
  surface-tint: '#1b55d0'
  primary: '#003594'
  on-primary: '#ffffff'
  primary-container: '#004ac6'
  on-primary-container: '#b8c8ff'
  inverse-primary: '#b4c5ff'
  secondary: '#006c4a'
  on-secondary: '#ffffff'
  secondary-container: '#9af1c6'
  on-secondary-container: '#0b714e'
  tertiary: '#603200'
  on-tertiary: '#ffffff'
  tertiary-container: '#824500'
  on-tertiary-container: '#ffbc85'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#9df4c9'
  secondary-fixed-dim: '#81d8ae'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005237'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77c'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#faf8ff'
  on-background: '#181b28'
  surface-variant: '#e0e1f4'
typography:
  display:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  huge: 48px
---

## Brand & Style
CareerIntel embodies a **Corporate/Modern** aesthetic tailored for professional growth and data-driven insights. The brand personality is reliable, systematic, and empowering, focusing on "Career Intelligence." 

The UI uses a structured, information-dense layout that remains breathable through purposeful whitespace and a refined color palette. It avoids unnecessary decoration, opting for functional clarity and a sense of "executive precision." The visual style leans into high-quality typography and subtle tonal variations to guide the user's focus through complex data sets.

## Colors
The palette is rooted in a deep "Trust Blue" (Primary), supported by "Growth Green" (Secondary) and "Insight Amber" (Tertiary). 

- **Primary (#004ac6):** Used for brand identity, key actions, and primary data highlights.
- **Secondary (#006c4a):** Represents positive trends, readiness, and success metrics.
- **Neutral:** A range of cool-toned grays and off-whites facilitate a layered "Surface" system, ensuring that data containers are distinct from the background without relying on heavy shadows.
- **Functional Tints:** Backgrounds leverage subtle blue-tinted whites (`#f8f9ff`) to maintain a clean, modern feel that is easier on the eyes than pure white.

## Typography
The system uses **Inter** exclusively to achieve a utilitarian and corporate feel. 

- **Hierarchy:** Dramatic contrast is created by using `display` for page titles and `label-sm` for metadata.
- **Weights:** Heavy use of Semibold (600) and Bold (700) for headers ensures clear section breaks in data-heavy views.
- **Readability:** Tight letter-spacing on larger displays maintains a contemporary, "tight" look, while slightly increased spacing on labels ensures legibility at small sizes.

## Layout & Spacing
The layout follows a **Fixed Grid** approach for desktop, centering content within a `max-w-screen-xl` (1280px) container.

- **Grid System:** A 12-column bento-style grid is used for the dashboard. Sections typically span 4, 8, or 12 columns.
- **Breakpoints:** 
  - **Desktop (768px+):** Horizontal navigation in the TopAppBar, 12-column grid layout, increased padding (`xl`).
  - **Mobile (<768px):** Bottom navigation bar for ergonomics, single-column stack, reduced horizontal margins (`lg`).
- **Rhythm:** Spacing follows a 4px/8px base-2 scale. `24px (xl)` is the standard gap between major cards and sections.

## Elevation & Depth
The system utilizes **Tonal Layers** and **Low-contrast Outlines** rather than heavy shadows to denote elevation.

- **Surface Levels:** The background uses `surface` (#f8f9ff). Primary content containers use `surface-container-lowest` (#ffffff).
- **Borders:** Containers are defined by a 1px border using `outline-variant` (#c3c6d7).
- **Interactive Depth:** Hover states are indicated by shifting background colors to `surface-container-low` (#eef4ff) rather than increasing shadow depth.
- **Shadows:** Avoid shadows entirely to maintain a flat, professional, and performance-oriented aesthetic.

## Shapes
A **Rounded** shape language is applied to balance the "serious" corporate typography. 

- **Standard Cards:** Use `12px` (rounded-xl) for main containers to provide a modern, friendly frame for data.
- **Buttons/Interactive Elements:** Use `8px` (rounded-lg) for a more precise, clickable feel.
- **Tags/Status Pills:** Use `9999px` (full) to clearly distinguish them from structural elements.
- **Small Components:** Icons or small hover states use `4px` (rounded-sm) or `full` depending on the context.

## Components
- **Buttons:**
  - *Primary:* High-contrast background (on-primary-container) with bold text. Full-width on mobile.
  - *Ghost:* No border, primary text, background appears on hover.
- **Cards:** White background, 1px `outline-variant` border, `12px` corner radius. Used for "Bento" sections.
- **Status Chips:** Small, uppercase bold text with low-opacity backgrounds (`secondary-container/20`).
- **Data Visualizations:** Vertical bars with rounded tops (`rounded-t-sm`). Use varying opacities of the `primary` color to show historical vs. current data.
- **Navigation:**
  - *Web:* Top-aligned, text-based with active states highlighted in the primary color.
  - *Mobile:* Bottom-fixed bar with icons (Material Symbols Outlined) and labels.
- **Lists:** Horizontal padding of `12px`, with thin separators (`outline-variant/30`) and chevron indicators for drill-down actions.