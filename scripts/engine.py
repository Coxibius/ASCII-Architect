import os
import re
import sys
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Configuración de consola para Windows (UTF-8)
sys.stdout.reconfigure(encoding='utf-8')

class ArchitectEngine:
    def __init__(self):
        # --- 1. LOCALIZADOR DE MODELOS (Pathfinder) ---
        # Detectamos dónde está este script (src/)
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Subimos un nivel para ir a la raíz del proyecto (ASCII-Architect/)
        project_root = os.path.dirname(current_script_dir)
        
        # Definimos la ruta esperada de los modelos según tu captura
        # Ruta: project_root/models/ASCII_Architect_V1_Models
        self.models_base_path = os.path.join(project_root, "models", "ASCII_Architect_V1_Models")
        
        # Validación de seguridad
        if not os.path.exists(self.models_base_path):
            print(f"❌ ERROR CRÍTICO: No encuentro la carpeta de modelos en:\n{self.models_base_path}")
            print("   -> Verifica que descomprimiste el ZIP correctamente.")
            sys.exit(1)
            
        print(f"✅ MOTOR ARQUITECTO ONLINE.")
        print(f"   📂 Modelos cargados desde: {self.models_base_path}")
        
        self.device = "cpu" # Inferencia ligera en CPU

    def generate(self, expert_type, tags, metadata):
        """
        expert_type: "BOX" o "ARROW"
        tags: [STYLE:SOLID], [DIR:RIGHT], etc.
        metadata: [DIM:10x5] o [LEN:5]
        """
        # Mapeo de tipos a nombres de carpeta (expert_box, expert_arrow)
        folder_name = f"expert_{expert_type.lower()}"
        model_path = os.path.join(self.models_base_path, folder_name)
        
        if not os.path.exists(model_path):
            return f"❌ Error: No encuentro el experto '{folder_name}'"

        try:
            # Cargar Modelo y Tokenizer (Bajo demanda para ahorrar RAM)
            # local_files_only=True asegura que no intente buscar en internet
            tokenizer = GPT2Tokenizer.from_pretrained(model_path, local_files_only=True)
            model = GPT2LMHeadModel.from_pretrained(model_path, local_files_only=True)
            
            # Construir Prompt V18
            # Ej: [TYPE:BOX] [STYLE:SOLID] [DIM:10x5]
            prompt = f"[TYPE:{expert_type}] {tags} {metadata}"
            inputs = tokenizer(prompt, return_tensors="pt")

            # Generación Determinista (Greedy Search)
            # Queremos precisión estructural, no creatividad
            out = model.generate(
                **inputs, 
                max_length=250, # Suficiente para cajas grandes
                pad_token_id=50256, 
                do_sample=False 
            )
            raw = tokenizer.decode(out[0])
            
            # Limpieza y Renderizado
            return self._clean_v18(raw, prompt)

        except Exception as e:
            return f"❌ Error de Inferencia: {str(e)}"

    def _clean_v18(self, raw_text, prompt):
        """
        Aplica la lógica de limpieza V17/V18:
        1. Cortar en [STOP]
        2. Extraer desde <L01>
        3. Quitar espacios del tokenizer
        4. Renderizar ░ como espacio vacío
        5. Borrar metadatos técnicos
        """
        # 1. La Guillotina
        content = raw_text.split("[STOP]")[0]
        
        # 2. Extracción de contenido visual
        if "<L01>" in content:
            # Tomamos todo lo que hay después de la primera etiqueta de línea
            # pero volvemos a agregar <L01> para que el regex lo limpie igual que el resto
            parts = content.split("<L01>", 1)
            content = "<L01>" + parts[1]
        else:
            # Fallback: quitar el prompt manualmente
            content = content.replace(prompt, "")

        # 3. Limpieza de Tokenizer (GPT-2 separa símbolos con espacios)
        content = content.replace(" ", "")

        # 4. Renderizado Visual (El secreto de la V17)
        # Convertimos la transparencia en espacio real
        ascii_art = content.replace("░", " ")
        
        # 5. Fix de Encoding Windows (Si aparece el rombo negro)
        ascii_art = ascii_art.replace("\ufffd", "+") # Reemplazar error por un borde genérico

        # 6. Borrar Metadatos con Regex
        # Borra <L01>...<L99> y [S:00]...[S:99]
        ascii_art = re.sub(r'<L\d+>', '', ascii_art) 
        ascii_art = re.sub(r'\[S:\d+\]', '', ascii_art)
        
        return ascii_art.strip()

# ==========================================
# 🧪 ZONA DE PRUEBAS (MAIN)
# ==========================================
if __name__ == "__main__":
    try:
        engine = ArchitectEngine()
        
        print("\n=== 🏗️ PRUEBA DE INGENIERÍA V18 ===")
        
        # 1. Prueba de Caja
        print("\n📦 Generando Caja (Base de Datos)...")
        box = engine.generate("BOX", "[STYLE:SOLID]", "[DIM:12x5]")
        print(box)
        
        # 2. Prueba de Flecha
        print("\n➡️ Generando Flecha (Conexión)...")
        arrow = engine.generate("ARROW", "[DIR:RIGHT]", "[LEN:8]")
        print(arrow)
        
        print("\n===================================")
        input("Presiona ENTER para salir...")
        
    except ImportError:
        print("\n⚠️ ERROR: Faltan librerías.")
        print("Ejecuta: pip install torch transformers")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")