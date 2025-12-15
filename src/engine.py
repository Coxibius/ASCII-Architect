import os
import re
import sys
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Configuración de consola para Windows
sys.stdout.reconfigure(encoding='utf-8')

class ArchitectEngine:  # <--- ¡ESTA ES LA CLASE QUE FALTA!
    def __init__(self):
        # 1. LOCALIZADOR DE MODELOS
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_script_dir)
        
        # Ruta a la carpeta de modelos descomprimida
        self.models_base_path = os.path.join(project_root, "models", "ASCII_Architect_V1_Models")
        
        # Auto-corrección de rutas (por si el zip creó subcarpetas)
        if not os.path.exists(os.path.join(self.models_base_path, "expert_box")):
            # Intento: ¿Quizás está dentro de una subcarpeta con el mismo nombre?
            alt_path = os.path.join(self.models_base_path, "ASCII_Architect_V1_Models")
            if os.path.exists(os.path.join(alt_path, "expert_box")):
                self.models_base_path = alt_path

        if not os.path.exists(self.models_base_path):
            print(f"❌ ERROR: No encuentro modelos en {self.models_base_path}")
        else:
            print(f"✅ MOTOR ARQUITECTO ONLINE. Modelos en: {self.models_base_path}")
        
        self.device = "cpu"

    def generate(self, expert_type, tags, metadata):
        # Mapeo: BOX -> expert_box
        folder_name = f"expert_{expert_type.lower()}"
        model_path = os.path.join(self.models_base_path, folder_name)
        
        if not os.path.exists(model_path):
            return f"❌ Error: No existe la carpeta {folder_name}"

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