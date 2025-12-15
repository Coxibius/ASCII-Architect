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
        
    def draw_flow(self, flow_string):
        """
        Matrix Layout Engine V1.0
        Parses input string into a grid of nodes and stamps them onto the canvas.
        Input: "A -> B ; C -> D"
        Visual:
          [A]--->[B]
           |      |
          v      v (Vertical arrows not implemented yet, just grid structure)
          [C]--->[D]
        """
        print(f"🔄 Processing Flow: {flow_string}")
        
        # 1. Parsing into Grid
        rows_str = flow_string.split(";")
        grid = []
        for r_idx, row_str in enumerate(rows_str):
            col_nodes = [n.strip() for n in row_str.split("->") if n.strip()]
            if col_nodes:
                grid.append(col_nodes)
        
        if not grid:
            return ""

        # 2. Grid Dimensions calculation
        num_rows = len(grid)
        num_cols = max(len(row) for row in grid)
        
        # Stores calculated dimensions for the grid structure
        # col_widths[c] = max width found in column c
        # row_heights[r] = max height found in row r (usually fixed for now, but good for future proofing)
        col_widths = [0] * num_cols
        row_heights = [0] * num_rows
        
        # Pre-calculate node boxes to measure them
        # node_cache[(r, c)] = (raw_box, width, height)
        node_cache = {}
        
        print("   Calculating Grid Layout...")
        for r in range(num_rows):
            # Default height for a row if no content (unlikely)
            current_row_max_h = 5 
            
            for c in range(len(grid[r])):
                node_text = grid[r][c]
                
                # Logic to generate box and measure it
                # Min width 12, or text legnth + 4 padding
                width = max(12, len(node_text) + 4)
                dims = f"[DIM:{width}x5]"
                
                # Generate box
                raw_box = self.brain.generate("BOX", "[STYLE:SOLID]", dims)
                final_box = inject_text(raw_box, node_text)
                
                # Store in cache
                node_cache[(r, c)] = final_box
                
                # Update Grid Stats
                if width > col_widths[c]:
                    col_widths[c] = width
                
                # Assuming constant height 5 for V1 boxes, but logic supports variable
                # If we had taller boxes, we'd parse newlines in final_box
                if 5 > current_row_max_h:
                    current_row_max_h = 5
            
            row_heights[r] = current_row_max_h

        # 3. Calculate Layout Coordinates (X, Y)
        # col_coords[0] -> X position of column 0
        col_coords = []
        current_x = 2 # Initial Padding Left
        gap_x = 4      # Space between columns (for short arrows)
        
        for w in col_widths:
            col_coords.append(current_x)
            current_x += w + gap_x
            
        # row_coords[0] -> Y position of row 0
        row_coords = []
        current_y = 2 # Initial Padding Top
        gap_y = 3     # Space between rows
        
        for h in row_heights:
            row_coords.append(current_y)
            current_y += h + gap_y

        # 4. Canvas Resizing
        total_width = current_x + 2 # Padding Right
        total_height = current_y + 2 # Padding Bottom
        
        print(f"   Resizing Canvas to {total_width}x{total_height}...")
        self.paper = Canvas(width=total_width, height=total_height)
        
        # 5. Rendering Loop
        for r in range(num_rows):
            for c in range(len(grid[r])):
                # Stamp the Node
                if (r, c) in node_cache:
                    box_art = node_cache[(r, c)]
                    self.paper.stamp(col_coords[c], row_coords[r], box_art)
                    
                    # Draw Horizontal Arrow (if not last in its row)
                    if c < len(grid[r]) - 1:
                        # Determine start and end points for arrow
                        start_x_node = col_coords[c]
                        # We need the actual width of THIS node to know where it ends
                        # But visually, we are aligning columns, so the arrow might stretch?
                        # Or should the arrow just be between the columns?
                        
                        # Requirement: "Calculate x and y px positions based on MAX width"
                        # This implies columns are fixed width blocks.
                        # So the arrow starts after the column width? 
                        # Or does it start after the node?
                        # "Grid Layout" usually implies alignment.
                        # Let's anchor arrows to the grid column boundaries for clean alignment.
                        
                        # Arrow logic:
                        # Start: col_coords[c] + col_widths[c]
                        # End: col_coords[c+1] 
                        # Let's just put a standard arrow right after CURRENT node width?
                        # No, if we want grid alignment, visually it looks better if arrows are consistent.
                        # BUT, if node is small in a big column, arrow will float.
                        # Let's stick to simple: Arrow connects visual right edge of node to next element.
                        
                        # Re-eval for V1:
                        # Stamp arrow at End of current Node Box?
                        # Or fixed relative to Grid?
                        
                        # Let's try: Arrow starts at end of Node Box.
                        # Problems: If Node A is short, and Node B (below it) is long,
                        # Column 2 starts at the same X. 
                        # So Arrow from A needs to be longer to reach Column 2.
                        
                        box_lines = box_art.split('\n')
                        box_actual_width = len(box_lines[0]) if box_lines else col_widths[c]
                        
                        arrow_start_x = col_coords[c] + box_actual_width - 1
                        arrow_target_x = col_coords[c+1]
                        
                        dist = arrow_target_x - arrow_start_x
                        if dist < 2: dist = 2 # Safety min len
                        
                        # Generate dynamic length arrow??
                        # For now, just a fixed small arrow or whatever fits.
                        # User said: "For now, keep arrows simple (Horizontal only within same row)"
                        # Let's use a simple arrow generation logic or fixed.
                        
                        arrow_len = dist
                        # Note: Our arrow generator might support variable length?
                        # "raw_arrow = self.brain.generate("ARROW", ... f"[LEN:{arrow_len}]")"
                        # The old code used this. Let's assume engine supports LEN param dynamically or we mock it.
                        
                        raw_arrow = self.brain.generate("ARROW", "[DIR:RIGHT]", f"[LEN:{arrow_len}]")
                        
                        # Centering Y
                        # Box is height 5. Center is +2.
                        arrow_y = row_coords[r] + 2
                        
                        self.paper.stamp(arrow_start_x, arrow_y, raw_arrow)

        return self.paper.render()

if __name__ == "__main__":
    router = AutoRouter()
    
    print("\n🏗️ MATRIX LAYOUT TEST V1.0...")

    # TEST 1: Simple 2x2 Grid
    #  USER -> API
    #   |?(virtual)
    #  DB   -> CACHE
    flow1 = "USER -> API ; DB -> CACHE"
    print(f"\n[TEST 1: 2x2 Grid]\nPrompt: '{flow1}'")
    print("-" * 60)
    print(router.draw_flow(flow1).replace("░", " "))
    
    # TEST 2: Uneven Columns
    #  LONG_NAME_SERVICE -> B
    #  A                 -> C
    flow2 = "LONG_NAME_SERVICE -> B ; A -> C"
    print(f"\n[TEST 2: Alignment Check]\nPrompt: '{flow2}'")
    print("-" * 60)
    print(router.draw_flow(flow2).replace("░", " "))

    # TEST 3: 1D Fallback
    flow3 = "JUST -> ONE -> LINE"
    print(f"\n[TEST 3: Standard Linear]\nPrompt: '{flow3}'")
    print("-" * 60)
    print(router.draw_flow(flow3).replace("░", " "))