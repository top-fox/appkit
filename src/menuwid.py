from kivy.uix.stacklayout import StackLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from appkit.src.tooltip import ToolTip

Builder.load_string('''

<SubMenu>:
    canvas.before:
        Rectangle:
            source: self.background
            size: self.size
            pos: self.pos

<SubMenuButton>:
    text_size: self.size
''')

class TopMenuButton(Button):
    def __init__(self, theme=None, context=set(), menu=None, menu_data=None, **kwargs):
        super().__init__(**kwargs)
        self.menu = menu
        self.text = menu[0]
        self.context = context
        self.callback = menu_data
        self.theme = theme
        self.width = theme.top_menu_item_width
        self.size_hint = (None, 1)
        self.border = 0,0,0,0
        self.background_normal = theme.im_path + 'menu-normal.png'
        self.background_down = theme.im_path + 'menu-select.png'

    def on_press(self):
        self.show_sub_menu()

    def show_sub_menu(self):
        self.context.add(self.text)
        submenu = SubMenu(self.menu, theme=self.theme, callback=self.callback, context=self.context)
        menu = submenu
        position = [self.pos[0], self.pos[1] - menu.size[1]]
        menu.position = position
        menu.size_hint = (None, None)
        menu.overlay_color = (0,0,0,0.3)
        menu.pos_hint = {'x': position[0] / Window.size[0], 'y': position[1] / Window.size[1]}
        menu.open()

class MenuWid(StackLayout):
    def __init__(self, menu_data=None, theme=None, context=set(), callback=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.theme = theme
        self.height = theme.top_bar_height
        self.size_hint = (1, None)
        for menu in menu_data.menus.items():
            button = TopMenuButton(theme=theme, context=context, menu=menu, menu_data=menu_data, markup=True,)
            self.add_widget(button)

    def window_maximise_actions(self):
        self.height = 0

    def window_restore_actions(self):
        self.height = self.theme.top_bar_height

class Menus():  
    def __init__(self, menu_data=None, theme=None, context=set(), callback=None):
        self.context = context
        self.top_menu = TopMenu(menu_data, theme=theme, context=context, callback=callback)
        
class SubMenuList(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 5
        self.orientation = 'vertical'

class SubMenuButton(Button):
    def __init__(self, name='', disable=set(), theme=None, callback=None, context=set(), submenu=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.submenu = submenu
        self.context = context
        self.disable = disable
        self.background_normal = theme.im_path + 'submenu-normal.png'
        self.background_down = theme.im_path + 'submenu-select.png'
        self.background_disabled_down = theme.im_path + 'submenu-normal.png'
        self.background_disabled_normal = theme.im_path + 'submenu-normal.png'
        self.border = (0,0,0,0)
        self.halign = 'left'
        self.valign = 'center'
        self.callback = callback
        callback_method = name + '_' + self.text + '_callback'
        self.callback_method = callback_method.lower().replace('.', '_').replace(' ', '_')
        dis = self.text in disable
        self.color = theme.disabled_info_text_colour if dis else theme.info_text_colour
        self.tooltip = ToolTip(trigger=self, text='tool tip for'+self.text+' - very long description of what it does', )

    def on_press(self):
        self.submenu.dismiss()
        self.context.discard(self.name)
        error_code = getattr(self.callback, self.callback_method)()
        return super().on_press()

class SubMenu(ModalView):
    def __init__(self, menu=None, theme=None, callback=None, context=set()) -> None:
        super().__init__()
        self.border: (0,0,0,0)
        self.background = theme.im_path + 'menu-normal.png'
        self.overlay_color = theme.menu_overlay
        list = SubMenuList()
        self.add_widget(list)
        for item in menu[1]['item']:
            self.size = (theme.menu_width, len(menu[1]['item']) * theme.menu_row_height)
            list.add_widget(SubMenuButton(name=menu[0], text=item, disable=menu[1]['disabled'], theme=theme, callback=callback, context=context, submenu=self))

    def on_dismiss(self):
        for wid in self.walk(restrict=True):
            if hasattr(wid, 'tooltip'):
                print('hasattr(', wid, ',tooltip) =', hasattr(wid, 'tooltip'))
                wid.tooltip.remove()