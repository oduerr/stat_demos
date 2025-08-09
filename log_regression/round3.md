# Logistic Regression GUI – Round 3 Polishing

## File
`logistic_regression.html`

## Goal
Polish the current GUI for clarity and usability while keeping all existing functionality intact.

## Requirements

### 1. Loss Curve
- Add **axis labels**:  
  - x-axis: “Iterations”  
  - y-axis: “Log loss”
- Add numeric ticks to both axes (auto-scale, ~5–7 ticks).
- Increase plot height to better use available space.
- Match style (colors, font sizes, weight) to the **Probability Curve** plot.
- **Always show the loss curve**, even at iteration 0. Initialize with an empty (flat) line and update dynamically.

### 2. Controls
- Group **Fit One Step**, **Fit N Steps**, and **Start Continuous Fit** under a “Fitting Controls” section.
- Show **learning rate** as a numeric value next to the slider.
- Keep `Iter:` counter visible and move it next to the loss curve plot.
- **Reset Weights**: replace “Reset Data” button with “Reset Weights” and implement functionality to reset slope (w) and intercept (b) to their initial values (zero or small random), without changing the dataset.

### 3. Additional Dataset Functionality
- Add a **second dataset** to the data table:
  - Class 0: points centered at -1, standard deviation 2
  - Class 1: points centered at 1, standard deviation 2
  - ~5 points per class (randomly generated on creation)
  - Allow data points to be moved vertically after creation
- Add a **dropdown** to switch between datasets (and later a possible third one).
- Switching datasets should immediately refresh the plot and metrics.
- Switching to the first dataset should randomly generate the data points again.

### 4. Output Metrics
- Group `Log loss (avg)`, `Accuracy @ τ=0.5`, and `Iter` into a single compact metrics bar.
- Optionally add small icons or subtle color coding to improve readability.

### 5. General
- Reduce unused space in the lower-right panel.
- Ensure **color, font, and size consistency** across all plots, labels, and metrics.