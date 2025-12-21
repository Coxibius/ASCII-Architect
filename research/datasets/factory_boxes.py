import json
import random
import os

# CONFIGURATION
OUTPUT_FILENAME = "dataset_boxes.jsonl"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
SAMPLES = 5000

# DICTIONARY V18 (Architect)
ALPHA = "░"
ANCHOR_N = "N"
ANCHOR_S = "S"
ANCHOR_E = "E"
ANCHOR_W = "W"
BORDER_H = "-"
BORDER_V = "|"
CORNER = "+"

def generate_box_art(width, height, style="SOLID"):
    """
    Generates a perfect ASCII box with logical anchors.
    Example 5x3:
    +N--+
    W░░░E
    +S--+
    """
    art = []
    
    # 1. TOP (With North Anchor)
    # Calculate center for N
    mid = width // 2
    # Ensure mid is within bounds for very small widths, though min width is 5
    top = CORNER + (BORDER_H * (mid - 1)) + ANCHOR_N + (BORDER_H * (width - mid - 2)) + CORNER
    art.append(top)
    
    # 2. BODY (With West/East Anchors and transparent fill)
    inner_width = width - 2
    filler = ALPHA * inner_width 
    
    for _ in range(height - 2):
        # Default row: Vertical Border + Filler + Vertical Border
        # Note: The logic in text file mentions putting W/E in the middle row.
        # For simplicity in loop, we use standard borders, and then inject W/E later.
        row = BORDER_V + filler + BORDER_V
        art.append(row)
        
    # Inject W/E anchors in the center row
    if len(art) > 1: # Validation for safety
        center_row_idx = len(art) // 2
        # Reconstruct center row with anchors
        # W + filler + E
        art[center_row_idx] = ANCHOR_W + filler + ANCHOR_E

    # 3. BOTTOM (With South Anchor)
    bottom = CORNER + (BORDER_H * (mid - 1)) + ANCHOR_S + (BORDER_H * (width - mid - 2)) + CORNER
    art.append(bottom)
    
    return art

def format_hybrid_v18(line, line_idx):
    """
    V18 HYBRID LOGIC ADAPTED:
    [S:xx] + <Lxx> + Content
    """
    # For training, we assume the box starts at X=0, so S is always 00.
    s_token = "[S:00]" 
    l_token = f"<L{line_idx+1:02d}>"
    
    return f"{l_token} {s_token} {line}"

def main():
    print(f"Generating {SAMPLES} samples to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for _ in range(SAMPLES):
            # Vary dimensions
            w = random.randint(5, 20) # Width between 5 and 20 chars
            h = random.randint(3, 10) # Height between 3 and 10 lines
            
            # Generate raw art
            raw_art = generate_box_art(w, h)
            
            # Create Prompt with explicit metadata
            prompt = f"[TYPE:BOX] [STYLE:SOLID] [DIM:{w}x{h}]"
            
            # Format Completion (V18 Logic)
            comp_lines = [format_hybrid_v18(l, i) for i, l in enumerate(raw_art)]
            completion = "\n".join(comp_lines) + " [STOP]"
            
            f.write(json.dumps({"prompt": prompt, "completion": completion}, ensure_ascii=False) + "\n")

    print("✅ Architect Dataset generated successfully.")

if __name__ == "__main__":
    main()
