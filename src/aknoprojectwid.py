from kivy.uix.label import Label

class AKNoProjectWid(Label):
    def __init__(self) -> None:
        super().__init__()
        self.text = 'No project loaded'