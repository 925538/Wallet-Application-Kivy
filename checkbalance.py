from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.base import EventLoop
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from anvil.tables import app_tables
import os
import anvil.server
import traceback  # Import traceback module for printing exceptions


KV = '''
<BalanceScreen>:
    name: 'balance'

    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Currency Balance"
            anchor_title:'left'
            
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "20dp"
'''

# Dynamically generate the KV string for MDCards
for currency in ['INR', 'USD', 'EUR', 'GBP']:
    icon_path = f"images/{currency.lower()}icon.png"
    if os.path.exists(icon_path):
        icon_source = icon_path
    else:
        icon_source = "images/iconINR.jpg"

    card_kv = f'''
                MDCard:
                    orientation: 'vertical'
                    size_hint: None, None
                    size: "280dp", "100dp"
                    pos_hint: {{"center_x": .5}}
                    md_bg_color: [250/255, 250/255, 250/255, 1]  # Correct usage of color
                    radius:[20,20,20,20]
                    canvas.before:
                        Color:
                            rgba: [137/255, 137/255, 137/255, 1]  # Border color
                        Line:
                            rounded_rectangle: [self.x, self.y, self.width, self.height,20,20,20,20]
                            width: 2


                    BoxLayout:
                        orientation: 'horizontal'


                        MDBoxLayout:
                            orientation: 'horizontal'
                            MDIconButton:
                                icon: "{icon_source}"
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                md_bg_color: [250/255, 250/255, 250/255, 1]
                                valign: 'top'  # Align the icon vertically at the top
                                padding: "30dp", "0dp", "40dp", "38dp"


                            MDLabel:
                                text: "{currency}"
                                theme_text_color: "Secondary"
                                halign: 'left'
                            MDCard:
                                orientation: 'vertical'
                                size_hint: 1, None
                                size: "80dp", "40dp"
                                pos_hint: {{"center_x": .3,"center_y": .5}}
                                md_bg_color: [250/255, 250/255, 250/255, 1]
                                MDLabel:
                                    id: {currency.lower()}_balance_label
                                    halign: 'center'  
    '''
    KV += card_kv

KV += '''
        MDBoxLayout:
            padding: "40dp", "10dp", "40dp", "10dp"
            adaptive_height: True
            MDRaisedButton:
                text: 'Add currency'
                md_bg_color: 20/255, 142/255, 254/255, 1
                size_hint_x: 1.5
                height: dp(50)
                width: dp(50)
                on_release: root.navigate_to_wallet()
'''


class BalanceScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('checkbalance')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(BalanceScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.fetch_balances()

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def fetch_balances(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]
            print(f"Phone number: {phone}")  # Print phone number
            currencies = ['INR', 'USD', 'EUR', 'GBP']  # Add more currencies as needed
            for currency in currencies:
                self.fetch_and_update_balance(phone, currency)
        except Exception as e:
            print(f"Error fetching balances: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

    def fetch_and_update_balance(self, phone, currency):
        try:
            balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
            balance = balance_table['balance']
            print(f"Balance for {currency}: {balance}")  # Print balance
            label_id = f"{currency.lower()}_balance_label"
            if balance is None:
                balance = 0  # Set balance to 0 if it is None
            else:
                balance = round(balance, 2)  # Round balance to two decimal places
            self.ids[label_id].text = f" {balance:.2f}"  # Update the text property with the formatted balance
        except Exception as e:
            print(f"Error fetching {currency} balance: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')
            balance = 0  # Set balance to 0 if an error occurs (currency not found or other exceptions)
            label_id = f"{currency.lower()}_balance_label"
            self.ids[label_id].text = f" {balance:.2f}"
            traceback.print_exc()

    def navigate_to_wallet(self):
        self.manager.add_widget(Factory.loadingScreen(name='loading'))
        self.manager.current = "loading"
        Clock.schedule_once(lambda dt: self.show_addmoney_screen(), 2)

    def show_addmoney_screen(self):
        self.manager.add_widget(Factory.AddMoneyScreen(name='Wallet'))
        self.manager.current = 'Wallet'


Builder.load_string(KV)
