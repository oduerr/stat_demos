Requirement – Round 1: MLE Fitting Modes with Loss Curve

Context

Enhancement of the MLE teaching demo to provide flexible fitting modes and live visualization of optimization progress. Follow all style and functional constraints in AGENT_RULES.md and preserve existing layout and offline capability.

Features to Implement
	1.	Fitting Modes
	•	Fit One Step – perform exactly one gradient descent update, then stop.
	•	Fit N Steps – perform a fixed number of steps (default 1000) then stop.
	•	Continuous Fit – run gradient descent until convergence or until stopped by the user.
	2.	UI Changes
	•	Add a mode selector above the existing Fit button:
	•	Three radio buttons or a dropdown: One Step, N Steps, Continuous.
	•	Replace the single “Fit MLE” button with:
	•	“Fit One Step”
	•	“Fit N Steps”
	•	“Start Continuous Fit” / “Stop Continuous Fit” (toggle)
	3.	Loss Curve Plot
	•	Add a small plot showing Negative Log-Likelihood vs. iteration.
	•	Update the plot live while fitting.
	•	For Fit One Step: append the new point to the plot without clearing.
	•	For Fit N Steps and Continuous: clear the plot at the start of fitting.
	4.	Responsiveness
	•	UI must remain interactive during Continuous Fit.
	•	Use requestAnimationFrame or an async loop to avoid blocking rendering.
	5.	Preserve Existing Behavior
	•	Predictions, residuals (or observation spread), and MLE displays must still work.
	•	Follow Design Contract v1 for all layout, tick formatting, and offline rules.

Acceptance Criteria
	•	All three fitting modes are available and functional.
	•	Loss curve updates in real-time during fitting.
	•	Continuous fit can be stopped via toggle button.
	•	No external CDN usage; all scripts and styles remain local.
	•	UI remains responsive during fitting.
	•	Styling matches other teaching demos.