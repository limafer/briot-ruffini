from manim import *
import numpy as np


def fmt(val):
    if val == int(val):
        return str(int(val))
    return str(round(val, 4))


def avaliar(coef_vals, x):
    resultado = 0.0
    for c in coef_vals:
        resultado = resultado * x + c
    return resultado


def auto_range(coef_vals, a, padding=1.5):
    xs = np.linspace(a - 5, a + 5, 400)
    ys = [avaliar(coef_vals, x) for x in xs]
    y_abs_max = max(abs(y) for y in ys)
    x_range = [a - 4, a + 4, 1]
    y_max = max(y_abs_max * 1.2, 2)
    y_range = [-y_max, y_max, max(1, round(y_max / 4))]
    return x_range, y_range


class BriotRuffiniDinamico(Scene):
    def construct(self):
        self.add_sound("audio.aac")

        try:
            with open("coef.txt", "r") as f:
                coef_str = f.read().strip()
        except Exception:
            coef_str = "1,-6,11,-6"

        try:
            with open("raiz.txt", "r") as f:
                a = float(f.read().strip())
        except Exception:
            a = 1.0

        mycolor = ManimColor('#00424A')
        self.camera.background_color = mycolor

        coef_vals = [float(x) for x in coef_str.split(",")]
        n = len(coef_vals)
        grau = n - 1

        COR_TITULO    = WHITE
        COR_RAIZ      = YELLOW
        COR_COEF      = WHITE
        COR_MULT      = ORANGE
        COR_RESULTADO = BLUE_B
        COR_RESTO     = RED_B
        COR_LINHA     = GRAY_B
        COR_GRAFICO   = TEAL_B

        TAB_OFFSET = LEFT * 3.2
        GRF_OFFSET = RIGHT * 3.0

        titulo = Text("Dispositivo de Briot-Ruffini", font_size=32, color=COR_TITULO)
        self.play(Write(titulo), run_time=0.8)
        self.play(titulo.animate.to_edge(UP).shift(DOWN * 0.1), run_time=0.8)

        formula_div = MathTex(
            r"P(x) = (x - a)\,Q(x) + R",
            font_size=36, color=WHITE
        )
        self.play(Write(formula_div), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(formula_div), run_time=0.8)

        polinomio_str = ""
        for i, c in enumerate(coef_vals):
            exp = grau - i
            if exp == 0:
                part = fmt(abs(c))
            elif exp == 1:
                part = (fmt(abs(c)) + "x") if abs(c) != 1 else "x"
            else:
                part = (fmt(abs(c)) + f"x^{{{exp}}}") if abs(c) != 1 else f"x^{{{exp}}}"
            if i == 0:
                polinomio_str += ("-" if c < 0 else "") + part
            else:
                polinomio_str += (" - " if c < 0 else " + ") + part

        polinomio_label = MathTex("p(x) =", polinomio_str, font_size=26, color=GRAY_A)
        polinomio_label.next_to(titulo, DOWN, buff=0.25)

        raiz_label = MathTex(f"a = {fmt(a)}", font_size=26, color=COR_RAIZ)
        raiz_label.next_to(polinomio_label, DOWN, buff=0.15)

        self.play(Write(polinomio_label), run_time=1)
        self.play(Write(raiz_label), run_time=0.8)

        x_range, y_range = auto_range(coef_vals, a)

        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=4.5,
            y_length=4.0,
            axis_config={"color": GRAY_B, "stroke_width": 1.5, "include_tip": True},
            x_axis_config={"numbers_to_include": range(int(x_range[0]), int(x_range[1]) + 1, max(1, int((x_range[1] - x_range[0]) / 5))), "font_size": 16},
            y_axis_config={"numbers_to_include": [], "font_size": 16},
        ).shift(GRF_OFFSET + DOWN * 0.3)

        axes_label = MathTex("p(x)", font_size=22, color=GRAY_A)
        axes_label.next_to(axes, UP, buff=0.1)

        curva = axes.plot(
            lambda x: avaliar(coef_vals, x),
            x_range=[x_range[0], x_range[1]],
            color=COR_GRAFICO,
            stroke_width=2.5,
            use_smoothing=True,
        )

        self.play(Create(axes), Write(axes_label), run_time=1)
        self.play(Create(curva), run_time=1.2)

        ponto_raiz = Dot(axes.c2p(a, 0), color=COR_RAIZ, radius=0.1)
        raiz_ponto_label = MathTex(fmt(a), font_size=20, color=COR_RAIZ)
        raiz_ponto_label.next_to(ponto_raiz, DOWN, buff=0.15)

        self.play(FadeIn(ponto_raiz, scale=1.5), Write(raiz_ponto_label), run_time=0.8)

        y_top = avaliar(coef_vals, a)
        if abs(y_top) > 0.05:
            linha_raiz = DashedLine(
                axes.c2p(a, 0),
                axes.c2p(a, y_top),
                color=COR_RAIZ, stroke_width=1.2, dash_length=0.1
            )
            self.play(Create(linha_raiz), run_time=0.6)

        self.wait(1)

        CELL_W = 0.85
        ROW_H  = 0.65
        table_y = 0.3
        start_x = TAB_OFFSET[0] - (n * CELL_W) / 2

        linha_h = Line(
            RIGHT * (start_x - 0.1)             + UP * table_y,
            RIGHT * (start_x + n * CELL_W + 0.1) + UP * table_y,
            color=COR_LINHA, stroke_width=2
        )

        linha_v = Line(
            RIGHT * (start_x - 0.05) + UP * (table_y + ROW_H * 0.6),
            RIGHT * (start_x - 0.05) + UP * (table_y - ROW_H * 1.4),
            color=COR_LINHA, stroke_width=2
        )

        raiz_lado = MathTex(fmt(a), font_size=28, color=COR_RAIZ)
        raiz_lado.move_to(
            RIGHT * (start_x - 0.55) + UP * (table_y + ROW_H * 0.5)
        )

        self.play(Create(linha_h), Create(linha_v), Write(raiz_lado), run_time=0.6)

        coef_mobjs = []
        for i, c in enumerate(coef_vals):
            pos_x = start_x + (i + 0.5) * CELL_W
            mob = MathTex(fmt(c), font_size=28, color=COR_COEF)
            mob.move_to(RIGHT * pos_x + UP * (table_y + ROW_H * 0.5))
            coef_mobjs.append(mob)

        self.play(LaggedStart(*[Write(m) for m in coef_mobjs], lag_ratio=0.15), run_time=0.8)

        highlight = SurroundingRectangle(coef_mobjs[0], color=YELLOW, buff=0.1)
        self.play(Create(highlight), run_time=0.6)

        mult_mobjs   = [None]
        result_mobjs = []

        r0 = MathTex(fmt(coef_vals[0]), font_size=28, color=COR_RESULTADO)
        r0.move_to(RIGHT * (start_x + 0.5 * CELL_W) + UP * (table_y - ROW_H * 0.8))
        self.play(TransformFromCopy(coef_mobjs[0], r0), run_time=0.5)
        result_mobjs.append(r0)

        resultados_vals = [coef_vals[0]]

        for i in range(1, n):
            self.play(highlight.animate.move_to(coef_mobjs[i]), run_time=0.3)

            mult_val = resultados_vals[-1] * a
            pos_x_i  = start_x + (i + 0.5) * CELL_W

            mult_mob = MathTex(fmt(mult_val), font_size=24, color=COR_MULT)
            mult_mob.move_to(RIGHT * pos_x_i + UP * (table_y - ROW_H * 0.3))
            mult_mobjs.append(mult_mob)
            self.play(Write(mult_mob), run_time=0.4)

            soma_val = coef_vals[i] + mult_val
            resultados_vals.append(soma_val)

            cor = COR_RESTO if (i == n - 1) else COR_RESULTADO
            soma_mob = MathTex(fmt(soma_val), font_size=28, color=cor)
            soma_mob.move_to(RIGHT * pos_x_i + UP * (table_y - ROW_H * 0.8))
            self.play(Write(soma_mob), run_time=0.4)
            result_mobjs.append(soma_mob)

        self.play(FadeOut(highlight), run_time=0.5)
        self.wait(0.7)

        resto_rect = SurroundingRectangle(result_mobjs[-1], color=COR_RESTO, buff=0.12)
        self.play(Create(resto_rect), run_time=0.6)

        quociente_vals = resultados_vals[:-1]
        resto_val      = resultados_vals[-1]
        grau_q         = grau - 1

        q_str = ""
        for j, c in enumerate(quociente_vals):
            exp = grau_q - j
            if exp == 0:
                part_tex = fmt(abs(c))
            elif exp == 1:
                part_tex = (fmt(abs(c)) + "x") if abs(c) != 1 else "x"
            else:
                part_tex = (fmt(abs(c)) + f"x^{{{exp}}}") if abs(c) != 1 else f"x^{{{exp}}}"
            if j == 0:
                q_str += ("-" if c < 0 else "") + part_tex
            else:
                q_str += (" - " if c < 0 else " + ") + part_tex

        resultado_group = VGroup()
        if grau >= 1:
            lbl_q = MathTex("Q(x) =", q_str, font_size=24, color=COR_RESULTADO)
            resultado_group.add(lbl_q)
        lbl_r = MathTex("R =", fmt(resto_val), font_size=24, color=COR_RESTO)
        resultado_group.add(lbl_r)

        resultado_group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        resultado_group.next_to(linha_h, DOWN, buff=ROW_H * 1.4)
        resultado_group.align_to(linha_h, LEFT).shift(RIGHT * 0.1)

        self.play(Write(resultado_group), run_time=0.8)

        self.wait(4)
