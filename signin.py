import re
import sqlite3
from datetime import datetime
from anvil.tables import app_tables
from kivy.base import EventLoop
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.core.image import  Image as CoreImage
from io import BytesIO
from kivy.core.window import Keyboard

KV = """
<SignInScreen>:
    MDScreen:

        MDIconButton:
            icon: "close"
            pos_hint: {"top": 1, "left": 1}
            on_release: root.go_back()
            user_font_size: "100sp"
            theme_text_color: "Custom"
            text_color: rgba(53,56,64,255)

        Widget:
            size_hint_y: None
            height: '10dp'

        BoxLayout:
            size_hint_y: None
            height: self.minimum_height
            padding: "10dp"
            spacing: "20dp"
            orientation: 'vertical'

            MDLabel:
                text: "LOGIN"
                font_size: 46
                halign: "center"
                bold: True

            Widget:
                size_hint_y: None
                height: '0.5dp'

            MDTextField:
                id: input_text
                hint_text: "Mobile Number/Email ID"
                helper_text: "Enter your mobile number, user ID, or email ID"
                icon_left: "account"
                helper_text_mode: "on_focus"
                specific_text_color: "#ffffff"
                pos_hint: {"center_x": .5}
                multiline: False
                radius: (20, 20, 20, 20)
                mode: "rectangle"
                color_active: 1, 1, 1, 1
                normal_color: app.theme_cls.accent_color
                line_color_normal: colors['Gray']['500']

            MDTextField:
                id: password_input
                hint_text: "Password"
                helper_text: "Enter your password"
                specific_text_color: "#ffffff"
                icon_left: "lock"
                helper_text_mode: "on_focus"
                pos_hint: {"center_x": .5}
                multiline: False
                radius: (20, 20, 20, 20)
                mode: "rectangle"
                color_active: 1, 1, 1, 1
                normal_color: app.theme_cls.accent_color
                line_color_normal: colors['Gray']['500']

            MDTextButton:
                text: "     Forgot Password?"
                font_size: "12sp"
                bold: True
                halign: "left"
                theme_text_color: "Custom"
                text_color: 0.117, 0.459, 0.725, 1
                on_release: root.nav_reset()
                

            MDFillRoundFlatButton:
                text: "Login"
                pos_hint: {"center_x": .5}
                on_release: root.sign_in(input_text.text, password_input.text)
                size_hint: 1, None
                height: dp(48)

            Widget:
                size_hint_y: None
                height: '0.7dp'

            MDGridLayout:
                cols: 3
                size_hint: .8, None
                height: self.minimum_height
                pos_hint: {'center_x': .5}
            
                MDSeparator:
                    size_hint: (None, None)
                    width: self.parent.width / 3 - dp(10)
                    height: dp(1)
                    color: rgba(47, 144, 237, 255)
            
                MDLabel:
                    text: "OR"
                    font_size: "12sp"
                    halign: "center"
                    valign: "center"
                    # size_hint_y: None
                    # height: self.texture_size[1]
                    color: rgba(5, 5, 6, 255)
                    pos_hint:{"center_y":0.1}
            
                MDSeparator:
                    size_hint: (None, None)
                    width: self.parent.width / 3 - dp(10)
                    height: dp(1)
                    color: rgba(47, 144, 237, 255)
                                
            Widget:
                size_hint_y: None
                height: '2dp'
                

            MDLabel:
                text: "Social Media Login"
                # bold: True
                font_size: "13sp"
                halign: "center"
                color: rgba(5, 5, 6)

            Widget:
                size_hint_y: None
                height: "1dp"

            FloatLayout:

                MDIconButton:
                    icon: 'images/google.png'
                    user_font_size: '64sp'
                    pos_hint: {'center_x': 0.34, 'center_y': 0.5}
                    on_release: app.open_link()

                MDIconButton:
                    icon: 'images/facebook.png'
                    user_font_size: '64sp'
                    pos_hint: {'center_x': 0.50, 'center_y': 0.5}
                    on_release: app.open_link()
                    
                MDIconButton:
                    icon: 'images/instagram.jpg'
                    user_font_size: '64sp'
                    pos_hint: {'center_x': 0.66, 'center_y': 0.5}
                    on_release: app.open_link()
                    
            Widget:
                size_hint_y: None
                height: "0.7dp"

            BoxLayout:
                orientation: 'horizontal'
                size_hint: 1.1,None
                height: self.minimum_height
                spacing: dp(1) 
                Widget:
                    size_hint_x: None
                    height: '1dp'
                
                # Widget:
                #     size_hint_y: None
                #     height: dp(3)
                
                MDLabel:
                    text: "Dont have an account?"
                    font_size: "11sp"
                    theme_text_color: "Primary"
                    halign: 'right'
                    height: self.texture_size[1] + dp(2)
                    
                MDTextButton:
                    text: "  Sign Up"
                    font_size: "12sp"
                    halign: 'center'
                    underline:True
                    size_hint_y: None
                    height: self.texture_size[1] + dp(2)  # Adjust padding
                    bold:True
                    theme_text_color: "Custom"
                    text_color: 0.117, 0.459, 0.725, 1
                    on_press: root.nav_sign_up()
                    
                Widget:
                    size_hint_y: None
                    height: dp(10)


            Widget:
                size_hint_y: None
                height: dp(30)
"""

Builder.load_string(KV)


class SignInScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('signin')
        existing_screen.ids.input_text.text = ''
        existing_screen.ids.password_input.text = ''
        self.manager.add_widget(Factory.LandingScreen(name='landing'))
        self.manager.current = 'landing'
        self.manager.remove_widget(existing_screen)

    def init(self, **kwargs):
        super(SignInScreen, self).init(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def sign_in(self, input_text, password):
        date = datetime.now()
        if input_text == '' or password == '':
            # Show popup for required fields
            self.show_popup("All Fields are Required")
            # self.manager.show_notification('Alert!','All Fields are Required')
        else:
            try:
                if re.match(r'^\d{10}$', input_text):  # Phone number with 10 digits
                    self.user = app_tables.wallet_users.get(users_phone=float(input_text), users_password=password)
                elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', input_text):  # Email
                    self.user = app_tables.wallet_users.get(users_email=input_text, users_password=password)
                else:
                    self.manager.show_notification('Alert!','Invalid Email or Password.')
                    # self.manager.show_notification('Alert!','Invalid phone or email.')

                # Check if the user was found
                if self.user is None:
                    # Show popup for invalid user
                    self.manager.show_notification('Alert!','Invalid User.')
                    # self.manager.show_notification('Alert!','Invalid User.')
                else:
                    # Now 'user' contains the Anvil row
                    self.user.update(users_last_login=date)
                    user_data = dict(self.user)
                    user_data['users_profile_pic'] = None
                    user_data['users_last_login'] = str(user_data['users_last_login'])
                    self.user.update(users_last_login=date)
                    print(user_data)

                    if user_data['users_banned']:  # Check if user is banned
                        print("User is banned. Showing popup.")
                        # Show popup for banned user
                        self.show_popup(
                            "You have been banned due to some credential issue. Your amount will be debited to your account within 5 days.")
                        # self.manager.show_notification('Alert!','You have been banned due to some credential issue. Your amount will be debited to your account within 5 days.')
                    else:
                        # Proceed with login
                        # Show popup for successful login
                        # self.show_popup("Login Successful")

                        # for screen in self.manager.screens:
                        #     self.manager.remove_widget(screen)
                        # App.get_running_app().authenticated_user_number = row['phone']
                        existing_screen = self.manager.get_screen('signin')
                        self.manager.add_widget(Factory.DashBoardScreen(name='dashboard'))
                        dashboard = self.manager.get_screen('dashboard')
                        try:
                            image_stored = self.user['users_profile_pic']
                            if image_stored :
                                print('yes in users')
                                decoded_image_bytes =image_stored.get_bytes()
                                core_image =  CoreImage(BytesIO(decoded_image_bytes), ext='png',filename='image.png')
                                print(core_image)
                                dashboard.ids.user_image.texture = core_image.texture
                        except Exception as e:
                            print(e)
                        self.manager.current='dashboard'
                        self.manager.remove_widget(existing_screen)

                        # Save user data to JsonStore (if needed)
                        store = JsonStore('user_data.json')
                        store.put('user', value=user_data)
                        try:
                            conn = sqlite3.connect('wallet_database.db')
                            cursor = conn.cursor()
                            user = JsonStore('user_data.json').get('user')['value']
                            phone = user['users_phone']
                            username = user['users_username']
                            email = user['users_email']
                            password = user['users_password']
                            confirm_email = user['users_confirm_email']
                            aadhar_number = user['users_aadhar']
                            pan = user['users_pan']
                            address = user['users_address']
                            usertype = user['users_usertype']
                            banned = user['users_banned']
                            balance_limit = user['users_user_limit']
                            daily_limit = user['users_daily_limit']
                            last_login = user['users_last_login']

                            # Insert into wallet_users table
                            cursor.execute('''
                                   INSERT INTO wallet_users (phone, username, email, password, confirm_email, aadhar_number,
                                                            pan, address, usertype, banned, balance_limit, daily_limit, last_login)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               ''', (phone, username, email, password, confirm_email, aadhar_number,
                                     pan, address, usertype, banned, balance_limit, daily_limit, last_login))

                            conn.commit()
                            conn.close()
                        except Exception as e:
                            print(e)
                            # self.manager.show_notification('Alert!','An error occured. Please try again.')

            except Exception as e:
                print(e)
                # self.manager.show_notification('Alert!','An error occured. Please try again.')

    def show_popup(self, text):
        dialog = MDDialog(
            title="Alert",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                    # pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
            ]
        )
        dialog.open()
        self.ids.input_text.text = ''
        self.ids.password_input.text = ''

    def nav_reset(self):
        self.manager.add_widget(Factory.ResetPassword(name='reset'))
        self.manager.current = 'reset'

    def nav_sign_up(self):
        self.manager.add_widget(Factory.SignUpScreen(name='signup'))
        self.manager.current = 'signup'
