from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.factory import Factory
from default_currency import DefaultCurrency
from anvil.tables import app_tables
from kivy.storage.jsonstore import JsonStore

KV = '''
<PaysettingScreen>:
    Screen:
        MDScreen:
            on_pre_enter: self.bind_keyboard()
            on_pre_leave: self.unbind_keyboard()

            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'PaysettingScreen Content'
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Payment Settings'
                    anchor_title:'left'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:

                    BoxLayout: 
                        size_hint_y: None
                        height: dp(260)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "UPI Settings"
                                IconLeftWidget:
                                    icon: "at"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "Auto Topup"
                                IconLeftWidget:
                                    icon: "refresh-auto" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "UPI International"
                                IconLeftWidget:
                                    icon: "web"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Reminders"
                                IconLeftWidget:
                                    icon: "bell-check-outline"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")     
                            OneLineIconListItem:
                                text: "Default currency"
                                on_press:root.currency_set()
                                IconLeftWidget:
                                    id:curr_icon
                                    icon:""
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")

'''
Builder.load_string(KV)


class PaysettingScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('paysetting')
        self.manager.current = 'settings'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(PaysettingScreen, self).__init__(**kwargs)
        lambda x: Window.bind(on_keyboard=self.on_key)
        # EventLoop.window.bind(on_keyboard=self.on_key)
    
    def on_key(self, key):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def currency_set(self):
        sm = self.manager
        defaultcurrency = Factory.DefaultCurrency(name='defaultcurrency')
        sm.add_widget(defaultcurrency)
        sm.current = 'defaultcurrency'

    def on_enter(self):
        options_button_icon_mapping = {
            "INR": "currency-inr",
            "GBP": "currency-gbp",
            "USD": "currency-usd",
            "EUR": "currency-eur"
        }
        # print(self.ids.keys())
        # setting the default currency icon based on currency selected
        phone = JsonStore("user_data.json").get('user')['value']['users_phone']
        data = app_tables.wallet_users.get(users_phone=phone)
        currency = data['users_defaultcurrency']
        if currency:
            self.ids.curr_icon.icon = options_button_icon_mapping[currency]
        else:
            self.ids.curr_icon.icon = options_button_icon_mapping['INR']
