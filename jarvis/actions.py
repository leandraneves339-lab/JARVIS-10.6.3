import platform
import subprocess
import webbrowser

class Actions:
    def open_browser(self, url="https://www.google.com"):
        webbrowser.open(url)
        return "Navegador aberto."

    def open_calculator(self):
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(["calc.exe"])
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", "Calculator"])
            else:
                for cmd in (["gnome-calculator"], ["kcalc"], ["xcalc"]):
                    try:
                        subprocess.Popen(cmd)
                        return "Calculadora aberta."
                    except OSError:
                        continue
                return "Não encontrei uma calculadora gráfica."
            return "Calculadora aberta."
        except Exception:
            return "Não consegui abrir a calculadora."

    def open_app(self, app_name):
        # Lista fechada de aplicativos conhecidos; não executa shell arbitrário.
        aliases = {
            "calculadora": self.open_calculator,
            "navegador": self.open_browser,
        }
        action = aliases.get(app_name.lower())
        return action() if action else "Esse aplicativo ainda não foi cadastrado."
