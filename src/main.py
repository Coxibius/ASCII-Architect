import sys
import os
import re

# Configuración de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

# Importación de Router (Maneja Canvas internamente)
try:
    from ascii_architect.router import Router
except ImportError:
    # Intento de importación relativa si se ejecuta desde src/
    from router import Router

# ==========================================
# 🖌️ FUNCIONES DE MAQUILLAJE (UTILS)
# ==========================================
def inject_text(box_art, text):
    """Mete el texto centrado y limpia los anchors visuales."""
    lines = box_art.split("\n")
    new_lines = []
    
    # Encontrar la línea central (donde suelen estar W y E)
    center_idx = len(lines) // 2
    
    for i, line in enumerate(lines):
        # 1. Limpiar Anchors (N/S -> -, W/E -> |)
        clean_line = line.replace("N", "-").replace("S", "-").replace("W", "|").replace("E", "|")
        
        # 2. Inyectar Texto si es la línea central
        if i == center_idx:
            # Calcular espacio interno disponible (quitando bordes)
            # Asumimos bordes de 1 char
            inner_space = len(clean_line) - 2
            if len(text) > inner_space:
                text = text[:inner_space] # Cortar si es muy largo
            
            # Centrar texto
            padding_total = inner_space - len(text)
            pad_left = padding_total // 2
            pad_right = padding_total - pad_left
            
            # Reconstruir línea central: Borde + Espacio + Texto + Espacio + Borde
            # Usamos ░ temporalmente para que el Canvas sepa que es fondo
            # O mejor, usamos espacios reales si ya vamos a renderizar final.
            new_line = clean_line[0] + (" " * pad_left) + text + (" " * pad_right) + clean_line[-1]
            new_lines.append(new_line)
        else:
            new_lines.append(clean_line)
            
    return "\n".join(new_lines)

from ascii_architect.router import Router

def main():
    # Permitir que el usuario pase un flow string por linea de comandos
    # Ej: python src/main.py "A -> B ; C -> D"
    if len(sys.argv) > 1:
        layout = sys.argv[1]
    else:
        # Ejemplo por defecto si no hay argumentos
        layout = "POSTGRES -> FASTAPI ; REDIS -> FASTAPI"

    print("--- ASCII ARCHITECT - MOTOR V1.8 ---")
    
    # Usamos el Router oficial que ya maneja Canvas, Anchors y Layout
    router = Router(use_neural_engine=False)
    router.process(layout)

if __name__ == "__main__":
    main()