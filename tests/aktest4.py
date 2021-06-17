import appkit
print(dir(appkit))
from appkit.src.akapp import AKApp
from appkit.src.akprojectwid import AKProjectWid
from appkit.src.navigator import Navigator, NavClass
from appkit.src.akproject import AKProject
from appkit.src.hoveraction import HoverAction
from appkit.src.tooltip import ToolTip
from appkit.src.windowgrid import GridContent
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.label import Label

class TestApp(AKApp):
    def __init__(self) -> None:
        super().__init__(Project=MyAKProject)

    def main_loop(self):
        # Any blocking code will stop Kivy UI
        pass

class NavTest(Navigator, GridContent):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)  
        self.size_limit['min'] = [self.min_wide, self.min_height]

    def callback_add(*args):
        print('args', args)
        return TestObj(name = 'another')

class MyToolTip(ToolTip):
    def __init__(self) -> None:
        super().__init__()

class TestPane(GridContent, Label):
    def __init__(self, tooltip=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tooltip = ToolTip(trigger=self, text='tool tip for'+self.text+' - very long description of what it does', )

class TestObj(Label, NavClass):
    def __init__(self, name='') -> None:
        super().__init__()
        self.text = 'This is' + name
        self.name = name

class MyProjWid(AKProjectWid):
    def __init__(self, prefs=None, app_cursor=None, **kwargs) -> None:
        naved_obj1 = TestObj(name = 'Navigation area')
        obj_list = [naved_obj1]
        content1 = NavTest(base_class = TestObj, obj_list=obj_list, current=obj_list[0], 
                        label='MMM', theme=prefs.theme)
        content2 = TestPane(text = 'Area 2')
        content3 = TestPane(text = 'Area 3')
        content4 = TestPane(text = 'Area 4')
        print('in MyProjWid init, app_cursor', app_cursor)
        super().__init__(contents=[[content1, content2],[content3, content4]], app_cursor=app_cursor, **kwargs)
  
class MyAKProject(AKProject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, ProjWid=MyProjWid, **kwargs)
        
if __name__ == '__main__':
    app = TestApp()
    app.run_app()

