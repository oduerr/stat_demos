"""
Storyboard: The Three Estimators — Unbiasedness and Efficiency
==============================================================
6 scenes:
  1. Stage + three Pi creatures (Pi-Mean, Pi-Median, Pi-Liar) with their formulas
  2. Mother Nature drops data → each creature estimates → three colored stars fly back
  3. Fast-forward loop — green / blue / red stars pile up in Probability Land
  4. Green pile → histogram → narrow bell curve (unbiased + efficient)
  5. Blue pile → histogram → wider bell curve (unbiased but less efficient)
  6. Red pile → histogram → shifted bell curve + bias arrow (biased)

Run:
  manim -pql three_estimators.py ThreeEstimators     # low quality preview
  manim -pqh three_estimators.py ThreeEstimators     # 1080p
"""

from manim import *
import numpy as np

TRUE_MU  = 0.0    # displayed as μ = 42
TRUE_SD  = 0.7
SAMPLE_N = 10
BIAS     = 1.5    # axis units; label shows "+5"
N_REPS   = 20

MEAN_SAMP_SD = TRUE_SD / np.sqrt(SAMPLE_N)                       # ≈ 0.221
MED_SAMP_SD  = TRUE_SD * np.sqrt(np.pi / 2) / np.sqrt(SAMPLE_N) # ≈ 0.277

COL_MEAN = GREEN_B
COL_MED  = BLUE_B
COL_BIAS = RED_B


def norm_pdf(x: float, mu: float = 0.0, sd: float = 1.0) -> float:
    return float(np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)))


class ThreeEstimators(Scene):

    def construct(self) -> None:
        rng = np.random.default_rng(42)

        # ── 1. Stage ─────────────────────────────────────────────────────────
        divider  = DashedLine(3.8*UP, 3.8*DOWN, color=GREY_C, dash_length=0.18, stroke_width=1.5)
        prob_lbl = Text("Probability Land", font_size=26, color=BLUE_B).move_to([-4.0, 3.5, 0])
        data_lbl = Text("Data Land",        font_size=26, color=WHITE ).move_to([ 4.5, 3.5, 0])
        self.play(Create(divider), FadeIn(prob_lbl), FadeIn(data_lbl))

        # Mother Nature (left)
        mn_c    = np.array([-5.8, 1.8, 0])
        mn_head = (Circle(radius=0.38, color=BLUE_B)
                   .set_fill(BLUE_E, opacity=0.4).move_to(mn_c))
        mn_body = VGroup(
            Line(mn_c+[0,-0.38,0], mn_c+[0, -1.4, 0], stroke_width=3, color=BLUE_B),
            Line(mn_c+[0,-0.70,0], mn_c+[-0.65,-1.2,0], stroke_width=3, color=BLUE_B),
            Line(mn_c+[0,-0.70,0], mn_c+[ 0.65,-1.2,0], stroke_width=3, color=BLUE_B),
        )
        mn_name = Text("Mother Nature", font_size=18, color=BLUE_B).next_to(mn_head, UP, buff=0.1)
        self.play(FadeIn(VGroup(mn_head, mn_body, mn_name)))

        # Three Pi creatures (right side) ─────────────────────────────────────
        CREATURE_Y = 1.3
        CREATURE_INFO = [
            (2.0, COL_MEAN, r"\hat{\mu}_{\mathrm{mean}} = \bar{x}",        "Pi-Mean"),
            (4.5, COL_MED,  r"\hat{\mu}_{\mathrm{med}}  = \tilde{x}",      "Pi-Median"),
            (6.8, COL_BIAS, r"\hat{\mu}_{\mathrm{liar}} = \bar{x}+5",      "Pi-Liar"),
        ]
        creature_heads     = []
        creature_positions = []
        creature_colors    = [COL_MEAN, COL_MED, COL_BIAS]

        for cx, col, formula, cname in CREATURE_INFO:
            c = np.array([cx, CREATURE_Y, 0])
            creature_positions.append(c)

            head = Circle(radius=0.32, color=col).set_fill(col, opacity=0.2).move_to(c)
            creature_heads.append(head)

            body = VGroup(
                Line(c+[0,-0.32,0], c+[0, -1.2, 0], stroke_width=2.5, color=col),
                Line(c+[0,-0.55,0], c+[-0.5,-1.0,0], stroke_width=2.5, color=col),
                Line(c+[0,-0.55,0], c+[ 0.5,-1.0,0], stroke_width=2.5, color=col),
            )
            formula_mobj = (MathTex(formula, font_size=19, color=col)
                            .next_to(head, DOWN, buff=1.3))
            name_mobj = (Text(cname, font_size=15, color=col)
                         .next_to(formula_mobj, DOWN, buff=0.08))
            fig = VGroup(head, body, formula_mobj, name_mobj)

            if col == COL_BIAS:   # devil horns for the liar
                fig.add(
                    Triangle(color=col, fill_opacity=0.9).scale(0.12).move_to(c+[-0.18, 0.38, 0]),
                    Triangle(color=col, fill_opacity=0.9).scale(0.12).move_to(c+[ 0.18, 0.38, 0]),
                )
            self.play(FadeIn(fig), run_time=0.5)

        self.wait(0.5)

        # ── 2. Probability Land: bell curve + secret μ ───────────────────────
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
        lock_lbl = (Text("(unknown)  🔒", font_size=15, color=GREY_A)
                    .next_to(mu_lbl, DOWN, buff=0.08))

        self.play(Create(ax), run_time=0.8)
        self.play(Create(bell), run_time=1.0)
        self.play(Create(mu_tick), Write(mu_lbl), FadeIn(lock_lbl), run_time=0.7)
        self.wait(0.5)

        data_line = Line([0.8, -2.9, 0], [7.5, -2.9, 0], color=GREY_B, stroke_width=1.5)
        self.play(Create(data_line))

        # ── Sampling helper ───────────────────────────────────────────────────
        all_mean_ests, all_med_ests, all_bias_ests = [], [], []
        all_green_stars = VGroup()
        all_blue_stars  = VGroup()
        all_red_stars   = VGroup()
        star_groups     = [all_green_stars, all_blue_stars, all_red_stars]

        # Curve normalisation: green peak = 0.55 axis units
        curve_scale = 0.55 / norm_pdf(TRUE_MU, TRUE_MU, MEAN_SAMP_SD)

        def do_round(speed: float, show_detail: bool) -> None:
            samples  = rng.normal(TRUE_MU, TRUE_SD, SAMPLE_N)
            est_mean = float(np.mean(samples))
            est_med  = float(np.median(samples))
            est_bias = est_mean + BIAS
            all_mean_ests.append(est_mean)
            all_med_ests.append(est_med)
            all_bias_ests.append(est_bias)
            ests = [est_mean, est_med, est_bias]

            # Data dots: start on bell curve, fall to data line
            n_show = 6 if show_detail else 4
            s_show = np.clip(samples[:n_show], -3.0, 3.0)
            starts = [ax.c2p(float(s), norm_pdf(float(s), TRUE_MU, TRUE_SD)) for s in s_show]
            end_xs = np.clip(3.5 + s_show * 0.4, 1.0, 6.8)
            ends   = [np.array([float(ex), -2.9, 0]) for ex in end_xs]

            dots = VGroup(*[Dot(p, radius=0.07, color=YELLOW) for p in starts])
            self.add(dots)

            self.play(
                Flash(mn_head.get_center(), color=BLUE_C,
                      flash_radius=0.5, line_length=0.2, num_lines=8),
                run_time=0.22 * speed,
            )
            self.play(
                LaggedStart(*[MoveAlongPath(d, ArcBetweenPoints(s, e, angle=-PI/5))
                              for d, s, e in zip(dots, starts, ends)], lag_ratio=0.06),
                run_time=0.75 * speed,
            )

            if show_detail:
                lbls = VGroup(*[
                    MathTex(f"x_{{{i+1}}}", font_size=15, color=YELLOW).next_to(d, UP, buff=0.03)
                    for i, d in enumerate(dots[:3])
                ])
                self.play(FadeIn(lbls), run_time=0.25)
                self.wait(0.3)

            # Three colored dots fly from data centre to each creature
            data_center = np.array([3.5, -2.9, 0])
            merge_pts   = [np.array([cp[0], -2.9, 0]) for cp in creature_positions]
            c_dots      = [Dot(data_center, radius=0.09, color=c) for c in creature_colors]
            for d in c_dots:
                self.add(d)

            self.play(
                *[cd.animate.move_to(mp) for cd, mp in zip(c_dots, merge_pts)],
                run_time=0.30 * speed,
            )
            # Creature blink
            self.play(
                *[h.animate.set_fill(creature_colors[k], opacity=0.9)
                  for k, h in enumerate(creature_heads)],
                run_time=0.12 * speed,
            )
            self.play(
                *[h.animate.set_fill(creature_colors[k], opacity=0.2)
                  for k, h in enumerate(creature_heads)],
                run_time=0.12 * speed,
            )

            if show_detail:
                self.play(FadeOut(lbls), FadeOut(dots), run_time=0.2)
            else:
                self.play(FadeOut(dots), run_time=0.1 * speed)

            # Stars form at merge points and fly to Probability Land (all parallel)
            r      = 0.24 if show_detail else 0.18
            stars, dests = [], []
            for k in range(3):
                est_ax = float(np.clip(ests[k], -3.15, 3.15))
                y_j    = float(rng.uniform(0.03, 0.16))
                stars.append(
                    Star(n=5, outer_radius=r, color=creature_colors[k], fill_opacity=1.0)
                    .move_to(merge_pts[k])
                )
                dests.append(ax.c2p(est_ax, y_j))

            self.play(
                *[ReplacementTransform(cd, s) for cd, s in zip(c_dots, stars)],
                run_time=0.20 * speed,
            )
            self.play(
                *[s.animate.move_to(d) for s, d in zip(stars, dests)],
                run_time=0.50 * speed, rate_func=smooth,
            )
            for s, sg in zip(stars, star_groups):
                sg.add(s)

        # ── Scene 2: First round (detailed) ──────────────────────────────────
        do_round(speed=1.0, show_detail=True)
        self.wait(0.5)

        # ── Scene 3: Fast-forward loop ────────────────────────────────────────
        for i in range(N_REPS - 1):
            do_round(speed=max(0.10, 0.80 - i * 0.038), show_detail=False)
        self.wait(0.5)

        # ── Helper: histogram + smooth curve ─────────────────────────────────
        self.play(FadeOut(lock_lbl), FadeOut(data_line), run_time=0.4)

        def make_hist(ests, col):
            counts, edges = np.histogram(ests, bins=12, range=(-3.2, 3.2))
            max_cnt = max(counts) if max(counts) > 0 else 1
            bars = VGroup()
            for cnt, xL, xR in zip(counts, edges[:-1], edges[1:]):
                if cnt == 0:
                    continue
                bh = (cnt / max_cnt) * 0.55
                bars.add(Polygon(
                    ax.c2p(xL, 0), ax.c2p(xR, 0),
                    ax.c2p(xR, bh), ax.c2p(xL, bh),
                    fill_color=col, fill_opacity=0.75,
                    stroke_color=col, stroke_width=1,
                ))
            return bars

        def plot_curve(mu, sd, col):
            x_lo = max(mu - 3.5 * sd, -3.15)
            x_hi = min(mu + 3.5 * sd,  3.15)
            return ax.plot(
                lambda x: norm_pdf(x, mu, sd) * curve_scale,
                x_range=[x_lo, x_hi],
                color=col, stroke_width=4,
            )

        # ── Scene 4: Green — unbiased & efficient ─────────────────────────────
        green_hist  = make_hist(all_mean_ests, COL_MEAN)
        self.play(ReplacementTransform(all_green_stars, green_hist), run_time=1.2)
        green_curve = plot_curve(TRUE_MU, MEAN_SAMP_SD, COL_MEAN)
        self.play(ReplacementTransform(green_hist, green_curve), run_time=1.2)

        align_line = DashedLine(
            ax.c2p(TRUE_MU, 0), ax.c2p(TRUE_MU, 0.61),
            color=YELLOW, stroke_width=2, dash_length=0.12,
        )
        self.play(Create(align_line), run_time=0.5)
        lbl4 = (VGroup(Text("Unbiased", font_size=19, color=COL_MEAN),
                       Text("Efficient", font_size=19, color=COL_MEAN))
                .arrange(DOWN, buff=0.08)
                .next_to(green_curve, RIGHT, buff=0.1).shift(UP*0.2))
        self.play(Write(lbl4), run_time=0.6)
        self.wait(1.0)

        # ── Scene 5: Blue — unbiased but less efficient ───────────────────────
        blue_hist  = make_hist(all_med_ests, COL_MED)
        self.play(ReplacementTransform(all_blue_stars, blue_hist), run_time=1.2)
        blue_curve = plot_curve(TRUE_MU, MED_SAMP_SD, COL_MED)
        self.play(ReplacementTransform(blue_hist, blue_curve), run_time=1.2)
        lbl5 = (VGroup(Text("Unbiased",      font_size=19, color=COL_MED),
                       Text("Less efficient", font_size=19, color=COL_MED))
                .arrange(DOWN, buff=0.08)
                .next_to(blue_curve, LEFT, buff=0.1).shift(DOWN*0.1))
        self.play(Write(lbl5), run_time=0.6)
        self.wait(1.0)

        # ── Scene 6: Red — biased ─────────────────────────────────────────────
        red_hist  = make_hist(all_bias_ests, COL_BIAS)
        self.play(ReplacementTransform(all_red_stars, red_hist), run_time=1.2)
        red_curve = plot_curve(BIAS, MEAN_SAMP_SD, COL_BIAS)
        self.play(ReplacementTransform(red_hist, red_curve), run_time=1.2)

        # Bias arrow: true μ → biased center
        bias_y = 0.18
        bias_arrow = Arrow(
            ax.c2p(TRUE_MU, bias_y), ax.c2p(BIAS, bias_y),
            color=COL_BIAS, buff=0.04, stroke_width=3,
        )
        bias_txt = (MathTex(r"\text{Bias} = +5", color=COL_BIAS, font_size=22)
                    .next_to(bias_arrow, UP, buff=0.08))
        self.play(GrowArrow(bias_arrow), Write(bias_txt), run_time=0.8)
        lbl6 = (Text("Biased!", font_size=20, color=COL_BIAS)
                .next_to(red_curve, RIGHT, buff=0.15))
        self.play(Write(lbl6), run_time=0.5)
        self.wait(3.0)
