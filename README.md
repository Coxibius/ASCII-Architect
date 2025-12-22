# 🏛️ ASCII Architect

> **The Neural-Symbolic Diagram Generator for the Terminal.**

```text
    _    ____   ____ ___ ___      _         _     _ _            _   
   / \  / ___| / ___|_ _|_ _|    / \   _ __| |__ (_) |_ ___  ___| |_ 
  / _ \ \___ \| |    | | | |    / _ \ | '__| '_ \| | __/ _ \/ __| __|
 / ___ \ ___) | |___ | | | |   / ___ \| |  | | | | | ||  __/ (__| |_ 
/_/   \_\____/ \____|___|___| /_/   \_\_|  |_| |_|_|\__\___|\___|\__|
                                                       v1.1.0-beta
```
![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)
![alt text](https://img.shields.io/badge/Python-3.9%2B-blue)
![alt text](https://img.shields.io/badge/Architecture-Neural--Symbolic-purple)

ASCII Architect is an engineering-grade tool designed to generate precision ASCII diagrams directly in your CLI. Unlike standard generative art, this tool prioritizes structural integrity, grid alignment, and semantic logic for software documentation.

It uses a Hybrid Architecture:

🧠 Neural Engine (GPT-2): Fine-tuned Small Language Models (SLMs) generate the shapes (Cylinders, Diamonds, Softboxes).

📐 Symbolic Router (Python): A deterministic "Manhattan-style" engine handles grid layout, smart anchoring, and arrow routing.

🎙️ Virtual Architect (Gemini): An AI-powered explainer that analyzes the graph and provides architectural insights using project-specific context.

✨ Key Features

Matrix / Grid Layout: Use ; to define rows and -> for columns.

### 📑 Semantic Cheat Sheet (Keyword-to-Shape)

| Keyword / Context | Shape Type | Visual Meaning |
| :--- | :--- | :--- |
| `DB`, `DATA`, `SQL`, `SQLITE` | **CYLINDER** | Database / Storage |
| `?`, `IF`, `DECISION` | **DIAMOND** | Decision Node (Saturn Effect) |
| `USER`, `CLIENT`, `AUTH`, `[DIR]` | **SOFTBOX** | Human Actor / Entry Point / Folder |
| `PROCESS`, `API`, `DEFAULT` | **BOX** | Standard Operation / Task |

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

3. Extráelo exactamente en: `models/ASCII_Architect_V2_Expansion/`.

### 4. 🔑 Configure Gemini (Optional)
Para usar el **Narrador IA**, crea un archivo `.env` en la raíz del proyecto:
```ini
GOOGLE_API_KEY=tu_api_key_aqui
```
> [!TIP]
> Puedes obtener una llave gratuita en [Google AI Studio](https://aistudio.google.com/apikey).

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

# Analiza con mayor profundidad y especifica el directorio
# (Usa -- para separar el comando del directorio si usas opciones antiguas de Typer)
ascii-arch scan -- src --depth 2

# 📖 REPORTE LOCAL: Genera una explicación textual de las dependencias
ascii-arch scan . --explain

# 🤖 ANÁLISIS IA: Envía la topología a n8n para un análisis humano avanzado
ascii-arch scan . --ai
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

