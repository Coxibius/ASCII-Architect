import requests
import json

class Narrator:
    def __init__(self):
        # Tu URL de n8n
        self.webhook_url = "http://localhost:5678/webhook/explain"
        self.is_ready = True

    def explain(self, topology_text: str, use_ai: bool = False) -> str:
        if not topology_text or topology_text.strip() == "":
            return "❌ No hay diagrama para explicar."

        if use_ai:
            print(f"📡 Conectando con n8n ({self.webhook_url})...")
            payload = {
                "text": topology_text,
                "prompt": "Eres un Arquitecto Senior. Analiza esta topología y dame un resumen técnico corto y humano."
            }
            try:
                resp = requests.post(self.webhook_url, json=payload, timeout=45)
                
                if resp.status_code == 200:
                    try:
                        # Intenta parsear como JSON
                        d = resp.json()
                        
                        # CASO 1: Si n8n devolvió la respuesta cruda de Gemini (Lista)
                        if isinstance(d, list) and len(d) > 0:
                            # Navegamos la estructura fea de Google: [0]['content']['parts'][0]['text']
                            try:
                                return d[0]['content']['parts'][0]['text']
                            except (KeyError, IndexError):
                                pass # Si falla, seguimos intentando otras formas

                        # CASO 2: Si n8n devolvió un objeto bonito (Diccionario)
                        if isinstance(d, dict):
                            # Busca campos comunes de respuesta
                            return d.get('output', d.get('text', d.get('response', str(d))))
                        
                        # CASO 3: Si es otra cosa, devolver como texto
                        return str(d)

                    except json.JSONDecodeError:
                        # Si no es JSON, es texto plano (lo que queremos)
                        return resp.text
                
                return f"❌ Error n8n: {resp.status_code} - {resp.text}"
            except Exception as e:
                return f"❌ Falló conexión n8n: {e}"

        # --- MODO LOCAL (Igual que antes) ---
        relationships = topology_text.split(" ; ")
        report = []
        report.append("══════════════════════════════════════════════════")
        report.append("  📖 EXPLICACIÓN DEL GRAFO (MODO TEXTO)")
        report.append("══════════════════════════════════════════════════")
        report.append("")
        for rel in relationships:
            if "->" in rel:
                report.append(f"  🔗 {rel}")
        
        report.append("")
        report.append("══════════════════════════════════════════════════")
        return "\n".join(report)