import sys
import os

# Configuración de imports para que encuentre los módulos hermanos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

try:
    from engine import ArchitectEngine
    from ascii_architect.canvas import Canvas
    from utils import inject_text
except ImportError:
    from src.engine import ArchitectEngine
    from src.ascii_architect.canvas import Canvas
    from src.utils import inject_text

class AutoRouter:
    def __init__(self):
        self.brain = ArchitectEngine()
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
            'e': (x + w - 1, cy) # Default, works for BOX/CYLINDER
        }

        # Specific adjustments
        if shape_type == "DIAMOND":
            anchors['n'] = (cx, y)
            anchors['s'] = (cx, y + h - 1)
            anchors['w'] = (x, cy) # Left Tip
            anchors['e'] = (x + w - 1, cy) # Right Tip - Exact center horizontally
            
        return anchors

    def _draw_vertical_arrow(self, start, end):
        """
        Draws a vertical arrow from start(x,y) to end(x,y).
        Uses geometric routing (Manhattan/Elbow) if not aligned.
        """
        sx, sy = start
        ex, ey = end
        
        # 1. Simple Case: Straight down
        if sx == ex:
            # Draw line
            for y in range(sy + 1, ey):
                self.paper.put_char(sx, y, "|")
            # Draw Tip
            self.paper.put_char(ex, ey, "v")
            # Correct intersection with start line?
            # Typically start is the bottom of a box, so sy+1 is the first empty space.
            return

        # 2. Offset Case: Elbow Routing
        # Start -> Down to Mid -> Horizontal -> Down to End
        mid_y = sy + (ey - sy) // 2
        
        # Down to Mid
        for y in range(sy + 1, mid_y):
            self.paper.put_char(sx, y, "|")
            
        # Corner 1
        self.paper.put_char(sx, mid_y, "+")
        
        # Horizontal
        step = 1 if ex > sx else -1
        # range doesn't include stop, so for reverse we need to be careful
        # simpler to just iterate min to max
        start_x_h = min(sx, ex) + 1
        end_x_h = max(sx, ex)
        
        for x in range(start_x_h, end_x_h):
            self.paper.put_char(x, mid_y, "-")
            
        # Corner 2
        self.paper.put_char(ex, mid_y, "+")
        
        # Down to End
        for y in range(mid_y + 1, ey):
            self.paper.put_char(ex, y, "|")
            
        # Tip
        self.paper.put_char(ex, ey, "v")

    def draw_flow(self, flow_string):
        """
        Matrix Layout Engine V1.1
        Parses input string into a grid of nodes and stamps them onto the canvas.
        Input: "A -> B ; C -> D"
        """
        print(f"🔄 Processing Flow: {flow_string}")
        
        # 1. Parsing into Grid
        rows_str = flow_string.split(";")
        grid_data = [] # List of lists of strings
        for row_str in rows_str:
            col_nodes = [n.strip() for n in row_str.split("->") if n.strip()]
            if col_nodes:
                grid_data.append(col_nodes)
        
        if not grid_data:
            return ""

        num_rows = len(grid_data)
        num_cols = max(len(row) for row in grid_data)
        
        # 2. Generate & Measure Nodes
        # node_map[(r,c)] = { 'art': str, 'w': int, 'h': int, 'type': str }
        node_map = {}
        col_widths = [0] * num_cols
        row_heights = [0] * num_rows # Track max height per row
        
        print("   Calculating Grid Layout...")
        
        for r in range(num_rows):
            current_row_max_h = 5 # Min default
            
            for c in range(len(grid_data[r])):
                node_text = grid_data[r][c]
                
                # Heuristic for Width
                width = max(12, len(node_text) + 4)
                dims = f"[DIM:{width}x5]"
                
                # Type Detection
                u_text = node_text.upper()
                shape_type = "BOX"
                if any(x in u_text for x in ["DB", "DATA", "SQL"]): shape_type = "CYLINDER"
                elif any(x in u_text for x in ["?", "IF", "DECISION"]): shape_type = "DIAMOND"
                elif any(x in u_text for x in ["START", "END", "USER"]): shape_type = "SOFTBOX"
                
                # Generate
                # print(f"   Generating {shape_type} for '{node_text}'...") # Reduce noise
                raw_box = self.brain.generate(shape_type, "[STYLE:SOLID]", dims)
                final_box = inject_text(raw_box, node_text)
                
                # Measure exact
                lines = final_box.split('\n')
                real_h = len(lines)
                real_w = max(len(l) for l in lines) if lines else width
                
                node_map[(r,c)] = {
                    'art': final_box,
                    'w': real_w,
                    'h': real_h,
                    'type': shape_type,
                    'label': node_text
                }
                
                if real_w > col_widths[c]: col_widths[c] = real_w
                if real_h > current_row_max_h: current_row_max_h = real_h
            
            row_heights[r] = current_row_max_h

        # 3. Coordinate Calculation
        # col_x_coords[c] = absolute X
        col_x_coords = []
        current_x = 2
        GAP_X = 6 # Space for horizontal arrows
        
        for w in col_widths:
            col_x_coords.append(current_x)
            current_x += w + GAP_X
            
        row_y_coords = []
        current_y = 2
        GAP_Y = 4 # Space for vertical arrows
        
        for h in row_heights:
            row_y_coords.append(current_y)
            current_y += h + GAP_Y
            
        # 4. Canvas Resize
        total_width = current_x + 5
        total_height = current_y + 5
        print(f"   Resizing Canvas to {total_width}x{total_height}...")
        self.paper = Canvas(width=total_width, height=total_height)
        
        # 5. Rendering & Anchors
        # First pass: Stamp Nodes and Store Anchors
        node_positions = {} # (r,c) -> { 'anchors': ... }
        
        for r in range(num_rows):
            for c in range(len(grid_data[r])):
                if (r,c) in node_map:
                    node = node_map[(r,c)]
                    
                    # Position: Center in Grid Cell vs Left Align?
                    # Current: Left Align in Column
                    x = col_x_coords[c]
                    y = row_y_coords[r]
                    
                    # Optional: Center vertically in row if row height > node height
                    # y += (row_heights[r] - node['h']) // 2 
                    
                    self.paper.stamp(x, y, node['art'])
                    
                    # Calculate Anchors
                    anchors = self._get_anchors(node['type'], x, y, node['w'], node['h'])
                    node_positions[(r,c)] = anchors
        
        # Second pass: Draw Arrows
        for r in range(num_rows):
            cols = len(grid_data[r])
            for c in range(cols):
                curr_anchors = node_positions.get((r,c))
                if not curr_anchors: continue
                
                # A. Horizontal Arrow (Right Neighbor)
                if c < cols - 1:
                    next_anchors = node_positions.get((r, c+1))
                    if next_anchors:
                        # Draw ->
                        start = curr_anchors['e'] # (x,y)
                        end = next_anchors['w']   # (x,y)
                        
                        # Logic: Draw line from start.x to end.x at start.y (assuming aligned centers for now)
                        # If diamonds are centered differently, y might mismatch.
                        
                        sy = start[1]
                        
                        # Simple straight line if Ys approx match
                        for lx in range(start[0] + 1, end[0]):
                             self.paper.put_char(lx, sy, "-")
                        self.paper.put_char(end[0] - 1 if end[0]>start[0] else end[0], sy, ">" if end[0]>start[0] else "<")

                # B. Vertical Arrow (Bottom Neighbor)
                # Look for node at grid[r+1][c]
                if r < num_rows - 1:
                    if c < len(grid_data[r+1]) and (r+1, c) in node_positions:
                        next_anchors = node_positions[(r+1, c)]
                        
                        start = curr_anchors['s']
                        end = next_anchors['n']
                        
                        self._draw_vertical_arrow(start, end)

        return self.paper.render()

if __name__ == "__main__":
    router = AutoRouter()
    
    print("\n🏗️ ROUTER REFACTOR TEST...")
    
    # TEST 1: Diamond Anchors
    # A -> IF -> B
    print("\n[TEST 1: Diamond Anchors]")
    t1 = "Start -> Is_Ready? -> Process"
    print(router.draw_flow(t1).replace("░", " "))
    
    # TEST 2: Vertical Internal
    # Top
    # |
    # Bottom
    print("\n[TEST 2: Vertical Routing]")
    t2 = "Top_Node ; Bottom_Node"
    print(router.draw_flow(t2).replace("░", " "))

    # TEST 3: Misalignment (ZigZag)
    # Long________Node
    # |
    # Small
    print("\n[TEST 3: Layout Alignment]")
    t3 = "Long_Node_Here ; Small"
    print(router.draw_flow(t3).replace("░", " "))