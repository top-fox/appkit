from kivy.core.window import Window

class HotKeys():
    def __init__(self, keys=None, print=False) -> None:
        self.context = {'project'}
        self.disabled = False
        self.callback = keys
        self.set_keys(keys=keys)
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)
        self.print = print

    def set_keys(self, keys=None):
        self.hk_list = keys.keys

    def on_key_down(self, window, keyboard, keycode, text, modifiers):
        if self.print: print('On_key_down. window=', window, 'keyboard=', keyboard, 'keycode=', keycode, 'text=', text, 'modifiers=', modifiers)
        if not self.disabled:
            for hk in self.hk_list:
                if hk.context in self.context and keyboard == hk.keyboard and modifiers == hk.mods:
                    hk.key_down_callback()

    def on_key_up(self, window, keyboard, keycode):
        if self.print: print('On_key_up. window=', window, 'keyboard=', keyboard, 'keycode=', keycode)
        if not self.disabled:
            for hk in self.hk_list:
                if hk.context in self.context and keyboard == hk.keyboard:
                        hk.key_up_callback()

