# factory_soft_boxes.py
# Generator for "Soft Box" logic (Rounded Corners)
# Standard V18 Protocol: <Lxx> [S:00] CONTENT
# 
# Usage:
# Represents: Entities, Start/End Nodes, Microservices
# Distinguishing feature: Rounded corners (., ')

import random
import json
import os

OUTPUT_FILENAME = "dataset_soft_boxes.jsonl"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
SAMPLES = 6000

# VISUAL TOKENS
CORNER_TL = "."
CORNER_TR = "."
CORNER_BL = "'"
CORNER_BR = "'"
BORDER_H  = "-"
BORDER_V  = "|"
ALPHA     = "░"  # Transparent filler

# ANCHORS
ANCHOR_N = "N"
ANCHOR_S = "S"
ANCHOR_E = "E"
ANCHOR_W = "W"

def generate_soft_box_art(width, height):
    """
    Generates a Soft Box (Rounded Entity).
    Example 7x4:
     .N---. 
    W|   |E
     'S---'
    """
    art = []
    
    # Validation
    if width < 5: width = 5
    if height < 3: height = 3
    
    inner_w = width - 2
    mid_idx = inner_w // 2
    
    # 1. TOP LID (.-N-.)
    lid_chars = list(BORDER_H * inner_w)
    lid_chars[mid_idx] = ANCHOR_N
    top_line = CORNER_TL + "".join(lid_chars) + CORNER_TR
    art.append(top_line)
    
    # 2. BODY
    body_h = height - 2
    filler = ALPHA * inner_w
    
    for r in range(body_h):
        # Default row
        row_str = BORDER_V + filler + BORDER_V
        
        # Middle Row: Inject W / E anchors
        if r == body_h // 2:
            row_l = list(row_str)
            row_l[0] = ANCHOR_W  # Left Anchor
            row_l[-1] = ANCHOR_E # Right Anchor
            row_str = "".join(row_l)
            
        art.append(row_str)

    # 3. BOTTOM BASE ('-S-')
    base_chars = list(BORDER_H * inner_w)
    base_chars[mid_idx] = ANCHOR_S
    bot_line = CORNER_BL + "".join(base_chars) + CORNER_BR
    art.append(bot_line)
    
    return art

def format_hybrid_v18(line, line_idx):
    """
    Formats the line to match V18 Engine Protocol.
    Format: <L01> [S:00] ...content...
    """
    s_token = "[S:00]" 
    # Ensure line index is 2 digits (01, 02, 10)
    l_token = f"<L{line_idx+1:02d}>" 
    return f"{l_token} {s_token} {line}"

def main():
    print(f"📦 Generating {SAMPLES} Soft Box samples...")
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for _ in range(SAMPLES):
            # Dimensions
            w = random.randint(5, 15)
            h = random.randint(3, 9)
            
            # Generate Raw Art
            art_lines = generate_soft_box_art(w, h)
            
            # Create Prompt
            # [TYPE:SOFTBOX] matches the visual style
            prompt = f"[TYPE:SOFTBOX] [STYLE:SOLID] [DIM:{w}x{h}]"
            
            # Create Completion
            # 1. Format each line with <Lxx> and [S:00]
            formatted_lines = [format_hybrid_v18(l, i) for i, l in enumerate(art_lines)]
            
            # 2. Join with newlines and add ONE [STOP] token at the very end
            completion = "\n".join(formatted_lines) + " [STOP]"
            
            # Write to JSONL
            entry = {"prompt": prompt, "completion": completion}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ SoftBox Dataset generated: {OUTPUT_FILENAME}")
    print("   (Ready for training along with Diamond and Cylinder/DB datasets)")

if __name__ == "__main__":
    main()