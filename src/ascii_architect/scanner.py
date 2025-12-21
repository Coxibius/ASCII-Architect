import os
from pathlib import Path
from typing import List, Set

class ProjectScanner:
    IGNORE_DIRS: Set[str] = {
        '.git', 'node_modules', '__pycache__', '.venv', 'venv', 
        'dist', 'build', '.idea', '.vscode', '__pypackages__'
    }
    
    def __init__(self):
        pass

    def scan(self, root_path: str, max_depth: int = 1) -> str:
        """
        Analiza la estructura de carpetas y genera un string de flujo compatible con el Router.
        Ejemplo: "Root -> Folder1 ; Folder1 -> File1 ; Root -> File2"
        """
        root = Path(root_path).resolve()
        if not root.exists():
            return "Error -> Path_Not_Found"
        
        connections: List[str] = []
        self._recursive_scan(root, max_depth, 0, connections)
        
        if not connections:
            return f"{root.name}"
            
        return " ; ".join(connections)

    def _recursive_scan(self, current_path: Path, max_depth: int, current_depth: int, connections: List[str]):
        if current_depth >= max_depth:
            return

        try:
            # Usamos listdir para tener control sobre lo que ignoramos
            for entry_name in sorted(os.listdir(current_path)):
                if entry_name in self.IGNORE_DIRS or entry_name.startswith('.'):
                    continue
                
                entry_path = current_path / entry_name
                
                # Crear la conexión: Parent -> Child
                # Usamos el nombre base para el diagrama
                parent_name = current_path.name if current_path.name else "ROOT"
                child_name = entry_name
                
                # Aplicamos sugerencias semánticas al nombre para ayudar al Router
                # Si es un directorio, le añadimos un tag o simplemente dejamos que el router decida.
                # El usuario sugirió: Directorios -> SOFTBOX
                # El Router actual usa "USER", "START", "END" para SOFTBOX.
                # Podríamos "decorar" el nombre si fuera necesario, pero el usuario dijo: 
                # "el Router infiere por texto, así que dejamos que el Router decida"
                # Sin embargo, para cumplir con los requerimientos específicos de forma, 
                # vamos a asegurarnos de que el Router pueda identificarlos.
                
                if entry_path.is_dir():
                    child_name = f"{entry_name} [DIR]"
                
                connections.append(f"{parent_name} -> {child_name}")
                
                if entry_path.is_dir():
                    self._recursive_scan(entry_path, max_depth, current_depth + 1, connections)
                    
        except PermissionError:
            connections.append(f"{current_path.name} -> ACCESS_DENIED")

    def get_shape_suggestion(self, filename: str, is_dir: bool = False) -> str:
        """
        Retorna el tipo de forma sugerida basado en el nombre del archivo/carpeta.
        Útil si queremos inyectar tipos específicos en el futuro.
        """
        if is_dir:
            return "SOFTBOX"
        
        u_name = filename.upper()
        ext = os.path.splitext(u_name)[1]
        
        if ext in ['.SQL', '.DB', '.SQLITE']:
            return "CYLINDER"
        
        if any(kw in u_name for kw in ["CONTROLLER", "SERVICE", "MANAGER"]):
            return "BOX"
            
        if any(kw in u_name for kw in ["USER", "CLIENT", "AUTH"]):
            return "SOFTBOX"
            
        return "BOX"
