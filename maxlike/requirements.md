# Demo Requirements – MLE for Normal Distribution

## Context
Interactive teaching demo for Maximum Likelihood Estimation of μ and σ in a Normal distribution, based on the dataset:
`xs = [-0.033, -0.76, 2.02, 1.13, 0.65, 0.49, 0.76, 0.40, 0.10, 0.61]`

Follow **Design Contract v1 – Teaching Demos** (in `AGENT_RULES.md`) for layout, style, and shared behavior.  
If unsure about a design decision, refer to the linear regression example `docs/linear_regression_nn.html`.  
Use the shared CSS/JS imports exactly as in the template.

## Features
- **Sliders:**
  - μ (mean): range [-5, 5], step 0.01
  - σ (standard deviation): range [0.1, 5], step 0.01
- **Plot:**
  - X-axis: fixed range [-2, 2], “nice” ticks
  - Y-axis: density scale, auto “nice” ticks
  - Display the Normal PDF `N(μ, σ²)` as a smooth SVG path
  - Show data points along baseline (y=0) as small circles
  - Clip all primitives to the plot area (`plotClip`)
- **KPI:**
  - Current negative log-likelihood (rounded to 3 decimals), updated live with slider changes
- **Table:**
  - Columns: x, density f(x), log f(x)
  - Fixed-width numeric columns (`tabular-nums`), no breathing when numbers update
  - Values rounded to 3 decimals
  - Below the table: sum of log-likelihood and the negative log-likelihood
- **Buttons:**
  - **Fit MLE** (computes μ̂, σ̂ by maximizing log-likelihood for given data)
- **Equation:**
  - Display: `f(x) = 1/(σ√(2π)) · exp(-(x-μ)² / (2σ²))`

## Acceptance Checks
- Sliders update plot, KPI, and table instantly
- Axes and ticks follow Design Contract rules
- Table layout stable when numbers change
- Works fully offline; no external CDN
- Styling, header, and cards match other teaching demos
- No elements draw outside plot area