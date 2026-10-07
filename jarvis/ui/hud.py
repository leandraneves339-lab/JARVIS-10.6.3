from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle, Quad
from kivy.clock import Clock
from kivy.metrics import dp
import math, random

class HUD(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state="ONLINE"
        self.phase=0.0
        self.activity=0.35
        self.signal=0.75
        self._last_state=None
        self.god_eye=False
        Clock.schedule_interval(self._tick,1/30)

    def set_god_eye(self, enabled=True):
        self.god_eye = bool(enabled)
        self._redraw()

    def set_state(self,state):
        self.state=state.upper()
        self.activity={
            "ONLINE":.35,"LISTENING":.75,"THINKING":.95,
            "SPEAKING":.85,"OFFLINE":.08
        }.get(self.state,.4)
        self._redraw()

    def _tick(self,dt):
        self.phase += dt
        self._redraw()

    def _line(self,points,width=1):
        Line(points=points,width=width)

    def _redraw(self):
        self.canvas.clear()
        with self.canvas:
            # Background
            Color(.005,.008,.012,1)
            Rectangle(pos=self.pos,size=self.size)

            w,h=self.size
            cx,cy=self.center
            R=min(w,h)*.20
            pulse=1 + .025*math.sin(self.phase*4)*(self.activity)

            # Faint radial glow layers
            for i in range(5,0,-1):
                rr=R*(.55+i*.11)*pulse
                Color(.015,.12,.18,.08)
                Ellipse(pos=(cx-rr,cy-rr),size=(2*rr,2*rr))

            # Technical horizontal scan lines
            Color(.06,.28,.38,.10)
            for y in range(int(self.y),int(self.top),int(dp(16))):
                Line(points=[self.x,y,self.right,y],width=.5)

            # Main rings
            for i in range(7):
                rr=R + i*dp(19)
                Color(.08,.55,.78,.18 if i>3 else .48)
                Line(circle=(cx,cy,rr),width=1)

            # Rotating segmented rings
            for i in range(4):
                rr=R+dp(28)+i*dp(27)
                speed=(1 if i%2==0 else -1)*(12+i*4)
                start=(self.phase*speed+i*80)%360
                for k in range(3):
                    a=start+k*120
                    Color(.1,.72,1,.8)
                    Line(circle=(cx,cy,rr,a,a+42),width=1.7)

            # GOD EYE: optional visual surveillance/targeting mode.
            # This is a HUD visualization only; it does not access cameras or devices.
            if self.god_eye:
                ew = R*1.45
                eh = R*.78
                Color(.03,.35,.50,.22)
                Ellipse(pos=(cx-ew,cy-eh),size=(2*ew,2*eh))
                Color(.12,.82,1,.95)
                Line(ellipse=(cx-ew,cy-eh,2*ew,2*eh),width=2)
                # Iris and pupil
                iris = R*.52 + R*.05*math.sin(self.phase*3)
                Color(.04,.25,.34,.95)
                Ellipse(pos=(cx-iris,cy-iris*.62),size=(2*iris,1.24*iris))
                Color(.18,.9,1,.95)
                Line(ellipse=(cx-iris,cy-iris*.62,2*iris,1.24*iris),width=2)
                pupil = R*.22*(1+.08*math.sin(self.phase*5))
                Color(.002,.008,.012,1)
                Ellipse(pos=(cx-pupil,cy-pupil),size=(2*pupil,2*pupil))
                Color(.45,.95,1,.95)
                Line(circle=(cx,cy,pupil*.72),width=1)
                # moving scan ray
                ang=math.radians((self.phase*80)%360)
                x=cx+math.cos(ang)*R*1.32
                y=cy+math.sin(ang)*R*1.32
                Color(.25,.95,1,.65)
                self._line([cx,cy,x,y],1.4)

            # Central reactor
            core=R*.58*pulse
            Color(.02,.18,.27,.95)
            Ellipse(pos=(cx-core,cy-core),size=(2*core,2*core))
            Color(.12,.8,1,.9)
            Line(circle=(cx,cy,core),width=2.2)

            # Inner rotating blades
            for i in range(12):
                a=self.phase*35+i*30
                ar=math.radians(a)
                r1=core*.35; r2=core*.86
                x1=cx+math.cos(ar)*r1; y1=cy+math.sin(ar)*r1
                x2=cx+math.cos(ar+.14)*r2; y2=cy+math.sin(ar+.14)*r2
                Color(.2,.85,1,.7 if i%2 else .95)
                self._line([x1,y1,x2,y2],1)

            # Equalizer / telemetry bars around the core
            bars=32
            for i in range(bars):
                a=2*math.pi*i/bars
                wave=(math.sin(self.phase*5+i*.72)+1)/2
                length=dp(7)+dp(23)*wave*self.activity
                r1=R+dp(74); r2=r1+length
                x1=cx+math.cos(a)*r1; y1=cy+math.sin(a)*r1
                x2=cx+math.cos(a)*r2; y2=cy+math.sin(a)*r2
                Color(.1,.62,1,.55+.35*wave)
                self._line([x1,y1,x2,y2],1.3)

            # Four corner targeting brackets
            s=dp(28); pad=dp(16)
            Color(.1,.7,1,.6)
            for sx,sy in ((self.x+pad,self.y+pad),
                          (self.right-pad,self.y+pad),
                          (self.x+pad,self.top-pad),
                          (self.right-pad,self.top-pad)):
                dx=1 if sx==self.x+pad else -1
                dy=1 if sy==self.y+pad else -1
                self._line([sx,sy,sx+dx*s,sy],1)
                self._line([sx,sy,sx,sy+dy*s],1)

            # Sweep arc
            sweep=(self.phase*45)%360
            Color(.25,.9,1,.7)
            Line(circle=(cx,cy,R+dp(96),sweep,sweep+65),width=2)
