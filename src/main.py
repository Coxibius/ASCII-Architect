import sys
import os
import re

# Configuración de rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path: sys.path.append(parent_dir)

try:
    from engine import ArchitectEngine
except ImportError:
    from ascii_architect.engine import ArchitectEngine

try:
    from ascii_architect.canvas import Canvas
except ImportError:
    from canvas import Canvas

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

# ==========================================
# 🚀 MAIN
# ==========================================
def main():
    print("🏗️ INICIANDO SISTEMA V18 (FINAL RENDER)...")
    
    brain = ArchitectEngine()      
    paper = Canvas(width=80, height=20) 
    
    # 1. GENERACIÓN
    print("🤖 Generando componentes...")
    raw_db = brain.generate("BOX", "[STYLE:SOLID]", "[DIM:14x5]")
    raw_api = brain.generate("BOX", "[STYLE:SOLID]", "[DIM:12x5]")
    raw_arrow = brain.generate("ARROW", "[DIR:RIGHT]", "[LEN:6]")
    
    # 2. PROCESAMIENTO (Texturizado)
    print("🖌️ Inyectando etiquetas...")
    final_db = inject_text(raw_db, "POSTGRES")
    final_api = inject_text(raw_api, "FASTAPI")
    
    # 3. COMPOSICIÓN (Layout Manual)
    print("🎨 Estampando en Canvas...")
    # Izquierda
    paper.stamp(4, 5, final_db)
    
    # Centro (La flecha empieza donde termina la caja 1)
    # x = 4 (inicio) + 14 (ancho caja) = 18.
    # Ajustamos un poco para que se solape visualmente
    paper.stamp(17, 7, raw_arrow) 
    
    # Derecha (Donde termina la flecha)
    # x = 17 + 6 = 23.
    paper.stamp(23, 5, final_api)
    
    # 4. RENDER FINAL
    print("\n" + "="*40)
    print("   DIAGRAMA DE ARQUITECTURA (V18)")
    print("="*40)
    
    # Renderizamos y limpiamos cualquier ░ residual
    print(paper.render().replace("░", " "))
    
    print("="*40)

if __name__ == "__main__":
    main()