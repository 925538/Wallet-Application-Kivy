from turtle import onclick
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from numpy import spacing  
kv_string = ''' 
<TransferScreen>:
    MDScreen:

        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: "Money Transfer"
                anchor_title:'left'
                right_action_items: [["", lambda x: None]]
                left_action_items: [["arrow-left", lambda x: root.go_back()]]
                md_bg_color: app.theme_cls.primary_color
                specific_text_color: 1, 1, 1, 1


            ScrollView:
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "10dp"
                    spacing: "13dp"
                    Widget:
                        size_hint_y: None
                        height: '4dp'
                    MDLabel:
                        text: "Transfer to New Number"
                        halign: 'center'
                        bold:True
                        theme_text_color: "Secondary"
                    Widget:
                        size_hint_y: None
                        height: '7dp'
                    MDRectangleFlatButton:
                        radius:[40,40,40,40]
                        id: currency_spinner
                        text: 'Currency'
                        size_hint: 1, None
                        size: "150dp", "50dp"
                        pos_hint: {'center_x': 0.5}
                        on_release: root.show_currency_menu()    

                    MDTextField:
                        id: name
                        mode: "rectangle"
                        hint_text: "  Beneficiary Name"
                        radius:[40,40,40,40]
                        pos_hint: {'center_x': .5}
                        line_color_normal: [137/255, 137/255, 137/255, 1]  
                        on_focus:
                            root.line_color_normal = app.theme_cls.primary_color if self.focus else [137/255, 137/255, 137/255, 1]




                    MDTextField:
                        id:mobile_no_field
                        input_type: "number"
                        mode: "rectangle"
                        radius:[40,40,40,40]
                        hint_text: "  Mobile Number"
                        pos_hint: {'center_x': .5}
                        line_color_normal: [137/255, 137/255, 137/255, 1]  
                        on_focus:
                            root.line_color_normal = app.theme_cls.primary_color if self.focus else [137/255, 137/255, 137/255, 1]


                    MDLabel:
                        text: "Note:Please note that only the beneficiary account number and IFSC information will be used for Quick transfer. (Please ensure correctness), the beneficiary name provided will not be considered as per RBI guidelines."
                        theme_text_color: "Secondary"
                        font_size: "12sp"
                        halign: 'left'
                        size_hint_y: None
                        height: self.texture_size[1] + dp(10)  # Adjust padding
                    Widget:
                        size_hint_y: None
                        height: '4dp'    
                    BoxLayout:
                        orientation: "horizontal"
                        row:1
                        col:2
                        spacing:dp(5)
                        padding:dp(-5)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.35}

                        MDCheckbox:
                            id: test_money
                            size_hint: None, None
                            size: "48dp", "48dp"
                            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                            on_active: root.update_transfer_amount(self.active)

                        MDLabel:
                            text: "Send 1$ as test money amount (Optional)"
                            theme_text_color: "Secondary"
                            font_size: "12sp"
                            halign: 'left'
                            size_hint_y: None
                            height: self.texture_size[1] + dp(10)  # Adjust padding
                            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
                    Widget:
                        size_hint_y: None
                        height: '3dp'
                    MDTextField:
                        id:amount_field
                        mode: "rectangle"
                        hint_text: "  Transfer Amount"
                        radius:[40,40,40,40]
                        pos_hint: {'center_x': .5}
                        line_color_normal: [137/255, 137/255, 137/255, 1]  
                        on_focus:
                            root.line_color_normal = app.theme_cls.primary_color if self.focus else [137/255, 137/255, 137/255, 1]


                    MDTextField:
                        id:purpose
                        mode: "rectangle"
                        hint_text: "  Enter Purpose"
                        radius:[40,40,40,40]
                        pos_hint: {'center_x': .5}
                        line_color_normal: [137/255, 137/255, 137/255, 1]  
                        on_focus:
                            root.line_color_normal = app.theme_cls.primary_color if self.focus else [137/255, 137/255, 137/255, 1]

                    Widget:
                        size_hint_y: None
                        height: '5dp'
                    MDRectangleFlatIconButton:
                        text: "Pay"
                        pos_hint: {"center_x": .5}
                        md_bg_color: app.theme_cls.primary_color
                        text_color: 1, 1, 1, 1
                        size_hint: .7, None
                        on_release: root.transfer_money()
                        radius:[40,40,40,40] 


'''
Builder.load_string(kv_string)


class TransferScreen(Screen):

    def go_back(self):
        existing_screen = self.manager.get_screen('transfer')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)
        self.ids.purpose.text = ''
        self.ids.amount_field.text = ''
        self.ids.name.text = ''
        self.ids.mobile_no_field.text = ''
        self.ids.test_money.active = False

    def __init__(self, **kwargs):
        super(TransferScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def transfer_money(self):
        amount = self.ids.amount_field.text.strip()
        receiver_phone = self.ids.mobile_no_field.text.strip()
        currency = self.ids.currency_spinner.text.strip()
        purpose = self.ids.purpose.text.strip()

        # Check if any field is empty
        if not all([amount, receiver_phone, currency, purpose]):
            # toast("Please fill in all fields.", duration=4)
            self.manager.show_notification('Alert!', 'Please fill in all fields.')
            return

        # Get data from the text fields and spinner
        amount = float(self.ids.amount_field.text)
        try:
            receiver_phone = float(self.ids.mobile_no_field.text)
        except ValueError:
            # toast("Invalid mobile number. Please enter a valid numeric value.", duration=4)
            self.manager.show_notification('Alert!',"Invalid mobile number. Please enter a valid numeric value.")
            return
        currency = self.ids.currency_spinner.text

        store = JsonStore('user_data.json')
        senders_phone = store.get('user')['value']["users_phone"]
        date = datetime.now()
        sender = app_tables.wallet_users_balance.get(users_balance_phone=senders_phone, users_balance_currency_type=currency)
        # check reciever is exist or not
        rec_exist = self.check_reg(receiver_phone)
        if rec_exist is None:
            # self.show_not_registered_dialog()
            self.manager.show_notification("Alert!","User not registered. Consider inviting the user to join.")

            return
        reciever = app_tables.wallet_users_balance.get(users_balance_phone=receiver_phone, users_balance_currency_type=currency)
        try:
            if sender is not None:
                s_old_balance = sender['users_balance']
                if amount <= s_old_balance:
                    new_balance = s_old_balance - amount
                    sender['users_balance'] = new_balance
                    if reciever is None:
                        app_tables.wallet_users_balance.add_row(
                            users_balance_phone=receiver_phone,
                            users_balance_currency_type=currency,
                            users_balance=amount
                        )
                    else:
                        r_old_balance = reciever['users_balance']
                        r_new_balance = r_old_balance + amount
                        reciever['users_balance'] = r_new_balance
                        reciever.update()
                        app_tables.wallet_users_transaction.add_row(
                                    users_transaction_receiver_phone=receiver_phone,
                                    users_transaction_phone=senders_phone,
                                    users_transaction_fund=amount,
                                    users_transaction_date=date,
                                    users_transaction_status="success",
                                    users_transaction_type="Debit",
                                    users_transaction_currency = currency
                                )
                        app_tables.wallet_users_transaction.add_row(
                            users_transaction_receiver_phone=senders_phone,
                            users_transaction_phone=receiver_phone,
                            users_transaction_fund=amount,
                            users_transaction_date=date,
                            users_transaction_type="Credit",
                            users_transaction_status="success",
                            users_transaction_currency = currency
                        )
                        self.manager.show_notification('Success', "Money transferred successfully.")
                        # toast("Money added successfully.")
                        # self.manager.current = 'dashboard'
                        # self.manager.show_balance()
                        self.ids.purpose.text = ''
                        self.ids.amount_field.text = ''
                        self.ids.name.text = ''
                        self.ids.mobile_no_field.text = ''
                        self.ids.test_money.active = False
                    sender.update()
                else:
                    # toast("balance is less than entered amount")
                    self.manager.show_notification('Alert!', "balance is less than entered amount.")
            else:
                # toast("you dont have a balance in this currency type", duration=5)
                self.manager.show_notification('Alert!', "you dont have a balance in this currency type.")
                self.ids.purpose.text = ''
                self.ids.amount_field.text = ''
                self.ids.name.text = ''
                self.ids.mobile_no_field.text = ''
                self.ids.test_money.active = False
        except Exception as e:
            # toast("an error occurred", duration=5)
            self.manager.show_notification('Alert!', "An error occurred. please try again.")
            self.ids.purpose.text = ''
            self.ids.amount_field.text = ''
            self.ids.name.text = ''
            self.ids.mobile_no_field.text = ''
            self.ids.test_money.active = False
            print(e)

    # def show_not_registered_dialog(self):
    #     # Show a dialog indicating that the receiver's phone number is not registered
    #     dialog = MDDialog(
    #         title="Receiver Not Registered",
    #         text="The provided phone number is not registered. Consider inviting the user to join.",
    #         buttons=[
    #             MDFlatButton(
    #                 text="OK",
    #                 on_release=lambda *args: dialog.dismiss()
    #             )
    #         ]
    #     )
    #     dialog.open()
    #     self.ids.purpose.text = ''
    #     self.ids.amount_field.text = ''
    #     self.ids.name.text = ''
    #     self.ids.mobile_no_field.text = ''
    #     self.ids.test_money.active = False

    def check_reg(self, phone):
        return app_tables.wallet_users.get(users_phone=phone)

    def show_currency_menu(self):
        currencies = ['INR', 'USD', 'EUR', 'GBP']
        menu_items = [{"text": currency, "viewclass": "OneLineListItem", "height": dp(44),
                       "on_release": lambda x=currency: self.test(x)} for currency in currencies]

        self.menu = MDDropdownMenu(
            caller=self.ids.currency_spinner,
            items=menu_items,
            width_mult=4,
        )

        self.menu.open()

    def test(self, text):
        self.ids.currency_spinner.text = text
        self.menu.dismiss()

    def update_transfer_amount(self, active):
        if active:
            self.ids.amount_field.text = "1"
        else:
            self.ids.amount_field.text = ""