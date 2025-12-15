import sys
import os

# Configuración de imports para que encuentre los módulos hermanos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path: sys.path.append(current_dir)

try:
    from engine import ArchitectEngine
    from ascii_architect.canvas import Canvas
    from utils import inject_text
except ImportError:
    from src.engine import ArchitectEngine
    from src.ascii_architect.canvas import Canvas
    from src.utils import inject_text

class AutoRouter:
    def __init__(self):
        self.brain = ArchitectEngine()
        # Canvas más ancho para que quepa el flujo
        self.paper = Canvas(width=120, height=20) 
        
        # Cursor X, Y (Dónde va el siguiente elemento)
        self.cursor_x = 2
        self.cursor_y = 5 # Altura fija por ahora (centrado vertical)

    def draw_flow(self, flow_string):
        """
        Recibe: "REDIS -> API -> CLIENT"
        Dibuja: [REDIS]---->[API]---->[CLIENT]
        """
        print(f"🔄 Procesando flujo: {flow_string}")
        
        # 1. Separar los nodos
        nodes = [n.strip() for n in flow_string.split("->")]
        
        for i, node_text in enumerate(nodes):
            # --- PASO A: DIBUJAR CAJA ---
            print(f"   Generating node: {node_text}...")
            
            # Calculamos tamaño dinámico según texto (aprox)
            # Minimo 10, o largo del texto + padding
            width = max(12, len(node_text) + 4)
            dims = f"[DIM:{width}x5]"
            
            raw_box = self.brain.generate("BOX", "[STYLE:SOLID]", dims)
            final_box = inject_text(raw_box, node_text)
            
            # Estampar caja en cursor actual
            self.paper.stamp(self.cursor_x, self.cursor_y, final_box)
            
            # Actualizar cursor X para lo que sigue
            # Sumamos el ancho de la caja (width)
            self.cursor_x += width 
            
            # --- PASO B: DIBUJAR FLECHA (Si no es el último nodo) ---
            if i < len(nodes) - 1:
                print(f"   Connecting...")
                # Generar flecha estándar
                # Ajustamos un poco la posición para que salga del borde
                arrow_len = 6
                raw_arrow = self.brain.generate("ARROW", "[DIR:RIGHT]", f"[LEN:{arrow_len}]")
                
                # La flecha se estampa donde terminó la caja anterior (con un pequeño ajuste visual)
                # Ajuste: -1 para que se solape con el borde y parezca conectado
                arrow_x = self.cursor_x - 1 
                # Ajuste Y: +2 para centrar en caja de altura 5 (0,1,2,3,4 -> 2 es centro)
                arrow_y = self.cursor_y + 2 
                
                self.paper.stamp(arrow_x, arrow_y, raw_arrow)
                
                # Mover cursor al final de la flecha para la siguiente caja
                # Ajuste: -1 (antes -2) para que la punta de la flecha (>) no sea borrada por la siguiente caja
                self.cursor_x += (arrow_len - 1)

        return self.paper.render()

# ... (Todo tu código de clase AutoRouter arriba igual) ...

if __name__ == "__main__":
    router = AutoRouter()
    
    print("\n🏗️ INICIANDO PRUEBAS DE ESTRÉS DEL ROUTER V18...")

    # ESCENARIO 1: El Clásico Web (Validar flujo estándar)
    # Objetivo: Ver si conecta 4 nodos sin salirse del canvas.
    flow1 = "USER -> CLOUDFLARE -> NGINX -> GUNICORN -> DJANGO"
    print(f"\n[TEST 1: Web Stack Standard]\nPrompt: '{flow1}'")
    print("-" * 60)
    print(router.draw_flow(flow1).replace("░", " "))

    # ESCENARIO 2: Data Pipeline (Validar Cajas Anchas)
    # Objetivo: Ver si el padding del texto funciona con nombres largos.
    flow2 = "RAW_DATA_LAKE -> APACHE_SPARK_PROCESSOR -> DATA_WAREHOUSE"
    print(f"\n[TEST 2: Big Data Pipeline]\nPrompt: '{flow2}'")
    print("-" * 60)
    print(router.draw_flow(flow2).replace("░", " "))

    # ESCENARIO 3: Microservicios (Validar Cajas Cortas)
    # Objetivo: Ver si las cajas pequeñas (AUTH, S3) mantienen su forma.
    flow3 = "APP -> AUTH -> S3 -> LOGS"
    print(f"\n[TEST 3: AWS Microservices]\nPrompt: '{flow3}'")
    print("-" * 60)
    print(router.draw_flow(flow3).replace("░", " "))

    # ESCENARIO 4: El DevOps (Validar caracteres especiales si los hubiera)
    flow4 = "GIT_COMMIT -> GITHUB_ACTIONS -> DOCKER_BUILD -> KUBERNETES"
    print(f"\n[TEST 4: CI/CD Pipeline]\nPrompt: '{flow4}'")
    print("-" * 60)
    print(router.draw_flow(flow4).replace("░", " "))
    
    print("\n✅ PRUEBAS FINALIZADAS.")