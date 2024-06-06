from datetime import datetime
import requests
from anvil.tables import app_tables
from kivymd.toast import toast
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.menu import MDDropdownMenu
from kivy.base import EventLoop
from kivy.core.window import Window
KV = """
<Topup>
    Screen:
        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["bank", lambda x: root.manager.nav_account()]]
            title: "Top Up"
            anchor_title:'left'
            md_bg_color: "#1e75b9"
            specific_text_color: "#ffffff"
            pos_hint: {'top': 1}

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(400)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

            Image:
                source: 'images/addmoney.png'  # Update with your image file path
                size_hint_y: None
                height: dp(300)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}    

            RelativeLayout:

            MDTextField:
                id: amount_field
                hint_text: "Enter Amount"
                mode: "rectangle"
                keyboardType: "numeric"
                required: True
                size_hint: None, None
                size: dp(320), dp(48)  # Adjust the size as needed
                pos_hint: {'center_x': 0.5, 'center_y': 0.65}

            MDRectangleFlatButton:
                id: bank_dropdown
                text: "change bank account"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1  # White text color
                line_color: 0, 0, 0, 1  # Black border color
                size_hint: None, None
                on_release: root.dropdown()
                size: dp(100), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.45}

            MDRaisedButton:
                text: "Add Money"
                on_press: root.add_money()
                size_hint: None, None
                size: dp(200), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.3}

"""
Builder.load_string(KV)

class Topup(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'
    def __init__(self, **kwargs):
        super(Topup, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)


    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def dropdown(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["users_phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(users_account_phone=phone)
            bank_names_str = [str(row['users_account_bank_name']) for row in bank_names]
            print(bank_names_str)
            if bank_names_str:
                # Create the menu list dynamically based on the fetched bank names
                self.menu_list = [
                    {"viewclass": "OneLineListItem", "text": bank_name,
                     "on_release": lambda x=bank_name: self.test(x)}
                    for bank_name in bank_names_str
                ]

                # Create and open the dropdown menu
                self.menu = MDDropdownMenu(
                    caller=self.ids.bank_dropdown,
                    items=self.menu_list,
                    width_mult=4
                )
                self.menu.open()
            else:
                # toast("No accounts found")
                self.manager.show_notification('Alert!','No accounts found.')

        except Exception as e:
            print(f"Error fetching bank names: {e}")
            self.manager.show_notification('Alert!','An error occured. Please try again.')

        finally:
            # No need to close a connection in Firebase Realtime Database
            pass

    def test(self, text):
        self.account_number = None
        self.ids.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["users_phone"]

        try:
            # Call the server function to fetch account details and update dropdown
            matching_accounts = app_tables.wallet_users_account.search(users_account_phone=phone, users_account_bank_name=text)
            account = [str(row['users_account_number']) for row in matching_accounts]
            if matching_accounts:
                # Fetch the account number from the first matching account
                self.account_number = account[0]
                print(self.account_number)
            else:
                # toast("Account not found")
                self.manager.show_notification('Alert!', 'Account not found.')

            self.menu.dismiss()

        except Exception as e:
            print(f"Error fetching account number: {e}")
            self.manager.show_notification('Alert!','An error occured. Please try again.')


    def add_money(self):
        topup_scr = self.manager.get_screen('topup')
        amount = float(topup_scr.ids.amount_field.text)
        bank_name = topup_scr.ids.bank_dropdown.text
        date = datetime.now()
        currency = topup_scr.ids.currency_spinner.text
        rate_response = self.currency_rate(currency, amount)
        print(rate_response)
        if 'response' in rate_response and rate_response['meta']['code'] == 200:
            # Access the 'value' from the 'response' dictionary
            self.exchange_rate_value = rate_response['response']['value']
            print(f"The exchange rate value is: {self.exchange_rate_value}")
        else:
            print("Error fetching exchange rates.")
            self.manager.show_notification('Alert!','An error occured. Please try again.')
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["users_phone"]
        balance_table = app_tables.wallet_users_balance.get(users_balance_phone=phone, users_balance_currency_type=currency)
        print(balance_table)
        # Check if the amount is within the specified range
        if 500 <= amount <= 100000:
            if balance_table is None:
                app_tables.wallet_users_balance.add_row(
                    users_balance_currency_type=currency,
                    users_balance=self.exchange_rate_value,
                    users_balance_phone=phone
                )
            else:
                if balance_table["users_balance"] is not None:
                    new_e_money = self.exchange_rate_value + balance_table['users_balance']
                    balance_table['users_balance'] = new_e_money
                    balance_table.update()
                else:
                    new_e_money = self.exchange_rate_value
                    balance_table['users_balance'] = new_e_money
                    balance_table.update()
            try:
                app_tables.wallet_users_transaction.add_row(
                    users_transaction_receiver_phone=float(self.account_number),
                    users_transaction_phone=phone,
                    users_transaction_fund=self.exchange_rate_value,
                    users_transaction_date=date,
                    users_transaction_type="Credit",
                    users_transaction_currency = currency
                )
                # Show a success toast
                # toast("Money added successfully.")
                self.manager.show_notification('Success','Money added successfully.')
                self.manager.current = 'dashboard'
                self.manager.show_balance()

            except Exception as e:
                print(f"Error adding money: {e}")
                # toast("An error occurred. Please try again.")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')

        else:
            # Show an error toast
            # toast("Invalid amount. Please enter an amount between 500 and 100000.")
            self.manager.show_notification('Alert!','Invalid amount. Please enter an amount between 500 and 100000.')

    def currency_rate(self, currency_type, money):
        # Set API Endpoint and access key (replace 'API_KEY' with your actual API key)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'

        # Set base currency and any other parameters (replace 'USD' with your desired base currency)
        base_currency = 'INR'
        target_currency = currency_type  # Replace with your desired target currency

        # Build the URL
        url = f'https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={currency_type}&amount={money}&api_key={api_key}'

        try:
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Decode JSON response
            exchange_rates = response.json()

            return exchange_rates

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')
            

        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')