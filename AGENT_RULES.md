# Design Contract v1 – Teaching Demos

## Non-negotiables
- **Do NOT** change fonts, font sizes, or copy unless asked
- **Do** import shared files exactly as shown in the demo templates
- Keep all demos offline-capable (no CDN, no build steps)

## Layout & components
- Use the standard shell: header → 2-column grid → two `.card`s.
- Numeric UI (tables, KPI pills): `tabular-nums`, fixed column widths, no “breathing”.
- Axes: call `niceTicks()` for Y, exact tick list for X when specified.
- Plot: SVG only; pointer events for drag; pixel-snap gridlines.

### Clipping (plot hygiene)
- All plot primitives (prediction line, best-fit line, residuals, data points) MUST be drawn inside a `<g clip-path="url(#plotClip)">` where the clip rect equals the inner plot area (`x=pad.l`, `y=pad.t`, `width=innerW`, `height=innerH`).
- Axes, tick labels, titles, and legends MUST NOT be clipped.
- No math or statistics is altered for clipping; it is purely visual.
- Acceptance: Nothing renders outside the inner plot area on any window size.

## Model-specific bits per demo
- **Linear:** ŷ = w·x + b; KPI label: “MSE”.
- **Logistic:** p̂ = σ(w·x+b); y ∈ {0,1}; KPI: “Log loss” (+ optional accuracy @ τ).
- **Poisson:** λ̂ = exp(w·x+b); y ∈ ℕ; KPI: “Poisson NLL”.
- New demos must:
  - Reuse the same header/subtitle/card/legend styles.
  - Keep buttons: Fit Weights, Add Data Point, Create New Data.
  - Fill the table with 5 cols (x, target, prediction, helper metric, per-point loss).

## Acceptance checks (agent must ensure)
- No external `<script>` or `<link>` except the two shared local files.
- Table columns do not change width when sliders move.
- Axes ticks are “nice”; labels clean (no long floats).
- Equation line shows correct model (σ for logistic, exp for Poisson).

## Only touch
- The target demo file you’re asked to edit