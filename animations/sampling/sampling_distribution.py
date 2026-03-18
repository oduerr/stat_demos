"""
Storyboard: From Probability Land to Data Land (The Sampling Distribution)
===========================================================================
5 scenes:
  1. Split screen — Mother Nature (left, Probability Land) shows bell curve, μ=42 secret
  2. Mother Nature snaps → data falls to Fred in Data Land
  3. Fred uses MLE → red star flies back to Probability Land
  4. Loop 14 more rounds (accelerating) — stars accumulate near μ
  5. Stars morph → histogram → narrower sampling-distribution bell curve

Run:
  manim -pql sampling_distribution.py SamplingDistribution        # low quality, preview
  manim -pqh sampling_distribution.py SamplingDistribution        # high quality
"""

from manim import *
import numpy as np

TRUE_MU = 0.0   # axis coordinates; labelled as μ = 42 on screen
TRUE_SD = 0.7
SAMPLE_N = 10
N_REPS = 15     # total number of repeated sampling rounds


def norm_pdf(x: float, mu: float = 0.0, sd: float = 1.0) -> float:
    return float(np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)))


class SamplingDistribution(Scene):

    def construct(self) -> None:
        rng = np.random.default_rng(42)

        # ── 1. Stage: divider + labels + characters ─────────────────────────

        divider = DashedLine(
            3.8 * UP, 3.8 * DOWN,
            color=GREY_C, dash_length=0.18, stroke_width=1.5,
        )
        prob_lbl = Text("Probability Land", font_size=26, color=BLUE_B).move_to([-4.0, 3.5, 0])
        data_lbl = Text("Data Land",        font_size=26, color=GREEN_B).move_to([ 4.5, 3.5, 0])
        self.play(Create(divider), FadeIn(prob_lbl), FadeIn(data_lbl))

        # Mother Nature (left side)
        mn_c = np.array([-5.8, 1.8, 0])
        mn_head = (Circle(radius=0.38, color=BLUE_B)
                   .set_fill(BLUE_E, opacity=0.4)
                   .move_to(mn_c))
        mn_body = VGroup(
            Line(mn_c + [0, -0.38, 0], mn_c + [0, -1.4,  0], stroke_width=3, color=BLUE_B),
            Line(mn_c + [0, -0.70, 0], mn_c + [-0.65, -1.2, 0], stroke_width=3, color=BLUE_B),
            Line(mn_c + [0, -0.70, 0], mn_c + [ 0.65, -1.2, 0], stroke_width=3, color=BLUE_B),
        )
        mn_name = (Text("Mother Nature", font_size=18, color=BLUE_B)
                   .next_to(mn_head, UP, buff=0.1))
        mn = VGroup(mn_head, mn_body, mn_name)
        self.play(FadeIn(mn))

        # Fred Stanton (right side)
        fred_c = np.array([5.8, 1.8, 0])
        fred_head = (Circle(radius=0.38, color=GREEN_B)
                     .set_fill(GREEN_E, opacity=0.4)
                     .move_to(fred_c))
        glasses = VGroup(
            Circle(radius=0.12, color=WHITE, stroke_width=1.5).move_to(fred_c + [-0.14,  0.04, 0]),
            Circle(radius=0.12, color=WHITE, stroke_width=1.5).move_to(fred_c + [ 0.14,  0.04, 0]),
        )
        fred_body = VGroup(
            Line(fred_c + [0, -0.38, 0], fred_c + [0, -1.4,  0], stroke_width=3, color=GREEN_B),
            Line(fred_c + [0, -0.70, 0], fred_c + [-0.65, -1.2, 0], stroke_width=3, color=GREEN_B),
            Line(fred_c + [0, -0.70, 0], fred_c + [ 0.65, -1.2, 0], stroke_width=3, color=GREEN_B),
        )
        calc_rect = (RoundedRectangle(width=0.7, height=0.9, corner_radius=0.08,
                                      color=GREY_B, fill_opacity=0.8)
                     .move_to(fred_c + [1.0, -0.85, 0]))
        calc_txt  = Text("MLE", font_size=16, color=YELLOW).move_to(calc_rect.get_center())
        fred_name = (Text("Fred Stanton", font_size=18, color=GREEN_B)
                     .next_to(fred_head, UP, buff=0.1))
        fred = VGroup(fred_head, glasses, fred_body, fred_name)
        calc = VGroup(calc_rect, calc_txt)
        self.play(FadeIn(fred), FadeIn(calc))

        # ── 2. Probability Land: axes + bell curve + secret μ ───────────────

        ax = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[0, 0.70, 0.2],
            x_length=5.5,
            y_length=2.8,
            tips=False,
            axis_config={"color": BLUE_B},
        ).move_to([-3.2, -1.3, 0])

        bell = ax.plot(
            lambda x: norm_pdf(x, TRUE_MU, TRUE_SD),
            x_range=[-3, 3], color=BLUE_B, stroke_width=3,
        )
        mu_tick = DashedLine(
            ax.c2p(TRUE_MU, 0),
            ax.c2p(TRUE_MU, norm_pdf(TRUE_MU, TRUE_MU, TRUE_SD) + 0.06),
            color=YELLOW, stroke_width=2, dash_length=0.1,
        )
        mu_lbl   = (MathTex(r"\mu = 42", color=YELLOW, font_size=28)
                    .next_to(ax.c2p(TRUE_MU, 0), UR, buff=0.15))
        lock_lbl = (Text("(unknown to Fred)  🔒", font_size=15, color=GREY_A)
                    .next_to(mu_lbl, DOWN, buff=0.08))

        self.play(Create(ax), run_time=0.8)
        self.play(Create(bell), run_time=1.0)
        self.play(Create(mu_tick), Write(mu_lbl), run_time=0.7)
        self.play(FadeIn(lock_lbl), run_time=0.4)
        self.wait(0.8)

        # Fred's data axis (right side)
        data_line = Line([1.1, -2.9, 0], [6.8, -2.9, 0], color=GREEN_B, stroke_width=2)
        data_line_lbl = (MathTex(r"y_1, y_2, \ldots", color=GREEN_B, font_size=20)
                         .next_to(data_line, RIGHT, buff=0.1))
        self.play(Create(data_line), FadeIn(data_line_lbl))

        # ── Helper: one full sampling + estimation round ─────────────────────

        all_ests: list = []
        all_stars = VGroup()

        def do_round(speed: float, show_detail: bool) -> None:
            samples = rng.normal(TRUE_MU, TRUE_SD, SAMPLE_N)
            est = float(np.mean(samples))
            all_ests.append(est)

            n_show = 8 if show_detail else 5
            s_show = np.clip(samples[:n_show], -3.0, 3.0)

            # Starting positions: on the bell curve (left side)
            starts = [ax.c2p(float(s), norm_pdf(float(s), TRUE_MU, TRUE_SD)) for s in s_show]
            # Ending positions: on Fred's data line (right side)
            end_xs = np.clip(4.0 + s_show * 0.55, 1.3, 6.7)
            ends   = [np.array([float(ex), -2.9, 0]) for ex in end_xs]

            dots = VGroup(*[Dot(p, radius=0.07, color=YELLOW) for p in starts])
            self.add(dots)

            # Mother Nature snaps her fingers
            self.play(
                Flash(mn_head.get_center(), color=BLUE_C,
                      flash_radius=0.5, line_length=0.2, num_lines=8),
                run_time=0.25 * speed,
            )

            # Data falls in arcs
            self.play(
                LaggedStart(
                    *[MoveAlongPath(d, ArcBetweenPoints(s, e, angle=-PI / 5))
                      for d, s, e in zip(dots, starts, ends)],
                    lag_ratio=0.06,
                ),
                run_time=0.8 * speed,
            )

            if show_detail:
                lbls = VGroup(*[
                    MathTex(f"y_{{{i+1}}}", font_size=16, color=YELLOW).next_to(d, UP, buff=0.04)
                    for i, d in enumerate(dots[:3])
                ])
                self.play(FadeIn(lbls), run_time=0.3)
                self.wait(0.4 * speed)

            # Calculator blinks
            self.play(calc_rect.animate.set_fill(YELLOW, opacity=0.9), run_time=0.15 * speed)
            self.play(calc_rect.animate.set_fill(GREY_B,  opacity=0.8), run_time=0.15 * speed)

            if show_detail:
                self.play(FadeOut(lbls), run_time=0.2)

            # Dots merge to estimate position on Fred's axis
            est_ax   = float(np.clip(est, -3.0, 3.0))
            est_x_sc = float(np.clip(4.0 + est_ax * 0.55, 1.3, 6.7))
            merge_pt = np.array([est_x_sc, -2.9, 0])
            self.play(*[d.animate.move_to(merge_pt) for d in dots], run_time=0.35 * speed)

            # Dots → red star
            r    = 0.26 if show_detail else 0.20
            star = Star(n=5, outer_radius=r, color=RED, fill_opacity=1.0).move_to(merge_pt)
            self.play(ReplacementTransform(dots, star), run_time=0.25 * speed)

            # Star flies back to Probability Land
            y_jitter  = float(rng.uniform(0.04, 0.18))
            star_dest = ax.c2p(est_ax, y_jitter)
            self.play(star.animate.move_to(star_dest), run_time=0.55 * speed, rate_func=smooth)

            all_stars.add(star)

        # ── 3. First round (detailed) ────────────────────────────────────────

        do_round(speed=1.0, show_detail=True)
        self.wait(0.5)

        # ── 4. 14 more rounds, accelerating ─────────────────────────────────

        for i in range(N_REPS - 1):
            spd = max(0.12, 0.85 - i * 0.055)
            do_round(speed=spd, show_detail=False)

        self.wait(0.5)

        # ── 5. Stars → histogram → sampling distribution ─────────────────────

        self.play(FadeOut(lock_lbl), FadeOut(data_line), FadeOut(data_line_lbl), run_time=0.5)

        # Build histogram from estimates
        n_bins  = 10
        h_range = (-2.5, 2.5)
        counts, edges = np.histogram(all_ests, bins=n_bins, range=h_range)
        max_cnt = max(counts) if max(counts) > 0 else 1
        scale_h = 0.55  # max bar height in axis y-units

        hist_bars = VGroup()
        for cnt, xL, xR in zip(counts, edges[:-1], edges[1:]):
            if cnt == 0:
                continue
            bh  = (cnt / max_cnt) * scale_h
            bar = Polygon(
                ax.c2p(xL, 0), ax.c2p(xR, 0),
                ax.c2p(xR, bh), ax.c2p(xL, bh),
                fill_color=RED, fill_opacity=0.75,
                stroke_color=RED_E, stroke_width=1,
            )
            hist_bars.add(bar)

        self.play(ReplacementTransform(all_stars, hist_bars), run_time=1.5)
        self.wait(0.6)

        # Sampling distribution bell curve (peak scaled to match histogram)
        samp_sd    = TRUE_SD / np.sqrt(SAMPLE_N)
        peak_pdf   = norm_pdf(TRUE_MU, TRUE_MU, samp_sd)
        curve_scale = scale_h / peak_pdf

        samp_curve = ax.plot(
            lambda x: norm_pdf(x, TRUE_MU, samp_sd) * curve_scale,
            x_range=[-2.5, 2.5],
            color=RED, stroke_width=4,
        )
        self.play(ReplacementTransform(hist_bars, samp_curve), run_time=1.5)

        sd_text = (Text("Sampling Distribution", font_size=24, color=RED)
                   .next_to(ax, UP, buff=0.2)
                   .shift(LEFT * 0.3))
        self.play(Write(sd_text), run_time=0.8)

        # Dashed alignment line connecting μ to peak of sampling distribution
        align = DashedLine(
            ax.c2p(TRUE_MU, 0),
            ax.c2p(TRUE_MU, norm_pdf(TRUE_MU, TRUE_MU, samp_sd) * curve_scale + 0.05),
            color=YELLOW, stroke_width=2.5, dash_length=0.13,
        )
        self.play(Create(align), run_time=0.6)
        self.wait(3.0)
