import requests

class Narrator:
    def __init__(self):
        # URL de n8n (Asegúrate que el workflow esté ACTIVO)
        self.webhook_url = "http://localhost:5678/webhook/explain"
        self.is_ready = True

    def explain(self, topology_text: str, use_ai: bool = False) -> str:
        """
        Si use_ai=True -> Manda a n8n.
        Si use_ai=False -> Genera reporte de texto local.
        """
        if not topology_text or topology_text.strip() == "":
            return "❌ No hay diagrama para explicar."

        if use_ai:
            print(f"📡 Conectando con n8n ({self.webhook_url})...")
            payload = {
                "text": topology_text,
                "prompt": "Eres un Arquitecto Senior. Analiza esta topología y dame un resumen técnico corto y humano."
            }
            try:
                resp = requests.post(self.webhook_url, json=payload, timeout=30)
                if resp.status_code == 200:
                    try:
                        d = resp.json()
                        return d.get('output', d.get('text', str(d)))
                    except:
                        return resp.text
                return f"❌ Error n8n: {resp.status_code}"
            except Exception as e:
                return f"❌ Falló conexión n8n: {e}"

        # MODO LOCAL (Solo texto) - Lo que sigue es la lógica actual

        # Analizar el texto crudo (A -> B ; C -> D)
        relationships = topology_text.split(" ; ")
        
        # Generar reporte estilizado
        report = []
        report.append("══════════════════════════════════════════════════")
        report.append("  📖 EXPLICACIÓN DEL GRAFO (MODO TEXTO)")
        report.append("══════════════════════════════════════════════════")
        report.append("")
        report.append("Relaciones detectadas:")
        report.append("")
        
        # Categorizar relaciones para que se vea profesional
        files_count = 0
        dirs_count = 0
        
        for rel in relationships:
            if "->" in rel:
                source, target = rel.split("->")
                source = source.strip()
                target = target.strip()
                
                # Traducir a lenguaje natural
                if "[DIR]" in source:
                    clean_source = source.replace("[DIR]", "").strip()
                    report.append(f"  📁 El directorio {clean_source} contiene {target}")
                    dirs_count += 1
                elif ".py" in source and ".py" in target:
                    report.append(f"  🐍 {source} importa a {target}")
                    files_count += 1
                else:
                    report.append(f"  🔗 {source} conecta con {target}")
        
        # Estadísticas simples
        report.append("")
        report.append("Resumen:")
        report.append(f"  📦 Nodos totales: {len(relationships)}")
        report.append(f"  🔗 Conexiones: {len(relationships)}")
        report.append(f"  📊 Filas de layout: {len(relationships)}") # En matriz simple es 1:1 aprox
        report.append("")
        report.append("══════════════════════════════════════════════════")
        
        return "\n".join(report)