---
name: Empório da Música & Ozzy
colors:
  surface: '#1A1330'
  surface-dim: '#1d100c'
  surface-bright: '#463630'
  surface-container-lowest: '#170b08'
  surface-container-low: '#261814'
  surface-container: '#2a1c18'
  surface-container-high: '#352722'
  surface-container-highest: '#41312c'
  on-surface: '#f7ddd5'
  on-surface-variant: '#e1bfb5'
  inverse-surface: '#f7ddd5'
  inverse-on-surface: '#3c2d28'
  outline: '#a98a80'
  outline-variant: '#594139'
  surface-tint: '#ffb59d'
  primary: '#FF6B35'
  on-primary: '#5d1900'
  primary-container: '#ff6b35'
  on-primary-container: '#5f1900'
  inverse-primary: '#ab3500'
  secondary: '#7C5CFF'
  on-secondary: '#31009a'
  secondary-container: '#4816cb'
  on-secondary-container: '#b9aaff'
  tertiary: '#59d5fb'
  on-tertiary: '#003543'
  tertiary-container: '#00a7cb'
  on-tertiary-container: '#003744'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#ffb59d'
  on-primary-fixed: '#390c00'
  on-primary-fixed-variant: '#832600'
  secondary-fixed: '#e6deff'
  secondary-fixed-dim: '#cabeff'
  on-secondary-fixed: '#1c0062'
  on-secondary-fixed-variant: '#4816cb'
  tertiary-fixed: '#b5ebff'
  tertiary-fixed-dim: '#59d5fb'
  on-tertiary-fixed: '#001f28'
  on-tertiary-fixed-variant: '#004e60'
  background: '#1d100c'
  on-background: '#f7ddd5'
  surface-variant: '#41312c'
  bg: '#0F0B1A'
  surface-2: '#251B45'
  accent: '#F7C948'
  success: '#3DDC97'
  text: '#F5F1FF'
  text-muted: '#A79FC4'
  danger: '#FF4D6D'
typography:
  headline-lg:
    fontFamily: Poppins
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-md:
    fontFamily: Poppins
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Poppins
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system channels an acoustic-meets-digital aesthetic, combining the warm, inviting charm of a traditional instrument shop with the sleek efficiency of a modern AI assistant. The personality is vibrant, approachable, and deeply musical—evoking the feeling of walking into a friendly boutique studio.

We utilize a **Glassmorphism-infused Dark UI** style, featuring deep stage-like backgrounds, translucent layered surfaces, and soft chromatic glows that mimic vacuum-tube amplifiers and polished instrument brass.

## Colors

The color palette is anchored by a near-black purple background (`#0F0B1A`) representing a dark stage or studio environment. The chromatic hierarchy relies on an energetic valve-amplifier orange (`#FF6B35`) for primary actions and user messages, complemented by instrument-brass gold (`#F7C948`) for accents and promotions. Secondary purple (`#7C5CFF`) and supportive surface tones create clear visual depth for the chat assistant's interface elements.

## Typography

Typography pairs **Poppins** for expressive, geometric headings with **Inter** for clean, highly legible chat body text and metadata. This combination maintains a modern technical edge while keeping conversational elements exceptionally readable. Use `--text-muted` (`#A79FC4`) at 12px for timestamps, tags, and microcopy.

## Layout & Spacing

The layout model employs a centered chat card structure (420px–480px width) on desktop, maximizing focus within a subtle gradient background, and expands to a fluid, full-screen layout on mobile devices. Spacing follows a consistent 4px/8px rhythm utilizing tokens to govern gaps between message bubbles, interactive chips, and action bars.

## Elevation & Depth

Visual hierarchy is achieved through **tonal surface layering** combined with **ambient low-opacity glows**. 
- Base surfaces (`#0F0B1A`) sit underneath container cards (`#1A1330`) and interactive bubbles (`#251B45`).
- Key interactive elements feature subtle, diffused orange glows (`#FF6B35` at low opacities) to simulate warm tube-amp illumination.
- Borders are kept minimal, relying on soft, low-contrast outlines to separate panels without visual clutter.

## Shapes

The shape language is heavily rounded and friendly, reinforcing the approachable mascot personality. 
- Message bubbles use a 20px radius, with specific directional flattening (e.g., bottom-left corner squared on Ozzy's bubbles).
- Cards and structural containers use a 16px radius.
- Buttons, input fields, and suggestion chips use fully rounded "pill" geometries.

## Components

### Buttons
- **Primary:** Pill-shaped, filled with `#FF6B35`, featuring a soft orange ambient glow and crisp text contrast.
- **Icon / Action:** Circular send buttons with primary gradient fills and hover scale transitions.

### Chips & Tags
- **Suggestion Chips:** Pill containers with translucent surfaces and `--accent-2` borders (`#7C5CFF`), transitioning to solid fills on hover.
- **Policy/Status Tags:** Small rectangular badges with subtle background padding, incorporating tiny leading icons (documents, checks).

### Input Fields
- **Chat Input:** Full-width pill container using `--surface-2` background, featuring a subtle gradient border on focus and integrated inline actions.

### Lists & Messages
- **Ozzy Bubble:** Background `--surface-2`, aligned left, accompanied by the 40x40px avatar and stylized tail.
- **User Bubble:** Background `--primary`, aligned right, with high-contrast text.
- **Typing Indicator:** Animated 4-bar vertical equalizer accompanied by contextual microcopy.

### Cards
- **Product Card:** Square media thumbnail, bold typography for product names, highlighted active pricing, struck-through MSRP, and a gold `-20%` promo badge (`#F7C948`).
- **Handoff / Support Card:** Elevated container with gradient borders for agent transfer states.