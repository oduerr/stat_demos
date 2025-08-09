# Poisson & Negative Binomial Regression Demo – COVID-19 Count Data

**File:** `poisson_nb_regression.html`

## Context
Create an interactive teaching demo for Poisson and Negative Binomial regression, based on the real German COVID-19 case counts (March 1–20, 2020) and an artificial, fully draggable dataset.

The interface and behavior must match **`logistic_regression.html`** from the teaching demos, except that:
- This is **count data** with a **log-link** model.
- No classification probabilities; output is the expected count \(\hat{\mu}\).
- Reuse **exactly the same fitting loop and gradient descent mechanism** from `logistic_regression.html`, just replacing the loss and gradient formulas for Poisson and Negative Binomial.

## Dataset 1 – Real Data (fixed)

Just use t(called x in plot) and y values.

| t  | y     | date       |
|----|-------|------------|
| 1  | 130   | 2020-03-01 |
| 2  | 159   | 2020-03-02 |
| 3  | 196   | 2020-03-03 |
| 4  | 262   | 2020-03-04 |
| 5  | 482   | 2020-03-05 |
| 6  | 670   | 2020-03-06 |
| 7  | 799   | 2020-03-07 |
| 8  | 1040  | 2020-03-08 |
| 9  | 1176  | 2020-03-09 |
| 10 | 1457  | 2020-03-10 |
| 11 | 1908  | 2020-03-11 |
| 12 | 2078  | 2020-03-12 |
| 13 | 3675  | 2020-03-13 |
| 14 | 4585  | 2020-03-14 |
| 15 | 5795  | 2020-03-15 |
| 16 | 7272  | 2020-03-16 |
| 17 | 9257  | 2020-03-17 |
| 18 | 12327 | 2020-03-18 |
| 19 | 15320 | 2020-03-19 |
| 20 | 19848 | 2020-03-20 |

- Fixed data — cannot be dragged.

## Dataset 2 – Artificial Data (draggable)
- 8 points generated around a linear trend:
  \[
  y \sim \text{Poisson}(\mu), \quad \log(\mu) = 2 + 0.3x
  \]
- X values initially between 0 and 10, spaced evenly.
- Points are fully draggable in **both X and Y** directions.

## Model
Fit:
\[
y_i \sim \text{Poisson}(\mu_i), \quad \log(\mu_i) = b + w \cdot x_i
\]
and
\[
y_i \sim \text{NB}(\mu_i, \theta), \quad \log(\mu_i) = b + w \cdot x_i
\]
where \(\theta\) is the dispersion parameter.

## Requirements

### 1. Match Logistic Regression Demo Structure
- Same control layout: **Fit One Step**, **Fit N Steps**, **Start Continuous Fit**.
- Same iterative fitting loop, same gradient descent mechanics.
- Loss curve = negative log-likelihood for Poisson/NB.
- Show iteration counter.
- Keep **Reset Weights** button and functionality.

### 2. Dataset Handling
- Dropdown to switch between **Dataset 1 (COVID)** and **Dataset 2 (Artificial)**.
- Dataset 1: fixed, no dragging.
- Dataset 2: fully draggable in X and Y.

### 3. Plots
- Main plot:
  - X-axis = time/index (for COVID) or X variable (for artificial).
  - Y-axis = counts.
  - Points = observed data.
  - Line = predicted \(\hat{\mu}\).
  - Optional shaded area = ± 1 std dev (variance from Poisson/NB).
- Loss curve:
  - X-axis = iterations, Y-axis = negative log-likelihood.
  - Numeric ticks, styled consistently with logistic regression demo.

### 4. Output Distributions at Data Points
- Like in the **linear regression demo** where Gaussians were shown at each data point, here show:
  - **Poisson probability mass functions** for Poisson regression.
  - **Negative Binomial probability mass functions** for NB regression.
- Draw these small PMF plots vertically aligned at each X position, centered on \(\hat{\mu}\) and scaled appropriately.
- The height of the distribution should reflect the probability values.

### 5. Controls
- Model type dropdown: **Poisson** / **Negative Binomial**.
- Learning rate slider + numeric display.

### 6. Output Metrics
- Show fitted parameters: intercept \(b\), slope \(w\), dispersion parameter \(\theta\) (NB only).
- Show final negative log-likelihood.
- If NB selected, also show estimated variance.

### 7. General
- Style and layout consistent with `logistic_regression.html`.
- No external dependencies (CDN-free).