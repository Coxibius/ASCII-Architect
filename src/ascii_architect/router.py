from ascii_architect.canvas import Canvas
from ascii_architect.renderers import BoxRenderer, CylinderRenderer, SoftBoxRenderer, DiamondRenderer
from ascii_architect.utils import inject_text

class Router:
    def __init__(self, use_neural_engine: bool = False):
        self.use_neural_engine = use_neural_engine
        self.neural_engine = None
        
        if self.use_neural_engine:
            try:
                # Importación Lazy: Solo cargamos PyTorch si es necesario
                from ascii_architect.neural_engine import ArchitectEngine as NeuralEngine
                
                self.neural_engine = NeuralEngine()
                print("🧠 [INFO] Neural Engine Loaded (Experimental Mode)")
            except (ImportError, Exception) as e:
                if isinstance(e, ImportError):
                    print("⚠️ [WARNING] No se pudo cargar el Neural Engine (¿Faltan dependencias/modelos?).")
                else:
                    print(f"⚠️ [ERROR] Error inicializando IA: {e}")
                print("   -> Cambiando automáticamente a modo Plantillas.")
                self.use_neural_engine = False

        # Initial canvas, will be resized dynamically
        self.paper = Canvas(width=1, height=1) 
        
    def _get_anchors(self, shape_type, x, y, w, h):
        """
        Calculates Smart Anchors (N, S, E, W) based on shape type and dimensions.
        Returns dict: {'n': (x,y), 's': (x,y), 'e': (x,y), 'w': (x,y)}
        """
        cx = x + w // 2
        cy = y + h // 2
        
        anchors = {
            'n': (cx, y),
            's': (cx, y + h - 1),
            'w': (x, cy),
            'e': (x + w - 1, cy)
        }

        # Specific adjustments for DIAMOND (Saturn Effect Alignment)
        if shape_type == "DIAMOND":
            # In the Saturn Effect renderer, text is floating but the cone tips are fixed at 3 lines.
            CONE_HEIGHT = 4 # Including tip line in sharp mode
            anchors['n'] = (cx, y)
            anchors['s'] = (cx, y + h - 1)
            # Find the true vertical center of the floating text area
            # Total height = cone_top(4) + text_lines + cone_bottom(4)
            # Actually our DiamondRenderer height calculation is dynamic.
            # We align E/W to the geometric middle for now.
            anchors['w'] = (x, cy)
            anchors['e'] = (x + w - 1, cy)
            
        return anchors

    def _get_node_shape(self, node_text: str, shape_type: str, default_width: int = 12):
        """
        Generates or retrieves the ASCII art for a node using Deterministic or Neural engine.
        """
        clean_text = node_text.strip().upper()
        art = None

        # 1. Intento con IA (Si está activado y cargado)
        if self.use_neural_engine and self.neural_engine:
            try:
                width = max(default_width, len(clean_text) + 4)
                dims = f"[DIM:{width}x5]"
                # Asumiendo que ArchitectEngine usa generate(shape, style, dims)
                raw_box = self.neural_engine.generate(shape_type, "[STYLE:SOLID]", dims)
                art = inject_text(raw_box, clean_text)
            except Exception:
                # Fallback silencioso a plantillas si la IA falla
                pass

        # 2. Modo Determinista (Plantillas) - EL DEFAULT ROBUSTO
        if art is None:
            if shape_type == "CYLINDER":
                art = CylinderRenderer.render(clean_text)
            elif shape_type == "SOFTBOX":
                art = SoftBoxRenderer.render(clean_text)
            elif shape_type == "DIAMOND":
                art = DiamondRenderer.render(clean_text)
            else:
                art = BoxRenderer.render(clean_text)
        
        # Measure dimensions
        lines = art.split('\n')
        real_h = len(lines)
        real_w = max(len(l) for l in lines) if lines else 0
        
        return {
            'art': art,
            'w': real_w,
            'h': real_h,
            'type': shape_type,
            'label': clean_text
        }

    def process(self, layout_str: str):
        """
        Procesa el string de flujo, calcula el layout y DIBUJA el resultado con separadores.
        """
        mode = "NEURAL MODE" if self.use_neural_engine else "TEMPLATE MODE"
        print(f"🔄 Processing Flow: {layout_str[:50]}... [{mode}]")

        diagram = self.draw_flow(layout_str)

        print("\n" + "="*60)
        print(diagram.replace("░", " "))
        print("="*60 + "\n")
        
        return diagram

    def draw_flow(self, flow_string: str):
        """
        Matrix Layout Engine V1.1
        Parses input string into a grid of nodes and stamps them onto the canvas.
        """
        # Parsing into Grid
        rows_str = flow_string.split(";")
        grid_data = [] 
        for row_str in rows_str:
            col_nodes = [n.strip() for n in row_str.split("->") if n.strip()]
            if col_nodes:
                grid_data.append(col_nodes)
        
        if not grid_data:
            return ""

        num_rows = len(grid_data)
        num_cols = max(len(row) for row in grid_data)
        
        # 2. Generate & Measure Nodes
        node_map = {}
        col_widths = [0] * num_cols
        row_heights = [0] * num_rows 
        
        for r in range(num_rows):
            current_row_max_h = 0
            for c in range(len(grid_data[r])):
                node_text = grid_data[r][c]
                
                # Type Detection
                u_text = node_text.upper()
                shape_type = "BOX"
                if any(x in u_text for x in ["DB", "DATA", "SQL", "SQLITE"]): shape_type = "CYLINDER"
                elif any(x in u_text for x in ["?", "IF", "DECISION"]): shape_type = "DIAMOND"
                elif any(x in u_text for x in ["START", "END", "USER", "CLIENT", "AUTH", "ROOT", "[DIR]"]): shape_type = "SOFTBOX"
                # Note: Directories are hard to distinguish by name alone here, 
                # but ProjectScanner can be tweaked if needed.
                
                node = self._get_node_shape(node_text, shape_type)
                node_map[(r,c)] = node
                
                if node['w'] > col_widths[c]: col_widths[c] = node['w']
                if node['h'] > current_row_max_h: current_row_max_h = node['h']
            
            row_heights[r] = current_row_max_h

        # 3. Coordinate Calculation
        col_x_coords = []
        current_x = 2
        GAP_X = 6 
        for w in col_widths:
            col_x_coords.append(current_x)
            current_x += w + GAP_X
            
        row_y_coords = []
        current_y = 2
        GAP_Y = 4 
        for h in row_heights:
            row_y_coords.append(current_y)
            current_y += h + GAP_Y
            
        # 4. Canvas Creation
        self.paper = Canvas(width=current_x + 5, height=current_y + 5)
        
        # 5. Rendering & Anchors
        node_positions = {} 
        for r in range(num_rows):
            for c in range(len(grid_data[r])):
                if (r,c) in node_map:
                    node = node_map[(r,c)]
                    x = col_x_coords[c]
                    # Center in row
                    y = row_y_coords[r] + (row_heights[r] - node['h']) // 2
                    
                    self.paper.stamp(x, y, node['art'])
                    node_positions[(r,c)] = self._get_anchors(node['type'], x, y, node['w'], node['h'])
        
        # 6. Draw Arrows
        for r in range(num_rows):
            cols = len(grid_data[r])
            for c in range(cols):
                curr_anchors = node_positions.get((r,c))
                if not curr_anchors: continue
                
                if c < cols - 1:
                    next_anchors = node_positions.get((r, c+1))
                    if next_anchors:
                        start = curr_anchors['e']
                        end = next_anchors['w']
                        sy = start[1]
                        for lx in range(start[0] + 1, end[0]):
                             self.paper.put_char(lx, sy, "-")
                        self.paper.put_char(end[0] - 1, sy, ">")

                if r < num_rows - 1:
                    if c < len(grid_data[r+1]) and (r+1, c) in node_positions:
                        next_anchors = node_positions[(r+1, c)]
                        self._draw_vertical_arrow(curr_anchors['s'], next_anchors['n'])

        return self.paper.render()

    def _draw_vertical_arrow(self, start, end):
        sx, sy = start
        ex, ey = end
        if sx == ex:
            for y in range(sy + 1, ey): self.paper.put_char(sx, y, "|")
            self.paper.put_char(ex, ey, "v")
            return

        mid_y = sy + (ey - sy) // 2
        for y in range(sy + 1, mid_y): self.paper.put_char(sx, y, "|")
        self.paper.put_char(sx, mid_y, "+")
        step = 1 if ex > sx else -1
        for x in range(sx + step, ex, step): self.paper.put_char(x, mid_y, "-")
        self.paper.put_char(ex, mid_y, "+")
        for y in range(mid_y + 1, ey): self.paper.put_char(ex, y, "|")
        self.paper.put_char(ex, ey, "v")

if __name__ == "__main__":
    router = Router(use_neural_engine=False)
    print(router.draw_flow("Start -> Decision? -> Process ; Process -> DB").replace("░", " "))
