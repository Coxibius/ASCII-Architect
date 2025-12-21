import os
import re
from pathlib import Path
from typing import List, Set

class ProjectScanner:
    IGNORE_DIRS: Set[str] = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv', 
        'dist', 'build', '.idea', '.vscode', '__pypackages__', 'research'
    }
    
    def __init__(self):
        # Cache para saber qué archivos existen en el proyecto y no alucinar imports externos
        self.project_files: Set[str] = set()

    def _map_project_files(self, root: Path):
        """Indexa todos los nombres de archivo del proyecto (sin extensión)"""
        self.project_files.clear()
        for root_dir, dirs, files in os.walk(root):
            # Filtrar directorios ignorados in-place
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                if file.endswith(".py"):
                    # Guardamos el nombre base (ej: "router" de "router.py")
                    self.project_files.add(Path(file).stem)

    def _find_imports(self, file_path: Path) -> List[str]:
        """Lee el archivo y extrae imports que coincidan con archivos del proyecto."""
        detected_dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Regex mejorada para detectar sub-módulos (ej: from package.module import ...)
            # Grupo 1 captura el módulo base o el path completo previo al import
            import_patterns = [
                r'^from\s+([\w\.]+)\s+import',  # from ascii_architect.router import
                r'^import\s+([\w\.]+)'           # import router
            ]
            
            for line in content.splitlines():
                stripped_line = line.strip()
                for pattern in import_patterns:
                    match = re.search(pattern, stripped_line)
                    if match:
                        full_module_path = match.group(1)
                        # El nombre del archivo suele ser la última parte (ej: router en ascii_architect.router)
                        module_name = full_module_path.split('.')[-1]
                        
                        # Solo agregamos si es un archivo que existe en nuestro proyecto y no es a sí mismo
                        if module_name in self.project_files and module_name != file_path.stem:
                            detected_dependencies.append(module_name)
                            
        except Exception:
            pass # Si falla leer uno, ignoramos
            
        return list(set(detected_dependencies)) # Deduplicar por archivo

    def scan(self, root_path: str, max_depth: int = 2) -> str:
        """
        Analiza la estructura de carpetas y las dependencias de código.
        Prioriza conexiones por IMPORT en archivos Python.
        """
        root = Path(root_path).resolve()
        if not root.exists():
            return "Error -> Path_Not_Found"
        
        # Paso 1: Mapear archivos existentes en el proyecto
        self._map_project_files(root)
        
        connections: List[str] = []
        
        # Paso 2: Recorrer y conectar
        for root_dir, dirs, files in os.walk(root):
            # Control de profundidad
            current_depth = Path(root_dir).relative_to(root).parts
            if len(current_depth) >= max_depth:
                dirs.clear() # Detener recursión
                continue
                
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                full_path = Path(root_dir) / file
                
                # --- LÓGICA DE CONEXIÓN ---
                
                # 1. Archivos Python: Buscamos dependencias reales
                if file.endswith(".py"):
                    deps = self._find_imports(full_path)
                    
                    if deps:
                        # Conexión Real: Archivo -> Dependencia
                        for dep in deps:
                            connections.append(f"{file} -> {dep}.py")
                    else:
                        # Fallback: Si no tiene imports, conectar a su carpeta padre
                        parent_folder = Path(root_dir).name if Path(root_dir) != root else root.name
                        connections.append(f"{parent_folder} [DIR] -> {file}")
                
                # 2. Otros archivos (SQL, MD, TXT): Conexión estática a carpeta
                elif file.endswith((".sql", ".md", ".txt", ".toml")):
                    parent_folder = Path(root_dir).name if Path(root_dir) != root else root.name
                    connections.append(f"{parent_folder} [DIR] -> {file}")

        if not connections:
            return f"Project: {root.name}"

        # Deduplicar y unir con separador
        unique_connections = sorted(list(set(connections)))
        return " ; ".join(unique_connections)

    def get_shape_suggestion(self, filename: str, is_dir: bool = False) -> str:
        """
        Sugerencia semántica para el Router basada en extensiones o nombres clave.
        """
        if is_dir:
            return "SOFTBOX"
        
        u_name = filename.upper()
        if u_name.endswith(('.SQL', '.DB', '.SQLITE')):
            return "CYLINDER"
        
        if any(kw in u_name for kw in ["CONTROLLER", "SERVICE", "MANAGER"]):
            return "BOX"
            
        if any(kw in u_name for kw in ["USER", "CLIENT", "AUTH"]):
            return "SOFTBOX"
            
        return "BOX"
