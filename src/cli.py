import typer
import sys
import os
from typing import Optional

# --- CONFIGURACIÓN DE RUTAS ---
# Aseguramos que Python encuentre 'engine.py' y 'canvas.py' en la misma carpeta
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importamos las clases del Core
# Importamos las clases del Core
try:
    from engine import ArchitectEngine
    from ascii_architect.canvas import Canvas
    from router import AutoRouter
    from utils import inject_text
except ImportError:
    # Fallback debug
    print("⚠️ Error de importación. Verificando paths...")
    from src.engine import ArchitectEngine
    from src.ascii_architect.canvas import Canvas
    from src.router import AutoRouter
    from src.utils import inject_text

# --- INICIALIZACIÓN APP ---
app = typer.Typer(
    name="ASCII Architect CLI",
    help="Generador de diagramas de arquitectura en terminal (V18 Hybrid Engine)",
    add_completion=False
)

# Instancia global del cerebro (Lazy loading podría ser mejor, pero esto es más simple)
# Lo inicializamos dentro de los comandos para no cargar torch si solo piden --help
brain = None

def get_brain():
    global brain
    if brain is None:
        typer.echo("🧠 Cargando Motor Neuronal (GPT-2)... espera un momento...")
        brain = ArchitectEngine()
    return brain

# --- UTILS DE MAQUILLAJE ---
# inject_text importado de utils.py


# --- COMANDOS ---

@app.command()
def box(
    text: str = typer.Option(..., "--text", "-t", help="Texto dentro de la caja (ej: Database)"),
    size: str = typer.Option("12x5", "--size", "-s", help="Dimensiones WxH (ej: 14x5)"),
    style: str = typer.Option("SOLID", "--style", help="Estilo visual: SOLID, VINTAGE, ROUND")
):
    """
    Genera una CAJA rectangular perfecta usando IA.
    """
    engine = get_brain()
    
    typer.echo(f"📦 Generando caja '{size}' estilo '{style}'...")
    
    # 1. Generar prompt
    # tags = [STYLE:SOLID]
    tags = f"[STYLE:{style.upper()}]"
    metadata = f"[DIM:{size}]"
    
    # 2. Inferencia
    raw_art = engine.generate("BOX", tags, metadata)
    
    # 3. Post-proceso
    final_art = inject_text(raw_art, text.upper())
    
    # 4. Render
    typer.secho("\n" + final_art, fg=typer.colors.CYAN)
    typer.echo("") # Newline

@app.command()
def arrow(
    direction: str = typer.Option("RIGHT", "--dir", "-d", help="Dirección: RIGHT, LEFT, UP, DOWN"),
    length: int = typer.Option(6, "--len", "-l", help="Longitud de la flecha en caracteres"),
):
    """
    Genera una FLECHA conectora.
    """
    engine = get_brain()
    
    typer.echo(f"➡️ Generando flecha hacia {direction} (Len: {length})...")
    
    # 1. Inferencia
    tags = f"[DIR:{direction.upper()}]"
    metadata = f"[LEN:{length}]"
    
    raw_art = engine.generate("ARROW", tags, metadata)
    
    # 2. Render
    typer.secho("\n" + raw_art, fg=typer.colors.GREEN)
    typer.echo("")

@app.command()
def flow(
    nodes: str = typer.Argument(..., help="Flujo de nodos separados por '->' (ej: 'USER -> API -> DB')")
):
    """
    Genera un DIAGRAMA DE FLUJO completo automáticamente.
    """
    typer.echo(f"🔄 Trazando flujo: {nodes}...")
    
    # Instanciamos el router
    # Nota: El router crea su propio Canvas y Engine internamente
    router = AutoRouter()
    
    # Generar
    try:
        diagram = router.draw_flow(nodes)
        
        # Render
        typer.secho("\n" + diagram.replace("░", " "), fg=typer.colors.YELLOW)
        typer.echo("")
        
    except Exception as e:
        typer.secho(f"❌ Error trazando flujo: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
