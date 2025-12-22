# 🧠 IA Context: ASCII Architect Project (v1.1 Stable)

> **System Note:** This document is the SOURCE OF TRUTH for the codebase structure. Use this to understand the Hybrid Neuro-Symbolic Architecture and the n8n integration.

---

## 1. Project Identity
**Name:** ASCII Architect  
**Goal:** Engineering-grade ASCII diagram generator & Reverse Engineering tool.  
**Version:** v1.1.0 (Modular CLI & AI Narrator)  
**Package:** `ascii-architect` (Setuptools/Typer)

---

## 2. Architecture Overview

### A. The CLI Layer (`src/ascii_architect/cli.py`)
- **Library:** Typer.
- **Entry Point:** `app()` -> `ascii-arch` command.
- **Commands:**
    - `flow`: Manual diagram generation.
    - `scan`: Automated project analysis.
- **Flags:** Modular flags (`--graph`, `--explain`, `--ai`) allow independent execution of drawing vs. text analysis.

### B. The Orchestrator (`src/ascii_architect/router.py`)
- **Role:** Central Hub. Receives commands from CLI and delegates to engines.
- **Logic:**
    - Parses input strings (`A -> B`).
    - Calculates Grid Layout & Manhattan Routing (Elbow arrows).
    - **Hybrid Decision:** Calls `neural_engine` (experimental) OR `renderers` (deterministic/templates).

### C. The Eyes (`src/ascii_architect/scanner.py`)
- **Role:** Deep dependency analysis.
- **Mechanism:**
    - Recursive directory walk.
    - **Strict Depth Filter:** Prevents connecting to files deeper than the requested `--depth`.
    - **Regex Parsing:** Reads Python files to find `import X` and draws dynamic connections.
- **Semantic Mapping:**
    - `.sql` -> Cylinder
    - `.py` -> Box
    - Directories -> Softbox

### D. The Voice (`src/ascii_architect/narrator.py`)
- **Role:** Generates architectural explanations.
- **Modes:**
    1.  **Local (`--explain`):** Formats the raw graph topology into a readable text list.
    2.  **AI (`--ai`):** Sends the topology to a local **n8n Webhook** (`http://localhost:5678/webhook/explain`).
    - **Why n8n?** Bypasses complex local API setups and quota limits by offloading logic to a visual workflow.

### E. The Hybrid Engine
- **Deterministic:** `renderers.py` (Box, Cylinder, Diamond Saturn Effect).
- **Neural:** `neural_engine.py` (GPT-2 Wrapper, uses `<L01>` tokens).

---

## 3. File Structure (Refactored)

```text
ASCII-Architect/
│
├── pyproject.toml                    # 📦 Build configuration
├── requirements.txt
├── README.md
├── ROADMAP.txt
│
├── research/                         # 🔬 ML Artifacts
│   ├── models/                       # GPT-2 Weights
│   └── datasets/                     # JSONL Training data
│
└── src/                              # 🛠️ Production Code
    └── ascii_architect/
        ├── __init__.py
        ├── cli.py                    # Commands & Flags
        ├── router.py                 # Layout Engine
        ├── scanner.py                # File System Analyzer
        ├── narrator.py               # Text/AI Generation
        ├── renderers.py              # Templates
        ├── neural_engine.py          # AI Wrapper
        ├── canvas.py                 # Drawing Matrix
        └── utils/                    # Shared Helpers
```

---

## 4. Development Rules
1. **Dependency Isolation:** `scanner.py` must NEVER draw. It only returns a string representation of the graph.
2. **CLI Modularity:** Do not couple rendering with analysis. `cli.py` controls the flow:
   ```python
   if graph: router.process()
   if ai: narrator.explain()
   ```
3. **n8n Contract:** The Narrator sends a JSON payload `{"text": "A->B", "prompt": "..."}` to the webhook. It expects a JSON response containing the explanation text.
4. **Path Safety:** All file operations must use `pathlib` relative to `__file__`.