import json
import random
import os

# CONFIGURATION
OUTPUT_FILENAME = "dataset_diamonds.jsonl"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
SAMPLES = 6000 # Increased sample size for better pattern recognition

# VISUAL TOKENS (V18 Standard)
ALPHA = "░"
ANCHOR_N = "N"
ANCHOR_S = "S"
ANCHOR_E = "E"
ANCHOR_W = "W"
SLANT_UP = "/"
SLANT_DOWN = "\\"

def generate_diamond_entry(radius):
    """
    Generates a Diamond constrained to a Box.
    Radius 2 = 5x5 Box
    Radius 3 = 7x7 Box
    Formula: Width = (Radius * 2) + 1
             Height = (Radius * 2) + 1
    """
    
    # 1. Calculate Dimensions
    width = (radius * 2) + 1
    height = width # Keep it square 1:1 ratio for simplicity in V1
    
    # Center index (0-based)
    center_idx = radius 
    
    art_lines = []

    # 2. Build the ASCII (Line by Line)
    # We iterate from y=0 to y=height-1
    for y in range(height):
        row_chars = [ALPHA] * width
        
        # DISTANCE FROM EQUATOR (Middle Row)
        # If radius is 3 (Height 7), middle is row 3.
        dist = abs(center_idx - y)
        
        # SPREAD calculation (Inverse of distance)
        # At middle (dist 0), spread is max (radius)
        # At tips (dist radius), spread is 0
        spread = radius - dist

        # Logic for Edges
        left_pos = center_idx - spread
        right_pos = center_idx + spread

        # A. TIPS (North / South)
        if dist == radius:
            if y == 0:
                row_chars[center_idx] = ANCHOR_N
            else:
                row_chars[center_idx] = ANCHOR_S
        
        # B. EQUATOR (West / East / Text Line)
        elif dist == 0:
            row_chars[0] = ANCHOR_W
            row_chars[-1] = ANCHOR_E
            # Note: The inside remains ALPHA ░ for Python text injection
            
        # C. SLOPES (The Walls)
        else:
            # Upper Half
            if y < center_idx:
                row_chars[left_pos] = SLANT_UP
                row_chars[right_pos] = SLANT_DOWN
            # Lower Half
            else:
                row_chars[left_pos] = SLANT_DOWN
                row_chars[right_pos] = SLANT_UP

        art_lines.append("".join(row_chars))

    return art_lines, width, height

def format_hybrid_v18(line, line_idx):
    """
    V18 Protocol: <Lxx> [S:00] content
    """
    # We use S:00 because the diamond itself contains the spacing (ALPHA)
    # The Router handles the absolute positioning on the canvas.
    s_token = "[S:00]" 
    l_token = f"<L{line_idx+1:02d}>"
    return f"{l_token} {s_token} {line}"

def main():
    print(f"💎 Generating {SAMPLES} Diamond samples...")
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for _ in range(SAMPLES):
            # Generate a random size
            # Radius 1 = 3x3 (Too small for text)
            # Radius 2 = 5x5 (Minimum)
            # Radius 8 = 17x17 (Large)
            r = random.randint(2, 9)
            
            art_lines, w, h = generate_diamond_entry(r)
            
            # V18 PROMPT SYNTAX
            # Crucial: We map the exact calculated WxH to the prompt
            prompt = f"[TYPE:DIAMOND] [STYLE:SOLID] [DIM:{w}x{h}]"
            
            # COMPLETION SYNTAX
            formatted_lines = [format_hybrid_v18(line, i) for i, line in enumerate(art_lines)]
            completion = "\n".join(formatted_lines) + " [STOP]"
            
            # JSONL Write
            entry = {"prompt": prompt, "completion": completion}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Success! Dataset saved to: {OUTPUT_FILENAME}")
    print(f"ℹ️  Next Step: Run your training script on this file.")

if __name__ == "__main__":
    main()