def inject_text(box_art: str, text: str) -> str:
    """
    Inyecta texto en el centro de una caja generada (ASCII art).
    Limpia los anchors (N, S, E, W) y centra el texto.
    """
    if not text:
        return box_art
        
    lines = box_art.split("\n")
    new_lines = []
    center_idx = len(lines) // 2
    
    for i, line in enumerate(lines):
        # Limpiar anchors (V18 design)
        clean_line = line.replace("N", "-").replace("S", "-").replace("W", "|").replace("E", "|")
        
        if i == center_idx:
            # Calcular padding
            inner_space = len(clean_line) - 2
            # Truncar si es muy largo
            trunc_text = text[:inner_space]
            
            padding_total = inner_space - len(trunc_text)
            pad_left = padding_total // 2
            pad_right = padding_total - pad_left
            
            # Reconstruir línea
            new_line = clean_line[0] + (" " * pad_left) + trunc_text + (" " * pad_right) + clean_line[-1]
            new_lines.append(new_line)
        else:
            new_lines.append(clean_line)
    
    return "\n".join(new_lines)
