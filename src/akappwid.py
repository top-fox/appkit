from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from appkit.src.akstatusbar import AKStatusBar
from appkit.src.akmenu import AKMenu
from appkit.src.akprojects import AKProjects
from appkit.src.projecttabs import AKTabStrip
from appkit.src.cursor import AppCursor

Builder.load_string('''
<AKAppWid>:
    width: self.minimum_width
    canvas.before:
        Color:
            rgba: self.app_background_colour
        Rectangle:
            pos: self.pos
            size: self.size

''')

class DummyWidget(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.size_hint = (0,0)
        self.size = (0,0)

class AKAppWid(BoxLayout):
    def __init__(self, main_app=None, contents=None, **kwargs) -> None:
        self.app_background_colour = main_app.prefs.theme.app_background_colour
        super().__init__(**kwargs)
        if contents == None:
            self.contents = [AKMenu, AKTabStrip, AKProjects, AKStatusBar]
        else: self.contents = contents
        self.ma = main_app
        self.size_hint = (1,1)
        self.full_screen = self.ma.prefs.full_screen_on_start
        self.orientation = 'vertical'
        Window.minimum_width = self.ma.prefs.min_window_size[0]
        Window.minimum_height = self.ma.prefs.min_window_size[1]
        self.cont = []
        for i, el in enumerate(self.contents):
                print('el', el)
                self.cont.append(el(main_app=self.ma))
                self.add_widget(self.cont[i].wid)
        if self.full_screen:
            self.do_full_screen()
        self.app_cursor = AppCursor()

    def re_build_elements(self):
        self.clear_widgets()
        if self.full_screen:
            self.add_widget(self.ma.projects_wid)
        else:
            for index, el in enumerate(self.contents):
                self.add_widget(self.cont[index].wid)

    def update_projects(self):
        for proj in self.ma.projects:
            if proj.screen not in self.ma.sm.children:
                self.ma.sm.add_widget(proj.screen)
                self.ma.sm.current = proj.screen.name

    def do_full_screen(self):
        self.full_screen = True
        self.re_build_elements()
        Window.fullscreen = True
        Window.maximize()

    def end_full_screen(self):
        Window.fullscreen = False
        self.full_screen = False
        self.re_build_elements()

    def toggle_full_screen(self):
        if self.full_screen:
            self.end_full_screen()
        else: self.do_full_screen()
