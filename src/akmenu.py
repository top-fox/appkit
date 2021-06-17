from appkit.src.menuwid import MenuWid

class AKMenu():
    def __init__(self, main_app=None, hotkey_context=None) -> None:
        super().__init__()
        self.ma = main_app
        self.context = hotkey_context
        self.menus = {  'File':
                            {'item':['New Project', 'Open Project', 'Open Recent...', 'Save', 'Save As...', 'Close Project', 'Quit'],
                            'disabled':{'Save', 'Save As...', 'Close Project'}},
                        'View':
                            {'item':['Design', 'Optimise', 'Resources', 'Measure', 'Report', 'Wizard'],
                            'disabled':{'Optimise', 'Resources', 'Measure', 'Report', 'Wizard'}},
                        'Help':
                            {'item':['About', 'Licence', 'Show Help Pane'],
                            'disabled':{'About', 'Licence'}},
                        }
        self.disabled = {'View'}
        self.callbacks = {}
        self.wid = MenuWid(menu_data=self, theme=self.ma.prefs.theme)

    def file_new_project_callback(self):
        self.ma.new_project()
        self.menus['File']['disabled'].discard('Save As...')
        self.menus['File']['disabled'].discard('Close Project')
