# Dockerfile EXACTO del Docker antiguo que funciona + servidor
FROM paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6

# Instalar PaddleOCR estable (EXACTO como el Docker antiguo)
RUN pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
RUN pip install paddleocr==2.8.1

# Agregar dependencias mínimas para el servidor
RUN pip install flask pdf2image

# Directorio de trabajo
WORKDIR /app

# Copiar servidor
COPY app.py /app/app.py

# Crear directorios básicos
RUN mkdir -p /app/data/input /app/data/output

# Volúmenes (como el antiguo)
VOLUME ["/root/.paddleocr"]
VOLUME ["/app/data"]

# Puerto del servidor
EXPOSE 8501

# Comando: servidor en lugar de tail
ENTRYPOINT ["python", "/app/app.py"]
