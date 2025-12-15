    import json
    import random
    import os

    # CONFIGURATION
    OUTPUT_FILENAME = "dataset_arrows.jsonl"
    OUTPUT_PATH = os.path.join(os.path.dirname(__file__), OUTPUT_FILENAME)
    SAMPLES = 5000

    # V18 ARROW TOKENS
    HEAD_UP = "^"
    HEAD_DOWN = "v"
    HEAD_LEFT = "<"
    HEAD_RIGHT = ">"
    SHAFT_H = "-"
    SHAFT_V = "|"
    CORNER = "+" # Optional for turning arrows, but let's stick to straight for now as per Phase 1

    def generate_arrow_art(length, direction="RIGHT"):
        """
        Generates a simple straight arrow.
        """
        art = []
        
        if direction == "RIGHT":
            # Example: -------->
            # Shaft length = length - 1 (head)
            row = (SHAFT_H * (length - 1)) + HEAD_RIGHT
            art.append(row)
            
        elif direction == "LEFT":
            # Example: <--------
            row = HEAD_LEFT + (SHAFT_H * (length - 1))
            art.append(row)
            
        elif direction == "DOWN":
            # Example:
            # |
            # |
            # v
            for _ in range(length - 1):
                art.append(SHAFT_V)
            art.append(HEAD_DOWN)
            
        elif direction == "UP":
            # Example:
            # ^
            # |
            # |
            art.append(HEAD_UP)
            for _ in range(length - 1):
                art.append(SHAFT_V)

        return art

    def format_hybrid_v18(line, line_idx):
        """
        V18 HYBRID LOGIC ADAPTED:
        [S:xx] + <Lxx> + Content
        """
        s_token = "[S:00]" 
        l_token = f"<L{line_idx+1:02d}>"
        return f"{l_token} {s_token} {line}"

    def main():
        print(f"Generating {SAMPLES} samples to {OUTPUT_PATH}...")
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            for _ in range(SAMPLES):
                # Randomize direction and length
                direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                length = random.randint(3, 10) 
                
                # Generate raw art
                raw_art = generate_arrow_art(length, direction)
                
                # Create Prompt
                # [TYPE:ARROW] [DIR:RIGHT] [LEN:10]
                prompt = f"[TYPE:ARROW] [DIR:{direction}] [LEN:{length}]"
                
                # Format Completion
                comp_lines = [format_hybrid_v18(l, i) for i, l in enumerate(raw_art)]
                completion = "\n".join(comp_lines) + " [STOP]"
                
                f.write(json.dumps({"prompt": prompt, "completion": completion}, ensure_ascii=False) + "\n")

        print("✅ Arrow Dataset generated successfully.")

    if __name__ == "__main__":
        main()
