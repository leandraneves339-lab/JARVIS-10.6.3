
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

        self._TextToSpeech = None
        self._listener = None

        self._init()

    def _init(self):
        """Initialize Android TextToSpeech asynchronously."""
        try:
            from jnius import autoclass, PythonJavaClass, java_method

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            TextToSpeech = autoclass(
                "android.speech.tts.TextToSpeech"
            )

            Locale = autoclass(
                "java.util.Locale"
            )

            self._TextToSpeech = TextToSpeech

            owner = self

            class InitListener(PythonJavaClass):
                __javainterfaces__ = [
                    "android/speech/tts/TextToSpeech$OnInitListener"
                ]

                @java_method("(I)V")
                def onInit(self, status):
                    with owner._lock:
                        if status != TextToSpeech.SUCCESS:
                            owner._ready = False
                            owner._error = (
                                "Text-to-Speech não inicializou "
                                f"(status {status})."
                            )
                            return

                        try:
                            language = owner.language.replace("_", "-")
                            parts = language.split("-", 1)

                            if len(parts) == 2:
                                locale = Locale(
                                    parts[0],
                                    parts[1],
                                )
                            else:
                                locale = Locale(parts[0])

                            result = owner._tts.setLanguage(locale)

                            if result in (
                                TextToSpeech.LANG_MISSING_DATA,
                                TextToSpeech.LANG_NOT_SUPPORTED,
                            ):
                                owner._ready = False
                                owner._error = (
                                    f"Idioma {owner.language} não está "
                                    "disponível no mecanismo de voz."
                                )
                                return

                            owner._tts.setSpeechRate(owner.rate)
                            owner._tts.setPitch(owner.pitch)

                            owner._ready = True
                            owner._error = None

                        except Exception as exc:
                            owner._ready = False
                            owner._error = str(exc)

            # Keep the listener alive for the lifetime of the TTS object.
            self._listener = InitListener()

            self._tts = TextToSpeech(
                PythonActivity.mActivity,
                self._listener,
            )

        except Exception as exc:
            self._tts = None
            self._ready = False
            self._error = str(exc)

    @property
    def available(self):
        """Return True when Android TTS is ready to speak."""
        with self._lock:
            return (
                self._tts is not None
                and self._ready
            )

    @property
    def error(self):
        """Return the last TTS error, if any."""
        with self._lock:
            return self._error

    def speak(self, text):
        """Speak text using Android's native TTS.

        Returns True when the utterance is accepted by Android.
        """
        if text is None:
            return False

        text = str(text).strip()

        if not text:
            return False

        with self._lock:
            if not self.available:
                return False

            try:
                result = self._tts.speak(
                    text,
                    self._TextToSpeech.QUEUE_FLUSH,
                    None,
                    "jarvis_response",
                )

                if result == self._TextToSpeech.SUCCESS:
                    self._error = None
                    return True

                self._error = (
                    "Android TTS retornou código de erro: "
                    f"{result}"
                )
                return False

            except TypeError:
                # Compatibility with older PyJNIus/Android bindings.
                try:
                    self._tts.speak(
                        text,
                        self._TextToSpeech.QUEUE_FLUSH,
                        None,
                    )

                    self._error = None
                    return True

                except Exception as exc:
                    self._error = str(exc)
                    return False

            except Exception as exc:
                self._error = str(exc)
                return False

    def stop(self):
        """Stop the current Android TTS utterance."""
        with self._lock:
            if self._tts is None:
                return

            try:
                self._tts.stop()
            except Exception:
                pass

    def shutdown(self):
        """Release the Android TTS engine."""
        with self._lock:
            if self._tts is not None:
                try:
                    self._tts.stop()
                except Exception:
                    pass

                try:
                    self._tts.shutdown()
                except Exception:
                    pass

            self._tts = None
            self._listener = None
            self._ready = False
            self._error = None
