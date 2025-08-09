
Round 8 – MLE Mode Final Polishing Requirements

1. Header
	•	In MLE mode, remove the text = Single-Layer Neural Network (No Hidden Layer) from the header.
	•	Header should simply read “Linear Regression”.

2. Formula Panel (Right Side)
	•	In MLE mode, show:
y_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = w \cdot x_i + b
	•	Ensure subscripts (y_i, x_i, \mu_i) are vertically aligned and correctly placed.
	•	Dynamically insert the current estimated \sigma value (rounded to 2–3 decimals) into the formula.
	•	Use proper minus sign (U+2212) for negative values.
	•	Round w, b, and \sigma consistently to 2–3 decimals.
	•	If lowercase \sigma does not render correctly in the current JS math rendering, force it to lowercase via Unicode σ or MathJax equivalent.

3. Controls Panel
	•	Use lowercase symbols in labels:
	•	Slope (w) instead of SLOPE (W)
	•	Intercept (b) instead of INTERCEPT (B)
	•	σ (Spread) instead of Σ (SPREAD)
	•	Keep “Observation Spread” term instead of “Noise”.

4. Prediction Line & Legend
	•	In MLE mode, rename the “Prediction line” legend to “Prediction line (\hat{\mu})”.
	•	Match legend color exactly to the plot line.
	•	Keep “Observation Spread (\sigma)” label in the legend.

5. Table
	•	In MLE mode, add a per-point log-likelihood column before the per-point NLL.
	•	Ensure numbers are right-aligned for easy reading.

6. Network Diagram Replacement
	•	In MLE mode, remove the neural network diagram.
	•	Replace with a parameter summary panel showing:
	•	Estimated w, b, \sigma
	•	95% confidence intervals for each (computed with Gaussian approximation to the MLE covariance matrix — this is acceptable).
	•	CI format: \text{estimate} \; [\text{lower}, \text{upper}].

7. General Visual Fixes
	•	Ensure consistent math font and symbol style across all parts of the UI (plot labels, formulas, controls).
	•	Keep equation indices and symbols visually aligned.
