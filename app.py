import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils import render_manim, parse_polinomio


def avaliar(coef_vals, x):
    resultado = 0.0
    for c in coef_vals:
        resultado = resultado * x + c
    return resultado


def plot_polinomio(coef_list, a):
    xs = np.linspace(a - 4, a + 4, 500)
    ys = [avaliar(coef_list, x) for x in xs]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    ax.plot(xs, ys, color="#2dd4bf", linewidth=2)
    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.axvline(0, color="#6b7280", linewidth=0.8)

    ax.scatter([a], [0], color="#facc15", zorder=5, s=60)
    ax.annotate(
        f"a = {a:g}",
        xy=(a, 0),
        xytext=(a + 0.2, max(ys) * 0.08 if max(ys) != 0 else 0.5),
        color="#facc15",
        fontsize=9,
    )

    ax.tick_params(colors="#9ca3af", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#374151")

    ax.set_title("p(x)", color="#d1d5db", fontsize=10)
    fig.tight_layout()
    return fig

st.set_page_config(
    page_title="Briot-Ruffini",
    page_icon="polynomial",
    layout="centered"
)

st.title("Dispositivo de Briot-Ruffini")
st.caption("Gera uma animação passo a passo da divisão de polinômios pelo dispositivo prático.")

st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    expr = st.text_input(
        "Polinômio p(x)",
        value="x^3 - 6x^2 + 11x - 6",
        placeholder="Ex: x^3 - 6x^2 + 11x - 6",
        help="Use ^ para expoentes. Exemplo: 2x^3 - x + 5"
    )

with col2:
    a = st.number_input(
        "Valor de a",
        value=1.0,
        step=0.5,
        help="Raiz que divide o polinômio: p(x) ÷ (x − a)"
    )

coef_list   = None
coef_string = None

if expr.strip():
    try:
        coef_list   = parse_polinomio(expr)
        coef_string = ",".join(map(str, coef_list))
        grau        = len(coef_list) - 1
        st.info(f"Grau {grau}  |  Coeficientes: {coef_list}")
    except Exception as e:
        st.error(f"Erro ao interpretar o polinômio: {e}")

if coef_list is not None:
    st.pyplot(plot_polinomio(coef_list, a))

st.divider()

if st.button("Gerar Animacao", type="primary", use_container_width=True):
    if coef_string is None:
        st.error("Corrija o polinômio antes de continuar.")
    else:
        with st.spinner("Renderizando animação..."):
            video_path = render_manim(coef_string, a)

        if video_path:
            st.success("Animação gerada com sucesso.")
            st.video(video_path)
        else:
            st.error("Falha ao gerar o vídeo. Verifique o terminal para detalhes.")
