import os
import re
from pathlib import Path

class ProjectScanner:
    IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.idea', '.vscode', 'research', 'ascii_architect.egg-info'}
    
    def __init__(self):
        # Lista blanca estricta: Solo archivos permitidos por el depth
        self.allowed_files = set() 

    def _find_imports(self, file_path: Path) -> list[str]:
        """Busca imports SOLO hacia archivos que están en la lista blanca."""
        detected = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Regex para imports
            patterns = [r'^from\s+(\w+)\s+import', r'^import\s+(\w+)']
            
            for line in content.splitlines():
                for pat in patterns:
                    match = re.search(pat, line.strip())
                    if match:
                        module = match.group(1)
                        # LA REGLA DE ORO:
                        # Solo existe conexión si el destino TAMBIÉN pasó el filtro de profundidad
                        if module in self.allowed_files and module != file_path.stem:
                            detected.append(module)
        except:
            pass
        return detected

    def scan(self, root_path: str, max_depth: int = 1) -> str:
        root = Path(root_path).resolve()
        if not root.exists(): return "Error -> Path_Not_Found"
        
        self.allowed_files.clear()
        connections = []

        # --- FASE 1: RECOLECCIÓN (Crear Lista Blanca) ---
        # Solo lo que entra aquí puede ser dibujado o conectado.
        for root_dir, dirs, files in os.walk(root):
            # Calcular profundidad actual
            rel_path = Path(root_dir).relative_to(root)
            depth_level = len(rel_path.parts)
            if str(rel_path) == ".": depth_level = 0

            # CORTE RADICAL: Si superamos profundidad, vaciamos dirs y continuamos
            if depth_level >= max_depth:
                del dirs[:] 
                continue
            
            # Limpiar carpetas ignoradas
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            
            for f in files:
                if f.endswith(".py"):
                    # Registramos "router" (sin .py) como permitido
                    self.allowed_files.add(f.replace(".py", ""))

        # --- FASE 2: CONEXIÓN (Usar Lista Blanca) ---
        for root_dir, dirs, files in os.walk(root):
            rel_path = Path(root_dir).relative_to(root)
            depth_level = len(rel_path.parts)
            if str(rel_path) == ".": depth_level = 0

            if depth_level >= max_depth:
                del dirs[:]
                continue
            
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            folder_name = Path(root_dir).name
            if str(rel_path) == ".": folder_name = "ROOT"

            for file in files:
                if file.endswith(".py"):
                    full_path = Path(root_dir) / file
                    deps = self._find_imports(full_path)
                    
                    if deps:
                        for dep in deps:
                            # Aquí se aplica el filtro de la fase 1
                            connections.append(f"{file} -> {dep}.py")
                    else:
                        connections.append(f"{folder_name} [DIR] -> {file}")
                
                elif file.endswith((".sql", ".md", ".txt")):
                    connections.append(f"{folder_name} [DIR] -> {file}")

        if not connections: return ""
        return " ; ".join(sorted(list(set(connections))))