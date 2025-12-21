# 🏛️ ASCII Architect

> **The Neural-Symbolic Diagram Generator for the Terminal.**

```text
    _    ____   ____ ___ ___      _         _     _ _            _   
   / \  / ___| / ___|_ _|_ _|    / \   _ __| |__ (_) |_ ___  ___| |_ 
  / _ \ \___ \| |    | | | |    / _ \ | '__| '_ \| | __/ _ \/ __| __|
 / ___ \ ___) | |___ | | | |   / ___ \| |  | | | | | ||  __/ (__| |_ 
/_/   \_\____/ \____|___|___| /_/   \_\_|  |_| |_|_|\__\___|\___|\__|
                                                       v1.0-beta
```
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

### 1. Clone the Repository
```bash
git clone https://github.com/Coxibius/ASCII-Architect.git
cd ASCII-Architect
```

### 2. Install the Package
Instala la herramienta y sus dependencias de forma global o en tu entorno virtual:
```bash
pip install .
```
> [!NOTE]
> Esto registrará el comando `ascii-arch` en tu sistema.

### 3. 📥 Download the Brains (Models)
*Opcional: Solo necesario para el modo Neural.*

Puesto que los pesos de los modelos son pesados, se alojan en la sección de Releases.
1. Ve a la [Releases Page](https://github.com/Coxibius/ASCII-Architect/releases).
2. Descarga `ASCII_Architect_V2_Expansion.zip`.
3. Extráelo exactamente en: `models/ASCII_Architect_V2_Expansion/`.

🎮 Usage

Tras la instalación, puedes usar el comando global `ascii-arch`.

### Basic Horizontal Flow
```bash
ascii-arch flow "CLIENT -> API_GATEWAY -> SERVER"
```

### 🕵️ Auto-Discovery (Scan)
Analiza automáticamente la estructura de tu proyecto y genera un diagrama:
```bash
# Analiza la raíz con profundidad 1 (por defecto)
ascii-arch scan .

# Analiza con mayor profundidad
ascii-arch scan . --depth 2
```

### 🚀 Advanced Matrix Flow
Usa `;` para saltos de línea y el flag `--neural` (o `-n`) para usar la IA:
```bash
ascii-arch flow "USER -> LOGIN_API -> AUTH_SERVICE ; IS_LOGGED? -> USER_DB ; ERROR_PAGE" --neural
```

Output Preview:
```text
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
    \       /
      \   /
        v
  +-----------+
  |           |
  | ERROR_PG  |
  |           |
  +-----------+
```
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

