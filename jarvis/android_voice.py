"""Native Android SpeechRecognizer adapter."""

class AndroidVoice:
    def __init__(self):
        self._recognizer = None
        self._listener = None
        self._intent = None

    def listen(self, callback, on_error=None):
        try:
            from jnius import autoclass, PythonJavaClass, java_method

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            RecognizerIntent = autoclass("android.speech.RecognizerIntent")
            Intent = autoclass("android.content.Intent")
            SpeechRecognizer = autoclass("android.speech.SpeechRecognizer")

            activity = PythonActivity.mActivity
            if not SpeechRecognizer.isRecognitionAvailable(activity):
                raise RuntimeError("Reconhecimento de voz não está disponível neste aparelho.")

            owner = self

            class Listener(PythonJavaClass):
                __javainterfaces__ = ["android/speech/RecognitionListener"]

                @java_method("(Landroid/os/Bundle;)V")
                def onReadyForSpeech(self, params): pass

                @java_method("()V")
                def onBeginningOfSpeech(self): pass

                @java_method("(F)V")
                def onRmsChanged(self, rmsdB): pass

                @java_method("([B)V")
                def onBufferReceived(self, buffer): pass

                @java_method("()V")
                def onEndOfSpeech(self): pass

                @java_method("(I)V")
                def onError(self, error):
                    if on_error:
                        on_error(f"Reconhecimento de voz Android: erro {error}")
                    owner._destroy()

                @java_method("(Landroid/os/Bundle;)V")
                def onResults(self, results):
                    try:
                        arr = results.getStringArrayList("results_recognition")
                        if arr and arr.size():
                            callback(str(arr.get(0)))
                        elif on_error:
                            on_error("Nenhum comando foi reconhecido.")
                    finally:
                        owner._destroy()

                @java_method("(Landroid/os/Bundle;)V")
                def onPartialResults(self, partial): pass

                @java_method("(ILandroid/os/Bundle;)V")
                def onEvent(self, eventType, params): pass

            self._listener = Listener()
            self._recognizer = SpeechRecognizer.createSpeechRecognizer(activity)
            self._recognizer.setRecognitionListener(self._listener)
            self._intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            self._intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                                  RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            self._intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR")
            self._intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "pt-BR")
            self._intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
            self._recognizer.startListening(self._intent)
            return True
        except Exception as exc:
            self._destroy()
            if on_error:
                on_error(str(exc))
            return False

    def _destroy(self):
        try:
            if self._recognizer:
                self._recognizer.destroy()
        except Exception:
            pass
        self._recognizer = None
        self._intent = None
        self._listener = None
