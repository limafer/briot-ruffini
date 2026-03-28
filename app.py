import streamlit as st
import base64

try:
    from utils import render_manim, parse_polinomio
except Exception as e:
    import streamlit as st
    st.error(f"Erro ao importar utils: {e}")


st.set_page_config(layout="wide")
st.title("🎥 Briot-Ruffini Interativo")

def video_grande(path):
    st.video(path)
    #video_bytes = open(path, "rb").read()
    video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
    <video width="100%" height="600" controls>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

# -------------------------------
# Entrada do polinômio
# -------------------------------
expr = st.text_input(
    "Polinômio:",
    "x^3 - 6x^2 + 11x - 6"
)

# -------------------------------
# Entrada da raiz
# -------------------------------
a = st.number_input("Valor de a:", value=1.0)

# -------------------------------
# Processamento
# -------------------------------

try:
    coef_list = parse_polinomio(expr)
    coef_string = ",".join(map(str, coef_list))
    st.write("Coeficientes:", coef_list)
except Exception as e:
    st.error(f"Erro no polinômio: {e}")
    coef_string = None

if st.button("🎬 Gerar Animação"):

    if coef_string is None:
        st.error("Entrada inválida")
    else:
        with st.spinner("Renderizando..."):
            video_path = render_manim(coef_string, a)

        if video_path:
            st.video(video_path)
            st.success("Vídeo gerado 🚀")
        else:
            st.error("Erro ao gerar vídeo")


#try:
#    coef_list = parse_polinomio(expr)
#    coef_string = ",".join(map(str, coef_list))
#    st.write("Coeficientes:", coef_list)
#except:
#    st.error("Erro no polinômio")
#    coef_string = None

#@st.cache_data
#def gerar_video(coef_string,a):
#    return render_manim(coef_string,a)


# -------------------------------
# Botão
# -------------------------------
#if st.button("🎬 Gerar Animação"):
#
#    if coef_string is None:
#        st.error("Entrada inválida")
#
#    else:
#        with st.spinner("Renderizando..."):
#            video_path = gerar_video(coef_string, a)

#        if video_path:
#            video_grande(video_path)
#            st.success("Vídeo gerado 🚀")
#        else:
#            st.error("Erro ao gerar vídeo")
