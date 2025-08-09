# Round 2 – Polishing

**File:** `logistic_regression.html`  
**Follow:** `AGENT_RULES.md`. Don’t change unrelated code.

---

## Fix the fit modes (functional)

1. **Single button set**
   - Remove the radio group for mode selection.
   - Keep three buttons:
     - **Fit One Step**
     - **Fit N Steps** (default N=1000; add a small numeric input for N)
     - **Start/Stop Continuous Fit** (toggle state)

2. **Refactor optimizer**
   - Implement a pure `step(w,b)` function that returns  
     `{ wNew, bNew, loss, gw, gb }` for one gradient descent update.
   - Maintain global training state:  
     `{ iter, running, history: [] }`.
   - **Fit One Step:**  
     Call `step` once, push loss to `history`, re-render.
   - **Fit N Steps:**  
     Reset `history`, loop `N` times (synchronously), push each loss, re-render at the end.
   - **Continuous:**  
     Reset `history`, set `running = true`, then iterate with `requestAnimationFrame` (or `setTimeout(0)`), one `step` per frame; stop on button press or convergence.
   - Convergence criteria:  
     Stop if `|Δw| + |Δb| < 1e-7` **or** if loss change < `1e-8` for 20 consecutive steps.
   - Sync sliders to updated `w,b` after each step.

3. **Show iterations**
   - Add a small counter “Iter: ####” next to the KPI; update it live.

---

## Loss curve

4. Add a compact SVG under the controls titled **“Log loss vs. iteration”**:
   - X axis = iteration, Y axis = loss.
   - Use *nice* tick marks on both axes; display numeric labels.
   - For **One Step**: append a single point without resetting axes.
   - For **N Steps** & **Continuous**: clear `history` before starting.
   - Clip to plot area (using an SVG `clipPath`); no overflow drawing.
   - Keep colors consistent with the main palette.

---

## UI cleanup

5. **Remove “Add Data Point”** button and delete all related logic.
6. **Legend color match:**  
   Ensure the curve stroke color exactly matches the legend swatch.
7. **Typography:**
   - Use **U+2212** (minus) in the equation box.
   - Round `w` and `b` to 3 decimal places in the equation.
   - Round `p̂` and loss values to 3 decimal places.
   - Use `tabular-nums` for aligned numeric columns.

---

## Y-axis & tooltips

9. Point tooltip should display:  
   `x, y, p̂, logit, per-point loss`.

---

## Acceptance criteria

- **Fit One Step** visibly nudges the curve once; `iter` increases by 1; loss history gains one entry.
- **Fit N Steps** runs exactly N updates; `iter` increases by N; loss curve shows N samples.
- **Continuous Fit** animates until stopped or convergence; UI remains responsive.
- Loss curve has labeled axes and correct scaling.
- “Add Data” UI and its code are fully removed.
- Layout is stable with no jitter.
- Works fully offline with no console errors.