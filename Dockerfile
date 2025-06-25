# Dockerfile Optimizado - PaddleOCR 2.8.1 + Servidor Estable
FROM paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6

# Instalar PaddleOCR estable (versión que funciona mejor)
RUN pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
RUN pip install paddleocr==2.8.1

# Instalar dependencias adicionales para el servidor
RUN pip install flask opencv-python numpy pdf2image pillow

# Instalar dependencias del sistema para PDF
RUN apt-get update && \
    apt-get install -y \
      poppler-utils \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender-dev \
      libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar servidor
COPY app.py /app/app.py

# Crear directorios de datos
RUN mkdir -p /app/data/input /app/data/output

# Volúmenes persistentes
VOLUME ["/root/.paddleocr"]
VOLUME ["/app/data"]

# Puerto del servidor
EXPOSE 8501

# Comando por defecto
ENTRYPOINT ["python", "/app/app.py"]