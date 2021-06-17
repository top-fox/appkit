from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from appkit.src.hoveraction import HoverAction
from appkit.src.basic import move_into_window

Builder.load_string('''

<ToolTip>:
    height: self.texture_size[1] +10
    text_size: self.width -10, None

    canvas.before:
        Color:
            rgba: 0.2, 0.2, 0.2, 1 #change to theme colour
        BorderImage:
            pos: self.pos
            size: self.size
            source: 'white rectangle.png'
            border: 0, 12, 2, 12
''')

class ToolTip(Label):
    def __init__(self, trigger=None, expire=True,  main_app=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint =  (None, None)
        self.width = 150
        self.halign = 'center'
        self.shown = False
        if expire:
            self.hover = HoverAction(trigger=trigger, hover_base=self, second_hover_callback=self.second_hover_callback, second_hover_delay=5)      
        else: self.hover = HoverAction(trigger=trigger, hover_base=self, main_app=main_app)
        Window.add_widget(self.hover)
        self.offset = [0, -25]

    def hover_callback(self, *args, **kwargs):
        self.opacity = 1
        self.x = Window.mouse_pos[0] + self.offset[0]
        self.top = Window.mouse_pos[1] + self.offset[1]
        self.pos = move_into_window(self.pos, self.size)
        if not self.shown:
            Window.add_widget(self)
        self.shown = True

    def second_hover_callback(self, *args, **kwargs):
        if self.shown:
            self.anim = Animation(opacity=0, duration=0.7, t='in_out_quint')
            self.anim.start(self)

    def mouse_move_callback(self, *args):
        if self.shown:
            Window.remove_widget(self)
            self.shown = False
    
    def on_size(self, *args):
        self.pos = move_into_window(self.pos, self.size)

    def remove(self):
        Clock.unschedule(self.hover.hover_callback)
        Window.remove_widget(self)
        self.hover.remove_bindings()
