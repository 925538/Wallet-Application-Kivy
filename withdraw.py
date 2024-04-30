from datetime import datetime
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window

Builder.load_string(
    """
<WithdrawScreen>:
    MDScreen:
        MDTopAppBar:
            title: 'Withdraw Money'  # Updated title to 'Withdraw Money'
            anchor_title: 'center'
            elevation: 1
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [["",lambda x:None]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint:{'top':1}
        MDBoxLayout:
            orientation: 'vertical'

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y:0.9
            pos_hint: {"top":0.9}
            #md_bg_color: "#fe1616"
            MDBoxLayout:
                orientation: 'vertical'
            MDBoxLayout:
                orientation: 'vertical'
                MDCard:
                    orientation: 'vertical'
                    size_hint: 1, None  # Full width
                    height: dp(150)
                    pos_hint: {"center_x": 0.5,'y':0.2}
                    radius: [20, 20, 20, 20]
                    padding: dp(20)
                    spacing: dp(20)
                    md_bg_color: "#ffffff"        #0.7961, 0.9019, 0.9412, 1   #d7ecfa
                    elevation:1
                    shadow_softness: 12
                    shadow_offset:10,-12
                    shadow_color:0,0,0,0.3
                    line_color:colors['Gray']['500']
                    
                    GridLayout:
                        cols: 2
                        # row_force_default: True  # Ensure equal row heights (optional)
                        spacing:dp(5)
                        pos_hint_y:None
                        pos_hint_x:None
                        
                        # Column 1 (Labels)
                        MDBoxLayout:  # Use BoxLayout for vertical alignment
                            orientation: 'vertical'
                            spacing: dp(10)  # Adjust spacing as needed

                            MDLabel:
                                text: 'Total Wallet Balance'
                                font_size: dp(21)
                                halign: 'left'
                                size_hint_y: None
                                height: self.texture_size[1]  # Dynamic height for label content

                            MDLabel:
                                id: balance_lbl
                                text: ''    #Available Balance
                                halign: 'left'
                                valign: 'center'
                                readonly: True
                                size_hint_y: None
                                height: dp(43)  # Adjust height as needed
                                mode: "fill"
                                fill_mode: True
                                radius: [15, 15, 15, 15]  # Rounded edges
                                padding: dp(5), dp(5)
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                md_bg_color: '#ffffff'

                        # Column 2 (MDIconButton)                    
                        AnchorLayout:
                            size_hint_y:None
                            height:dp(100)
                            size_hint_x:None
                            width:dp(50)
                            MDIconButton:
                                id: options_button
                                # pos_hint:{'center_x':0.5,'center_y':0.5}
                                icon: "currency-inr"
                                md_bg_color: colors['LightBlue']['A400']
                                theme_text_color: "Custom"
                                text_color: 0, 0, 0, 1
                                on_release: root.show_currency_options(self)

                Widget:
                    size_hint_y: None
                    height:dp(10)
                MDLabel:
                    text: "Send Money from Wallet to Bank" 
                    font_size:dp(21)
                    halign: 'center'
                    valign:'center'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: dp(30)
                    bold: True 
                MDLabel:
                    text: "No direct or hidden charges. Send money from" 
                    font_size:dp(10)
                    halign: 'center'
                    valign:'center'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: dp(20)
 
                MDLabel:
                    text: "your wallet to bank for FREE" 
                    font_size:dp(15)
                    halign: 'center'
                    valign:'center'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: dp(20)

                MDBoxLayout:
                    padding: dp(15)
                    spacing: dp(20)
                    adaptive_height: True

                    MDRaisedButton:
                        id: bank_dropdown
                        text: 'Select bank account'
                        size_hint_x: 1
                        height: dp(50)
                        md_bg_color: '#ffffff'           #"#3dd2ff"        # b0d9f9    #0.7961, 0.9019, 0.9412, 1
                        on_release: root.fetch_bank_names()
                        text_color: 0, 0, 0, 1
                        elevation:1
                        line_color:colors['Gray']['500']
                        shadow_softness: 15
                        shadow_offset:10,-12
                        shadow_color:0,0,0,0.3

                MDBoxLayout:
                    # padding: dp(5)
                    spacing: dp(10)
                    adaptive_height: True
                    MDTextField:
                        id: amount_textfield
                        mode: "rectangle"
                        radius:[15,15,15,15]
                        hint_text: "Enter amount"
                        size_hint_x: 1
                        hint_text_color_normal:0,0,0,0.7
                        line_color_normal:colors['Gray']['500']      

                MDSeparator:
                    height: dp(1)

                MDBoxLayout:
                    padding: dp(10) #(dp(27),dp(10),dp(24),dp(10))
                    spacing: dp(20)
                    adaptive_height: True
                    adaptive_width: True
                    # orientation: 'horizontal'
                    pos_hint: {'center_x': 0.5}


                    MDFlatButton:
                        text: '+100'
                        size_hint_x: None
                        width: dp(64)
                        height: dp(40)
                        md_bg_color:colors['LightBlue']['100']    #0.7961, 0.9019, 0.9412, 1
                        on_release: root.update_amount(100)

                    MDFlatButton:
                        text: '+200'
                        size_hint_x: None
                        width: dp(64)
                        height: dp(40)
                        md_bg_color: colors['LightBlue']['100']     #0.7961, 0.9019, 0.9412, 1
                        on_release: root.update_amount(200)

                    MDFlatButton:
                        text: '+500'
                        size_hint_x: None
                        width: dp(64)
                        height: dp(40)
                        md_bg_color: colors['LightBlue']['100']       #0.7961, 0.9019, 0.9412, 1
                        on_release: root.update_amount(500)

                    MDFlatButton:
                        text: '+1000'
                        size_hint_x: None
                        width: dp(64)
                        height: dp(40)
                        md_bg_color: colors['LightBlue']['100']         #0.7961, 0.9019, 0.9412, 1
                        on_release: root.update_amount(1000)

                MDBoxLayout:
                    padding: dp(10)
                    adaptive_height: True

                    MDRaisedButton:
                        text: 'Proceed '
                        md_bg_color: 20/255, 142/255, 254/255, 1
                        size_hint_x: 1.5
                        height: dp(50)
                        on_press: root.withdraw()
                        shadow_softness: 12
                        shadow_offset:10,-12
                        shadow_color:0,0,0,0.3
            MDBoxLayout:
                orientation: 'vertical'    
        MDBoxLayout:
            size_hint_y: None
            height: dp(100)
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            size_hint_x: None
            width: dp(100)
"""
)


class WithdrawScreen(Screen):
    def __init__(self, **kwargs):
        super(WithdrawScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def go_back(self):
        self.ids.amount_textfield.text = ""  # Clear the amount input field
        self.ids.bank_dropdown.text = "Select bank account"  # Reset the bank dropdown text
        self.update_balance_label(self.ids.options_button.text)  # Update the balance label
        existing_screen = self.manager.get_screen('withdraw')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def on_key(self, window, key, scancode, codepoint, modifier):
        if key in [27, 9]:
            self.go_back()
            return True
        return False

    def fetch_bank_names(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
            if bank_names_str:
                self.menu_list = [
                    {"viewclass": "OneLineListItem", "text": bank_name,
                     "on_release": lambda x=bank_name: self.test(x)}
                    for bank_name in bank_names_str
                ]

                self.menu = MDDropdownMenu(
                    caller=self.ids.bank_dropdown,
                    items=self.menu_list,
                    width_mult=4
                )
                self.menu.open()
            else:
                toast("No accounts found")

        except Exception as e:
            print(f"Error fetching bank names: {e}")

        finally:
            pass

    def test(self, text):
        self.account_number = None
        self.account_holder_name = None
        self.ids.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        try:
            matching_accounts = app_tables.wallet_users_account.search(phone=phone, bank_name=str(text))
            if matching_accounts:
                self.account_number = matching_accounts[0]['account_number']
            else:
                toast("Account not found")
            if self.menu:
                self.menu.dismiss()
        except Exception as e:
            print(f"Error fetching account details: {e}")

    def select_currency(self, currency):
        wdrw_scr = self.manager.get_screen('withdraw')
        wdrw_scr.ids.options_button.text = currency

    def withdraw(self):
        wdrw_scr = self.manager.get_screen('withdraw')
        amount = wdrw_scr.ids.amount_textfield.text
        currency = wdrw_scr.ids.options_button.text  # Get the selected currency from options_button
        date = datetime.now()
        phone = JsonStore('user_data.json').get('user')['value']["phone"]
        balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
        selected_bank = wdrw_scr.ids.bank_dropdown.text

        if not selected_bank or not amount or not currency:
            self.manager.show_error_popup("Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            self.manager.show_error_popup("Invalid amount. Please enter a valid number.")
            return

        try:
            if balance_table is not None:
                old_balance = balance_table['balance']
                if amount <= old_balance:
                    new_balance = old_balance - amount
                    balance_table['balance'] = new_balance
                    balance_table.update()
                else:
                    toast("Balance is less than the entered amount")
            else:
                toast("You don't have a balance in this currency type")
            app_tables.wallet_users_transaction.add_row(
                receiver_phone=float(self.account_number),
                phone=phone,
                fund=amount,
                date=date,
                transaction_type="Debit"
            )

            success_message = f"Withdrawal successful."
            self.manager.show_success_popup(success_message)
            # self.manager.show_balance()
        except Exception as e:
            print(f"Error withdrawing money: {e}")
            self.manager.show_error_popup("An error occurred. Please try again.")

    def update_amount(self, amount):
        self.ids.amount_textfield.text = str(amount)

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]
        print(button)
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    menu = None
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)

        self.ids.options_button.text = instance_menu_item
        self.ids.balance_lbl.text = f'{int(total_balance)} '   #Available Balance: 
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def currencyDropdown(self):
        try:
            currencies = ["INR", "USD", "EUR", "GBP", "JPY", "AUD"]
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": currency,
                 "on_release": lambda x=currency: self.select_currency(x)}
                for currency in currencies
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.currency_dropdown,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching currencies: {e}")

    def update_balance_label(self, currency):
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, currency)
        self.ids.balance_lbl.text = f'{total_balance} {currency}'  #Available Balance: 

    def on_pre_enter(self, *args):
        #in this function it will display the balance as per the default currency selected in default currency settings
        store1 = JsonStore('user_data.json')
        phone_no = store1.get('user')['value']["phone"]
        user_data=app_tables.wallet_users.get(phone=phone_no)
        user_default_currency = user_data['defaultcurrency']
        print(user_default_currency)
        # for icon_btn in self.options_button_icon_mapping:
        if user_default_currency:
            self.ids.options_button.icon = self.options_button_icon_mapping[user_default_currency]
            total_balance = self.manager.get_total_balance(phone_no, user_default_currency)
            self.ids.options_button.text= user_default_currency
            # Convert the total balance to the selected currency
            self.ids.balance_lbl.text = f'{int(total_balance)}'   #Available Balance: 
        
        #users data
        
        users_default_account = user_data['default_account']
        if users_default_account:
            ban_name = app_tables.wallet_users_account.get(account_number=float(users_default_account))
            if ban_name:
                bank_name = ban_name['bank_name']
                self.ids.bank_dropdown.text = bank_name
                self.test(bank_name)
