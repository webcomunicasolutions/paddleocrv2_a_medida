# Dockerfile Optimizado - PaddleOCR 2.8.1 + Servidor Estable
FROM paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6

# Actualizar system packages primero
RUN apt-get update && \
    apt-get install -y \
      poppler-utils \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender-dev \
      libgl1-mesa-glx \
      curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar PaddleOCR estable (versión que funciona mejor)
RUN pip install --no-cache-dir paddleocr==2.8.1

# Instalar dependencias adicionales para el servidor
RUN pip install --no-cache-dir flask opencv-python numpy pdf2image pillow

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8501/health || exit 1

# Comando por defecto
ENTRYPOINT ["python", "/app/app.py"]
