from kivy.uix.button import Button

class AKStatusBarWid(Button):
    def __init__(self, main_app=None, height=10, **kwargs):
        super().__init__(**kwargs)
        self.text = 'bottom bar'
        self.normal_height = height
        self.height = height
        self.size_hint = (1, None)
        #self.background_color = (1, 1, 1, 0.3)

    def window_maximise_actions(self):
        self.height = 0

    def window_restore_actions(self):
        self.height = self.normal_height
