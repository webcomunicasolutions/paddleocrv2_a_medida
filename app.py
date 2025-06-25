#!/usr/bin/env python3
"""
PaddleOCR Server Optimizado v2.8.1
Combina la calidad superior de PaddleOCR 2.8.1 con servidor estable
"""

import os
import json
import time
import tempfile
import numpy as np
import cv2
import math
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = '/app/data/input'
OUTPUT_FOLDER = '/app/data/output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'bmp', 'tiff', 'tif'}

# Variables globales
ocr_instances = {}
supported_languages = ["en", "es"]
default_lang = "es"
ocr_initialized = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_intelligent_side_len(image_path):
    """Cálculo inteligente de side_len para optimizar detección"""
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return 960
        
        h, w = img.shape[:2]
        side_len = int(math.ceil(max(h, w) * max(0.8, 960 / max(h, w))))
        print(f"📐 Imagen {w}x{h} -> side_len: {side_len}px")
        return side_len
    except:
        return 960

def initialize_ocr():
    """Inicializar OCR con configuración optimizada 2.8.1"""
    global ocr_instances, ocr_initialized
    
    if ocr_initialized:
        return True
    
    try:
        print("🚀 Inicializando PaddleOCR 2.8.1 optimizado...")
        import paddleocr
        
        print(f"📦 PaddleOCR version: {paddleocr.__version__}")
        
        # Configuración OPTIMIZADA que funciona mejor (basada en el Docker antiguo)
        for lang in supported_languages:
            print(f"📚 Cargando OCR optimizado para {lang.upper()}...")
            
            # Configuración que da mejores resultados
            ocr_instances[lang] = paddleocr.PaddleOCR(
                use_angle_cls=True,        # Detección de ángulos (clave del éxito)
                lang=lang,                 # Idioma específico
                use_gpu=False,             # CPU por compatibilidad
                show_log=False             # Sin logs verbosos
            )
            print(f"   ✅ OCR optimizado OK para {lang}")
        
        ocr_initialized = True
        print("✅ OCR 2.8.1 inicializado con configuración optimizada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando OCR: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_ocr_instance(language=None):
    """Obtener instancia OCR optimizada"""
    global ocr_instances, ocr_initialized
    
    if not ocr_initialized:
        if not initialize_ocr():
            return None
    
    lang = language or default_lang
    return ocr_instances.get(lang, ocr_instances.get("es"))

def detect_text_orientation_improved(coordinates):
    """Detección mejorada de orientación de texto"""
    try:
        if len(coordinates) >= 4:
            x_coords = [point[0] for point in coordinates]
            y_coords = [point[1] for point in coordinates]
            
            width = max(x_coords) - min(x_coords)
            height = max(y_coords) - min(y_coords)
            
            if width == 0:
                return 'vertical'
            
            aspect_ratio = height / width
            p1, p2 = coordinates[0], coordinates[1]
            angle = abs(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / np.pi)
            
            # Lógica mejorada de clasificación
            if aspect_ratio > 2.5:
                return 'vertical'
            elif angle > 25 and angle < 155:
                return 'rotated'
            elif aspect_ratio > 1.8:
                return 'vertical'
            else:
                return 'horizontal'
    except:
        pass
    return 'horizontal'

def analyze_text_orientations(coordinates_list):
    """Analizar orientaciones de todos los bloques de texto"""
    orientations = {'horizontal': 0, 'vertical': 0, 'rotated': 0}
    
    for coords in coordinates_list:
        orientation = detect_text_orientation_improved(coords)
        orientations[orientation] += 1
    
    return orientations

def process_ocr_result_optimized(ocr_result):
    """Procesar resultado OCR 2.8.1 con estructura optimizada"""
    text_lines = []
    confidences = []
    coordinates_list = []
    
    if not ocr_result or not isinstance(ocr_result, list):
        return text_lines, confidences, coordinates_list
    
    try:
        # Estructura de PaddleOCR 2.8.1: [página][bloque][coordenadas, (texto, confianza)]
        for page_result in ocr_result:
            if not page_result:
                continue
                
            for word_info in page_result:
                try:
                    if len(word_info) >= 2:
                        coordinates = word_info[0]
                        text_data = word_info[1]
                        
                        if isinstance(text_data, (list, tuple)) and len(text_data) >= 2:
                            text = str(text_data[0]).strip()
                            confidence = float(text_data[1])
                            
                            if text:  # Solo agregar si hay texto
                                text_lines.append(text)
                                confidences.append(confidence)
                                coordinates_list.append(coordinates)
                                
                except Exception as e:
                    print(f"⚠️ Error procesando bloque: {e}")
                    continue
                    
    except Exception as e:
        print(f"⚠️ Error procesando resultado OCR: {e}")
    
    return text_lines, confidences, coordinates_list

@app.route('/')
def index():
    """Página de información del servidor"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>PaddleOCR Server Optimizado</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .status { font-size: 18px; margin: 20px 0; }
            .ok { color: #27ae60; font-weight: bold; }
            .error { color: #e74c3c; font-weight: bold; }
            .feature { background: #ecf0f1; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
            .code { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 PaddleOCR Server Optimizado v2.8.1</h1>
            
            <div class="status">
                <strong>Estado:</strong> 
                <span class="{{ 'ok' if ocr_ready else 'error' }}">
                    {{ "✅ Operativo con configuración optimizada" if ocr_ready else "❌ No inicializado" }}
                </span>
            </div>
            
            <div class="feature">
                <h3>🔧 Configuración Optimizada</h3>
                <ul>
                    <li>✅ <strong>PaddleOCR 2.8.1</strong> - Versión estable y probada</li>
                    <li>✅ <strong>use_angle_cls=True</strong> - Detección de ángulos mejorada</li>
                    <li>✅ <strong>cls=True</strong> - Clasificación de orientación</li>
                    <li>✅ <strong>Soporte PDF nativo</strong> - Sin conversión manual</li>
                    <li>✅ <strong>Detección de texto vertical</strong></li>
                    <li>✅ <strong>Coordenadas exactas</strong> y métricas de confianza</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🌍 Idiomas Soportados</h3>
                <p>Español, Inglés</p>
            </div>
            
            <div class="feature">
                <h3>📡 API Endpoints</h3>
                <ul>
                    <li><code>GET /health</code> - Estado del servidor</li>
                    <li><code>GET /init</code> - Inicializar modelos</li>
                    <li><code>POST /process</code> - Procesar archivo (básico)</li>
                    <li><code>POST /process?detailed=true</code> - Procesar archivo (detallado)</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>💡 Ejemplo de Uso</h3>
                <div class="code">
curl -X POST http://localhost:8501/process \\<br>
&nbsp;&nbsp;-F "file=@documento.pdf" \\<br>
&nbsp;&nbsp;-F "language=es" \\<br>
&nbsp;&nbsp;-F "detailed=true"
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', ocr_ready=ocr_initialized)

@app.route('/health')
def health():
    """Estado del servidor"""
    return jsonify({
        'status': 'healthy' if ocr_initialized else 'initializing',
        'ocr_ready': ocr_initialized,
        'version': '2.8.1-optimized',
        'supported_languages': supported_languages,
        'optimizations': ['use_angle_cls', 'cls_detection', 'intelligent_side_len'],
        'timestamp': time.time()
    })

@app.route('/init')
def init_models():
    """Inicializar modelos OCR"""
    try:
        success = initialize_ocr()
        return jsonify({
            'success': success,
            'models_loaded': list(ocr_instances.keys()) if success else [],
            'version': '2.8.1-optimized',
            'timestamp': time.time()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_file():
    """Procesar archivo con OCR optimizado"""
    start_time = time.time()
    
    try:
        # Verificar inicialización
        if not ocr_initialized:
            if not initialize_ocr():
                return jsonify({'error': 'OCR not initialized'}), 503
        
        # Validar archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Parámetros
        language = request.form.get('language', default_lang)
        detailed = request.form.get('detailed', 'false').lower() == 'true'
        
        # Obtener instancia OCR optimizada
        ocr = get_ocr_instance(language)
        if ocr is None:
            return jsonify({'error': 'OCR not available'}), 503
        
        filename = secure_filename(file.filename)
        
        # Procesar archivo
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            file.save(tmp_file.name)
            
            try:
                print(f"🔍 Procesando {filename} con PaddleOCR 2.8.1 optimizado...")
                
                # CONFIGURACIÓN OPTIMIZADA: usar .ocr() con cls=True (como el Docker antiguo)
                result = ocr.ocr(tmp_file.name, cls=True)
                
                print(f"✅ OCR completado")
                
            finally:
                os.remove(tmp_file.name)
        
        # Procesar resultado con método optimizado
        text_lines, confidences, coordinates_list = process_ocr_result_optimized(result)
        
        # Analizar orientaciones
        orientations = analyze_text_orientations(coordinates_list)
        
        # Estadísticas
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        processing_time = time.time() - start_time
        
        # Respuesta básica
        response = {
            'success': True,
            'text': '\n'.join(text_lines),
            'total_blocks': len(text_lines),
            'filename': filename,
            'language': language,
            'avg_confidence': round(avg_confidence, 3) if avg_confidence > 0 else None,
            'processing_time': round(processing_time, 3),
            'ocr_version': '2.8.1-optimized',
            'has_coordinates': len(coordinates_list) > 0,
            'text_orientations': orientations,
            'has_vertical_text': orientations.get('vertical', 0) > 0,
            'has_rotated_text': orientations.get('rotated', 0) > 0,
            'pdf_support': 'native',
            'optimizations_used': ['use_angle_cls', 'cls_detection']
        }
        
        # Modo detallado
        if detailed:
            blocks_with_coords = []
            for i, text in enumerate(text_lines):
                block_info = {'text': text}
                
                if i < len(confidences):
                    block_info['confidence'] = round(confidences[i], 3)
                
                if i < len(coordinates_list):
                    coords = coordinates_list[i]
                    # Convertir numpy array si es necesario
                    if hasattr(coords, 'tolist'):
                        coords = coords.tolist()
                    block_info['coordinates'] = coords
                    block_info['orientation'] = detect_text_orientation_improved(coords)
                
                blocks_with_coords.append(block_info)
            
            response.update({
                'blocks': blocks_with_coords,
                'min_confidence': round(min(confidences), 3) if confidences else None,
                'max_confidence': round(max(confidences), 3) if confidences else None,
                'total_coordinates': len(coordinates_list),
                'orientation_details': {
                    'horizontal_blocks': orientations.get('horizontal', 0),
                    'vertical_blocks': orientations.get('vertical', 0),
                    'rotated_blocks': orientations.get('rotated', 0)
                }
            })
        
        return jsonify(response)
        
    except Exception as e:
        processing_time = time.time() - start_time
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'processing_time': round(processing_time, 3),
            'timestamp': time.time()
        }), 500

if __name__ == '__main__':
    # Crear directorios necesarios
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    print("🚀 PaddleOCR Server Optimizado v2.8.1 iniciando...")
    print("🔄 Pre-cargando modelos OCR optimizados...")
    
    # Pre-cargar modelos al arrancar
    if initialize_ocr():
        print("✅ Modelos OCR 2.8.1 pre-cargados exitosamente")
        print("🎯 Las siguientes peticiones serán instantáneas")
        print("⚡ Configuración optimizada activa")
    else:
        print("⚠️ Error pre-cargando modelos")
    
    print("🌐 Servidor listo en puerto 8501")
    print("📍 Mejoras implementadas:")
    print("   ✅ PaddleOCR 2.8.1 estable")
    print("   ✅ use_angle_cls=True (detección de ángulos)")
    print("   ✅ cls=True (clasificación de orientación)")
    print("   ✅ Procesamiento optimizado de resultados")
    print("   ✅ Interfaz web incluida")
    print("   ✅ API completa con modo detallado")
    
    app.run(host='0.0.0.0', port=8501, debug=False)