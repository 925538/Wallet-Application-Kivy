import anvil
import sys
import requests
from anvil.tables import app_tables
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from landing import LandingScreen
from dashboard import DashBoardScreen
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.uix.menu import MDDropdownMenu
from help import HelpScreen
from settings import SettingsScreen
from loadingScreen import loadingScreen
from contactus import ContactUsScreen
from noInternetScreen import NoInternetPage
from kivymd.uix.label import MDLabel
from kivy.uix.anchorlayout import AnchorLayout

class ScreenManagement(ScreenManager):
    current_user_data = None  # Class attribute to store the current user data

    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.transition = NoTransition()
        self.show_loading_screen()

    def show_loading_screen(self):
        self.clear_widgets()
        self.add_widget(Factory.loadingScreen(name='loading'))
        Clock.schedule_once(self.connect_to_anvil, 3)

    def connect_to_anvil(self, dt):
        try:
            # Check for internet connection
            requests.get("http://www.google.com", timeout=5)

            # If there is an internet connection, connect to Anvil server
            client = anvil.server.connect("server_7JA6PVL5DBX5GSBY357V7WVW-TLZI2SSXOVZCVYDM")# server_HCPXSEPK7H5QFVBH5DD4CAWG-CQAJC3TXYQYKC5WX

            # Schedule the login status check after 5 seconds
            Clock.schedule_once(self.check_login_status, 5)

        except requests.ConnectionError:
            # If no internet connection, navigate to the no-internet page
            self.add_widget(Factory.NoInternetPage(name='no_internet'))
            self.current = 'no_internet'



    def check_login_status(self, dt):
        try:
            store = JsonStore('user_data.json')
            self.remove_widget(self.get_screen('loading'))
            if 'user' in store:
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                print('yes')
                self.add_widget(Factory.DashBoardScreen(name='dashboard'))
                self.current = "dashboard"
                users = app_tables.wallet_users.get(phone = phone)
                try:
                    if users['profile_pic'] is not None:
                        self.current_screen.user_pic()
                except Exception as e:
                    print(e)
                self.get_username()
                #self.fetch_and_update_navbar()
                self.fetch_and_update_complaint()
                self.fetch_and_update_addPhone()
                #self.show_balance()
                # ... add other screens as needed
            else:
                self.add_widget(Factory.LandingScreen(name='landing'))
                self.current = "landing"
        except Exception as e:
            print(e)

    # def connect_to_server(self):
    #     if self.is_internet_connected():
    #         # If internet is connected, connect to the Anvil server
    #         self.anvil_server_connected = True
    #         self.client = anvil.server.connect("server_QVP7TBTIZPTLZZTXO5LN7GBD-2QQVRBJQQ5M7D6YM")
    #     else:
    #         # If no internet, use local database or show a popup
    #         self.anvil_server_connected = False
    #         toast("no internet connection", duration=3)
    #         # self.show_no_internet_popup()
    #         # Connect to local database (replace this with your local database code)
    #
    # def is_internet_connected(self):
    #     try:
    #         # Try to make a simple HTTP request to a known server (e.g., Anvil's server)
    #         response = requests.get("https://anvil.works")
    #         return response.status_code == 200
    #     except requests.ConnectionError:
    #         return False

    # checking users login statu

    def logout(self):
        # Remove the stored user data when logging out
        store = JsonStore('user_data.json')
        if 'user' in store:
            del store['user']

        try:
            store.clear()
        except Exception as e:
            print(f"Error deleting JSON file: {e}")

        # Clear all screens
        existing_screen = self.get_screen('dashboard')
        self.add_widget(Factory.LandingScreen(name='landing'))
        self.current = 'landing'
        self.remove_widget(existing_screen)
        # Navigate to the landing page


    def get_username(self):
        store = JsonStore('user_data.json')
        return store.get('user')['value']["username"]

    def nav_navbar(self):
        self.current = 'navbar'

    def nav_complaint(self):
        self.current = 'complaint'

    def fetch_and_update_complaint(self):
        # store = JsonStore('user_data.json').get('user')['value']
        # # Update labels in ComplaintScreen
        # complaint_screen = self.get_screen('complaint')
        # complaint_screen.ids.email_label.text = store["email"]
        pass

    def fetch_and_update_addPhone(self):
        # store = JsonStore('user_data.json').get('user')['value']
        # # Update labels in ComplaintScreen
        # addPhone_screen = self.get_screen('addphone')
        # # addPhone_screen.ids.contact_label.text = store["phone"]
        # addPhone_screen.current_user_phone = str(store["phone"])
        pass

    def nav_account(self):
        self.current = 'addaccount'


    def get_total_balance(self, phone, currency_type):
        try:
            acc_row = app_tables.wallet_users_balance.get(phone=phone, currency_type=currency_type)
            if acc_row:
                return acc_row['balance']
            else:
                return 0
        except Exception as e:
            print(f"Error fetching data from anvil Database: {e}")
            return 0

    def nav_settings(self):
        self.add_widget(Factory.SettingsScreen(name='settings'))
        self.current = 'settings'

    def show_success_popup(self, message):
        content = BoxLayout(orientation='vertical', spacing='10dp')
        content.add_widget(MDLabel(text=message, halign='center'))

        ok_button = Button(text='OK', size_hint=(None, None), size=('150dp', '50dp'))
        ok_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(ok_button)

        popup = Popup(
            title='Success',
            content=content,
            size_hint=(None, None),
            size=('300dp', '200dp'),
            auto_dismiss=True
        )
        popup.open()
        # self.current = 'dashboard'

    def nav_contactus(self):
        self.add_widget(Factory.ContactUsScreen(name='contactus'))
        self.current = 'contactus'

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', spacing='10dp')
        content.add_widget(MDLabel(text=message, halign='center'))

        ok_button = Button(text='OK', size_hint=(None, None), size=('150dp', '50dp'))
        ok_button.bind(on_press=lambda *args: popup.dismiss())
        content.add_widget(ok_button)

        popup = Popup(
            title='Error',
            content=content,
            size_hint=(None, None),
            size=('300dp', '200dp'),
            auto_dismiss=True
        )
        popup.open()

    def nav_accmanage(self):
        self.current = 'accmanage'

    def nav_userdetails(self):
        self.current = 'userdetails'

    def Add_Money(self):
        self.current = 'Wallet'
    def show_notification(self, title, message):
    # Create content layout
        content_layout = BoxLayout(orientation="vertical", padding="10dp",spacing = '5dp')

        # Create title label with bold font
        # title_label = MDLabel(text=text, font_size="20sp", bold=True, theme_text_color="Custom", text_color=(1, 1, 1, 1))

        # Create message label
        message_label = MDLabel(text=message, font_size=(150, None), halign="left", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        ok_button = Button(text='OK', size_hint=(None, None), size=('50dp', '30dp'))
        ok_button.bind(on_press=lambda *args: popup.dismiss())
        # Add labels to content layout
        anchor_layout = AnchorLayout(anchor_x='right')
        anchor_layout.add_widget(ok_button)\

        # Add labels and button to content layout
        # content_layout.add_widget(title_label)
        content_layout.add_widget(message_label)
        content_layout.add_widget(anchor_layout)

        # Create and display the notification popup
        popup = Popup(
            title=title,  # Remove default title
            content=content_layout,
            size_hint=(None, None),
            size=('250dp','250dp'),
            auto_dismiss=True,  # Close on touch outside the card
            background_color=(0.078, 0.557, 0.996, 1.0)
        )
        popup.open()
        return


class WalletApp(MDApp):
    def build(self):
        self.scr_mgr = ScreenManagement()
        # self.scr_mgr.check_login_status()
        # self.createTables()
        return self.scr_mgr

    # def createTables(self):
    #     # Connect to SQLite database (or create it if it doesn't exist)
    #     conn = sqlite3.connect('wallet_database.db')
    #     cursor = conn.cursor()
    #
    #     # Create the wallet_users table
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS wallet_users (
    #             phone INTEGER PRIMARY KEY,
    #             username TEXT,
    #             email TEXT,
    #             password TEXT,
    #             confirm_email BOOLEAN,
    #             aadhar_number INTEGER,
    #             pan TEXT,
    #             address TEXT,
    #             usertype TEXT,
    #             banned BOOLEAN,
    #             balance_limit INTEGER,
    #             daily_limit INTEGER,
    #             last_login DATE
    #         )
    #     ''')
    #
    #     # Create the wallet_users_account table
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS wallet_users_account (
    #             phone INTEGER,
    #             account_number INTEGER,
    #             account_holder_name TEXT,
    #             bank_name TEXT,
    #             branch_name TEXT,
    #             ifsc_code TEXT,
    #             account_type TEXT,
    #             FOREIGN KEY (phone) REFERENCES wallet_users(phone)
    #         )
    #     ''')
    #
    #     # Create the wallet_users_balance table
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS wallet_users_balance (
    #             phone INTEGER,
    #             currency_type TEXT,
    #             balance INTEGER,
    #             PRIMARY KEY (phone, currency_type),
    #             FOREIGN KEY (phone) REFERENCES wallet_users(phone)
    #         )
    #     ''')
    #
    #     # Create the wallet_users_transaction table
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS wallet_users_transaction (
    #             phone INTEGER,
    #             date DATETIME,
    #             fund INTEGER,
    #             transaction_type TEXT,
    #             transaction_status TEXT,
    #             FOREIGN KEY (phone) REFERENCES wallet_users(phone)
    #         )
    #     ''')
    #
    #     # Commit the changes and close the connection
    #     conn.commit()
    #     conn.close()


if __name__ == '__main__':
    WalletApp().run()
