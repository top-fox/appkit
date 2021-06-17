from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.textinput import TextInput

Builder.load_string('''
<BackArrow>:
    border: 0,0,0,0
    width: self.height / 2
   
<ForwardArrow>:
    border: 0,0,0,0
    width: self.height / 2

<ObjTextButton3>:
    text_size: self.size

<Navigator>:
    min_wide: self.nav_row.obj_label.texture_size[0]+4*self.min_height
''')

class NavClass():
    pass

class Navigator(BoxLayout):
    '''
    Navigator layout consists of a navigation strip at the top, with a ScreenManager below showing the navigated content.
    Each item in list must have .name attribute (string) and be of class base_class.
    '''
    min_wide = NumericProperty()
    def __init__(self,  base_class = NavClass,
                        obj_list=[],
                        current=None,
                        label='no label',
                        theme=None
                        ) -> None:
        self.min_height = 0
        self.obj_list = obj_list
        self.orientation = 'vertical'
        self.vm = ContScreenMan(obj_list=obj_list, current=current)
        self.nav_row = ObjNavRow(base=self, view_man=self.vm, obj_list=self.obj_list, 
                                    label=label, current=current, theme=theme)
        super().__init__()
        self.add_widget(self.nav_row)
        self.add_widget(self.vm)
        self.min_height = theme.nav_row_height

    def on_min_wide(self, *args):
        self.size_limit['min'] = [self.min_wide, self.min_height]
        self.size_set = True

    def callback_add(*args):
        # must return new item to add to ScreenManager (it will be put in a Screen)
        print('callback_add in Navigator')

    def callback_add_first():
        pass

    def callback_select(*args):
        pass

class ContScreenMan(ScreenManager):
    def __init__(self, obj_list=[], current=None) -> None:
        super().__init__()
        for obj in obj_list:
            screen = Screen(name=obj.name)
            screen.add_widget(obj)
            self.add_widget(screen)
        self.current = current.name


class ObjNavRow(BoxLayout):
    # base is the object called with callback functions: callback_add(), callback_add_first() and callback_select()
    # view_man is the Kivy ScreenManager; it is set to the .name parameter of the chosen list member
    # list is the list within which the navigation row navigates
    # current is the currently selected item in the list
    # label is the name of the object, used at the left of the navigation row and in dialogue box
    # select_callback is the method of base object called when a list item is selected
    def __init__(self, base=None, view_man=None, obj_list=[], current='no item', 
                label='no label', height=None, select_callback=None, 
                theme=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation ='horizontal'
        if height:
            self.height = height
        else:
            self.height = theme.nav_row_height
        self.size_hint = (1, None)
        self.old_index = 0
        self.view_man = view_man
        self.current = current
        self.select_callback = select_callback
        self.label = label
        self.obj_list = obj_list
        self.base = base
        self.theme = theme
        self.obj_label = ObjectLabel3(label_text=label, obj_row_height=self.height, theme=theme)
        self.add_widget(self.obj_label)
        self.go_back = ObjBackArrow3(self, item_height=self.height, theme=theme)
        self.add_widget(self.go_back)
        self.obj_text = ObjText3(self, item_height=self.height, label=current, theme=theme)
        self.add_widget(self.obj_text)
        self.go_forward = ObjForwardArrow3(self, item_height=self.height, theme=theme)
        self.add_widget(self.go_forward)
        self.obj_menu = ObjMenuButton3(self, size=(self.height, self.height),  theme=theme)
        self.add_widget(self.obj_menu)
        self.obj_add = ObjAddButton3(self, base, item_height=self.height, theme=theme)
        self.add_widget(self.obj_add)
        self.obj_del = ObjDelButton3(self, item_height=self.height, theme=theme)
        self.add_widget(self.obj_del)
    
    def on_press_back(self):
        index = self.obj_list.index(self.current)
        if index > 0:
            self.current = self.obj_list[index-1]
            self.update_view()

    def on_press_forward(self):
        index = self.obj_list.index(self.current)
        if index < len(self.obj_list) - 1:
            self.current = self.obj_list[index+1]
            self.update_view()

    def on_press_menu(self):
        glb.modal_window = SelectWindow(title='Select '+ self.label, 
                                        list = self.obj_list, 
                                        callback=self.set_item)

    def set_item(self, index):
        self.current = self.obj_list[index]
        self.update_view()

    def update_arrows(self):
        index = self.obj_list.index(self.current)
        if index == 0:
            self.go_back.disabled = True
        else:
            self.go_back.disabled = False
        if index == len(self.obj_list) - 1:
            self.go_forward.disabled = True
        else:
            self.go_forward.disabled = False

    def update_view(self):
        index = self.obj_list.index(self.current)
        for n in self.obj_list: print('list member:', n, 'name: ', n.name)
        if index > self.old_index:
            self.view_man.transition.direction = 'left'
        else: self.view_man.transition.direction = 'right'
        self.view_man.current = self.current.name
        self.obj_text.text_button.text = self.current.name
        self.old_index = index
        self.base.callback_select(self.current)
        self.update_arrows()

    def on_press_del(self):
        OKCancel(title='Delete ' + self.label.lower() + ' - are you sure?', 
                ok_callback=self.do_del, 
                cancel_callback=self.no_del)

    def do_del(self):
        index = self.obj_list.index(self.current)
        length = len(self.list)
        self.obj_list.remove(self.current)
        # insert default item if the last item has been deleted
        if length == 1:
            self.current = self.base.callback_add_first()
            self.update_view()
        # if the scene at the end of the list was deleted
        else:
            if index == length - 1:
                index -= 1
            self.current = self.obj_list[index]
        self.view_man.current = self.current.name
        self.update_view()

    def no_del(self):
        pass

class ObjectLabel3(Label):
    def __init__(self, obj_row_height=20, label_text='no text', theme=None) -> None:
        super().__init__(text=label_text)
        self.font_size = obj_row_height/ theme.font_ratio
        self.height = obj_row_height
        self.size_hint = (None, None)
        Clock.schedule_once(lambda dt: setattr(self,'width',self.texture_size[0]))

class BackArrow(Button):
    def __init__(self, object_type=None, item_height=20, theme=None) -> None:
        super().__init__()
        self.size_hint = (None, None)
        self.background_normal = theme.im_path + 'back-control.png'
        self.background_down = theme.im_path + 'back-highlight.png'
        self.background_disabled_normal = theme.im_path + 'back-disabled.png'
        self.background_disabled_down = theme.im_path + 'back-disabled.png'
        self.height = item_height
        self.disabled = True

class ForwardArrow(Button):
    def __init__(self, item_height=20, theme=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.background_normal = theme.im_path + 'forward-control.png'
        self.background_down = theme.im_path + 'forware-highlight.png'
        self.background_disabled_normal = theme.im_path + 'forward-disabled.png'
        self.background_disabled_down = theme.im_path + 'forward-disabled.png'
        self.height = item_height
        self.disabled = True

class StateColours(Button):
    def on_state(self, widget, value):
        pass
        
class ObjBackArrow3(BackArrow):
    def __init__(self, row, item_height=20, **kwargs) -> None:
        super().__init__(**kwargs)
        self.row = row
        self.height = item_height
        self.disabled = True

    def on_press(self):
        self.row.on_press_back()

class ObjForwardArrow3(ForwardArrow):
    def __init__(self, row, item_height=20, **kwargs) -> None:
        super().__init__(**kwargs)
        self.row = row
        self.height = item_height
        self.disabled = True

    def on_press(self):
        print('object forward pressed')
        self.row.on_press_forward()

# Button in same place as ObjText; display switches between the two widgets
class ObjTextButton3(Button):
    def __init__(self, item_height=20, label='no text', theme=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.height = item_height
        self.font_size = item_height / theme.font_ratio
        self.text = label
        self.size_hint = (1,None)
        self.border = (0,0,0,0)
        self.shorten = True
        self.halign = 'left'
        self.valign = 'center'
        self.font_name = theme.nav_font_name
        self.color = theme.info_text_colour
        self.background_color = theme.text_box_colour

    def on_press(self):
        self.parent.parent.switch_to_input()

class ObjTextInput3(TextInput):
    def __init__(self, item_height=20, label='none', theme=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.height = item_height
        self.font_size = item_height / theme.font_ratio
        self.text = label
        self.write_tab = False

    def on_focus(self, instance, value):
        # check that hotkeys don't disrupt text input
        if self.focus:
            pass
        else:
            self.parent.parent.switch_to_button()

class ObjText3(ScreenManager):
    def __init__(self, row, item_height=20, label='none',theme=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.row = row
        self.text_button = ObjTextButton3(item_height=item_height, label = row.current.name, theme=theme)
        self.text_input = ObjTextInput3(item_height=item_height, theme=theme)
        self.button_screen = Screen(name='button')
        self.input_screen = Screen(name='input')
        self.button_screen.add_widget(self.text_button)
        self.input_screen.add_widget(self.text_input)
        self.add_widget(self.button_screen)
        self.add_widget(self.input_screen)
        self.transition = NoTransition()

    def switch_to_input(self):
        self.current = 'input'
        self.text_input.text = self.text_button.text
        Clock.schedule_once(lambda dt: setattr(self.text_input, 'focus', True), 0.1)

    def switch_to_button(self):
        self.current = 'button'
        if self.text_input.text in self.row.view_man.screen_names:
            self.text_input.text = self.text_button.text
        else:
            self.text_button.text = self.text_input.text
            self.row.view_man.current_screen.name = self.text_input.text
            self.row.current.name = self.text_input.text

class ObjAddButton3(StateColours):
    def __init__(self, row, base, item_height=20, theme=None) -> None:
        super().__init__()
        self.theme = theme
        self.border = 0,0,0,0
        self.size_hint = (None, None)
        self.background_normal = theme.im_path + 'plus-control.png'
        self.background_down = theme.im_path + 'plus-highlight.png'
        self.size = (item_height, item_height)
        self.base = base
        self.row = row

    def on_press(self):
        self.row.current = self.base.callback_add(self)
        self.row.obj_list.append(self.row.current)
        s = Screen(name=self.row.current.name)
        s.add_widget(self.row.current)
        self.row.view_man.add_widget(s)
        self.row.update_view()

class ObjMenuButton3(Button):
    def __init__(self, row, theme=None, **kwargs) -> None:
        super().__init__( **kwargs)
        self.border = (0,0,0,0)
        self.size_hint = (None, None)
        self.background_normal = theme.im_path + 'choose-control.png'  #theme.choose_button_image
        self.background_down = theme.im_path + 'choose-highlight.png'
        self.background_disabled_normal = theme.im_path + 'choose-disabled.png'
        self.background_disabled_down = theme.im_path + 'choose-disabled.png'
        self.row = row
 
    def on_press(self):
        self.row.on_press_menu()

class ObjDelButton3(Button):
    def __init__(self, row, item_height=20, theme=None) -> None:
        super().__init__()
        self.border = (0,0,0,0)
        self.size_hint = (None, None)
        self.background_normal = theme.im_path + 'x-control.png'
        self.background_down = theme.im_path + 'x-highlight-png'
        self.background_disabled_normal = theme.im_path + 'x-disabled.png'
        self.background_disabled_down = theme.im_path + 'x-disabled.png'
        self.row = row
        self.size = (item_height, item_height)

    def on_press(self):
        self.row.on_press_del()
