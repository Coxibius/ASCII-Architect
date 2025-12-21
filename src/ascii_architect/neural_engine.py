import os
import re
import sys
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from pathlib import Path

# Detectar dónde está instalado el archivo y buscar modelos relativos
# Estructura: root/src/ascii_architect/neural_engine.py -> Sube 3 niveles
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# PRIORIDADES DE BÚSQUEDA:
# 1. Variable de Entorno
# 2. Carpeta research/models (Entorno de desarrollo / Local)
# 3. Carpeta models/ (Directorio raíz estándar tras descarga manual)
DEFAULT_V2_RESEARCH = BASE_DIR / "research" / "models" / "ASCII_Architect_V2_Expansion"
DEFAULT_V1_RESEARCH = BASE_DIR / "research" / "models" / "ASCII_Architect_V1_Models"
DEFAULT_V2_ROOT = BASE_DIR / "models" / "ASCII_Architect_V2_Expansion"
DEFAULT_V1_ROOT = BASE_DIR / "models" / "ASCII_Architect_V1_Models"

class ArchitectEngine:
    def __init__(self):
        # 1. LOCALIZADOR DE MODELOS CON FALLBACK ROBUSTO
        self.models_v2_path = os.getenv("ASCII_ARCH_MODELS_V2")
        self.models_v1_path = os.getenv("ASCII_ARCH_MODELS_V1")

        if not self.models_v2_path:
            # Buscar en research o en root
            if DEFAULT_V2_RESEARCH.exists():
                self.models_v2_path = str(DEFAULT_V2_RESEARCH)
            elif DEFAULT_V2_ROOT.exists():
                self.models_v2_path = str(DEFAULT_V2_ROOT)
            else:
                self.models_v2_path = str(DEFAULT_V2_ROOT) # Default final path

        if not self.models_v1_path:
            if DEFAULT_V1_RESEARCH.exists():
                self.models_v1_path = str(DEFAULT_V1_RESEARCH)
            elif DEFAULT_V1_ROOT.exists():
                self.models_v1_path = str(DEFAULT_V1_ROOT)
            else:
                self.models_v1_path = str(DEFAULT_V1_ROOT)

        # Check existencia final
        self.v2_ready = os.path.exists(self.models_v2_path)
        self.v1_ready = os.path.exists(self.models_v1_path)
        
        if not self.v1_ready and not self.v2_ready:
             print(f"⚠️ [IA WARNING] No se encontraron modelos en:")
             print(f"   V2: {self.models_v2_path}")
             print(f"   V1: {self.models_v1_path}")
             print(f"   Nota: El sistema usará el modo Plantillas automáticamente.")
        else:
             print(f"✅ MOTOR ARQUITECTO ONLINE.")
             if self.v2_ready: print(f"   - V2 Models: ACTIVE")
             if self.v1_ready: print(f"   - V1 Models: ACTIVE (Fallback)")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def generate(self, expert_type, tags, metadata):
        # Mapeo: BOX -> expert_box
        folder_name = f"expert_{expert_type.lower()}"
        
        # Lógica de búsqueda de modelo: Prioridad V2 > V1
        model_path = None
        
        if self.v2_ready:
            candidate = os.path.join(self.models_v2_path, folder_name)
            if os.path.exists(candidate):
                model_path = candidate
        
        if not model_path and self.v1_ready:
            candidate = os.path.join(self.models_v1_path, folder_name)
            if os.path.exists(candidate):
                model_path = candidate
                
        if not model_path or not os.path.exists(model_path):
            return f"❌ Error: No existe el modelo {folder_name}"

        try:
            tokenizer = GPT2Tokenizer.from_pretrained(model_path, local_files_only=True)
            model = GPT2LMHeadModel.from_pretrained(model_path, local_files_only=True)
            
            prompt = f"[TYPE:{expert_type}] {tags} {metadata}"
            inputs = tokenizer(prompt, return_tensors="pt")

            out = model.generate(
                **inputs, 
                max_length=250, 
                pad_token_id=50256, 
                do_sample=False 
            )
            raw = tokenizer.decode(out[0])
            return self._clean_v18(raw, prompt)

        except Exception as e:
            return f"❌ Error Inferencia: {str(e)}"

    def _clean_v18(self, raw_text, prompt):
        content = raw_text.split("[STOP]")[0]
        
        if "<L01>" in content:
            parts = content.split("<L01>", 1)
            content = "<L01>" + parts[1]
        else:
            content = content.replace(prompt, "")

        content = content.replace(" ", "")
        ascii_art = content.replace("░", " ")
        ascii_art = ascii_art.replace("\ufffd", "+") # Fix rombo negro
        
        # Regex para limpiar metadatos
        ascii_art = re.sub(r'<L\d+>', '', ascii_art) 
        ascii_art = re.sub(r'\[S:\d+\]', '', ascii_art)
        
        return ascii_art.strip()