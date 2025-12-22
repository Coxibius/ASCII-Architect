import typer
import sys
from typing import Optional
from ascii_architect.router import Router
from ascii_architect.scanner import ProjectScanner
from ascii_architect.narrator import Narrator

app = typer.Typer(
    name="ascii-arch",
    help="ASCII Architect: The Neural-Symbolic Diagram Generator",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]}
)

@app.command()
def flow(
    layout: str = typer.Argument(..., help="String de flujo manual."),
    neural: bool = typer.Option(False, "--neural", "-n", help="Usa motor neuronal.")
):
    """Genera un diagrama manual."""
    try:
        router = Router(use_neural_engine=neural)
        router.process(layout)
    except Exception as e:
        typer.secho(f"❌ Error: {e}", fg=typer.colors.RED)

@app.command()
def scan(
    path: str = typer.Argument(".", help="Ruta a analizar"),
    depth: int = typer.Option(1, "--depth", "-d", help="Nivel de profundidad (1=Solo Raíz, 2=Subcarpetas)."),
    graph: bool = typer.Option(False, "--graph", "-g", help="Forzar el dibujo del diagrama ASCII."),
    explain: bool = typer.Option(False, "--explain", "-e", help="Mostrar reporte de texto local."),
    ai: bool = typer.Option(False, "--ai", help="Consultar análisis a IA (n8n).")
):
    """
    🕵️ ESCÁNER: Analiza código.
    Comportamiento:
    - Si no usas banderas, dibuja el diagrama por defecto.
    - Si usas --explain o --ai, NO dibuja el diagrama (a menos que añadas --graph).
    """
    # 1. Escaneo
    scanner = ProjectScanner()
    flow_string = scanner.scan(path, max_depth=depth)
    
    if not flow_string:
        typer.secho("❌ No se encontraron archivos.", fg=typer.colors.RED)
        return

    # LÓGICA DE VISUALIZACIÓN INTELIGENTE
    # Si no pidió explicaciones ni IA, asumimos que quiere ver el dibujo (comportamiento default)
    show_diagram = graph or (not explain and not ai)

    # 2. Dibujo
    if show_diagram:
        typer.secho(f"🔍 Escaneando '{path}' (Depth: {depth})...", fg=typer.colors.YELLOW)
        router = Router(use_neural_engine=False) 
        router.process(flow_string)

    # 3. Reportes
    if explain or ai:
        narrator = Narrator()
        
        if explain:
            typer.secho("\n📄 REPORTE LOCAL:", fg=typer.colors.CYAN, bold=True)
            print(narrator.explain(flow_string, use_ai=False))
            
        if ai:
            typer.secho("\n🤖 ANÁLISIS IA (n8n):", fg=typer.colors.MAGENTA, bold=True)
            print(narrator.explain(flow_string, use_ai=True))

if __name__ == "__main__":
    app()
