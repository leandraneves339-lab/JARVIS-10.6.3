"""Native Android Text-to-Speech adapter for JARVIS."""

import threading


class AndroidTTS:
    """Small wrapper around Android's native TextToSpeech API."""

    def __init__(self, language="pt-BR", rate=0.95, pitch=1.0):
        self.language = language
        self.rate = rate
        self.pitch = pitch
        self._tts = None
        self._ready = False
        self._error = None
        self._lock = threading.RLock()
        self._init()

    def _init(self):
        try:
            from jnius import autoclass, PythonJavaClass, java_method

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
            Locale = autoclass("java.util.Locale")

            owner = self

            class InitListener(PythonJavaClass):
                __javainterfaces__ = ["android/speech/tts/TextToSpeech$OnInitListener"]

                @java_method("(I)V")
                def onInit(self, status):
                    with owner._lock:
                        if status == TextToSpeech.SUCCESS:
                            try:
                                result = owner._tts.setLanguage(Locale("pt", "BR"))
                                # LANG_MISSING_DATA = -1, LANG_NOT_SUPPORTED = -2
                                if result in (-1, -2):
                                    owner._ready = False
                                    owner._error = "Português (Brasil) não está disponível no mecanismo de voz."
                                    return
                                owner._tts.setSpeechRate(owner.rate)
                                owner._tts.setPitch(owner.pitch)
                                owner._ready = True
                                owner._error = None
                            except Exception as exc:
                                owner._ready = False
                                owner._error = str(exc)
                        else:
                            owner._ready = False
                            owner._error = f"Text-to-Speech não inicializou (status {status})."

            # Keep the listener alive for the lifetime of the TTS object.
            self._listener = InitListener()
            self._tts = TextToSpeech(PythonActivity.mActivity, self._listener)
        except Exception as exc:
            self._ready = False
            self._error = str(exc)

    @property
    def available(self):
        return self._ready

    @property
    def error(self):
        return self._error

    def speak(self, text):
        """Speak text using the Android TTS engine. Returns True if queued."""
        if not text:
            return False
        with self._lock:
            if not self._tts or not self._ready:
                return False
            try:
                TextToSpeech = __import__("jnius").autoclass("android.speech.tts.TextToSpeech")
                # QUEUE_FLUSH prevents old responses from piling up.
                self._tts.speak(str(text), TextToSpeech.QUEUE_FLUSH, None, "jarvis_response")
                return True
            except TypeError:
                # Older Android bindings may expose the 3-argument overload.
                try:
                    self._tts.speak(str(text), TextToSpeech.QUEUE_FLUSH, None)
                    return True
                except Exception as exc:
                    self._error = str(exc)
                    return False
            except Exception as exc:
                self._error = str(exc)
                return False

    def stop(self):
        with self._lock:
            try:
                if self._tts:
                    self._tts.stop()
            except Exception:
                pass

    def shutdown(self):
        with self._lock:
            try:
                if self._tts:
                    self._tts.stop()
                    self._tts.shutdown()
            except Exception:
                pass
            self._tts = None
            self._ready = False
