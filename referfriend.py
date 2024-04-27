from anvil.tables import app_tables
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
import random
import string
import pyperclip
from kivy.storage.jsonstore import JsonStore
from kivy.base import EventLoop
Builder.load_string('''
<ReferFriendScreen>:
    Screen:
        MDTopAppBar:
            title: 'Referral'
            anchor_title:'left'
            elevation: 2
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint: {'top':1}
        BoxLayout:
            orientation: 'vertical'
            pos_hint:{'center_y':.91}
            padding:dp(10)
            
            # Widget:
            #     size_hint_y: None
            #     height:dp(15)    
            MDLabel:
                text: "Invite friends to GWallet"
                size_hint_y: None
                height: self.texture_size[1]
                # halign: 'left'  
                pos_hint:{'center_x':.5,'center_y':.78}
                font_size: dp(20)
                
            Widget:
                size_hint_y: None
                height:dp(10)
                     
            MDLabel:
                text: "Invite friends to GWallet and get ₹100 and when your friends make their first payment they get ₹50!"
                size_hint_y: None
                height: self.texture_size[1]
                # halign: ''
                theme_text_color: "Secondary"
                font_size: dp(15)
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(100)
                # padding:dp(10)
                spacing: dp(20)
    
                MDTextField:
                    id: textinput1
                    hint_text: "userfullname"
                    font_size: 24
                    color: 0, 0, 0, 1
                    size_hint_x: 0.5
    
                MDTextField:
                    id: textinput2
                    hint_text: "usercode"
                    font_size: 24
                    color: 0, 0, 0, 1
                    size_hint_x: 0.5
            
            MDRectangleFlatButton:
                text: 'Copy Code'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint: (0.4, None)  # Increase button size
                on_release: root.copy_code()
                text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
                line_color: [0, 0, 0, 0]  # Set line color to transparent
    
            MDRoundFlatButton: 
                id: button2
                text: 'Search Contacts'
                pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                size_hint: (0.8, None)  # Increase button size
                theme_text_color: "Custom"  # Use custom text color
                text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
                md_bg_color: (217 / 255, 217 / 255, 217 / 255, 1)  # Set background color to rgba(217, 217, 217, 1)
                line_color: [0, 0, 0, 0]  # Set line color to transparent    
            MDList:
                id: contacts_list
                OneLineListItem:
                    text: "Contact number 1"
                OneLineListItem:
                    text: "Contact number 2"

''')

class CustomLabel(Label):
    pass

class ReferFriendScreen(Screen):

    def __init__(self, **kwargs):
        super(ReferFriendScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        phone = JsonStore('user_data.json').get('user')['value']['phone']
        username = JsonStore('user_data.json').get('user')['value']['username']
        self.ids.textinput1.text = username
        user = app_tables.wallet_users.get(phone=phone)
        if not user['userreferral']:
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.ids.textinput2.text = random_code
            user.update(userreferral=random_code)
        else:
            self.ids.textinput2.text = user['userreferral']

    def copy_code(self):
        code_to_copy = self.ids.textinput2.text
        pyperclip.copy(code_to_copy)

    def go_back(self):
        existing_screen = self.manager.get_screen('refer')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
