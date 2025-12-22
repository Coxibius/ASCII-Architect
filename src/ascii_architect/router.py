from ascii_architect.canvas import Canvas
from ascii_architect.renderers import BoxRenderer, CylinderRenderer, SoftBoxRenderer, DiamondRenderer
# Nota: La importación de NeuralEngine es Lazy (dentro de __init__) para velocidad.

class Router:
    def __init__(self, use_neural_engine: bool = False):
        self.use_neural_engine = use_neural_engine
        self.neural_engine = None
        
        if self.use_neural_engine:
            try:
                from ascii_architect.neural_engine import ArchitectEngine
                self.neural_engine = ArchitectEngine()
                print("🧠 [INFO] Neural Engine Loaded (Experimental Mode)")
            except Exception as e:
                print(f"⚠️ [WARNING] Falló la carga de IA: {e}")
                print("   -> Usando modo Determinista (Plantillas).")
                self.use_neural_engine = False

        self.paper = Canvas(width=1, height=1)

    def _get_node_shape(self, node_text: str, shape_type: str):
        """Fabrica el ASCII para un nodo específico."""
        art = None
        clean_text = node_text.strip()

        # 1. Intento con IA
        if self.use_neural_engine and self.neural_engine:
            try:
                # Lógica simplificada de llamada a IA
                art = self.neural_engine.generate(clean_text, shape_type)
            except:
                pass 

        # 2. Fallback a Plantillas (Renderers)
        if not art:
            if shape_type == "CYLINDER":
                art = CylinderRenderer.render(clean_text)
            elif shape_type == "SOFTBOX":
                art = SoftBoxRenderer.render(clean_text)
            elif shape_type == "DIAMOND":
                art = DiamondRenderer.render(clean_text) # Incluye Saturn Effect
            else:
                art = BoxRenderer.render(clean_text)
        
        # Calcular dimensiones reales del dibujo
        lines = art.split('\n')
        h = len(lines)
        w = max(len(l) for l in lines) if lines else 0
        
        return {'art': art, 'w': w, 'h': h, 'type': shape_type}

    def _get_anchors(self, x, y, w, h):
        """Calcula puntos de conexión N, S, E, W."""
        cx = x + w // 2
        cy = y + h // 2
        return {
            'n': (cx, y), 
            's': (cx, y + h - 1), 
            'e': (x + w - 1, cy), 
            'w': (x, cy)
        }

    def process(self, layout_str: str):
        """
        [MAIN LOOP] Calcula el grid, estampa formas y dibuja flechas.
        """
        mode = "NEURAL MODE" if self.use_neural_engine else "TEMPLATE MODE"
        print(f"🔄 Processing Flow: {layout_str[:60]}... [{mode}]")

        # 1. Parsing Básico (Rows ; Cols ->)
        rows = layout_str.split(';')
        grid = [[node.strip() for node in r.split('->') if node.strip()] for r in rows]
        
        if not grid: return

        # 2. Calcular Dimensiones del Grid
        num_rows = len(grid)
        col_widths = {} # Ancho máximo por columna
        row_heights = {} # Alto máximo por fila
        
        node_data_map = {} # Guardamos los objetos nodo generados

        # Pre-generar nodos para medir tamaños
        for r_idx, row in enumerate(grid):
            current_row_h = 0
            for c_idx, node_text in enumerate(row):
                # Detectar tipo
                u_text = node_text.upper()
                stype = "BOX"
                if any(k in u_text for k in ["DB", "SQL", "DATA"]): stype = "CYLINDER"
                elif any(k in u_text for k in ["?", "IF", "DECISION"]): stype = "DIAMOND"
                elif any(k in u_text for k in ["START", "END", "USER", "[DIR]"]): stype = "SOFTBOX"
                
                # Generar forma
                node_obj = self._get_node_shape(node_text, stype)
                node_data_map[(r_idx, c_idx)] = node_obj
                
                # Actualizar maximos
                col_widths[c_idx] = max(col_widths.get(c_idx, 0), node_obj['w'])
                current_row_h = max(current_row_h, node_obj['h'])
            row_heights[r_idx] = current_row_h

        # 3. Calcular Coordenadas (X, Y) con Gaps
        GAP_X = 6
        GAP_Y = 4
        
        x_positions = {}
        curr_x = 2
        for c in sorted(col_widths.keys()):
            x_positions[c] = curr_x
            curr_x += col_widths[c] + GAP_X
            
        y_positions = {}
        curr_y = 2
        for r in sorted(row_heights.keys()):
            y_positions[r] = curr_y
            curr_y += row_heights[r] + GAP_Y

        # 4. Canvas Final
        self.paper = Canvas(curr_x + 5, curr_y + 5)

        # 5. Estampar y Guardar Anchors
        node_anchors = {}
        
        for (r, c), node in node_data_map.items():
            # Centrado vertical en su fila
            final_x = x_positions[c]
            row_h = row_heights[r]
            final_y = y_positions[r] + (row_h - node['h']) // 2
            
            self.paper.stamp(final_x, final_y, node['art'])
            node_anchors[(r,c)] = self._get_anchors(final_x, final_y, node['w'], node['h'])

        # 6. Rutear Flechas
        for (r, c), anchors in node_anchors.items():
            # Flecha Horizontal (Derecha)
            if (r, c+1) in node_anchors:
                target = node_anchors[(r, c+1)]
                self._draw_h_arrow(anchors['e'], target['w'])
            
            # Flecha Vertical (Abajo)
            # Solo si estamos en la ultima columna de la fila actual O explícito
            # Simplificación: Conectar con el nodo directamente abajo si existe
            if (r+1, c) in node_anchors:
                target = node_anchors[(r+1, c)]
                self._draw_v_arrow(anchors['s'], target['n'])

        # 7. PRINT FINAL (IMPORTANTE)
        print("\n" + "="*60)
        print(self.paper.render())
        print("="*60 + "\n")

    def _draw_h_arrow(self, start, end):
        y = start[1]
        for x in range(start[0] + 1, end[0]):
            self.paper.put_char(x, y, "-")
        self.paper.put_char(end[0]-1, y, ">")

    def _draw_v_arrow(self, start, end):
        sx, sy = start
        ex, ey = end
        mid_y = sy + (ey - sy) // 2
        
        # Bajar
        for y in range(sy + 1, mid_y): self.paper.put_char(sx, y, "|")
        self.paper.put_char(sx, mid_y, "+")
        
        # Viajar X
        step = 1 if ex > sx else -1
        if sx != ex:
            for x in range(sx + step, ex, step): self.paper.put_char(x, mid_y, "-")
            self.paper.put_char(ex, mid_y, "+")
            
        # Bajar final
        for y in range(mid_y + 1, ey): self.paper.put_char(ex, y, "|")
        self.paper.put_char(ex, ey, "v")