from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from appkit.src.imagecontrol import hex_to_rgba_1

Builder.load_string('''
<AKProjectTab>:
    width: self.minimum_width
    canvas.before:
        BorderImage:
            pos: self.pos
            size: self.size
            source: self.background_image  #self.im_path + 'tab-unselected.png'
            border: 0, 12, 2, 12


<AKProjTabButton>:
    width: self.texture_size[0]
    allow_no_selection: False

<TabSaved>:
    width: self.texture_size[0]

''')

class AKTabStrip(ScrollView):
    def __init__(self, main_app=None, show_min_projects=2, **kwargs) -> None:
        super().__init__(**kwargs)
        self.show_min_projects = show_min_projects
        self.size_hint = (1, None)
        self.height_when_shown = main_app.prefs.theme.project_tabs_height
        self.add_widget(main_app.tab_grid)
        self.wid = self
        main_app.is_tab_strip = True
        self.bar_width = main_app.prefs.theme.scroll_bar_width

    def hide_or_show(self):
        if len(self.children[0].children) >= self.show_min_projects:
            self.height = self.height_when_shown
        else: self.height = 0
    
    def window_maximise_actions(self):
        self.height = 0

    def window_restore_actions(self):
        self.hide_or_show()

class AKTabGrid(GridLayout):
    def __init__(self, height=10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rows = 1
        self.size_hint = (None, None)
        self.height = height
        self.bind(minimum_width=self.setter('width'))
        self.inside = GridLayout()
        self.inside.cols = 1
        self.inside.size_hint_y= None
        self.inside.spacing = 10

    def add_widget(self, widget):
        super().add_widget(widget) 
        self.parent.hide_or_show()

class AKProjectTab(GridLayout):
    background_image = StringProperty()
    saved = BooleanProperty()
    def __init__(self, main_app=None, project=None, index=0, **kwargs) -> None:
        self.im_path = main_app.prefs.theme.im_path
        super().__init__(**kwargs)
        background_image = self.im_path + 'tab-unselected.png'
        self.rows = 1
        self.padding = 0
        self.spacing = 0
        self.size_hint = (None, 1)
        self.but = AKProjTabButton(main_app=main_app, project=project, index=index)
        self.colours = main_app.prefs.theme.cols
        self.close_but = AKProjTabCloseButton(main_app=main_app, project=project, index=index)
        self.saved_wid = TabSaved(self.saved)
        self.add_widget(TabPadding(10))
        self.add_widget(self.but)
        self.add_widget(self.saved_wid)
        self.add_widget(self.close_but)
        self.add_widget(TabPadding(3))
        if project: self.saved = project.saved
        else: self.saved = False

    def set_state(self, state):
        if state == 'down':
            self.tab_image_col = [1, 1, 0.58, 1]
            self.background_image = self.im_path + 'tab-selected.png'
            for child in self.children:
                child.color = hex_to_rgba_1(self.colours['text'])  #[1, 1, 1, 1]
        else:
            #self.fade_test = 0.5
            self.tab_image_col = [0.4, 0.4, 0.4, 1]
            self.background_image = self.im_path + 'tab-unselected.png'
            for child in self.children:
                child.color = hex_to_rgba_1(self.colours['disabled'])  #[0.4, 0.4, 0.4, 1]

    def on_saved(self, *args):
        if self.saved:
            self.saved_wid.text = '*'
        else: self.saved_wid.text = ''

class AKProjTabButton(ToggleButton):
    def __init__(self, main_app=None, project=None, index=0, **kwargs) -> None:
        super().__init__()
        self.ma = main_app
        self.project = project
        self.project.tab = self
        self.index = index
        self.size_hint_x = None
        self.group = 'projects'
        self.text = project.name
        self.padding = (0, 0)
        self.background_color = (1, 1, 1, 0)

    def on_press(self):
        if self.index < self.ma.sm.previous_index:
            self.ma.sm.transition.direction = 'right'
        else: self.ma.sm.transition.direction = 'left'
        self.ma.sm.previous_index = self.project.tab.but.index
        self.ma.sm.current = self.project.name
        self.parent.saved = not self.parent.saved

    def on_state(self, *args):
        self.parent.set_state(self.state)
        
class TabPadding(Label):
    def __init__(self, wide) -> None:
        super().__init__()
        self.background_colour = (1,1,1,0)
        self.size_hint = (None, 1)
        self.width = wide

class TabSaved(Label):
    def __init__(self, saved) -> None:
        super().__init__()
        self.background_colour = (1,1,1,0)
        self.size_hint = (None, 1)
        self.padding = (0,0)
        if saved: self.text = ''
        else: self.text='*'

class AKProjTabCloseButton(Button):
    def __init__(self, main_app=None, project=None, **kwargs) -> None:
        super().__init__()
        self.text= 'x'
        self.ma = main_app
        self.project = project
        self.size_hint_x = None
        self.width = 20
        self.padding = (0, 0)
        self.background_color = (1, 1, 1, 0)

    def on_press(self):
        self.ma.sm.prev_current = self.ma.sm.current
        self.ma.sm.current = self.project.name
        self.project.check_close()
 
class ProjectTabsWid(TabbedPanel):
    def __init__(self, main_app=None, **kwargs) -> None:
        self.main_app = main_app
        self.do_default_tab = False
        super().__init__(**kwargs)
    
    def on_current_tab(self, *args):
        self.main_app.project = self.current_tab.project
        Window.set_title(self.main_app.project.name + ' - ' + self.main_app.prefs.app_name)
        if self.main_app.project.saved:
            self.main_app.menu['file'].disabled.discard('Save')
        else: self.main_app.menu.menus['File']['disabled'].add('Save')

    def refresh_tab_sizes(self):
        for proj in self.main_app.projects:
            proj.tab.size_hint[0] = None
            proj.tab.size[0] = 80