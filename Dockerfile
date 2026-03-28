# =========================
# 🐳 Dockerfile (OBRIGATÓRIO no Hugging Face)
# =========================
FROM python:3.10

WORKDIR /app

COPY packages.txt .
# Instalar dependências do sistema

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libcairo2-dev \
    pkg-config \
    texlive-latex-base \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*




#RUN apt-get update && xargs -a packages.txt apt-get install -y

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar pasta de mídia
RUN mkdir -p media/videos

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
