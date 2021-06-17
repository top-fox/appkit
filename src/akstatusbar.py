from kivy.uix.label import Label
from appkit.src.akstatusbarwid import AKStatusBarWid

class AKStatusBar(Label):
    def __init__(self, main_app=None) -> None:
        super().__init__()
        #self.text = 'Status Bar'
        self.wid = AKStatusBarWid(height=main_app.prefs.theme.bottom_bar_height)