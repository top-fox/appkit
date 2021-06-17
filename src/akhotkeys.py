from kivy.core.window import Window, Keyboard

class AKHotKeys():
    def __init__(self, main_app=None) -> None:
        # callback method name is automatically generated unless specified.
        ma = main_app
        self.keys = [
                    AKHotKey(ma=ma, context='project', name='listen',  text='l', ku='project_listen_up_callback'),
                    AKHotKey(ma=ma, context='project', name='file',  text='f', repeat=True),
                    AKHotKey(ma=ma, context='project', name='full screen', keyboard=292), #292 is F1
                    AKHotKey(ma=ma, context='file', name='quit',  text='q'),
                    AKHotKey(ma=ma, context='file', name='save as',  text='a'),
                    ]

class AKHotKey():
    # keyboard parameter overrides text parameter. Set print arg of Hotkeys to True for tool to find keyboard codes on key press
    def __init__(self, ma=None, context=None, name=None, text=None, keyboard=None, mods=[], repeat=False, kd=None, ku=None) -> None:
        self.main_app = ma
        self.context = context
        self.name = name
        self.text = text
        self.mods = mods
        self.repeat = repeat
        self.waiting = False
        self.disabled = False
        if keyboard == None:
            self.keyboard = Keyboard.string_to_keycode(Window._system_keyboard,text)
        else: self.keyboard = keyboard
        if kd == None:
            self.kd = context + '_' + name + '_callback'
            self.kd = self.kd.lower().replace('.', '_').replace(' ', '_')
        else:
            self.kd = kd
        self.ku = ku

    def key_down_callback(self):
        if not self.waiting and not self.disabled:
            if not self.repeat:
                self.waiting = True
            if self.kd != None:
                error_code = getattr(self, self.kd)()

    def key_up_callback(self):
        self.waiting = False
        if not self.disabled:
            if self.ku != None: 
                error_code = getattr(self, self.ku)()

    def project_file_callback(self):
        print('file callback')
    
    def project_full_screen_callback(self):
        print('full screen test')

    def project_listen_callback(self):
        print('in listen callback')

    def project_listen_up_callback(self):
        print('in listen end callback')

    def project_full_screen_callback(self):
        self.main_app.wid.toggle_full_screen()



