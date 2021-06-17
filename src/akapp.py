import kivy.resources
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from appkit.src.akstatusbar import AKStatusBar
from appkit.src.akhotkeys import AKHotKeys
from appkit.src.akmenu import AKMenu
from appkit.src.akpreferences import AKPreferences
from appkit.src.akproject import AKProject
from appkit.src.akprojects import AKProjects
from appkit.src.akappwid import AKAppWid
from appkit.src.hotkeys import HotKeys
from appkit.src.projecttabs import AKTabStrip, AKTabGrid


class KivyApp(App):

    def __init__(self, main_app, **kwargs):
        super(KivyApp, self).__init__(**kwargs)
        self.main_app = main_app

    def build(self):
        self.window_size = Window.size
        return self.main_app.wid

    def on_stop(self):
        # close other processes if using multiprocessing
        return True

    def on_start(self):
        self.main_app.on_kivy_start()

class AKApp():
    def __init__(self,
                preferences=None,
                hotkeys=None,
                Project=AKProject,
                projects=[],
                project=None,
                contents= [AKMenu, AKTabStrip, AKProjects, AKStatusBar],
                load_initial_project=True,
                ) -> None:
        if preferences == None: self.prefs = AKPreferences()
        else: self.prefs = preferences
        if hotkeys == None:
            self.hotkeys = AKHotKeys(main_app=self)
        else: self.hotkeys = hotkeys()
        self.hk = HotKeys(keys=self.hotkeys)
        self.tab_grid = AKTabGrid(height=self.prefs.theme.project_tabs_height)
        self.is_tab_strip = False
        self.wid = AKAppWid(main_app=self, contents=contents)
        self.new_project_number = 1
        self.Project = Project
        self.projects = projects
        if project != None:
            self.project = project
            if project not in projects:
                self.projects.append(project)
        elif projects != []:
            self.project = projects[0]
        elif load_initial_project:
            self.new_project()
        else: self.project = None        

    def new_project(self):
        self.project = self.Project(proj_number=self.new_project_number, main_app=self)
        self.new_project_number += 1
        self.projects.append(self.project)
        self.sm.add_widget(self.project.screen)
        self.sm.current = self.project.screen.name
        if self.is_tab_strip:
            self.tab_grid.add_widget(self.project.tab)

    def run_app(self):
        self.ka = KivyApp(self).run()

    def on_kivy_start(self):
        Window.set_title(self.prefs.app_name)
        Config.set('kivy', 'exit_on_escape', '0')
        self.main_loop()

    def main_loop(self):
        #Override this method with app-specific code
        pass
