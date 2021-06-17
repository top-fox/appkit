import os
from appkit.src.theme import Theme

class AKPreferences():
    def __init__(self) -> None:
        super().__init__()
        self.default_project = None
        self.show_help_pane = True
        self.default_left_pane_width = 300
        self.default_help_pane_width = 300
        self.default_audio_pane_height = 300 
        self.default_layout_panel_height = 400
        self.min_window_size = (800, 600)
        self.full_screen_on_start=False
        self.graphics_path = '.\\graphics\\'
        self.app_name = 'AKapp'
        self.file_locs = {'default_save':os.path.expanduser('~\\Documents\\'),
                        'backup':os.path.expanduser('~\\Documents\\'+ self.app_name + 'backup')}
        self.file_exts = {'project':'.hpf'}
        self.theme_number = 1
        self.theme = Theme(bw_path=self.graphics_path, im_path=self.graphics_path + 'Theme '+ str(self.theme_number)+'\\')
        self.theme.set_theme(self.theme_number)
        self.theme.create_theme_images()
    
