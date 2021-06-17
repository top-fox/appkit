from appkit.src.imagecontrol import combine_images_from_path, new_colour, hex_to_rgba_255, hex_to_rgba_1
from PIL import Image

class Theme():
    def __init__(self, bw_path=None, im_path=None) -> None:
        self.bw_path = bw_path # path to folder containing black & white images, to be coloured according to theme
        self.im_path = im_path # path in which to put images coloured according to theme, if create_theme_images() is used

    def create_theme_images(self):
        # Creates variants of the original image with the colours listed
        for name, variant_list in self.theme_images.items():
            bwimage = Image.open(self.bw_path + self.image_source[name])
            for suffix, colour in variant_list.items():
                image = new_colour(bwimage, hex_to_rgba_255(colour))
                image.save(self.im_path + name + suffix + '.png')
        for name, combination in self.combine_images.items():
            combined = combine_images_from_path(combination, path_prefix=self.im_path)
            combined.save(self.im_path + name + '.png')

    def set_theme(self, theme_number):
        # Colours
        col = {
                'dark grey 10%': '#191919',
                'dark grey 20%': '#323232',
                'dark grey 30%': '#494949',
                'light blue':    '#5555FF',
                'mid grey':      '#606060',
                'red':           '#FF0000',
                'white':         '#FFFFFF',
                'yellow':        '#FFFFA0',
            }

        self.cols = {
                'background 1': col['dark grey 10%'],
                'bg1 select':   col['mid grey'],
                'background 2': col['dark grey 20%'],
                'background 3': col['dark grey 30%'],
                'line':         col['mid grey'],
                'text':         col['white'],
                'highlight':    col['yellow'],
                'control':      col['light blue'],
                'disabled':     col['mid grey'],
            }

        if theme_number == 1:
            # Control graphics
            self.image_source = {
                'play': 'Playbutton.png',
                'stop': 'Stopbutton.png',
                'record': 'Recordbutton.png',
                'wrench': 'Wrenchbutton.png',
                'calibrate': 'Calibratebutton.png',
                'scene': 'scene_icon2.png',
                'notes': 'notes_icon3.png',
                'path': 'path_icon2.png',
                'blocks': 'blocks_icon2.png',
                'meter': 'meter_icon.png',
                'tick': 'tickbox_icon2.png',
                'target': 'target_icon2.png',
                'balance': 'balance_icon.png',
                'power': 'power_icon.png',
                'ear': 'ear_icon.png',
                'choose': 'choose_icon2.png',
                'plus': 'plus_icon3.png',
                'x': 'x_icon.png',
                'back': 'left arrow2.png',
                'forward': 'right arrow2.png',
                'menu': 'white rgba.png',
                'submenu': 'white rgba.png',
                'tab_edge': 'tab_edge3.png',
                'tab_fill': 'tab_fill5.png',
            }

            self.theme_images = {
                'back':     {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},
                'choose':   {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},
                'forward':  {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},   
                'play':     {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},  
                'plus':     {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},             
                'stop':     {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},  
                'record':   {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},  
                'wrench':   {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},
                'x':        {'-control':self.cols['control'], '-highlight':self.cols['highlight'], '-disabled':self.cols['disabled']},
                'menu':     {'-normal':self.cols['background 1'], '-select':self.cols['bg1 select']},
                'submenu':  {'-normal':self.cols['background 1'], '-select':self.cols['bg1 select']},
                'tab_edge': {'-unselected':self.cols['disabled'], '-selected':self.cols['highlight']},
                'tab_fill': {'-unselected':self.cols['background 2'], '-selected':self.cols['background 3']},
            }

            self.combine_images = {
                'tab-unselected':['tab_fill-unselected', 'tab_edge-unselected'],
                'tab-selected':['tab_fill-selected', 'tab_edge-selected'],
            }

            # Text
            self.info_text_colour = (1, 1, 1, 1)
            self.disabled_info_text_colour = (0.5, 0.5, 0.5, 1)
            self.base_font_name = 'Roboto'
            self.base_font_size = 15 #'12sp' - numeric value of 12 seems to have the same effect
            self.heading_font_size = '16sp'
            self.source_button_font = 'DejaVuSans' # Font for selection button (must support musical note character)
            self.text_box_colour = (0.15, 0.15, 0.15, 1)
        
            # Navigator
            self.nav_font_name = 'Roboto'
            self.nav_row_height = 25
            self.font_ratio = 1.2 # ratio of row height to size of contained font

            # Object select area
            self.object_font_name = 'Roboto'
            self.obj_row_height = 25
            self.object_font_size = '16sp'
            
            # Window graphics
            self.wb_fade = 0.5 # Window background fade. Fades border image too
            self.ab_fade = 0.25 # App background fade. Fades border image too
            self.shaded_colour = (1, 1, 1, 0.15) # Shaded area colour
            self.splitter_strip = '5pt' # Width of bar in Kivy Splitter window
            self.scroll_bar_width = 10 # for selection windows
            self.scroll_type = ['bars'] # scroll type for selection windows
            self.float_head_height = 50 # Height of header section of FloatingWindow
            self.modal_overlay = (0,0,0,0.3) # Fading of area outside window when modal / popup is open

            # Menus
            self.menu_row_height = 30
            self.top_menu_item_width = 50
            self.menu_width = 150
            self.menu_overlay = (0,0,0,0.3) # Fading of area outside sub-menu when sub-menu is open
    
            # Selection window
            self.select_window_size = (400,250)
            self.menu_item_height = 22
            self.menu_item_font = 'Roboto'

            # Small dialogue box
            self.small_dialogue_size = (250,150)

            # Other graphics
            self.app_background_colour = hex_to_rgba_1(self.cols['background 1'])
            self.info_graphics_colour = (0.5, 0.5, 0.5, 1)
            self.help_pane_background = 'blackwood.jpg'

            # Window area sizes
            self.top_bar_height = 25 
            self.project_tabs_height = 25
            self.bottom_bar_height = 30
            self.scene_pane_min_height = 200
            self.audio_pane_min_height = 120
            self.layout_pane_min_height = 50
            self.network_pane_min_height = 50
            # conveneience attribute, total of above items
            self.bars_height = self.top_bar_height + self.project_tabs_height + self.bottom_bar_height
            self.control_tabs_height = 25