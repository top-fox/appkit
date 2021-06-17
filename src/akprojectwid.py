from appkit.src.windowgrid import GridContent, ResizeableGrid

class AKProjectWid(ResizeableGrid):
    def __init__(self, project=None, prefs=None, app_cursor=None, **kwargs):
        self.prefs = prefs
        self.app_cursor = app_cursor
        super().__init__(app_cursor=app_cursor, **kwargs)
        
        