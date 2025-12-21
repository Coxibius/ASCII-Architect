import typer
from typing import Optional
from ascii_architect.router import Router
from ascii_architect.scanner import ProjectScanner

# --- ESTA ES LA VARIABLE CLAVE QUE FALTABA ---
app = typer.Typer(
    name="ascii-arch",
    help="ASCII Architect: The Neural-Symbolic Diagram Generator",
    add_completion=False
)
# ---------------------------------------------

@app.command()
def flow(
    layout: str = typer.Argument(..., help="String de flujo. Ej: 'A -> B ; C -> D'"),
    neural: bool = typer.Option(False, "--neural", "-n", help="[EXPERIMENTAL] Usa el motor GPT-2. Requiere modelos.")
):
    """
    Genera un diagrama a partir de un string de flujo manual.
    """
    try:
        # Inicializar Router con la opción elegida
        router = Router(use_neural_engine=neural)
        router.process(layout)
    except Exception as e:
        typer.secho(f"Error procesando el flujo: {e}", fg=typer.colors.RED)

@app.command()
def scan(
    path: str = typer.Argument(".", help="Ruta del directorio a analizar"),
    depth: int = typer.Option(1, help="Profundidad del análisis (1 = solo raíz, 2 = subcarpetas)")
):
    """
    🕵️ ESCÁNER: Analiza una carpeta y genera un diagrama de su estructura automáticamente.
    """
    scanner = ProjectScanner()
    typer.echo(f"🔍 Escaneando: {path} ...")
    
    flow_string = scanner.scan(path, max_depth=depth)
    
    if "Error" in flow_string:
        typer.secho(flow_string, fg=typer.colors.RED)
        return

    typer.echo(f"Generando diagrama para estructura detectada...")
    
    # Usamos el modo determinista (False) para el escáner por velocidad
    router = Router(use_neural_engine=False) 
    router.process(flow_string)

# Bloque para ejecución directa (python -m ascii_architect.cli)
if __name__ == "__main__":
    app()
