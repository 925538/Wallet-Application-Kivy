from anvil.tables import app_tables
from datetime import datetime, timezone
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.uix.switch import Switch
from kivy.app import App
import requests
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.factory import Factory
from kivy.uix.anchorlayout import AnchorLayout
from kivy.base import EventLoop
Builder.load_string(
    """
<AutoTopupScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.1
        pos_hint: {"top":1}

        MDTopAppBar:
            title: 'Auto Topup'
            anchor_title:'left'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [['dots-vertical', lambda x: root.show_menu(x)]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            #pos_hint:{'top':1}
        MDBoxLayout:
            orientation: 'vertical'

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        pos_hint: {"top":1.42} 

    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.25 
        pos_hint: {"top":1.08} 
        #md_bg_color: "fefe16" 

        MDRectangleFlatButton:
            id: currency_dropdown
            text: "Select Currency"
            theme_text_color: "Custom"  # Disable theme color
            text_color: 0,0,0,1
            line_color: 0.5, 0.5, 0.5, 1 
            size_hint: 0.9, None
            size: dp(100), dp(48)
            pos_hint: {"center_x": 0.5}
            on_release: root.currencyDropdown()
            #md_bg_color:(1, 1, 1, 1)
    MDBoxLayout:
        padding: dp(20)
        orientation: 'horizontal'
        spacing: dp(20)
        #adaptive_height: True
        #pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        pos_hint: {"top":1.72}

        MDFlatButton:
            id: toggle_card
            text: 'Minimum balance topup'
            theme_text_color: "Custom"  # Disable theme color
            text_color: 0,0,0,1     #20/255, 142/255, 254/255, 1
            md_bg_color: (1, 1, 1, 1)
            line_color: 0.5, 0.5, 0.5, 1 
            size_hint: 0.7, None  # Set the size_hint_x to 1 to fill the width
            size: dp(80), dp(5)
            on_press: root.toggle_card_visibility()

        MDFlatButton:
            id: toggle_button
            text: 'Timely topup'
            theme_text_color: "Custom"  # Disable theme color
            text_color: 0,0,0,1      #20/255, 142/255, 254/255, 1
            md_bg_color: (1, 1, 1, 1)
            line_color: 0.5, 0.5, 0.5, 1
            size_hint: 0.7, None  # Set the size_hint_x to 1 to fill the width
            height: dp(5)
            on_press: root.toggle_button_visibility()                    

<SetOnOffScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Topup Settings'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                ScrollView:
                    BoxLayout: 
                        orientation:'vertical'
                        size_hint_y: None
                        height: dp(70)
                        pos_hint: {'center_x': 0.45, 'y': 100}        
                        GridLayout:
                            id:grid
                            cols:2
                            # orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            TwoLineAvatarIconListItem:
                                id:twoline
                                text: 'Auto-Topup'
                                secondary_text: "If turned off, you won't be able to topup automatically" 
                                # divider:None
                        MDSeparator:
                            size_hint_y:None
                            height:dp(1)
                                


""")


class AutoTopupScreen(Screen):
    def __init__(self, **kwargs):
        super(AutoTopupScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def go_back(self):
        existing_screen = self.manager.get_screen('auto_topup')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)
    
    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def update_amount(self, amount):
        self.ids.balance.text = str(amount)

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
            print(f"API URL: {url}")
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Decode JSON response
            exchange_rates = response.json()
            print(f"Response: {exchange_rates}")

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
    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]
        print(button)
        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    menu = None  # Add this line to declare the menu attribute
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
        # Convert the total balance to the selected currency

        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def currencyDropdown(self):
        try:
            # Manually set currencies
            currencies = ["INR", "USD", "EUR", "GBP", "JPY", "AUD"]

            # Create the menu list dynamically based on the fetched currencies
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": currency,
                 "on_release": lambda x=currency: self.selected_currency(x)}
                for currency in currencies
            ]

            # Create and open the dropdown menu
            self.menu = MDDropdownMenu(
                caller=self.ids.currency_dropdown,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching currencies: {e}")

    def selected_currency(self, currency):
        autotopup_scr = self
        autotopup_scr.ids.currency_dropdown.text = currency
        self.menu.dismiss()
        print(currency)

    def on_enter(self):
        self.auto_topup_card = None

    def on_leave(self):
        if self.auto_topup_card is not None:
            self.remove_widget(self.auto_topup_card)
            self.auto_topup_card = None
        self.ids.toggle_button.disabled = False
        self.ids.toggle_card.disabled = False

    def toggle_card_visibility(self):
        self.ids.toggle_button.disabled = True
        if self.auto_topup_card is None:
            # Create and add AutoTopupCard widget if not already created
            self.auto_topup_card = AutoTopupCard()
            self.auto_topup_card.manager = self.manager
            self.add_widget(self.auto_topup_card)
            self.auto_topup_card.height = dp(285)
            self.auto_topup_card.opacity = 1
            self.auto_topup_card.is_visible = True

        else:
            self.remove_widget(self.auto_topup_card)
            self.auto_topup_card = None
            self.ids.toggle_button.disabled = False

    def toggle_button_visibility(self):
        self.ids.toggle_card.disabled = True
        if self.auto_topup_card is None:
            # Create and add AutoTopupCard widget if not already created
            self.auto_topup_card = ScheduledTopupCard()
            self.auto_topup_card.manager = self.manager
            self.add_widget(self.auto_topup_card)
            self.auto_topup_card.height = dp(285)
            self.auto_topup_card.opacity = 1
            self.auto_topup_card.is_visible = True
        else:
            # Remove the AutoTopupCard widget if it's already created
            self.remove_widget(self.auto_topup_card)
            self.auto_topup_card = None
            self.ids.toggle_card.disabled = False

    def show_menu(self, instance):
        menu_items = [
            {
                "text": "change settings",
                "on_release": lambda x=instance: self.go_to(),
            }
        ]
        self.menu = MDDropdownMenu(items=menu_items)
        self.menu.caller = instance  # Set the button that triggered the menu
        self.menu.open()

    def go_to(self):
        self.manager.add_widget(Factory.SetOnOffScreen(name='set_on_off'))
        self.manager.current = 'set_on_off'
        self.menu.dismiss()


class AutoTopupCard(MDCard):
    is_visible = BooleanProperty(False)
    money_dropdown = None
    balance = None

    def __init__(self, manager=None, show_error_popup=None, **kwargs):
        self.manager = manager
        self.show_error_popup = show_error_popup
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.9, None)
        self.height = dp(250)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.50}
        self.elevation = 1
        self.shadow_softness = 12
        self.shadow_offset = 10, -12
        self.shadow_color = 0, 0, 0, 0.3
        self.line_color = colors['Gray']['500']
        self.radius = [20, 20, 20, 20]
        self.padding = dp(10)
        self.spacing = dp(0)
        self.md_bg_color = 1,1,1,1

        label_1_box_layout = MDBoxLayout(padding=dp(3), spacing=dp(0), adaptive_height=True,
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label_1 = MDLabel(text='When wallet balance goes below', halign='left', valign='top',
                          size_hint_y=None, pos_hint={'center_y': 0.15})
        label_1.text_color = (0, 0, 0, 1)
        label_1.padding = (dp(4), dp(3), 0, dp(21))
        label_1.height = label_1.texture_size[1]
        self.add_widget(label_1_box_layout)
        self.add_widget(label_1)

        money_dropdown_box_layout = MDBoxLayout(padding=(dp(1), dp(3), dp(1), dp(15)), spacing=dp(65), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 1})  # Add padding top and bottom
        money_dropdown = MDRectangleFlatButton(text="Select money", halign="center", padding=dp(2),
                                               size_hint=(0.5, None), size=(dp(100), dp(30)),
                                               pos_hint={"center_x": 0.5})
        money_dropdown.md_bg_color = (1, 1, 1, 1)  # Setting background color to white
        money_dropdown.radius = [10, 10, 10, 10]
        money_dropdown.text_color = (0, 0, 0, 1)
        money_dropdown.line_color = (0.5, 0.5, 0.5, 1)
        money_dropdown.bind(on_release=lambda x: self.moneyDropdown(money_dropdown))
        money_dropdown_box_layout.add_widget(money_dropdown)
        self.add_widget(money_dropdown_box_layout)
        self.money_dropdown = money_dropdown  # Store a reference to the money_dropdown widget

        label_2_box_layout = MDBoxLayout(padding=dp(3), spacing=dp(0), adaptive_height=True,
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label_2 = MDLabel(text='Automatically Add', halign='left', valign='top',
                          size_hint_y=None, pos_hint={'center_y': 0.85})
        label_2.text_color = (0, 0, 0, 1)
        label_2.padding = (dp(4), dp(5), 0, dp(23))
        label_2.height = label_2.texture_size[1]
        self.add_widget(label_2_box_layout)
        self.add_widget(label_2)

        balance_box_layout = MDBoxLayout(padding=dp(3), spacing=dp(5), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5}) # Add padding top and bottom
        balance = MDTextField(halign='center', readonly=False)
        balance.mode = "rectangle"
        balance.height = dp(5)
        balance.padding = (0, dp(40), 0, dp(41))
        balance.fill_mode = True
        balance.radius = [10, 10, 10, 10]
        balance.fill_color_normal = "#ffffff"
        balance.theme_text_color = "Custom"
        balance.line_color = 0.5, 0.5, 0.5, 1
        balance_box_layout.add_widget(balance)
        self.add_widget(balance_box_layout)
        self.balance = balance  # Store a reference to the balance widget

        box_layout_3 = MDBoxLayout(padding=dp(3), spacing=dp(5), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(box_layout_3)

        self.add_buttons(box_layout_3)

        box_layout_4 = MDBoxLayout(padding=dp(3), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(box_layout_4)
        self.create_bank_dropdown(box_layout_4)

        box_layout_5 = MDBoxLayout(padding=dp(3), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(box_layout_5)
        self.add_proceed(box_layout_5)

    def add_buttons(self, parent_layout):
        button_texts = ['+100', '+200', '+500', '+1000']
        for text in button_texts:
            button_1 = MDFlatButton(text=text, size_hint=(1, None), height=dp(1), width=dp(10))
            button_1.theme_text_color = "Custom"
            button_1.text_color = (1, 1, 1, 1)
            button_1.md_bg_color = "#148EFE"
            button_1.bind(on_release=self.update_balance)
            parent_layout.add_widget(button_1)

    def create_bank_dropdown(self, parent_layout):
        bank_dropdown = MDFlatButton(text='Select bank')
        bank_dropdown.theme_text_color = "Custom"
        bank_dropdown.text_color = (0, 0, 0, 1)
        bank_dropdown.md_bg_color = (1, 1, 1, 1)
        bank_dropdown.line_color = (0.5, 0.5, 0.5, 1)
        bank_dropdown.size_hint = (1, None)
        bank_dropdown.height = dp(5)
        bank_dropdown.bind(on_release=lambda x: self.dropdown(bank_dropdown))
        parent_layout.add_widget(bank_dropdown)
        self.bank_dropdown = bank_dropdown

    def add_proceed(self, parent_layout):
        button_2 = MDFlatButton(text='Proceed to add')
        button_2.theme_text_color = "Custom"
        button_2.text_color = (1, 1, 1, 1)
        button_2.md_bg_color = "#148EFE"
        button_2.size_hint = (1, None)
        button_2.height = dp(50)
        button_2.bind(on_release=self.minimum_balance_topup)
        parent_layout.add_widget(button_2)

    def moneyDropdown(self, button):
        try:
            # Manually set currencies
            moneys = ["50", "100", "200", "500", "1000"]

            # Create the menu list dynamically based on the fetched currencies
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": money,
                 "on_release": lambda x=money: self.selected_money(x)}
                for money in moneys
            ]

            # Create and open the dropdown menu
            self.menu = MDDropdownMenu(
                caller=button,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching moneys: {e}")

    def selected_money(self, money):
        # Access the stored reference to the money_dropdown widget
        if self.money_dropdown:
            self.money_dropdown.text = money
            self.menu.dismiss()
            print(money)

    def dropdown(self, button):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
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
                    caller=button, #self.ids.bank_dropdown,
                    items=self.menu_list,
                    width_mult=4
                )
                self.menu.open()
            else:
                # toast("No accounts found")
                self.manager.show_notification('Alert!','No accounts found.')

        except Exception as e:
            print(f"Error fetching bank names: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

        finally:
            # No need to close a connection in Firebase Realtime Database
            pass

    def test(self, text):
        self.account_number = None
        self.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        try:
            # Call the server function to fetch account details and update dropdown
            matching_accounts = app_tables.wallet_users_account.search(phone=phone, bank_name=text)
            account = [str(row['account_number']) for row in matching_accounts]
            if matching_accounts:
                # Fetch the account number from the first matching account
                self.account_number = account[0]
                print(self.account_number)
            else:
                # toast("Account not found")
                self.manager.show_notification('Alert!','Account not found.')
            if self.menu:
                self.menu.dismiss()

        except Exception as e:
            print(f"Error fetching account number: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')


    def update_balance(self, button):
        amount_with_sign = button.text
        amount = ''.join(filter(str.isdigit, amount_with_sign))
        if self.balance:
            self.balance.text = amount

    def minimum_balance_topup(self, event):
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        user_table = app_tables.wallet_users.get(phone=phone)
        if user_table['auto_topup'] == True:
            money = self.balance.text
            amount = float(money)
            selected_money = self.money_dropdown.text
            date = datetime.now()
            currency_dropdown = self.parent.ids.currency_dropdown
            currency = currency_dropdown.text
            rate_response = self.currency_rate(currency, amount)
            print(rate_response)
            if 'response' in rate_response and rate_response['meta']['code'] == 200:
                # Access the 'value' from the 'response' dictionary
                self.exchange_rate_value = rate_response['response']['value']
                print(f"The exchange rate value is: {self.exchange_rate_value}")
            else:
                print("Error fetching exchange rates.")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]
            balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
            print(balance_table)

            try:
                if balance_table is not None:
                    old_balance = balance_table['balance']
                    user_table['minimum_topup'] = True
                    if old_balance < int(selected_money):
                        new_balance = old_balance + self.exchange_rate_value
                        balance_table['balance'] = new_balance
                        print(f'{new_balance}')
                        balance_table.update()
                        # toast("Minimum-Topup Successful.", duration=5)
                        self.manager.show_notification('Success','Minimum-Topup Successful.')
                        app = App.get_running_app()
                        app.root.current = 'dashboard'
                    else:
                        user_table['minimum_topup'] = False
                        # toast("Auto-topup is not required.")
                        self.manager.show_notification('Alert!','Auto-topup is not required.')
                else:
                    # toast(f"Insufficient balance in currency {currency}")
                    self.manager.show_notification('Alert!', f"Insufficient balance in currency {currency}")
                app_tables.wallet_users_transaction.add_row(
                    receiver_phone=None,
                    phone=phone,
                    fund=self.exchange_rate_value,
                    date=date,
                    transaction_type=f"{currency} - Credit",
                    transaction_status="Minimum-Topups",
                    currency = currency
                )

                # try:
                #     app = App.get_running_app()
                #     app.root.current = 'dashboard'
                # except AttributeError:
                #     print("Error: Could not find screen manager to navigate.")
                # self.balance.text = ""
            except Exception as e:
                print(f"Error minimum-topup money: {e}")
                # self.show_error_popup("An error occurred. Please try again.")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')
                self.balance.text = ""
        else:
            # toast("Please enable the auto-topup switch to proceed.")
            self.manager.show_notification('Alert!','Please enable the auto-topup switch to proceed.')

    def update_amount(self, amount):
        self.balance.text = str(amount)

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
            print(f"API URL: {url}")
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Decode JSON response
            exchange_rates = response.json()
            print(f"Response: {exchange_rates}")

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

class ScheduledTopupCard(MDCard):
    is_visible = BooleanProperty(False)
    frequency_dropdown = None
    balance = None

    def __init__(self, manager=None, show_error_popup=None, **kwargs):
        self.manager = manager
        self.show_error_popup = show_error_popup
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.9, None)
        self.height = dp(250)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.50}
        self.elevation = 1
        self.shadow_softness = 12
        self.shadow_offset = 10, -12
        self.shadow_color = 0, 0, 0, 0.3
        self.line_color = colors['Gray']['500']
        self.radius = [20, 20, 20, 20]
        self.padding = dp(10)
        self.spacing = dp(0)
        self.md_bg_color = 1, 1, 1, 1

        label_1_box_layout = MDBoxLayout(padding=dp(3), spacing = dp(0), adaptive_height = True,
        pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        label_1 = MDLabel(text='When wallet balance automatically added', valign='top',
                          size_hint_y=None, pos_hint={'center_y': 0.85})
        label_1.text_color = (0, 0, 0, 1)
        label_1.padding = (dp(4),dp(3),0,dp(21))
        label_1.height = label_1.texture_size[1]
        self.add_widget(label_1_box_layout)
        self.add_widget(label_1)

        frequency_dropdown_box_layout = MDBoxLayout(padding=(dp(1), dp(3), dp(1), dp(15)), spacing=dp(65), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 1})  # Add padding top and bottom
        frequency_dropdown = MDRectangleFlatButton(text="Select interval", halign="center", padding=dp(2),
                                                   size_hint=(0.5, None), size=(dp(100), dp(30)),
                                                   pos_hint={"center_x": 0.5})
        frequency_dropdown.md_bg_color = (1, 1, 1, 1)  # Setting background color to white
        frequency_dropdown.radius = [10, 10, 10, 10]
        frequency_dropdown.text_color = (0, 0, 0, 1)
        frequency_dropdown.line_color = (0.5, 0.5, 0.5, 1)
        frequency_dropdown.bind(on_release=lambda x: self.frequencyDropdown(frequency_dropdown))
        frequency_dropdown_box_layout.add_widget(frequency_dropdown)
        self.add_widget(frequency_dropdown_box_layout)
        self.frequency_dropdown = frequency_dropdown  # Store a reference to the frequency_dropdown widget

        label_2_box_layout = MDBoxLayout(padding=dp(3), spacing=dp(0), adaptive_height=True,
                                         pos_hint={'center_x': 0.5, 'center_y': 0.5})
        label_2 = MDLabel(text='Automatically Add', halign='left', valign='top',
                          size_hint_y=None, pos_hint={'center_y': 0.85})
        label_2.text_color = (0, 0, 0, 1)
        label_2.padding = (dp(4), dp(5), 0, dp(23))
        label_2.height = label_2.texture_size[1]
        self.add_widget(label_2_box_layout)
        self.add_widget(label_2)

        balance_box_layout = MDBoxLayout(padding=dp(3), spacing=dp(5), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        balance = MDTextField(halign='center', readonly=False)
        balance.mode = "rectangle"
        balance.height = dp(5)
        balance.padding = (0, dp(40), 0, dp(41))
        balance.fill_mode = True
        balance.radius = [10, 10, 10, 10]
        balance.fill_color_normal = "#ffffff"
        balance.theme_text_color = "Custom"
        balance.line_color = (0.5, 0.5, 0.5, 1)  # Set border color to black
        balance_box_layout.add_widget(balance)
        self.add_widget(balance_box_layout)
        self.balance = balance  # Store a reference to the balance widget

        box_layout_3 = MDBoxLayout(padding=dp(3), spacing=dp(5), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(box_layout_3)

        self.add_buttons(box_layout_3)

        # Create a separate box layout for bank dropdown
        box_layout_4 = MDBoxLayout(padding=dp(3), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(box_layout_4)
        self.create_bank_dropdown(box_layout_4)

        # Create a separate box layout for proceed button
        proceed_layout = MDBoxLayout(padding=dp(3), adaptive_height=True,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_proceed(proceed_layout)
        self.add_widget(proceed_layout)

    def add_buttons(self, parent_layout):
        button_texts = ['+100', '+200', '+500', '+1000']
        for text in button_texts:
            button_1 = MDFlatButton(text=text, size_hint=(1, None), height=dp(1), width=dp(10))
            button_1.theme_text_color = "Custom"
            button_1.text_color = (1, 1, 1, 1)
            button_1.md_bg_color = "#148EFE"
            button_1.bind(on_release=self.update_balance)
            parent_layout.add_widget(button_1)

    def create_bank_dropdown(self, parent_layout):
        bank_dropdown = MDFlatButton(text='Select bank')
        bank_dropdown.theme_text_color = "Custom"
        bank_dropdown.md_bg_color = (1, 1, 1, 1)
        bank_dropdown.text_color = (0, 0, 0, 1)
        bank_dropdown.line_color = (0.5, 0.5, 0.5, 1)
        bank_dropdown.size_hint = (1, None)
        bank_dropdown.height = dp(5)
        bank_dropdown.bind(on_release=lambda x: self.dropdown(bank_dropdown))
        parent_layout.add_widget(bank_dropdown)
        self.bank_dropdown = bank_dropdown

    def add_proceed(self, parent_layout):
        button_2 = MDFlatButton(text='Proceed to add')
        button_2.theme_text_color = "Custom"
        button_2.text_color = (1, 1, 1, 1)
        button_2.md_bg_color = "#148EFE"
        button_2.size_hint = (1, None)
        button_2.height = dp(15)
        button_2.bind(on_release=self.timely_topup)
        parent_layout.add_widget(button_2)

    def frequencyDropdown(self, button):
        try:
            # Manually set currencies
            frequencys = ["Every Week", "Every Month", "Every 3 Months", "Every 6 Months"]

            # Create the menu list dynamically based on the fetched currencies
            self.menu_list = [
                {"viewclass": "OneLineListItem", "text": money,
                 "on_release": lambda x=money: self.selected_frequency(x)}
                for money in frequencys
            ]

            # Create and open the dropdown menu
            self.menu = MDDropdownMenu(
                caller=button,
                items=self.menu_list,
                width_mult=4
            )
            self.menu.open()
        except Exception as e:
            print(f"Error fetching frequencys: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

    def selected_frequency(self, money):
        if self.frequency_dropdown:
            self.frequency_dropdown.text = money
            self.menu.dismiss()
            print(money)

    def dropdown(self, button):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            bank_names_str = [str(row['bank_name']) for row in bank_names]
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
                    caller=button,
                    items=self.menu_list,
                    width_mult=4
                )
                self.menu.open()
            else:
                # toast("No accounts found")
                self.manager.show_notification('Alert!','No accounts found.')

        except Exception as e:
            print(f"Error fetching bank names: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

        finally:
            # No need to close a connection in Firebase Realtime Database
            pass

    def test(self, text):
        self.account_number = None
        self.bank_dropdown.text = text
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        try:
            # Call the server function to fetch account details and update dropdown
            matching_accounts = app_tables.wallet_users_account.search(phone=phone, bank_name=text)
            account = [str(row['account_number']) for row in matching_accounts]
            if matching_accounts:
                # Fetch the account number from the first matching account
                self.account_number = account[0]
                print(self.account_number)
            else:
                # toast("Account not found")
                self.manager.show_notification('Alert!','Account not found.')
            if self.menu:
                self.menu.dismiss()

        except Exception as e:
            print(f"Error fetching account number: {e}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

    def update_balance(self, button):
        amount_with_sign = button.text
        amount = ''.join(filter(str.isdigit, amount_with_sign))
        if self.balance:
            self.balance.text = amount

    def timely_topup(self, event):
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        user_table = app_tables.wallet_users.get(phone=phone)
        if user_table['auto_topup'] == True:
            money = self.balance.text
            amount = float(money)
            selected_frequency = self.frequency_dropdown.text
            current_datetime = datetime.now().replace(tzinfo=timezone.utc)
            date = datetime.now()
            currency_dropdown = self.parent.ids.currency_dropdown
            currency = currency_dropdown.text
            rate_response = self.currency_rate(currency, amount)
            print(rate_response)
            if 'response' in rate_response and rate_response['meta']['code'] == 200:
                # Access the 'value' from the 'response' dictionary
                self.exchange_rate_value = rate_response['response']['value']
                print(f"The exchange rate value is: {self.exchange_rate_value}")
            else:
                print("Error fetching exchange rates.")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]
            balance_table = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency)
            print(balance_table)
            user_table = app_tables.wallet_users.get(phone=phone)

            try:
                # Calculate the time interval based on the frequency
                if selected_frequency == "Every Week":
                    print(selected_frequency)
                    interval_days = 7
                elif selected_frequency == "Every Month":
                    print(selected_frequency)
                    interval_days = 30
                elif selected_frequency == "Every 3 Months":
                    print(selected_frequency)
                    interval_days = 90
                elif selected_frequency == "Every 6 Months":
                    print(selected_frequency)
                    interval_days = 180
                else:
                    interval_days = 0

                try:
                    if user_table is not None:
                        if (user_table['last_auto_topup_time'] is None) or (
                                (current_datetime - user_table['last_auto_topup_time']).days >= interval_days):
                            user_table['timely_topup'] = True
                            user_table['timely_topup_interval'] = selected_frequency
                            old_balance = balance_table['balance']
                            new_balance = old_balance + self.exchange_rate_value
                            balance_table['balance'] = new_balance
                            balance_table.update()
                            # toast("Timely-Topup Successful.", duration=5)
                            self.manager.show_notification('Success','Timely-Topup successful.')
                            app_tables.wallet_users_transaction.add_row(
                                receiver_phone=None,
                                phone=phone,
                                fund=self.exchange_rate_value,
                                date=current_datetime,
                                transaction_type=f"{currency} - Credit",
                                transaction_status="Timely-Topups",
                                currency = currency
                            )
                            user_table['last_auto_topup_time'] = current_datetime
                            try:
                                app = App.get_running_app()
                                app.root.current = 'dashboard'
                            except AttributeError:
                                print("Error: Could not find screen manager to navigate.")
                                self.manager.show_notification('Alert!','An error occurred. Please try again.')
                            self.balance.text = ""
                        else:
                            # toast("Auto-topup is not required.")
                            self.manager.show_notification('Alert!','Aotu-topup is not required')
                            self.manager.current = 'dashboard'
                            self.balance.text = ""
                    else:
                        print("Error: No matching accounts found for the user or invalid account number.")
                        self.manager.show_notification('Alert!','No matching accounts found for the user or invalid account number.')


                except:
                    pass
            except Exception as e:
                print(f"Error timely-topup money: {e}")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')
                self.balance.text = ""
        else:
            # toast("Please enable the auto-topup switch to proceed.")
            self.manager.show_notification('Alert!','Please enable the auto-topup switch to proceed.')

    def update_amount(self, amount):
        self.balance.text = str(amount)

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
            print(f"API URL: {url}")
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Decode JSON response
            exchange_rates = response.json()
            print(f"Response: {exchange_rates}")

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

class SetOnOffScreen(Screen):
    def __init__(self, **kwargs):
        super(SetOnOffScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        user_table = app_tables.wallet_users.get(phone=phone)
        if user_table['auto_topup'] == True:
            button_text = 'ON'
            button_color = (0, 0.7, 1, 1)  # Blue color
        else:
            button_text = 'OFF'
            button_color = (0.5, 0.5, 0.5, 1)  # Grey color

        # self.box_layout = BoxLayout(
        #     orientation='vertical',
        #     padding=(dp(20), dp(20)),
        #     pos_hint={"top": 1.77}
        # )

        # Button Layout
        # self.button_layout = BoxLayout(
        #     size_hint=(1, None),
        #     height=dp(50),
        #     pos_hint={"top": 1, "right": 1}
        # )
        # Button
        self.auto_topup_button = Button(
            text=button_text,
            size_hint=(None, None),
            size=(dp(60), dp(30)),
            pos_hint={'center_x':0.5,'center_y':0.5},
            background_normal='',
            background_color=button_color,
            bold = True
        )
        self.auto_topup_button.bind(on_press=self.toggle_auto_topup)
        # self.box_layout.add_widget(self.auto_topup_button)
        # self.box_layout.add_widget(self.button_layout)
        # self.add_widget(self.box_layout)
        self.anchor_layout = AnchorLayout(size_hint_x=None,
                    width=dp(100))
        self.anchor_layout.add_widget(self.auto_topup_button)
        self.ids.grid.add_widget(self.anchor_layout)

    def toggle_auto_topup(self, instance):
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]
        user_table = app_tables.wallet_users.get(phone=phone)

        if user_table['auto_topup'] == True:
            user_table['auto_topup'] = False
            self.auto_topup_button.text = 'OFF'
            self.auto_topup_button.background_color = (0.5, 0.5, 0.5, 1)
            print("Auto top-up disabled")
        else:
            user_table['auto_topup'] = True
            self.auto_topup_button.text = 'ON'
            self.auto_topup_button.background_color = (0, 0.7, 1, 1)
            print("Auto top-up enabled")

    def go_back(self):
        self.manager.add_widget(Factory.AutoTopupScreen(name='autotopup'))
        self.manager.current = 'autotopup'

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False