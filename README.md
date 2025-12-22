# 🏛️ ASCII Architect

> **The Neural-Symbolic Diagram Generator for the Terminal.**
> *Turn your code structure into engineering-grade ASCII diagrams instantly.*

```text
    _    ____   ____ ___ ___      _         _     _ _            _   
   / \  / ___| / ___|_ _|_ _|    / \   _ __| |__ (_) |_ ___  ___| |_ 
  / _ \ \___ \| |    | | | |    / _ \ | '__| '_ \| | __/ _ \/ __| __|
 / ___ \ ___) | |___ | | | |   / ___ \| |  | | | | | ||  __/ (__| |_ 
/_/   \_\____/ \____|___|___| /_/   \_\_|  |_| |_|_|\__\___|\___|\__|
                                                       v1.1.0
```

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Architecture](https://img.shields.io/badge/Architecture-Neural--Symbolic-purple)
![AI](https://img.shields.io/badge/AI-Gemini%20via%20n8n-orange)

ASCII Architect is a CLI tool designed for backend developers and ML engineers who live in the terminal. It solves the "Documentation Rot" problem by reverse-engineering your code into diagrams on the fly.

It features a **Hybrid Neuro-Symbolic Architecture**:
- **Product Mode:** Deterministic rendering for pixel-perfect diagrams.
- **Research Mode:** Experimental GPT-2 Spatial Generation.
- **Narrator Mode:** AI-powered architectural analysis via n8n/Gemini.

## ✨ Key Features

### 🔍 Auto-Discovery Agent (`scan`)
Visualize your folder structure with semantic shape detection:
- `database.sql` → **Cylinder** (Database)
- `auth_service.py` → **Box** (Service)
- `user_model.py` → **Softbox** (Entity/Actor)
- `verify_logic.py` → **Diamond** (Decision/Logic)

### 🤖 "The Narrator" (AI Analysis)
Don't just draw it, explain it. The tool connects to **n8n** (Google Gemini) to analyze the generated graph and explain your system's architecture in natural language.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/Coxibius/ASCII-Architect.git
cd ASCII-Architect
pip install .
```

### 2. Scan your project (The Magic Command)
Analyze your current directory structure.
```bash
ascii-arch scan . --depth 2
```

### 3. Ask the AI (`--ai`)
Generate the diagram AND ask the AI to explain the architecture.
*(Requires local n8n setup).*
```bash
ascii-arch scan src --depth 2 --ai
```

### 4. Manual Design
Draw specific flows for your documentation.
```bash
ascii-arch flow "User -> API_Gateway -> [Service_A, Service_B] ; Service_A -> Redis_Cache"
```

---

## 🏗️ Example Output (Meta-Analysis)

Asking ASCII Architect to analyze its own source code:

**Command:** `ascii-arch scan src --ai`

**Diagram:**
```text
.-------------------.          +----------+
|  ascii_architect  |--------->|  cli.py  |
|       [DIR]       |          +----------+
'-------------------'                |
          |                          v
          |                    +-----------+
          +------------------->| router.py |
                               +-----------+
                                     |
                     +---------------+----------------+
                     |               |                |
               .-----v-----.   +-----v-----.   +------v-------+
               | neural_eng|   | renderers |   | narrator.py  |
               '-----------'   +-----------+   +--------------+
```

**AI Analysis (Gemini):**
> "This architecture follows a clear Command Dispatcher pattern. The `cli.py` acts as the interface layer, delegating execution to the `router.py`, which serves as the central orchestrator. The router creates a strong decoupling between the Logic Layer (Neural Engine/Renderers) and the Presentation Layer. The presence of `narrator.py` suggests a focus on user experience and explainability."

---

## 📄 License
MIT License. Created by Coxibius.

**Engineering over Art.**

