from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager

class HoverAction(Widget):
    '''
    Mixin class to use for tooltips, hover animations etc.
    Rmember to put the mixin class first when listing classes for multiple inheritance.

    Specify either:
     - hover_base object; callbacks will then be methods of that object
     - hover_callback and mouse_move_callback; to specify the callback methods explicitly

     second_hover_callback is only called if it is specified. 

    edge_right, if set to >0, is the active strip at the right side of the widget  
    Similar for edge_left, edge_top and edge_bottom.
    
    '''

    def __init__(self, 
                trigger=None,
                mouse_move_callback=None,
                hover_callback=None,
                hover_delay=1,
                second_hover_callback=None,
                second_hover_delay = 5,
                unhover_callback=None,
                unhover_delay=0,
                hover_base=None,
                edge_right=0,
                edge_left=0,
                edge_top=0,
                edge_bottom=0,
                **kwargs) -> None:
        Window.bind(mouse_pos=self.on_mouse_pos)
        Window.bind(on_mouse_down=self.on_mouse_down)
        Window.bind(on_mouse_up=self.on_mouse_up)
        if not hover_base:
            hover_base = self
        if not trigger:
            trigger = self
        self.trigger = trigger
        if hover_callback:
            self.hover_callback = hover_callback
        else: self.hover_callback = getattr(hover_base,'hover_callback')
        if mouse_move_callback:
            self.mouse_move_callback = mouse_move_callback
        else: self.mouse_move_callback = getattr(hover_base, 'mouse_move_callback')
        self.hover_delay = hover_delay
        self.second_hover_callback = second_hover_callback
        self.second_hover_delay = second_hover_delay
        self.unhover_callback = unhover_callback
        self.unhover_delay = unhover_delay
        self.edge_right = edge_right
        self.edge_left = edge_left
        self.edge_top = edge_top
        self.edge_bottom = edge_bottom
        self.lock = False
        super().__init__(**kwargs)
    
    def on_mouse_pos(self, *args):
        if not self.lock:
            Clock.unschedule(self.hover_callback)
            if self.second_hover_callback:
                Clock.unschedule(self.second_hover_callback)
            if self.mouse_move_callback:
                self.mouse_move_callback()
            position = args[1]
            if (self.trigger.collide_point(*self.trigger.to_widget(*position, relative=False)) 
                    and self.in_limits(position) 
                    and not self.outside_modalview(position)
                    and not self.in_hidden_screen(position)):
                Clock.schedule_once(self.hover_callback, self.hover_delay)
                if self.second_hover_callback:
                    Clock.schedule_once(self.second_hover_callback, self.second_hover_delay)
            else:
                if self.unhover_callback:
                    Clock.schedule_once(self.unhover_callback, self.unhover_delay)
    
    def on_mouse_down(self, *args):
        self.lock = True

    def on_mouse_up(self, window, x, y, button, modifiers):
        self.lock = False
        self.on_mouse_pos(window, (x,y), modifiers)

    def in_limits(self, position):
        if self.edge_right or self.edge_left:
            active_lr = False
            if self.edge_right:
                if self.trigger.to_widget(*position)[0] >= self.trigger.right - self.edge_right:
                    active_lr = True
            if self.edge_left:
                if self.trigger.to_widget(*position)[0] <= self.trigger.x + self.edge_left:
                    active_lr = True
        else: active_lr = True
        if self.edge_bottom or self.edge_top:
            active_tb = False
            if self.edge_top:
                if self.trigger.to_widget(*position)[1] >= self.trigger.top - self.edge_top:
                    active_tb = True
            if self.edge_bottom:
                if self.trigger.to_widget(*position)[1] <= self.trigger.y + self.edge_bottom:
                    active_tb = True
        else: active_tb = True
        return active_tb and active_lr

    def outside_modalview(self, position):
        for wid in App.get_running_app().root_window.children:
            if isinstance(wid, ModalView):
                if self.trigger in [child for child in wid.walk(restrict=True)]:
                    return False
                else:
                    return True
        return False

    def in_hidden_screen(self, position):
        for root_child in App.get_running_app().root_window.children:
            for wid in root_child.walk():
                if isinstance(wid, ScreenManager):
                    for screen in wid.screens:
                        if self.trigger in [screen_wid for screen_wid in screen.walk(restrict=True)]:
                            if screen.name == wid.current:
                                return False
                            else: return True
        return False
    
    def remove_bindings(self):
        Window.unbind(mouse_pos=self.on_mouse_pos)
        Window.unbind(on_mouse_down=self.on_mouse_down)
        Window.unbind(on_mouse_up=self.on_mouse_up)    