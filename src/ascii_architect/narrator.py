import requests
import json

class Narrator:
    def __init__(self):
        # URL de PRODUCCIÓN (sin -test)
        self.webhook_url = "http://localhost:5678/webhook/explain"

    def explain(self, topology_text: str, use_ai: bool = False) -> str:
        if not topology_text: return "Nada que explicar."

        # MODO LOCAL (TEXTO PLANO)
        if not use_ai:
            lines = topology_text.split(" ; ")
            report = []
            for l in lines:
                if "->" in l:
                    a, b = l.split("->")
                    if "[DIR]" in a: report.append(f"📂 Carpeta '{a.replace('[DIR]','').strip()}' contiene '{b.strip()}'")
                    elif ".py" in b: report.append(f"🐍 '{a.strip()}' importa/llama a '{b.strip()}'")
                    else: report.append(f"🔗 '{a.strip()}' conecta con '{b.strip()}'")
            return "\n".join(report)

        # MODO IA (N8N)
        payload = {
            "text": topology_text,
            "prompt": "Eres un Arquitecto. Explica esta estructura."
        }
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=40)
            if resp.status_code == 200:
                try: 
                    d = resp.json()
                    # Intenta sacar el texto limpio
                    return d.get('text', d.get('output', str(d)))
                except: return resp.text
            return f"Error n8n: {resp.status_code}"
        except Exception as e:
            return f"Error conexión: {e}"