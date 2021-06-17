from kivy.core.window import Window
from appkit.src.hoveraction import HoverAction

class HoverCursor(HoverAction):
    def __init__(self, cursor_type=None, normal_cursor='arrow', app_cursor=None, **kwargs) -> None:
        super().__init__(hover_delay=0, unhover_callback=self.unhover_callback, unhover_delay=0, **kwargs)
        self.cursor_type = cursor_type
        self.normal_cursor = normal_cursor
        self.app_cursor = app_cursor

    def hover_callback(self, *args):
        self.app_cursor.set_special(self, self.cursor_type)

    def unhover_callback(self, *args):
        self.app_cursor.remove_special(self)

    def mouse_move_callback(self, *args):
        pass

class AppCursor():
    def __init__(self) -> None:
        self.special_active = False
        self.special_cursors = set()
        self.normal_cursor = 'arrow'
    
    def set_special(self, object, type):
        Window.set_system_cursor(type)
        self.special_cursors.add(object)

    def remove_special(self, object):
        self.special_cursors.discard(object)
        if self.special_cursors:
            Window.set_system_cursor(list(self.special_cursors)[-1].cursor_type)
        else:
            Window.set_system_cursor(self.normal_cursor)

