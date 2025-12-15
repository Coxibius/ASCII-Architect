# ASCII Architect (Terminal-God)

**ASCII Architect** is a neural-symbolic engineering tool designed to generate precision ASCII diagrams directly in the terminal (`cli`). Unlike standard generative art, this tool prioritizes structural integrity, alignment, and technical readability for software documentation.

It leverages a hybrid architecture:
- **Neural Engine:** Fine-tuned GPT-2 Small Language Models (SLMs) for generating geometric shapes (Boxes, Cylinders, Diamonds).
- **Symbolic Router:** A Python-based deterministic engine for layout, alignment, and "Manhattan" arrow routing.

## 🚀 Current Capabilities (v0.1 - Prototype)

- **Text-to-Diagram:** Generates ASCII nodes from natural language prompts.
- **Auto-Routing:** Automatically connects nodes horizontally.
- **Hybrid Syntax:** Uses a strictly tokenized intermediate language (`<Lxx>`, `[S:xx]`) to ensure grid alignment.

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.9+
- CUDA-enabled GPU (Recommended for inference speed)

### Basic Commands

```bash
# 1. Generate a single component
python src/cli.py box --text "Microservice A" --type box

# 2. Generate a linear flow
python src/cli.py flow "USER -> LOAD_BALANCER -> API_GATEWAY"


🗺️ Roadmap

v0.1: Horizontal flows and Box generation (Completed).

v0.2: Vertical routing and Stacking logic (In Progress).

v0.3: Specialized Experts (Database/Cylinder, Decision/Diamond models).

v1.0: PyPI Release and branching logic.