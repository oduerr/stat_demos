Patch Requirements — MLE Normal Demo (UI polish)

Edit only: docs/<your_mle_demo>.html
Follow: Design Contract v1 – Teaching Demos (AGENT_RULES.md). Keep JS inline, CSS via ./shared/demo-shell.css. No external CDNs.

A. Plot fixes
	1.	X-axis domain
	•	Hard-set to [-1, 3] (no autoscale). Keep “nice” ticks.
	2.	Ensure points are always visible
	•	Keep points drawn on baseline y=0 but guarantee visibility within clip (use existing plotClip).
	3.	Data-to-curve connector
	•	For each data point x_i, draw a subtle vertical guide from (x_i, 0) up to the PDF value f(x_i | μ, σ).
	•	Style: thin, semi-transparent line (same hue as PDF, lower opacity). Pixel-snap for crispness.
	4.	Legend cleanup
	•	Remove “at y=0” in Data points legend entry.
    5. Rename y-axis to density f(x|μ,σ) 

B. Controls panel
	1.	Rename labels
	•	“M (MEAN)” → μ
	•	“Σ (STD DEV)” → σ (use lowercase sigma in the label).
	2.	Remove formula block under the sliders.
	3.	KPI
	•	Keep Negative log-likelihood pill, 3 decimals, updates live.

C. Table usability
	1.	Scrollable table body
	•	Fix header + footer; make tbody scrollable so the totals/footer remain visible.
	•	Show vertical scrollbar when rows overflow (desktop and small screens).
	2.	Footer totals
	•	Keep: Σ log f(x) and Negative log-likelihood.
	3.	Stability
	•	Maintain fixed column widths + tabular-nums (no breathing).

D. Accessibility & polish (small)
	•	Clip all plot primitives inside plotClip; axes/labels not clipped (per rules).
	•	Tooltip/aria-label on points: “x = {x}, f(x) = {density}”.
	•	Ensure contrast of points and connectors against background (use existing palette).
	•	Keep everything offline-ready; no new deps.

Acceptance checklist
	•	Changing μ or σ: points remain visible; PDF updates; vertical guides reach exactly the curve value.
	•	X-axis shows −1 … 3; Y uses nice ticks.
	•	Legend has no “data points at y=0” entry.
	•	Controls show Mean (μ) and Std dev (σ); no formula box.
	•	Table header/footer are fixed; tbody scrolls and totals always visible.
	•	No drawing outside the plot area; no layout jitter in the table.
	•	Works offline; no console errors.

⸻

If you want, I can also give the agent code hints (CSS for sticky header/footer + scrollable tbody, and the tiny SVG snippet for the vertical connectors).