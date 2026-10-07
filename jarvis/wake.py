import threading
import time

class WakeController:
    """Continuous listener using the available speech recognizer.

    It looks for the configured wake word in recognized phrases. On Android,
    the native recognizer is used; on desktop SpeechRecognition is used.
    This is intentionally a conservative loop: it does not execute commands
    until the wake word is detected.
    """
    def __init__(self, voice, wake_word="jarvis"):
        self.voice = voice
        self.wake_word = wake_word.lower()
        self.running = False
        self.thread = None
        self.on_command = None
        self.on_state = None

    def start(self, on_command, on_state=None):
        if self.running:
            return
        self.running = True
        self.on_command = on_command
        self.on_state = on_state
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            if self.on_state:
                self.on_state("LISTENING")
            done = threading.Event()

            def heard(text):
                if not self.running:
                    done.set()
                    return
                t = (text or "").strip()
                low = t.lower()
                if self.wake_word in low:
                    command = low.split(self.wake_word, 1)[1].strip(" ,.-")
                    if self.on_command:
                        self.on_command(command or "Estou ouvindo.")
                done.set()

            def error(_):
                done.set()

            try:
                self.voice.listen(heard, error)
            except Exception:
                done.set()

            # Prevent a tight loop if a platform recognizer fails instantly.
            done.wait(7.0)
            if self.running:
                time.sleep(.15)
