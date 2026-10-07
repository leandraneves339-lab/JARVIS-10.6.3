import threading

class DesktopVoice:
    def __init__(self, language="pt-BR"):
        self.language = language

    def listen(self, callback, on_error=None):
        def worker():
            try:
                import speech_recognition as sr
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.4)
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                text = r.recognize_google(audio, language=self.language)
                callback(text)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))
        threading.Thread(target=worker, daemon=True).start()
