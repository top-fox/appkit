from kivy.clock import Clock
from appkit.src.projecttabs import AKProjectTab
from appkit.src.akprojects import AKProjectScreen
from appkit.src.akprojectwid import AKProjectWid
from appkit.src.commandmanager import CommandManager

class AKProject():
    def __init__(self, proj_number=1, main_app=None, ProjWid=AKProjectWid,
                    save_loc='C:\\', extension='.akp', **kwargs):
        self.ProjWid = ProjWid
        self.ma = main_app
        self.name = 'Project ' + str(proj_number)
        self.saved = False
        self.path = save_loc + self.name + extension
        self.cm = CommandManager()
        self.create_wids()
    
    def create_wids(self): 
        self.wid = self.ProjWid(prefs=self.ma.prefs, app_cursor=self.ma.wid.app_cursor) #, contents=test_content)
        self.screen = AKProjectScreen(wid_inside=self.wid, name=self.name)
        index=len(self.ma.sm.screens)
        self.tab = AKProjectTab(project=self, main_app=self.ma, index=index)
        Clock.schedule_once(lambda dt:self.tab.but.trigger_action())

    def undotest():
        pass