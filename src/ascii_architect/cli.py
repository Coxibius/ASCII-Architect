import typer
import sys
from typing import Optional
from ascii_architect.router import Router
from ascii_architect.scanner import ProjectScanner
from ascii_architect.narrator import Narrator

# Definición de la App
app = typer.Typer(
    name="ascii-arch",
    help="ASCII Architect: The Neural-Symbolic Diagram Generator",
    add_completion=False,
    # Esto permite mezclar argumentos y opciones sin que explote
    context_settings={"help_option_names": ["-h", "--help"]}
)

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
        typer.secho(f"❌ Error procesando el flujo: {e}", fg=typer.colors.RED)

@app.command()
def scan(
    path: str = typer.Argument(".", help="Ruta del directorio a analizar"),
    depth: int = typer.Option(2, "--depth", "-d", help="Profundidad del análisis (1 = solo raíz, 2 = subcarpetas)"),
    explain: bool = typer.Option(False, "--explain", "-e", help="Genera un reporte estructural local detallado."),
    ai: bool = typer.Option(False, "--ai", help="Analiza la arquitectura usando IA (vía n8n/Gemini).")
):
    """
    🕵️ ESCÁNER: Analiza una carpeta y genera un diagrama de su estructura automáticamente.
    """
    # 1. Escaneo
    scanner = ProjectScanner()
    typer.secho(f"🔍 Escaneando: {path} (Profundidad: {depth})...", fg=typer.colors.YELLOW)
    
    flow_string = scanner.scan(path, max_depth=depth)
    
    if "Error" in flow_string:
        typer.secho(f"❌ {flow_string}", fg=typer.colors.RED)
        return

    if not flow_string or flow_string.strip() == "":
        typer.secho("⚠️ No se encontraron archivos para diagramar.", fg=typer.colors.YELLOW)
        return

    # 2. Dibujo (Render)
    typer.echo(f"Generando diagrama...")
    router = Router(use_neural_engine=False) 
    router.process(flow_string)

    # 3. Explicación (Narrador)
    if explain or ai:
        msg = "🤖 Invocando al Narrador (Conectando a n8n)..." if ai else "📖 Generando reporte estructural local..."
        typer.secho(f"\n{msg}", fg=typer.colors.MAGENTA)
        
        narrator = Narrator()
        # Pasamos el flag 'ai' al narrador
        explanation = narrator.explain(flow_string, use_ai=ai)
        
        header = "ANÁLISIS IA (n8n)" if ai else "REPORTE ESTÁTICO"
        typer.secho("\n" + "="*60, fg=typer.colors.CYAN)
        typer.secho(f"  🎙️  {header}", fg=typer.colors.CYAN, bold=True)
        typer.secho("="*60 + "\n", fg=typer.colors.CYAN)
        
        typer.echo(explanation)
        typer.echo("\n")

# Bloque para ejecución directa (python -m ascii_architect.cli)
if __name__ == "__main__":
    app()