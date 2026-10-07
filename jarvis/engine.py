import datetime as dt
import platform
import psutil
from .actions import Actions
from .memory import Memory
from .ai import AIClient

class JarvisEngine:
    def __init__(self, name="JARVIS 10.6.2", api_url="", api_key=""):
        self.name = name
        self.actions = Actions()
        self.memory = Memory()
        self.ai = AIClient(api_url, api_key)
        self.god_eye_active = False

    def status(self):
        cpu = psutil.cpu_percent(interval=0.12)
        ram = psutil.virtual_memory().percent
        return f"Sistema online. CPU {cpu:.0f} por cento. Memória {ram:.0f} por cento."

    def self_analysis(self):
        """Diagnóstico seguro do próprio aplicativo; não executa ações externas."""
        checks = []
        try:
            psutil.cpu_percent(interval=0.05)
            checks.append("núcleo OK")
        except Exception:
            checks.append("núcleo com atenção")
        try:
            _ = self.memory.recent(limit=1)
            checks.append("memória OK")
        except Exception:
            checks.append("memória com atenção")
        checks.append("voz disponível para resposta" )
        checks.append("GOD EYE " + ("ativo" if self.god_eye_active else "em espera"))
        checks.append("IA " + ("configurada" if self.ai.enabled() else "local"))
        checks.append(f"plataforma {platform.system()}")

        return (
            "Iniciando autoanálise completa. "
            + ". ".join(checks) + ". "
            "Protocolo Mundo: somente simulação e análise; controle autônomo de pessoas ou sistemas está desabilitado. "
            "Conclusão: núcleo operacional, com componentes externos dependentes das permissões e configurações do dispositivo."
        )

    def execute(self, text: str) -> str:
        t = (text or "").strip().lower()
        if not t:
            return "Estou ouvindo."

        if t in {"desligar", "desligar jarvis", "sair"}:
            return "__EXIT__"

        # Comando de voz solicitado pelo usuário.
        analysis_phrases = (
            "faça sua autoanálise", "faca sua autoanalise",
            "faça uma autoanálise", "faca uma autoanalise",
            "faça autoanálise", "faca autoanalise",
            "autoanálise", "autoanalise", "autodiagnóstico", "autodiagnostico"
        )
        if any(p in t for p in analysis_phrases):
            return self.self_analysis()

        if "hora" in t:
            return "Agora são " + dt.datetime.now().strftime("%H:%M") + "."
        if "data" in t or "dia de hoje" in t:
            return "Hoje é " + dt.datetime.now().strftime("%d/%m/%Y") + "."
        if "status" in t or "sistema" in t:
            return self.status()
        if "quem é você" in t or "quem e voce" in t:
            return "Eu sou o JARVIS 10.6.2, seu assistente pessoal."
        if "abrir navegador" in t or "abrir internet" in t:
            return self.actions.open_browser()
        if "abrir calculadora" in t or t == "calculadora":
            return self.actions.open_calculator()

        if t.startswith("lembre "):
            note = text[7:].strip()
            self.memory.remember(note)
            return "Certo. Salvei essa informação."
        if "o que você lembra" in t or "o que voce lembra" in t:
            notes = self.memory.recent()
            return "Eu lembro: " + " | ".join(notes) if notes else "Ainda não tenho anotações."

        if self.ai.enabled():
            reply = self.ai.ask(text)
            if reply:
                return reply

        return f"Entendi: {text}. Ainda não tenho uma ação local para esse comando."
