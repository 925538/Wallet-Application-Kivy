from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivy.base import EventLoop

KV = '''
<AddContactScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Select Contact'
                    anchor_title:'left'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    #right_action_items: [['magnify', lambda x: root.search()]]
                    md_bg_color: "#1e75b9"
                    specific_text_color: "#ffffff"

                # Scrollable part
                ScrollView:
                    BoxLayout: 
                        orientation: "vertical"
                        size_hint_y: None
                        height: dp(120)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        # OneLineIconListItem:
                        #     text: "Contacts on G-wallet"

                        BoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            MDIconButton:
                                icon: 'magnify'
                                theme_text_color: 'Custom'
                                text_color: [0, 0, 0, 1]

                            CustomMDTextField:
                                id: search_text_card
                                hint_text: 'Search name or phone number'
                                multiline: False
                                size_hint_x: 0.7
                                radius: [20, 20, 0, 0]
                                padding: dp(0)
                                background_color: 1, 1, 1, 0

                        OneLineIconListItem:
                            text: "Contacts on G-wallet"        

                        # MDRaisedButton:
                        #     text: 'Filter'
                        #     size_hint: None, None
                        #     size: dp(100), dp(20)
                        #     radius: [60, 60, 60, 60]
                        #     pos_hint: {'center_x': 0.5}
                        #     canvas.before:
                        #         Color:
                        #             rgba: 0, 0, 0, 0
                        #         Rectangle:
                        #             size: self.size
                        #             pos: self.pos
                        #     text_color: 0, 0, 0, 1

'''
Builder.load_string(KV)


class CustomMDTextField(MDTextField):
    pass


class AddContactScreen(Screen):
    def go_back(self):
        # existing_screen = self.manager.get_screen('addcontact')
        self.manager.current = 'dashboard'
        # self.manager.remove_widget(existing_screen)

    def search(self):
        pass

    def __init__(self, **kwargs):
        super(AddContactScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
##################################
