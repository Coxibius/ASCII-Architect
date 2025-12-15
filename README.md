🏛️ ASCII Architect
> **The Neural-Symbolic Diagram Generator for the Terminal.**


    _    ____   ____ ___ ___      _         _     _ _            _   
   / \  / ___| / ___|_ _|_ _|    / \   _ __| |__ (_) |_ ___  ___| |_ 
  / _ \ \___ \| |    | | | |    / _ \ | '__| '_ \| | __/ _ \/ __| __|
 / ___ \ ___) | |___ | | | |   / ___ \| |  | | | | | ||  __/ (__| |_ 
/_/   \_\____/ \____|___|___| /_/   \_\_|  |_| |_|_|\__\___|\___|\__|
                                                       v1.0-beta
![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

![alt text](https://img.shields.io/badge/Python-3.9%2B-blue)

![alt text](https://img.shields.io/badge/Architecture-Neural--Symbolic-purple)
ASCII Architect is an engineering-grade tool designed to generate precision ASCII diagrams directly in your CLI. Unlike standard generative art, this tool prioritizes structural integrity, grid alignment, and semantic logic for software documentation.
It uses a Hybrid Architecture:
🧠 Neural Engine (GPT-2): Fine-tuned Small Language Models (SLMs) generate the shapes (Cylinders, Diamonds, Softboxes).
📐 Symbolic Router (Python): A deterministic "Manhattan-style" engine handles grid layout, smart anchoring, and arrow routing.
✨ Key Features
Matrix / Grid Layout: Use ; to define rows and -> for columns.
Semantic Shape Detection: The engine automatically selects the right shape based on your text:
DB, DATA, SQL → Cylinder (Database)
?, IF, DECISION → Diamond (Decision Node)
USER, START, END → Softbox (Rounded)
Default → Box (Rectangular)
Smart Anchors: Arrows calculate exact entry/exit points (e.g., Diamond tips) to avoid visual clipping.
Vertical Routing: Automatically draws vertical connections between rows.
⚡ Quick Start
1. Clone the Repository
code
Bash
git clone https://github.com/Coxibius/ASCII-Architect.git
cd ASCII-Architect
2. Install Dependencies
code
Bash
pip install -r requirements.txt
3. 📥 Download the Brains (Models)
Since the neural weights are heavy, they are hosted in the Releases section.
Go to the Releases Page.
Download ASCII_Architect_V2_Expansion.zip.
Extract them exactly into:
ascii-architect/models/ASCII_Architect_V2_Expansion/
Your folder structure must look like this:
code
Text
models/
├── ASCII_Architect_V1_Models/   (Base models)
└── ASCII_Architect_V2_Expansion/
    ├── expert_cylinder/
    ├── expert_diamond/
    └── expert_softbox/
🎮 Usage
Run the CLI directly from the source:
Basic Horizontal Flow
code
Bash
python src/cli.py flow "CLIENT -> API_GATEWAY -> SERVER"
🚀 Advanced Matrix Flow (The "Architecture" Mode)
Use ; to break lines. The engine will align columns automatically.
code
Bash
python src/cli.py flow "USER -> LOGIN_API -> AUTH_SERVICE ; IS_LOGGED? -> USER_DB ; ERROR_PAGE"
Output Preview:
code
Text
.----------.        +-----------+      +--------------+
  |          |        |           |      |              |
  |   USER   |------->| LOGIN_API |----->| AUTH_SERVICE |
  |          |        |           |      |              |
  '----------'        +-----------+      +--------------+
        |                   |
        |                   |
  -     v             .=====v====.
       / \            |          |
      /   \           + USER_DB  +
     /     \          |          |
    /       \         '=====-===='
   IS_LOGGED?  ------>
  |           |
   \         /
      \   /
        v
  +-----------+
  |           |
  | ERROR_PG  |
  |           |
  +-----------+
🏗️ Architecture
ASCII Architect solves the "Generative AI Hallucination" problem by decoupling Shape Generation from Layout Logic.
Parser: Splits the input string into a Virtual Grid (Row, Col).
Dispatcher: Scans keywords (e.g., "DB") and requests a specific shape from the Neural Engine.
Inference: The specific GPT-2 Expert generates the ASCII character block.
Router: The Python engine calculates (x, y) coordinates, aligns centers, and draws connections (|, ->) using geometric logic, not AI.
🗺️ Roadmap

v0.1: Horizontal flow engine.

v1.0: Matrix Layout, Vertical Routing, and Semantic Models.

v1.5: Dynamic Text Resizing (Auto-expand shapes).

v2.0: "Manhattan" Elbow routing (complex paths around obstacles).
📄 License

MIT License. Created by Coxibius.
