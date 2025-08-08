## Goal

A single-page, self-contained web demo showing that **linear regression** is equivalent to a **single-layer neural network** (no hidden layer). The user should be able to play around with sliders and seeing the immediate effect on the one side the weights get larger, on the other side the slope or the intercept changes.



## Functional Requirements

### 1) Linear 1D Regression
- Use a small set of **initial data points** (≈ 5–10).
- Allow the user to **drag data points vertically** to change their values  
  *(x stays fixed, y changes with drag).*

### 2) Sliders
- **Slope (w)**
- **Intercept (b)**
- Slider changes must:
  - Update the **regression line**.
  - Update predicted values \( \hat{y} = w x + b \).
  - Update the **weights** in the neural-network visualization.

### 3) Neural Network Visualization
- Display two weights:
  - **Weight 1 = slope (w)**
  - **Weight 2 = intercept (bias, b)**
- When sliders are moved, the weights update **live**.
- Explicitly show \( \hat{y} = w \cdot x + b \).

### 4) Fit Button
- Button label: **Fit Weights**.
- On click:
  - Compute **best-fit slope and intercept** via **least squares**.
  - Update sliders and the displayed weights accordingly.

---

## UX / UI Suggestions
- **Left side**: plot with **draggable data points** and the **regression line**.
- **Right side**: schematic of a **neural network** (input → weights → output).
- Display **loss (MSE)**.
- Keep layout **responsive** and **intuitive**.