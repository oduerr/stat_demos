from manim import *
import numpy as np
import math


class PDFtoCDFLocalStack(Scene):
    """
    What this shows (your clarified intent):

    TOP (PDF):
      - Normal PDF curve
      - Riemann rectangles under the PDF (color gradient left->right)

    BOTTOM (CDF):
      - A *local* stack/column of width dx at the current x-bin
      - The column contains the full history: all previous contributions stacked below
      - Each new PDF bin transfers into a new layer added ON TOP of the current stack
      - (Optional) We leave behind faint 'ghost' stacks so the past is visible in x as well

    No always_redraw / updaters -> stable in manim 0.19.x.
    """

    def pdf(self, x: float) -> float:
        # Standard normal PDF
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

    def construct(self):
        # -----------------------------
        # Parameters
        # -----------------------------
        x_min, x_max = -3.2, 3.2
        n_bins = 30
        xs = np.linspace(x_min, x_max, n_bins + 1)
        dx = float(xs[1] - xs[0])

        # Animation feel
        ghost_history = True          # leave faint stacks behind
        ghost_opacity = 0.12          # opacity for old stacks
        layer_opacity = 0.88
        move_time = 0.10
        transfer_time = 0.22

        # -----------------------------
        # Axes layout
        # -----------------------------
        ax_pdf = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 0.45, 0.1],
            x_length=11.5,
            y_length=3.0,
            tips=False,
        ).shift(UP * 2.1)

        ax_cdf = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 1.05, 0.25],
            x_length=11.5,
            y_length=3.0,
            tips=False,
        ).shift(DOWN * 2.5)

        pdf_labels = ax_pdf.get_axis_labels(Tex("x"), Tex("f(x)"))
        cdf_labels = ax_cdf.get_axis_labels(Tex("x"), Tex("F(x)"))

        title = Tex(r"PDF $\rightarrow$ CDF as integration").scale(0.85).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.wait(0.5)
        self.play(
            FadeOut(title, shift=UP * 0.2),
            run_time=1.0,
        )
        
        self.play(Create(ax_pdf), FadeIn(pdf_labels), run_time=0.8)
        self.play(Create(ax_cdf), FadeIn(cdf_labels), run_time=0.8)

      
        
        # -----------------------------
        # PDF curve
        # -----------------------------
        pdf_graph = ax_pdf.plot(lambda x: self.pdf(x), x_range=[x_min, x_max], stroke_width=4)
        self.play(Create(pdf_graph), run_time=1.0)

        # -----------------------------
        # Color gradient for bins
        # -----------------------------
        colors = color_gradient([BLUE_E, TEAL, GREEN, YELLOW, ORANGE, RED_E], n_bins)

        # -----------------------------
        # PDF bins (Riemann rectangles)
        # -----------------------------
        def make_pdf_bin(i: int, opacity: float = 0.65) -> Polygon:
            xL, xR = float(xs[i]), float(xs[i + 1])
            mid = 0.5 * (xL + xR)
            h = self.pdf(mid)

            p1 = ax_pdf.c2p(xL, 0)
            p2 = ax_pdf.c2p(xR, 0)
            p3 = ax_pdf.c2p(xR, h)
            p4 = ax_pdf.c2p(xL, h)

            r = Polygon(p1, p2, p3, p4)
            r.set_fill(colors[i], opacity=opacity)
            r.set_stroke(width=1, opacity=0.18)
            return r

        pdf_bins = VGroup(*[make_pdf_bin(i) for i in range(n_bins)])
        self.play(LaggedStart(*[FadeIn(b) for b in pdf_bins], lag_ratio=0.02), run_time=0.9)

        # -----------------------------
        # Vertical guide lines (PDF and CDF)
        # -----------------------------
        def vline(ax: Axes, x: float, opacity: float = 0.35) -> Line:
            ln = Line(ax.c2p(x, 0), ax.c2p(x, ax.y_range[1]))
            ln.set_stroke(WHITE, width=2, opacity=opacity)
            return ln

        guide_pdf = vline(ax_pdf, x_min, opacity=0.35)
        guide_cdf = vline(ax_cdf, x_min, opacity=0.35)
        self.add(guide_pdf, guide_cdf)

        # small marker at x on CDF axis
        x_dot = Dot(ax_cdf.c2p(x_min, 0), radius=0.05, color=WHITE).set_opacity(0.6)
        self.add(x_dot)

        # -----------------------------
        # Helper: a CDF layer rectangle in the *current bin only*
        # width: [xL, xR], height: [y0, y1]
        # -----------------------------
        def cdf_layer_rect(xL: float, xR: float, y0: float, y1: float, color, opacity=0.85) -> Polygon:
            q1 = ax_cdf.c2p(xL, y0)
            q2 = ax_cdf.c2p(xR, y0)
            q3 = ax_cdf.c2p(xR, y1)
            q4 = ax_cdf.c2p(xL, y1)
            r = Polygon(q1, q2, q3, q4)
            r.set_fill(color, opacity=opacity)
            r.set_stroke(width=0.5, opacity=0.15)
            return r

        # Shift vector in screen coordinates for moving the stack by one bin
        # (constant because bins are equally spaced)
        shift_vec = ax_cdf.c2p(xs[1], 0) - ax_cdf.c2p(xs[0], 0)

        # This is the moving "current stack" that contains ALL previous layers
        current_stack = VGroup()
        cum = 0.0

        # -----------------------------
        # Main loop: move in x, transfer bin -> add new layer on top of stack
        # -----------------------------
        for i in range(n_bins):
            xL, xR = float(xs[i]), float(xs[i + 1])
            mid = 0.5 * (xL + xR)

            area = self.pdf(mid) * dx
            next_cum = min(1.0, cum + area)

            # Move guides to the right edge xR
            self.play(
                guide_pdf.animate.put_start_and_end_on(
                    ax_pdf.c2p(xR, 0), ax_pdf.c2p(xR, ax_pdf.y_range[1])
                ),
                guide_cdf.animate.put_start_and_end_on(
                    ax_cdf.c2p(xR, 0), ax_cdf.c2p(xR, ax_cdf.y_range[1])
                ),
                x_dot.animate.move_to(ax_cdf.c2p(xR, 0)),
                run_time=move_time,
                rate_func=linear,
            )

            # (Optional) leave the current stack behind as a faint ghost BEFORE moving on
            if ghost_history and len(current_stack) > 0:
                ghost = current_stack.copy()
                ghost.set_opacity(ghost_opacity)
                ghost.set_stroke(opacity=ghost_opacity)
                self.add(ghost)

            # Move the whole stack one bin to the right (except at i=0 where it's empty)
            if len(current_stack) > 0:
                self.play(current_stack.animate.shift(shift_vec), run_time=move_time, rate_func=linear)

            # Highlight current PDF bin
            self.play(pdf_bins[i].animate.set_fill(opacity=0.95), run_time=0.06)

            # Create the new layer rectangle at the CURRENT bin position only [xL, xR]
            new_layer = cdf_layer_rect(xL, xR, cum, next_cum, colors[i], opacity=layer_opacity)

            # Transfer: PDF bin -> new CDF layer (but keep PDF bin as "spent")
            self.play(
                ReplacementTransform(pdf_bins[i].copy(), new_layer),
                run_time=transfer_time,
                rate_func=smooth,
            )

            # Add the layer permanently to the moving stack (so history is visible UNDER it)
            current_stack.add(new_layer)

            # Make original PDF bin look "counted"
            self.play(
                pdf_bins[i].animate.set_fill(opacity=0.10).set_stroke(opacity=0.10),
                run_time=0.06,
            )

            cum = next_cum

        # -----------------------------
        # Final: draw CDF outline (piecewise linear) so the viewer sees the function
        # -----------------------------
        cdf_points = [(float(xs[0]), 0.0)]
        cum2 = 0.0
        for i in range(n_bins):
            mid = 0.5 * (float(xs[i]) + float(xs[i + 1]))
            cum2 = min(1.0, cum2 + self.pdf(mid) * dx)
            cdf_points.append((float(xs[i + 1]), cum2))

        cdf_outline = VMobject()
        cdf_outline.set_points_as_corners([ax_cdf.c2p(x, y) for x, y in cdf_points])
        cdf_outline.set_stroke(WHITE, width=4, opacity=0.9)
        self.play(Create(cdf_outline), run_time=0.8)

        # Formula
        formula = Tex(r"$F(x)=\int_{-\infty}^{x} f(t)\,dt$").scale(0.9)
        formula.next_to(ax_cdf, DOWN, buff=0.35)
        self.play(Write(formula), run_time=0.7)

        self.wait(1.5)


"""
Run:
  manim -pqh your_file.py PDFtoCDFLocalStack

Higher quality:
  manim -p -r 1920,1080 your_file.py PDFtoCDFLocalStack
"""