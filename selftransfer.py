from datetime import datetime

from kivy.base import EventLoop
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivy.storage.jsonstore import JsonStore
from anvil.tables import app_tables


KV = '''
<SelftransferScreen>:
    BoxLayout:
        orientation: "vertical"
        spacing: dp(10)

        MDTopAppBar:
            title: "Self Transfer"
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [["bank", lambda x: root.nav_account()]]
            elevation: 4


        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(60)
                id: account_details_container
                padding: dp(50)

                MDRaisedButton:
                    id: sender_button
                    text: "Select Sending Bank"
                    size_hint: None, None
                    size: root.width * 0.8, dp(40)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    on_release: root.fetch_bank_names(sender=True)
                    md_bg_color: 0.7961, 0.9019, 0.9412, 1
                    text_color: 0, 0, 0, 1
                    line_color: 1, 1, 1, 1

                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Line:
                            width: 1
                            rectangle: self.x, self.y, self.width, self.height

                MDRaisedButton:
                    id: receiver_button
                    text: "Select Receiver Bank"
                    size_hint: None, None
                    size: root.width * 0.8, dp(40)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    on_release: root.fetch_bank_names(sender=False)
                    md_bg_color: 0.7961, 0.9019, 0.9412, 1
                    text_color: 0, 0, 0, 1
                    line_color: 1, 1, 1, 1

                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        Line:
                            width: 1
                            rectangle: self.x, self.y, self.width, self.height

        MDBoxLayout:
            size_hint: None, None
            size: root.width, dp(60)
            padding: [dp(50), dp(40), dp(15), dp(100)]
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            MDRaisedButton:
                text: "Next"
                size_hint: None, None
                size: root.width * 0.8, dp(40)
                on_release: root.pay_button_click()

<PayScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Pay"
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            elevation: 4

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: [dp(15), dp(10), dp(15), dp(300)]  

            MDIconButton:
                icon: "images/selffff.png"
                pos_hint: {'center_x': 0.5}  

            TextInput:
                id: amount_input
                hint_text: "Enter Amount"
                multiline: False
                size_hint: None, None
                size: root.width * 0.4, dp(60)
                pos_hint: {'center_x': 0.5}
                icon_left: "u20B9"
                background_color: 0, 0, 0, 0
                foreground_color: 0.2, 0.2, 0.2, 1
                border: (0, 0, 0, 0)
                font_size: '24sp'
                bold: True

            MDTextField:
                id: add_note
                hint_text: "Add Note"
                icon_left: "credit-card"
                mode: "rectangle"
                readonly: False

            BoxLayout:
                size_hint_y: None
                height: dp(40)
                pos_hint: {'center_x': 0.5}
                padding: ['150dp', '500dp', '50dp', '1dp']

                MDRaisedButton:
                    text: "Pay"
                    size_hint_x: None
                    width: root.width * 0.2
                    on_release: root.pay_amount()
'''

Builder.load_string(KV)


class PayScreen(MDScreen):
    sender_account = ""
    receiver_account = ""

    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(PayScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        if key in [27, 9]:
            self.go_back()
            return True
        return False

    def pay_amount(self):
        amount_input = self.ids.amount_input
        amount = amount_input.text

        if amount:
            if self.sender_account and self.receiver_account:
                try:
                    sender_account = app_tables.wallet_users_account.get(bank_name=self.sender_account)
                    receiver_account = app_tables.wallet_users_account.get(bank_name=self.receiver_account)

                    app_tables.wallet_users_transaction.add_row(
                        date=datetime.now(),
                        fund=float(amount),
                        transaction_type='credit',
                        transaction_status='self_transfer',
                        receiver_phone=receiver_account['phone'],
                        phone=sender_account['phone']
                    )
                    print(f"Payment successful: {amount}")
                    # Navigate to the dashboard screen after successful payment
                    # self.manager.current = 'dashboard'
                except Exception as e:
                    print(f"Error processing payment: {e}")
                    self.manager.show_notification('Alert!','Error processing payment.')
            else:
                print("Please select sender and receiver banks.")
                self.manager.show_notification('Alert!','Please select sender and receiver banks.')
        else:
            print("Please enter a valid amount.")
            self.manager.show_notification('Alert!','Please enter a valid amount.')


class SelftransferScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard' 

    def __init__(self, **kwargs):
        super(SelftransferScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.sender_menu = None  # Initialize dropdown menu for sender button
        self.receiver_menu = None  # Initialize dropdown menu for receiver button

    def on_key(self, window, key, scancode, codepoint, modifier):
        if key in [27, 9]:
            self.go_back()
            return True
        return False

    def fetch_bank_names(self, sender=True):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]

            if bank_names_str:
                if len(bank_names_str) == 1:
                    self.ids.sender_button.text = f" Sending Bank: {bank_names_str[0]}        "
                    self.sender_account = bank_names_str[0]
                    self.ids.sender_button.size_hint = (None, None)
                    self.ids.sender_button.size = (self.width * 0.8, dp(40))
                    self.ids.receiver_button.text = f"Receiving Bank: {bank_names_str[0]}          "
                    self.receiver_account = bank_names_str[0]
                    self.ids.receiver_button.size_hint = (None, None)
                    self.ids.receiver_button.size = (self.width * 0.8, dp(40))
                else:
                    self.sender_menu_list = [
                        {"text": f"        {bank_name}        ",
                         "on_release": lambda bank_name=bank_name: self.set_selected_sender_bank(bank_name)}
                        for bank_name in bank_names_str
                    ]
                    self.receiver_menu_list = [
                        {"text": f"         {bank_name}          ",
                         "on_release": lambda bank_name=bank_name: self.set_selected_receiver_bank(bank_name)}
                        for bank_name in bank_names_str
                    ]

                    if sender:
                        self.sender_menu = MDDropdownMenu(
                            caller=self.ids.sender_button,
                            items=self.sender_menu_list,
                            width_mult=4
                        )
                        self.sender_menu.open()
                    else:
                        self.receiver_menu = MDDropdownMenu(
                            caller=self.ids.receiver_button,
                            items=self.receiver_menu_list,
                            width_mult=4
                        )
                        self.receiver_menu.open()

        except Exception as e:
            print(f"Error fetching bank names: {e}")
            self.manager.show_notification('Alert!','An error occured. Please try again.')

    def set_selected_sender_bank(self, bank_name):
        self.ids.sender_button.text = f"Sending Bank: {bank_name}"
        self.sender_account = bank_name
        self.ids.sender_button.size_hint = (None, None)
        min_button_width = self.ids.sender_button.width
        self.ids.sender_button.size = (
            max(self.ids.sender_button.children[0].texture_size[0] + dp(20), min_button_width), dp(40)
        )
        if self.sender_menu:
            self.sender_menu.dismiss()

    def set_selected_receiver_bank(self, bank_name):
        self.ids.receiver_button.text = f"Receiving Bank: {bank_name}"
        self.receiver_account = bank_name
        self.ids.receiver_button.size_hint = (None, None)
        min_button_width = self.ids.receiver_button.width
        self.ids.receiver_button.size = (
            max(self.ids.receiver_button.children[0].texture_size[0] + dp(20), min_button_width), dp(40)
        )
        if self.receiver_menu:
            self.receiver_menu.dismiss()

    def pay_button_click(self):
        self.manager.add_widget(Factory.PayScreen(name="PayScreen"))
        print("Pay button clicked")
        if self.sender_account and self.receiver_account:
            print("Sender and receiver banks selected")
            self.manager.get_screen('PayScreen').sender_account = self.sender_account
            self.manager.get_screen('PayScreen').receiver_account = self.receiver_account
            self.manager.current = 'PayScreen'
        else:
            print("Sender and receiver banks not selected")
            # toast("Please select sender and receiver banks first.")
            self.manager.show_notification('Alert!', "Please select Sender and Receiver Banks first.")