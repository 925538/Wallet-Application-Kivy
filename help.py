from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
KV = '''
<HelpScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Help & Support'
                    anchor_title:'left'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(110)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "Contact Us"
                                on_release: root.manager.nav_contactus()
                                IconLeftWidget:
                                    icon: "email-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            # OneLineIconListItem:
                            #     text: "App info"
                            #     IconLeftWidget:
                            #         icon: "information-outline" 
                            #         theme_text_color: 'Custom'
                            #         text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Terms and Policies"
                                IconLeftWidget:
                                    icon: "file-document-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")                      
                        
'''
Builder.load_string(KV)

class HelpScreen(Screen):
    def go_back(self):
        # existing_screen = self.manager.get_screen('help')
        self.manager.current = 'dashboard'
        # self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        # lambda x: Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def nav_contactus(self):
        self.manager.current = 'contactus'    

    