from manim import *
import os

class BriotRuffiniDinamico(Scene):
    def construct(self):

        # -------------------------------
        # 🔥 Entrada externa
        # -------------------------------
        try:
            with open("coef.txt", "r") as f:
                coef_str = f.read().strip()
        except:
            coef_str = "1,-6,11,-6"

        try:
            with open("raiz.txt", "r") as f:
                a = float(f.read().strip())
        except:
            a = 1

        coef_vals = [float(x) for x in coef_str.split(",")]

        # -------------------------------
        # Título
        # -------------------------------
        titulo = Text("Briot-Ruffini", font_size=40)
        self.play(Write(titulo))
        self.play(titulo.animate.to_edge(UP))

        # Mostrar raiz
        raiz_txt = MathTex(f"a = {a}", color=YELLOW)
        raiz_txt.next_to(titulo, DOWN)
        self.play(Write(raiz_txt))

        # -------------------------------
        # Coeficientes
        # -------------------------------
        coef = VGroup(*[MathTex(str(c)) for c in coef_vals])
        coef.arrange(RIGHT, buff=1.5)
        coef.next_to(raiz_txt, DOWN, buff=1)

        self.play(Write(coef))

        # Linha
        linha = Line(
            coef.get_left() + DOWN*0.5,
            coef.get_right() + DOWN*0.5
        )
        self.play(Create(linha))

        # Raiz à esquerda
        raiz_lado = MathTex(str(a))
        raiz_lado.next_to(coef, LEFT, buff=1)
        self.play(Write(raiz_lado))

        # Destaque
        highlight = SurroundingRectangle(coef[0], color=YELLOW)
        self.play(Create(highlight))

        resultados = []

        # -------------------------------
        # PASSO 1
        # -------------------------------
        b0 = coef[0].copy().set_color(BLUE)
        self.play(b0.animate.move_to(coef[0]).shift(DOWN*1.2))
        resultados.append(b0)

        # -------------------------------
        # LOOP
        # -------------------------------
        for i in range(1, len(coef)):

            self.play(highlight.animate.move_to(coef[i]))

            mult_val = float(resultados[-1].tex_string) * a

            mult = MathTex(
                f"{resultados[-1].tex_string} \\cdot {a} = {mult_val}",
                color=ORANGE
            ).scale(0.8)

            mult.next_to(resultados[-1], DOWN)
            self.play(Write(mult))

            soma_val = coef_vals[i] + mult_val

            soma = MathTex(
                f"{coef_vals[i]} + {mult_val} = {soma_val}",
                color=GREEN
            ).scale(0.8)

            soma.next_to(mult, DOWN)
            self.play(Write(soma))

            novo = MathTex(str(round(soma_val, 3)), color=BLUE)
            novo.move_to(coef[i]).shift(DOWN*1.2)

            self.play(Write(novo))
            resultados.append(novo)

            self.play(FadeOut(mult), FadeOut(soma))

        self.wait(1)

        # -------------------------------
        # RESULTADO FINAL
        # -------------------------------
        quociente = [float(r.tex_string) for r in resultados[:-1]]
        resto = float(resultados[-1].tex_string)

        resultado = MathTex(
            f"Q(x) = {quociente}, \\quad R = {resto}",
            color=BLUE
        ).to_edge(DOWN)

        self.play(Write(resultado))
        self.wait(3)