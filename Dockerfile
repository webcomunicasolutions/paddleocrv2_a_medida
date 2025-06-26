# Dockerfile EXACTO del Docker antiguo que funciona + servidor
FROM paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6

# Instalar PaddleOCR estable (EXACTO como el Docker antiguo)
RUN pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
RUN pip install paddleocr==2.8.1

# Agregar dependencias para el servidor y PDF
RUN pip install flask pdf2image PyMuPDF

# Directorio de trabajo
WORKDIR /app

# Copiar servidor
COPY app.py /app/app.py

# Crear directorios básicos
RUN mkdir -p /app/data/input /app/data/output

# Volúm# Dockerfile GANADOR - PaddleOCR 2.8.1 con configuración de 79 bloques
FROM paddlepaddle/paddle:2.6.1-gpu-cuda12.0-cudnn8.9-trt8.6

# Instalar PaddleOCR estable (EXACTO como el Docker antiguo)
RUN pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
RUN pip install paddleocr==2.8.1

# Agregar dependencias para el servidor y PDF (GANADOR requiere PyMuPDF)
RUN pip install flask pdf2image PyMuPDF

# Directorio de trabajo
WORKDIR /app

# Copiar servidor GANADOR
COPY app.py /app/app.py

# Crear directorios básicos
RUN mkdir -p /app/data/input /app/data/output

# Volúmenes (como el antiguo)
VOLUME ["/root/.paddleocr"]
VOLUME ["/app/data"]

# Puerto del servidor
EXPOSE 8501

# Comando: servidor GANADOR
ENTRYPOINT ["python", "/app/app.py"]
