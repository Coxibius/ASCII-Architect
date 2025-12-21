import json
import random
import os

# CONFIGURATION
OUTPUT_FILENAME = "dataset_cylinders.jsonl"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
SAMPLES = 6000

# VISUAL TOKENS
ALPHA = "░"
ANCHOR_N = "N"
ANCHOR_S = "S"
ANCHOR_E = "E"
ANCHOR_W = "W"

# ESTILO "DATABASE TOWER"
# Usamos '=' para la tapa y base (pesado)
# Usamos '-' para el separador interno
BORDER_HEAVY = "="  
BORDER_LIGHT = "-"
BORDER_V     = "|"
CORNER_TL    = "."
CORNER_TR    = "."
CORNER_BL    = "'"
CORNER_BR    = "'"
JOIN_L       = "+" # Conector para el separador
JOIN_R       = "+"

def generate_db_tower_art(width, height):
    """
    Genera un cilindro estilo Base de Datos con un "Header".
    
    Ejemplo 9x6:
      .===N===.
      |░░░░░░░|  <- Header (aprox 1 o 2 lineas)
      +-------+  <- Separador
      W░░░░░░░E  <- Cuerpo (Body)
      |░░░░░░░|
      '===S==='
    """
    art = []
    
    # 1. Validación de tamaño
    # Necesitamos altura mínima de 5 para que quepa: Tapa, Header, Separador, Cuerpo, Base
    if width < 5: width = 5
    if height < 5: height = 5 
    
    inner_w = width - 2
    mid_x = inner_w // 2
    
    # CALCULAMOS DONDE VA EL SEPARADOR
    # Generalmente la "tapa" (header) ocupa el 20-30% superior o fijo 1-2 líneas
    header_h = 1 if height < 7 else 2
    separator_y = header_h + 1 # Indice de la linea separadora (0-based inside body?)
    
    # --- 1. TOP LID (Tapa Superior) ---
    lid_chars = list(BORDER_HEAVY * inner_w)
    lid_chars[mid_x] = ANCHOR_N
    art.append(CORNER_TL + "".join(lid_chars) + CORNER_TR)
    
    # --- 2. EL CUERPO (Iteramos las filas internas) ---
    # Altura interna = height - 2 (quitamos tapa y base)
    inner_h = height - 2
    
    for r in range(inner_h):
        # r va de 0 a inner_h - 1
        
        # CASO A: Es la línea separadora?
        if r == header_h:
            # Dibujamos +-------+
            sep_line = JOIN_L + (BORDER_LIGHT * inner_w) + JOIN_R
            art.append(sep_line)
            continue
            
        # CASO B: Es contenido (Header o Body)
        # Por defecto relleno transparente
        row_content = list(ALPHA * inner_w)
        left_char = BORDER_V
        right_char = BORDER_V
        
        # LOGICA DE ANCLAS OESTE/ESTE (W/E)
        # Las ponemos en el centro vertical del CUERPO PRINCIPAL (debajo del separador)
        # El cuerpo empieza en header_h + 1
        body_start = header_h + 1
        body_rows = inner_h - body_start
        relative_mid = body_start + (body_rows // 2)
        
        if r == relative_mid:
            left_char = ANCHOR_W
            right_char = ANCHOR_E
        
        art.append(left_char + "".join(row_content) + right_char)

    # --- 3. BOTTOM BASE (Base Inferior) ---
    base_chars = list(BORDER_HEAVY * inner_w)
    base_chars[mid_x] = ANCHOR_S
    art.append(CORNER_BL + "".join(base_chars) + CORNER_BR)
    
    return art

def format_hybrid_v18(line, line_idx):
    s_token = "[S:00]" 
    l_token = f"<L{line_idx+1:02d}>"
    return f"{l_token} {s_token} {line}"

def main():
    print(f"🛢️ Generando {SAMPLES} muestras de 'Database Towers'...")
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for _ in range(SAMPLES):
            # Dimensiones
            w = random.randint(6, 14)
            h = random.randint(5, 10) # Altura mínima 5 para que se vea el efecto
            
            # Generar Arte
            raw_art = generate_db_tower_art(w, h)
            
            # Prompt: Mantenemos TYPE:CYLINDER
            prompt = f"[TYPE:CYLINDER] [STYLE:SOLID] [DIM:{w}x{h}]"
            
            # Completion
            comp_lines = [format_hybrid_v18(l, i) for i, l in enumerate(raw_art)]
            completion = "\n".join(comp_lines) + " [STOP]"
            
            f.write(json.dumps({"prompt": prompt, "completion": completion}, ensure_ascii=False) + "\n")

    print(f"✅ Dataset Cylinders actualizado: {OUTPUT_FILENAME}")
    print("   Ahora incluyen una línea separadora interna para parecer 'Bases de Datos'.")

if __name__ == "__main__":
    main()