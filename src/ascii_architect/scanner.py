import os
import re
from pathlib import Path

class ProjectScanner:
    # Carpetas basura a ignorar
    IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.idea', '.vscode', 'research', 'ascii_architect.egg-info'}
    
    def __init__(self):
        self.project_files = set()

    def _map_project_files(self, root: Path):
        """Indexa todos los nombres de archivo del proyecto para saber qué es interno."""
        for root_dir, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            for file in files:
                if file.endswith(".py"):
                    self.project_files.add(file.replace(".py", ""))

    def _find_imports(self, file_path: Path) -> list[str]:
        """Busca 'import X' o 'from X import Y' dentro del archivo."""
        detected_dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Regex simple para detectar imports
            import_patterns = [
                r'^from\s+(\w+)\s+import',  # from router import ...
                r'^import\s+(\w+)'          # import router
            ]
            
            for line in content.splitlines():
                for pattern in import_patterns:
                    match = re.search(pattern, line.strip())
                    if match:
                        module_name = match.group(1)
                        # Solo agregamos si el modulo existe en nuestro proyecto (no librerias externas)
                        if module_name in self.project_files and module_name != file_path.stem:
                            detected_dependencies.append(module_name)
        except Exception:
            pass
        return detected_dependencies

    def scan(self, root_path: str, max_depth: int = 2) -> str:
        root = Path(root_path)
        if not root.exists():
            return "Error -> Path_Not_Found"
        
        self._map_project_files(root)
        connections = []
        
        # Recorremos el árbol
        for root_dir, dirs, files in os.walk(root):
            # Control de profundidad
            current_depth = str(root_dir).count(os.sep) - str(root).count(os.sep)
            if current_depth >= max_depth:
                del dirs[:]
                continue
                
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            
            folder_name = Path(root_dir).name
            if folder_name == ".": folder_name = "ROOT"

            for file in files:
                # 1. Archivos Python: Buscamos imports reales
                if file.endswith(".py"):
                    full_path = Path(root_dir) / file
                    deps = self._find_imports(full_path)
                    
                    if deps:
                        # Si tiene dependencias, dibujamos la relación lógica
                        for dep in deps:
                            connections.append(f"{file} -> {dep}.py")
                    else:
                        # Si no, lo conectamos a su carpeta padre
                        connections.append(f"{folder_name} [DIR] -> {file}")
                
                # 2. Otros archivos importantes (SQL, DB, Markdown)
                elif file.endswith((".sql", ".db", ".md", ".txt")):
                    connections.append(f"{folder_name} [DIR] -> {file}")

        if not connections:
            return ""

        # Limpiar y ordenar
        return " ; ".join(sorted(list(set(connections))))