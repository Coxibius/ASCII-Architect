# 🧠 IA Context: ASCII Architect Project (V1.0 - Saturn Release)

> **System Note for AI Agents:**  
> This document is the SINGLE SOURCE OF TRUTH for the "ASCII Architect" codebase structure and capabilities. The project has undergone a major refactor to separate "Product" (CLI/Templates) from "Research" (ML Models).

---

## 1. Project Identity
**Name:** ASCII Architect  
**Goal:** Engineering-grade ASCII diagram generator for the terminal. Hybrid architecture (Deterministic + Neural).  
**Philosophy:** "Engineering over Art". Precision > Style.  
**Version:** v1.0.0 (The Saturn Update)  
**Package Name:** `ascii-architect` (Installable via pip)

---

## 2. Technical Architecture (The Hybrid Core)

### A. The "Product" Side (Deterministic & Fast)
Located in `src/ascii_architect/`. Used by default.

1.  **The Router (`router.py`)** [ORCHESTRATOR]:
    *   **Role:** Brain of the operation. Parses string flow (`A -> B`), calculates grid coordinates (Manhattan routing), and decides which engine to call.
    *   **Logic:**
        *   `process()`: Main entry point. Handles printing and layout calculation.
        *   `_get_node_shape()`: Calls `renderers` by default, or `neural_engine` if requested.
        *   **Saturn Logic:** Detects long diamonds and applies procedural generation.

2.  **The Renderers (`renderers.py`)**:
    *   **Role:** Pure Python string manipulation for instant, perfect shapes.
    *   **Classes:** `BoxRenderer`, `CylinderRenderer`, `SoftBoxRenderer`, `DiamondRenderer` (Saturn logic implemented here).

3.  **The Scanner (`scanner.py`)**:
    *   **Role:** Recursively scans project directories using `pathlib`.
    *   **Logic:** Semantic mapping (Extension -> Shape). `.sql`=Cylinder, `.py`=Box, Directory=SoftBox.

4.  **The CLI (`cli.py`)**:
    *   **Library:** `Typer`.
    *   **Commands:** `flow`, `scan`.
    *   **Entry Point:** `app()` instance connected to `pyproject.toml`.

### B. The "Research" Side (Neural & Experimental)
Located in `research/` (data/weights) and accessed via the engine wrapper.

1.  **The Neural Engine (`neural_engine.py`)**:
    *   **Role:** Wrapper for Fine-tuned GPT-2.
    *   **Mechanism:** Loads models from `research/models/` or `models/`.
    *   **Dynamic Paths:** Uses `Path(__file__).resolve().parent.parent.parent` to find root.
    *   **Search Priority:** Environment Vars > Research Folder > Root models/ Folder.

2.  **The Lab (`research/` folder)**:
    *   **Notebooks:** Training logs.
    *   **Datasets:** JSONL files (`dataset_boxes.jsonl`, etc.).

---

## 3. Critical Logic & Algorithms

### The Saturn Effect (Procedural Diamonds)
**Problem:** Large diamonds look like obelisks when AI tries to scale them.
**Solution:** Fixed height cones (3 lines) + floating body with dynamic width.
**Implementation:** `renderers.py` -> `DiamondRenderer`.

### Auto-Discovery (Semantic Scanning)
**Logic:**
- Ignores `.git`, `node_modules`, `venv`, `__pycache__`.
- `.sql`, `.db`, `.sqlite` -> **CYLINDER**.
- Names with `Service`, `Controller`, `Manager` -> **BOX**.
- Names with `User`, `Client`, `Auth` -> **SOFTBOX**.
- Directories -> **SOFTBOX [DIR]**.
- Others -> **BOX**.

---

## 4. File Structure (v1.0 Package)

```text
ASCII-Architect/
├── pyproject.toml                    # Packaging configuration
├── requirements.txt                  # Dependencies
├── README.md                         # User guide
│
├── research/                         # AI EXPERIMENTS & DATA
│   ├── models/                       # Weights (expert_box, etc.)
│   ├── notebooks/                    # Training Logs
│   └── datasets/                     # JSONL files
│
└── src/                              # SOURCE CODE
    └── ascii_architect/
        ├── cli.py                    # Entry Point
        ├── router.py                 # Core Engine
        ├── renderers.py              # Shape Templates
        ├── neural_engine.py          # AI Bridge
        ├── scanner.py                # Project Analyzer
        ├── canvas.py                 # 2D Grid
        └── utils/                    # Shared Helpers
            └── __init__.py           # Contains inject_text
```

## 5. Development Constraints
- **NO absolute paths**: Use `pathlib`.
- **Imports**: Use absolute package paths (`from ascii_architect.item import ...`).
- **Graceful Fallback**: The system must run without `torch` (Template Mode).
- **Console Output**: `router.process()` must handle the final `print()`.