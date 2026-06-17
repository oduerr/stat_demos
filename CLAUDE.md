# CLAUDE.md — Statistics Teaching Demos

A collection of standalone, interactive teaching demos for statistics / ML
concepts. Published as a GitHub Pages site from `docs/`. Each demo is a single
self-contained HTML file; `docs/index.html` is the catalog that links them all.

## Repo layout
- `docs/`            — the published site (each *.html is one demo)
- `docs/shared/`     — `demo-shell.css`, the shared dark theme (used by the SVG demos)
- `docs/<demo>/`     — multi-file demos (e.g. `bayes_lr/`: html + csv + stan)
- `animations/`      — Manim (Python) sources; rendered `.mp4` live in `docs/animations/`
- `<demo>/*.md`      — per-demo requirements / iteration notes (`lr/`, `log_regression/`, …)
- `documentation/`   — workflow notes

## Global rules (apply to every demo)
- Only touch the demo file you're asked to edit. Don't refactor neighbours.
- Don't change fonts, font sizes, or copy unless asked.
- Add every NEW demo as a link in `docs/index.html` (correct section).
- Preview locally: `cd docs && python3 -m http.server 8000`.

## Conventions (these vary per demo — match the file you're editing)
- Several demos load external libraries via CDN (Plotly, MathJax, Google Fonts).
  That is fine and intended — do **not** strip them out in the name of "offline".
- The SVG demos (`normal_mle`, `linear_regression_nn`, `logistic_regression`,
  `poisson_nb_regression`) are the exception: they import `shared/demo-shell.css`,
  stay fully offline (no CDN), and draw all plot primitives inside
  `<g clip-path="url(#plotClip)">` (clip rect = inner plot area), with axes,
  tick labels, titles and legends OUTSIDE the clip; use "nice" ticks. Follow
  those conventions only when editing that family.
- Regression demos: the equation line must show the right model (σ for logistic,
  exp for Poisson), and table columns must not change width when sliders move
  (`tabular-nums`).
- Animations are Manim Python in `animations/`, rendered to `.mp4` under
  `docs/animations/`.
