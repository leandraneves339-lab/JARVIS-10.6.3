import threading
import sys


class Voice:
    """Unified voice I/O: native Android TTS/recognizer or desktop backends."""

    def __init__(self):
        self._tts = None
        self._android_tts = None
        self._tts_available = False
        self._tts_error = None
        self._is_android = self._detect_android()

        if self._is_android:
            try:
                from .android_tts import AndroidTTS
                self._android_tts = AndroidTTS(language="pt-BR", rate=0.95, pitch=1.0)
                self._tts_available = self._android_tts.available
                self._tts_error = self._android_tts.error
            except Exception as exc:
                self._tts_error = str(exc)
        else:
            try:
                import pyttsx3
                self._tts = pyttsx3.init()
                self._tts.setProperty("rate", 175)
                self._tts_available = True
            except Exception as exc:
                self._tts_error = str(exc)

    @staticmethod
    def _detect_android():
        try:
            from kivy.utils import platform
            if platform == "android":
                return True
        except Exception:
            pass
        return sys.platform == "android"

    @property
    def tts_available(self):
        if self._android_tts is not None:
            return self._android_tts.available
        return self._tts_available and self._tts is not None

    @property
    def tts_error(self):
        if self._android_tts is not None:
            return self._android_tts.error
        return self._tts_error

    def speak(self, text, on_start=None, on_end=None, on_error=None):
        def run():
            try:
                if on_start:
                    on_start()

                ok = False
                if self._android_tts is not None:
                    ok = self._android_tts.speak(text)
                elif self._tts:
                    self._tts.say(text)
                    self._tts.runAndWait()
                    ok = True

                if not ok and on_error:
                    on_error(self.tts_error or "Text-to-Speech indisponível")
            except Exception as exc:
                if on_error:
                    on_error(str(exc))
            finally:
                if on_end:
                    on_end()

        threading.Thread(target=run, daemon=True).start()

    def listen(self, callback, on_error=None):
        if self._is_android:
            try:
                from .android_voice import AndroidVoice
                self._android_voice = getattr(self, "_android_voice", None) or AndroidVoice()
                return self._android_voice.listen(callback, on_error)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))
                return False

        try:
            from .desktop_voice import DesktopVoice
            DesktopVoice().listen(callback, on_error)
            return True
        except Exception as exc:
            if on_error:
                on_error(str(exc))
            return False

    def shutdown(self):
        if self._android_tts:
            self._android_tts.shutdown()
