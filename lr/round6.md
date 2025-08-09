# Round 6 – Linear Regression with MLE Mode

## Context
Extension of the existing **Linear Regression** teaching demo to include a **Maximum Likelihood Estimation (MLE) mode**.  
This builds on Round 5 and follows **Design Contract v1 – Teaching Demos** in `AGENT_RULES.md`.  
If unsure about layout or style, refer to `docs/linear_regression_nn.html`.

The MLE framing should estimate **w**, **b**, and the **observation spread (σ)** for a Gaussian likelihood model:
\[
y_i \sim \mathcal{N}(w x_i + b, \sigma^2)
\]

## New Features
- **Mode toggle**:
  - Two buttons at top of controls: **Least Squares** (default) and **MLE Mode**.
  - Switching mode updates KPI, table, and plot display.
- **In MLE Mode**:
  - Sliders:
    - **w** (slope) – same range/step as before.
    - **b** (intercept) – same range/step as before.
    - **σ** (observation spread) – range [0.1, 5], step 0.01.
  - KPI: **Negative Log-Likelihood (NLL)**, 3 decimal places.
  - Table:
    - Columns: x, y (target), ŷ (prediction), log f(y | x), per-point NLL.
    - Fixed-width numeric columns (`tabular-nums`), no breathing.
  - Plot:
    - Keep regression line.
    - **No residual lines** in MLE mode.
    - Draw Gaussian curves centered at each predicted point with width σ (clip to plot area).
    - Label σ as *observation spread* in legend/tooltips.
  - Fit MLE button:
    - Optimizes w, b, σ jointly by maximizing log-likelihood.
- **In Least Squares Mode**:
  - Same as current behavior (MSE KPI, residual lines).
  - σ slider hidden.

## Shared Requirements
- Axes:
  - X-axis: same range as current demo.
  - Y-axis: automatically “nice” ticks in both modes.
- Table:
  - Stable layout (no width changes when values update).
  - Values rounded to 3 decimals.
- Works offline (no external CDN).
- Matches header, card, legend styles of other teaching demos.

## Acceptance Checks
- Mode toggle updates all relevant UI and plot elements instantly.
- “Fit MLE” produces identical results to analytical OLS for w and b when σ is free.
- Gaussian curves in MLE mode visually match the estimated σ.
- Observation spread is shown in correct units (same as y-axis scale).
- Offline-capable and compliant with **AGENT_RULES.md**.