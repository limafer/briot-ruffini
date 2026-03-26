import subprocess
import os

import re

def parse_polinomio(expr):
    expr = expr.replace(" ", "")

    if expr[0] != "-":
        expr = "+" + expr

    termos = re.findall(r'[+-][^+-]+', expr)

    coef_dict = {}

    for termo in termos:
        sinal = -1 if termo[0] == '-' else 1
        termo = termo[1:]

        if 'x' not in termo:
            coef = int(termo) * sinal
            grau = 0
        else:
            if termo.startswith('x'):
                coef = 1
            else:
                coef = int(termo.split('x')[0])

            coef *= sinal

            if '^' in termo:
                grau = int(termo.split('^')[1])
            else:
                grau = 1

        coef_dict[grau] = coef

    grau_max = max(coef_dict.keys())

    coef_list = []
    for i in range(grau_max, -1, -1):
        coef_list.append(coef_dict.get(i, 0))

    return coef_list

def render_manim(coef_string, raiz):

    try:
        # salvar entradas
        with open("coef.txt", "w") as f:
            f.write(coef_string)

        with open("raiz.txt", "w") as f:
            f.write(str(raiz))

        cmd = [
            "manim",
            "-ql",
            "briot-dinamico.py",
            "BriotRuffiniDinamico"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        print(result.stdout)
        print(result.stderr)

        video_path = "media/videos/briot-dinamico/480p15/BriotRuffiniDinamico.mp4"

        if os.path.exists(video_path):
            return video_path
        return None

    except Exception as e:
        print("Erro:", e)
        return None