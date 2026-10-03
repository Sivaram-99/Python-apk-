
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line, Mesh
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.core.window import Window
from kivy.lang import Builder
from random import random, uniform
from math import sin, cos, pi

Window.clearcolor = (0.025, 0.035, 0.065, 1)


class ParticleField(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []
        with self.canvas:
            self.bg = Color(0.025, 0.035, 0.065, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(24)])
        self.bind(pos=self._sync, size=self._sync)
        Clock.schedule_once(self._spawn, 0)
        Clock.schedule_interval(self._tick, 1/60)

    def _sync(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _spawn(self, *_):
        self.particles = []
        for _ in range(48):
            self.particles.append([
                random(), random(), uniform(0.0003, 0.0012),
                uniform(-0.00025, 0.00025), uniform(1.2, 3.2)
            ])
        self._redraw()

    def _tick(self, dt):
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            if p[0] > 1.02: p[0] = -0.02
            if p[1] > 1.02 or p[1] < -0.02: p[3] *= -1
        self._redraw()

    def _redraw(self):
        self.canvas.after.clear()
        with self.canvas.after:
            for x, y, _, _, r in self.particles:
                Color(0.20, 0.75, 1.0, 0.35)
                Ellipse(pos=(self.x+x*self.width, self.y+y*self.height),
                        size=(dp(r), dp(r)))


class GlassCard(BoxLayout):
    def __init__(self, title="", value="", accent=(0.20, .75, 1, 1), **kwargs):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(4),
                         size_hint_y=None, height=dp(115), **kwargs)
        with self.canvas.before:
            Color(0.055, 0.075, 0.13, .92)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
            Color(*accent)
            self.glow = RoundedRectangle(pos=(self.x, self.y), size=(dp(3), self.height),
                                         radius=[dp(2)])
        self.bind(pos=self._sync, size=self._sync)
        self.add_widget(Label(text=title, color=(.55,.65,.78,1), font_size=dp(13),
                              halign="left", valign="middle", size_hint_y=None, height=dp(24)))
        self.value_label = Label(text=value, color=(.92,.97,1,1), font_size=dp(27),
                                 bold=True, halign="left", valign="middle")
        self.add_widget(self.value_label)

    def _sync(self, *_):
        self.bg.pos, self.bg.size = self.pos, self.size
        self.glow.pos = (self.x, self.y)
        self.glow.size = (dp(3), self.height)


class AnimatedChart(Widget):
    progress = NumericProperty(0)
    values = ListProperty([32, 48, 40, 70, 55, 82, 68, 92, 76, 100])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(.055, .075, .13, .96)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self._sync, size=self._sync, progress=self._draw)
        Clock.schedule_once(self.animate_in, .35)

    def _sync(self, *_):
        self.bg.pos, self.bg.size = self.pos, self.size
        self._draw()

    def animate_in(self, *_):
        self.progress = 0
        Animation(progress=1, duration=1.25, t='out_cubic').start(self)

    def _draw(self, *_):
        self.canvas.after.clear()
        if self.width < 10 or self.height < 10:
            return
        left, bottom = self.x+dp(18), self.y+dp(20)
        w, h = self.width-dp(36), self.height-dp(42)
        with self.canvas.after:
            # grid
            Color(.12,.17,.25,.65)
            for i in range(1,5):
                yy = bottom + h*i/5
                Line(points=[left,yy,left+w,yy], width=1)
            # line
            pts = []
            n = len(self.values)
            for i,v in enumerate(self.values):
                xx = left + w*i/(n-1)
                yy = bottom + (v/105)*h*self.progress
                pts += [xx,yy]
            Color(.18,.78,1,1)
            if len(pts) >= 4:
                Line(points=pts, width=2.5, joint='curve')
            for i in range(n):
                xx = left + w*i/(n-1)
                yy = bottom + (self.values[i]/105)*h*self.progress
                Color(.5,.9,1,1)
                Ellipse(pos=(xx-dp(3),yy-dp(3)), size=(dp(6),dp(6)))


class RadialViz(Widget):
    angle = NumericProperty(0)
    pulse = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(.055,.075,.13,.96)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(20)])
        self.bind(pos=self._sync, size=self._sync, angle=self._draw, pulse=self._draw)
        Clock.schedule_interval(self._animate, 1/60)

    def _sync(self,*_):
        self.bg.pos,self.bg.size=self.pos,self.size
        self._draw()

    def _animate(self,dt):
        self.angle = (self.angle + dt*55) % 360
        self.pulse = (sin(self.angle*pi/180)+1)/2

    def _draw(self,*_):
        self.canvas.after.clear()
        cx, cy = self.center
        r = min(self.width,self.height)*.28
        with self.canvas.after:
            Color(.08,.15,.25,1)
            Line(circle=(cx,cy,r), width=dp(8))
            Color(.18,.78,1,1)
            Line(circle=(cx,cy,r,self.angle,self.angle+285), width=dp(8))
            Color(.35,.9,1,.18)
            Line(circle=(cx,cy,r+dp(16)+self.pulse*dp(8)), width=dp(2))
            for i in range(12):
                a=(i*30+self.angle)*pi/180
                rr=r+dp(35)
                x=cx+cos(a)*rr; y=cy+sin(a)*rr
                Color(.25,.8,1,.45)
                Ellipse(pos=(x-dp(2),y-dp(2)),size=(dp(4),dp(4)))


class HomeScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.reveal, .05)

    def reveal(self, *_):
        for child in self.ids.cards.children:
            child.opacity = 0
            Animation(opacity=1, duration=.45, t='out_quad').start(child)

    def refresh(self):
        self.ids.status.text = "LIVE • updated just now"
        for card, value in [(self.ids.c1, "82.4"), (self.ids.c2, "1,284"), (self.ids.c3, "64.8%")]:
            card.value_label.text = value
            Animation(opacity=.35, duration=.12).then(Animation(opacity=1,duration=.35)).start(card)


class VisualScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class Root(ScreenManager):
    pass


Builder.load_file('visualize.kv')


class VisualizeApp(App):
    title = "Visualize"
    def build(self):
        return Root()

    def on_start(self):
        Clock.schedule_once(self.splash, 0)

    def splash(self, *_):
        # Main screen is already ready; animate the title elements.
        pass


if __name__ == "__main__":
    VisualizeApp().run()
