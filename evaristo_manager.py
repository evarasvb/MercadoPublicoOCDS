import os
import shutil
from openai import OpenAI  # Necesitaras instalar esto: pip install openai

# --- CONFIGURACION DE EVARISTO ---
# 1. Necesitas una API Key (de OpenAI o compatible). Pegala aqui.
API_KEY = "sk-..."  # IMPORTANTE: Reemplaza con tu API Key real
NOMBRE_AGENTE = "Evaristo (Bot)"

client = OpenAI(api_key=API_KEY)

# --- PERSONALIDAD DEL AGENTE ---
SYSTEM_PROMPT = """
Eres Evaristo, un Ingeniero de Datos Senior experto en R y OCDS (Open Contracting Data Standard).
Tu mision es mantener, corregir y optimizar scripts de R sin intervencion humana.
Conoces el repositorio 'dccp-hugo/mercadopublicoocds' a la perfeccion.
Tus respuestas deben ser UNICAMENTE CODIGO R corregido o mejorado. No des explicaciones, solo el bloque de codigo listo para reemplazar.
"""

def hacer_backup(ruta_archivo):
    """Regla de Oro: Siempre hacer copia de seguridad antes de tocar nada."""
    backup = f"{ruta_archivo}.backup"
    shutil.copy(ruta_archivo, backup)
    print(f"[{NOMBRE_AGENTE}] Backup creado: {backup}")

def leer_archivo(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()

def guardar_archivo(ruta, contenido):
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"[{NOMBRE_AGENTE}] Cambios aplicados en: {ruta}")

def cerebro_pensante(codigo_actual, instruccion, archivo_nombre):
    """Envia el codigo a la IA para que lo trabaje."""
    print(f"[{NOMBRE_AGENTE}] Analizando {archivo_nombre}...")
    
    prompt_usuario = f"""
    ARCHIVO: {archivo_nombre}
    MISION: {instruccion}
    
    CODIGO ACTUAL:
    ```{archivo_nombre.split('.')[-1]}
    {codigo_actual}
    ```
    
    Devuelveme el codigo completo corregido/mejorado.
    """

    respuesta = client.chat.completions.create(
        model="gpt-4o",  # O el modelo inteligente que prefieras
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt_usuario}
        ]
    )
    
    # Limpieza basica para obtener solo el codigo
    codigo_nuevo = respuesta.choices[0].message.content
    codigo_nuevo = codigo_nuevo.replace("```R", "").replace("```r", "").replace("```", "")
    return codigo_nuevo

def mision_principal():
    # MISION 1: Revisar el ETL principal
    target = "Extraccion.R"
    mision = "Revisa este script. Asegurate de que las URLs de descarga esten dentro de un bloque tryCatch para manejar errores 404. Si faltan librerias, agregalas arriba."
    
    if os.path.exists(target):
        codigo_viejo = leer_archivo(target)
        hacer_backup(target)
        
        codigo_nuevo = cerebro_pensante(codigo_viejo, mision, target)
        
        guardar_archivo(target, codigo_nuevo)
        print(f"[{NOMBRE_AGENTE}] Mision cumplida con {target}")
    else:
        print(f"[{NOMBRE_AGENTE}] No encuentro el archivo {target}. Estoy en la carpeta correcta?")

    # MISION 2: Optimizar la App Shiny
    target_app = "app/app.R"
    mision_app = "Analiza esta app Shiny. Verifica si la carga de datos es eficiente. Si usa read.csv, cambialo a data.table::fread para velocidad."
    
    if os.path.exists(target_app):
        codigo_viejo = leer_archivo(target_app)
        hacer_backup(target_app)
        codigo_nuevo = cerebro_pensante(codigo_viejo, mision_app, target_app)
        guardar_archivo(target_app, codigo_nuevo)
        print(f"[{NOMBRE_AGENTE}] Mision cumplida con {target_app}")

if __name__ == "__main__":
    print(f"--- INICIANDO PROTOCOLO {NOMBRE_AGENTE} ---")
    mision_principal()
