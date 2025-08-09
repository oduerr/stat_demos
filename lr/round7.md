# Agent Task – Round 7: MLE Mode (polishing)

## Context
You are refining the "Linear Regression = Single-Layer Neural Network" demo.  
Follow the general agent rules we have defined earlier (code in same HTML file unless explicitly stated otherwise, only CSS in separate file, consistent formatting, clear UI/UX, and responsive layout).

---

## Requirements

### MLE Mode Refinements
1. **Lowercase Parameters**
   - Ensure \( \mu \) and \( \sigma \) are rendered in lowercase everywhere in the Control Panel, formula displays, and network diagram.

2. **Prediction Naming**
   - In MLE mode, the prediction line should be labeled \( \hat{\mu} \) in the plot legend, in the network diagram, and anywhere else it appears (replace any “ŷ” or similar with \( \hat{\mu} \)).

3. **Table Enhancements**
   - Add a column for log-likelihood of each data point:  
     \( \log f(y_i \mid x_i) = -\frac{1}{2} \log(2\pi\sigma^2) - \frac{(y_i - \hat{\mu}_i)^2}{2\sigma^2} \).
   - Keep the Σ-row with sums/totals pinned at the bottom.
   - Add vertical scrolling if the table exceeds available space.

4. **Formula Update**
   - Change display from \( \hat{\mu} = b + w x \) to:
     \[
     y_i \sim N(\hat{\mu}_i, \hat{\sigma}), \quad \hat{\mu}_i = b + w x_i
     \]
   - Apply this in the formula area in the Control Panel.

5. **Hover Tooltips**
   - For each data point, show: \( x_i, y_i, \hat{\mu}_i, \sigma, \log f(y_i \mid x_i) \).

6. **Legend / Label Cleanup**
   - Rename “Observation Gaussians (σ)” → “Observation Spread (σ)”.
   - Remove “Data points” label if it is already visually obvious.

7. **Math Note (Optional but Preferred)**
   - Add a collapsible info section below the plot:
     - Briefly explain how MLE for a Gaussian leads to least squares when σ is unknown.
     - Mention why σ is estimated by maximizing the likelihood.

---

## General Implementation Rules (from previous agent instructions)
- Keep **all JavaScript logic in the same HTML file** (only extract CSS to a separate `.css` file).
- Use **clear, self-contained code** that can run without build tools.
- Maintain consistent visual style and layout as in the current design.
- Ensure the UI is responsive and works on both desktop and mobile.
- Write clean, commented code for maintainability.
- Follow mathematical notation exactly as described above.

---