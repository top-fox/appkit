from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from appkit.src.aknoprojectwid import AKNoProjectWid

class AKProjects():
    def __init__(self, main_app=None) -> None:
        self.ma = main_app
        self.wid = AKProjectsWid(main_app=self.ma)
        self.ma.projects_wid = self.wid

class AKProjectScreen(Screen):
    def __init__(self, wid_inside=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.add_widget(wid_inside)

class AKProjectsWid(ScreenManager):
    def __init__(self, main_app=None) -> None:
        super().__init__()
        main_app.sm = self
        self.ma = main_app
        self.add_widget(AKProjectScreen(wid_inside=AKNoProjectWid(), name='no project'))
        self.previous_index = 0
    
    def add_projects(self):
        for index, proj in enumerate(self.ma.projects):
            self.add_widget(self.ma.project.screen)
            proj.tab_index = index
        Clock.schedule_once(lambda dt: setattr(self, 'current', self.ma.project.screen.name))
    
    def window_maximise_actions(self):
        pass

    def window_restore_actions(self):
        pass