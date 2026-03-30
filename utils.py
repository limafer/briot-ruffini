import subprocess
import os
import re


def parse_polinomio(expr: str) -> list[float]:
    expr = expr.strip().replace(" ", "").replace("**", "^")

    expr = re.sub(r'(\d)(x)', r'\1*\2', expr)

    if not expr.startswith(("+", "-")):
        expr = "+" + expr

    termos = re.findall(r'[+\-][^+\-]+', expr)

    coef_dict: dict[int, float] = {}

    for termo in termos:
        sinal = -1.0 if termo[0] == '-' else 1.0
        corpo = termo[1:].replace("*", "")

        if 'x' not in corpo:
            coef = float(corpo) * sinal
            grau = 0
        else:
            partes = corpo.split('x')
            parte_coef = partes[0]
            parte_exp  = partes[1] if len(partes) > 1 else ""

            coef = float(parte_coef) * sinal if parte_coef else sinal

            if parte_exp.startswith("^"):
                grau = int(parte_exp[1:])
            else:
                grau = 1

        coef_dict[grau] = coef_dict.get(grau, 0.0) + coef

    if not coef_dict:
        raise ValueError("Nenhum termo encontrado no polinômio.")

    grau_max = max(coef_dict.keys())

    return [coef_dict.get(i, 0.0) for i in range(grau_max, -1, -1)]


def render_manim(coef_string: str, raiz: float) -> str | None:
    try:
        with open("coef.txt", "w") as f:
            f.write(coef_string)

        with open("raiz.txt", "w") as f:
            f.write(str(raiz))

        cmd = ["manim", "-ql", "briot-dinamico.py", "BriotRuffiniDinamico"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print("STDOUT:", result.stdout[-2000:])
            print("STDERR:", result.stderr[-2000:])

        video_path = "media/videos/briot-dinamico/480p15/BriotRuffiniDinamico.mp4"
        return video_path if os.path.exists(video_path) else None

    except subprocess.TimeoutExpired:
        print("Erro: timeout ao renderizar")
        return None
    except Exception as e:
        print("Erro:", e)
        return None
