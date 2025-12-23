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
    try:
        router = Router(use_neural_engine=neural)
        router.process(layout)
    except Exception as e:
        typer.secho(f"❌ Error: {e}", fg=typer.colors.RED)

@app.command()
def scan(
    path: str = typer.Argument(".", help="Ruta a analizar"),
    depth: int = typer.Option(1, "--depth", "-d", help="Profundidad de escaneo."),
    graph: bool = typer.Option(True, "--graph/--no-graph", help="Mostrar dibujo ASCII."),
    explain: bool = typer.Option(False, "--explain", "-e", help="Reporte de texto local."),
    ai: bool = typer.Option(False, "--ai", help="Análisis IA PRO (Estructura + Documentación).")
):
    """
    🕵️ ESCÁNER CONTEXTUAL: Analiza código y documentación.
    """
    scanner = ProjectScanner()
    
    if graph:
        typer.secho(f"🔍 Escaneando '{path}' (Depth: {depth})...", fg=typer.colors.YELLOW)
    
    flow_string = scanner.scan(path, max_depth=depth)
    
    if not flow_string:
        typer.secho("❌ No se encontraron archivos.", fg=typer.colors.RED)
        return

    # 1. DIBUJO
    if graph:
        router = Router(use_neural_engine=False) 
        router.process(flow_string)

    narrator = Narrator()

    # 2. EXPLICACIÓN LOCAL (Solo topología)
    if explain:
        typer.secho("\n📄 REPORTE ESTRUCTURAL:", fg=typer.colors.CYAN, bold=True)
        print(narrator.explain(flow_string, use_ai=False))

    # 3. INTELIGENCIA ARTIFICIAL (Contexto Completo)
    if ai:
        typer.secho("\n🤖 RECOPILANDO CONTEXTO PARA IA...", fg=typer.colors.MAGENTA)
        
        # A. Generamos el reporte de texto estructurado (más útil que el grafo crudo)
        text_report = narrator.explain(flow_string, use_ai=False)
        
        # B. Leemos README, ROADMAP, etc.
        docs_content = scanner.get_docs_content(path)
        
        # C. Preparamos el Mega-Prompt OPTIMIZADO (Texto procesado + Docs)
        full_context_payload = (
            f"ANÁLISIS ESTRUCTURAL DEL PROYECTO:\n{text_report}\n\n"
            f"DOCUMENTACIÓN ENCONTRADA:\n{docs_content}"
        )
        
        typer.secho("🚀 ENVIANDO A n8n (GEMINI)...", fg=typer.colors.MAGENTA, bold=True)
        print(narrator.explain(full_context_payload, use_ai=True))

if __name__ == "__main__":
    app()
