from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle

from .config import APP_NAME, API_URL, API_KEY, WAKE_WORD
from .engine import JarvisEngine
from .voice import Voice
from .wake import WakeController
from .ui.hud import HUD

class Panel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(.02,.04,.06,.92)
            self.bg=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(12)])
        self.bind(pos=self._sync,size=self._sync)
    def _sync(self,*_):
        self.bg.pos=self.pos; self.bg.size=self.size

class JarvisApp(App):
    title=APP_NAME

    def build(self):
        self.engine=JarvisEngine(api_url=API_URL,api_key=API_KEY)
        self.voice=Voice()
        self.wake=WakeController(self.voice, WAKE_WORD)
        self.auto_listen=False
        self.god_eye=False

        root=FloatLayout()
        self.hud=HUD(size_hint=(1,1))
        root.add_widget(self.hud)

        self.core_label=Label(text="J A R V I S",font_size=dp(24),
                              bold=True,size_hint=(None,None),
                              size=(dp(220),dp(45)),
                              pos_hint={"center_x":.5,"center_y":.50})
        root.add_widget(self.core_label)

        self.sub_label=Label(text="SYSTEM CORE // ONLINE",font_size=dp(10),
                             size_hint=(None,None),size=(dp(260),dp(30)),
                             pos_hint={"center_x":.5,"center_y":.44})
        root.add_widget(self.sub_label)

        header=BoxLayout(size_hint=(1,None),height=dp(54),pos_hint={"top":1},
                         padding=[dp(14),dp(8)])
        header.add_widget(Label(text=APP_NAME,font_size=dp(21),bold=True))
        self.state=Label(text="● ONLINE",font_size=dp(14))
        header.add_widget(self.state)
        root.add_widget(header)

        left=Panel(orientation="vertical",size_hint=(.31,.38),
                   pos_hint={"x":.025,"y":.10},padding=dp(12),spacing=dp(6))
        left.add_widget(Label(text="SYSTEM DIAGNOSTICS",bold=True))
        self.cpu=Label(text="CPU --"); self.ram=Label(text="RAM --")
        self.os=Label(text="OS --"); self.memory=Label(text="MEMORY READY")
        for w in (self.cpu,self.ram,self.os,self.memory): left.add_widget(w)
        root.add_widget(left)

        right=Panel(orientation="vertical",size_hint=(.31,.38),
                    pos_hint={"right":.975,"y":.10},padding=dp(12),spacing=dp(6))
        right.add_widget(Label(text="SUPPORT SYSTEMS",bold=True))
        self.voice_status=Label(text="VOICE     READY")
        self.wake_status=Label(text="WAKE      OFF")
        self.network=Label(text="AI CORE   LOCAL")
        self.core=Label(text="CORE      ONLINE")
        for w in (self.voice_status,self.wake_status,self.network,self.core): right.add_widget(w)
        root.add_widget(right)

        bottom=Panel(orientation="horizontal",size_hint=(.94,None),height=dp(58),
                     pos_hint={"x":.03,"y":.025},padding=dp(7),spacing=dp(7))
        self.input=TextInput(hint_text="Diga ou digite um comando...",multiline=False,font_size=dp(16))
        self.input.bind(on_text_validate=lambda *_: self.send())
        mic=Button(text="🎙",size_hint_x=None,width=dp(58))
        mic.bind(on_release=lambda *_: self.listen_once())
        wake=Button(text="WAKE",size_hint_x=None,width=dp(82))
        wake.bind(on_release=lambda *_: self.toggle_wake())
        god=Button(text="GOD EYE",size_hint_x=None,width=dp(92))
        god.bind(on_release=lambda *_: self.toggle_god_eye())
        send=Button(text="EXECUTAR",size_hint_x=None,width=dp(110))
        send.bind(on_release=lambda *_: self.send())
        bottom.add_widget(self.input); bottom.add_widget(mic); bottom.add_widget(wake); bottom.add_widget(god); bottom.add_widget(send)
        root.add_widget(bottom)

        self.commands=0
        Clock.schedule_interval(self.update_status,1)
        return root

    def set_state(self,state):
        self.state.text="● "+state
        self.hud.set_state(state)
        self.core_label.text = "J A R V I S"
        self.sub_label.text = "SYSTEM CORE // " + state

    def send(self):
        text=self.input.text.strip()
        self.input.text=""
        if not text: return
        self.commands += 1
        self.set_state("THINKING")
        response=self.engine.execute(text)
        if response=="__EXIT__":
            self.stop_wake()
            self.set_state("OFFLINE")
            Clock.schedule_once(lambda *_: self.stop(),.4)
            return
        self.set_state("SPEAKING")
        self.voice.speak(response,on_end=lambda: Clock.schedule_once(
            lambda *_: self.set_state("LISTENING" if self.auto_listen else "ONLINE"),0))

    def listen_once(self):
        self.set_state("LISTENING")
        self.voice_status.text="VOICE     LISTENING"
        if not self.voice.listen(self.on_heard,self.voice_error):
            self.voice_error("reconhecimento indisponível")

    def on_heard(self,text):
        Clock.schedule_once(lambda *_: self._receive(text),0)

    def _receive(self,text):
        self.input.text=text
        self.send()

    def voice_error(self,error):
        Clock.schedule_once(lambda *_: self._voice_error_ui(error),0)

    def _voice_error_ui(self,error):
        self.voice_status.text="VOICE     READY" if self.voice.tts_available else "VOICE     TTS OFF"
        if not self.auto_listen:
            self.set_state("ONLINE")
        print("VOICE:",error)

    def toggle_god_eye(self):
        self.god_eye = not self.god_eye
        self.engine.god_eye_active = self.god_eye
        self.hud.set_god_eye(self.god_eye)
        self.core.text = "CORE      GOD EYE" if self.god_eye else "CORE      ONLINE"

    def toggle_wake(self):
        if self.auto_listen:
            self.stop_wake()
        else:
            self.start_wake()

    def start_wake(self):
        self.auto_listen=True
        self.wake_status.text=f"WAKE      {WAKE_WORD.upper()}"
        self.set_state("LISTENING")
        self.wake.start(self.on_wake_command, self.on_wake_state)

    def stop_wake(self):
        self.auto_listen=False
        self.wake.stop()
        self.wake_status.text="WAKE      OFF"
        if self.state.text.endswith("LISTENING"):
            self.set_state("ONLINE")

    def on_wake_state(self,state):
        Clock.schedule_once(lambda *_: self.set_state(state),0)

    def on_wake_command(self,command):
        Clock.schedule_once(lambda *_: self._wake_command_ui(command),0)

    def _wake_command_ui(self,command):
        self.input.text=command
        self.send()

    def update_status(self,*_):
        try:
            import psutil,platform
            self.cpu.text=f"CPU  {psutil.cpu_percent():.0f}%"
            self.ram.text=f"RAM  {psutil.virtual_memory().percent:.0f}%"
            self.os.text=f"OS   {platform.system()}"
            self.network.text="AI CORE   ONLINE" if self.engine.ai.enabled() else "AI CORE   LOCAL"
        except Exception:
            pass

    def on_stop(self):
        self.stop_wake()
        try:
            self.voice.shutdown()
        except Exception:
            pass
