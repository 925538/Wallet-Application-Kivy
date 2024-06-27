import os
import random
import re
import smtplib
import string
from _socket import gethostbyname
from random import randint
import anvil
import requests
from anvil.tables import app_tables
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivymd.uix.textfield import MDTextField
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from verify import VerifyScreen

KV = '''
<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'
        ScrollView:

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "20dp"
                orientation: 'vertical'

                MDIconButton:
                    icon: "close"
                    pos_hint: {"top": 1, "left": 1}
                    on_release: root.go_back()
                    user_font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: rgba(53,56,64,255)

                # Widget:
                #     size_hint_y: None
                #     height: '10dp'

                BoxLayout:
                    size_hint_y: None
                    height: self.minimum_height
                    padding: "1dp"
                    spacing: "20dp"
                    orientation: 'vertical'

                    MDLabel:
                        text: "Get Started"
                        font_size: 46
                        halign: "center"
                        bold: True


                    Widget:
                        size_hint_y: None
                        height: '0.5dp'

                MDTextField:
                    id: user_name
                    hint_text: "User Name"
                    helper_text: "Enter your user name"
                    # icon_left: "account"
                    helper_text_mode: "on_focus"
                    specific_text_color: "#ffffff"
                    pos_hint: {"center_x": .5}
                    multiline: False
                    radius: (20, 20, 20, 20)
                    mode: "rectangle"
                    color_active: 1, 1, 1, 1
                    normal_color: app.theme_cls.accent_color
                    line_color_normal: colors['Gray']['500']


                BoxLayout:

                    id:my_box
                    size_hint_y: None
                    height: self.minimum_height
                    # padding: "10dp"
                    spacing: "20dp"
                    orientation: 'vertical'    

                    MDTextField:   
                        id: gmail
                        hint_text: "Email"
                        helper_text: "Enter your email ID"
                        # icon_left: "email"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        pos_hint: {"center_x": .5}
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']


                    MDRectangleFlatButton:
                        text: "SEND OTP"
                        id: verify_button
                        pos_hint: {"center_x": .5,"center_y":0.4}
                        on_release: root.send_email()
                        size_hint: 1, None
                        height: dp(48)
                        radius: [40, 40, 40, 40]
                        md_bg_color: app.theme_cls.primary_color
                        opacity: 1
                        text_color: 1, 1, 1, 1
                        font_name: 'Roboto-Bold'
                        # disabled: True  # Initially disabled


                BoxLayout:

                    size_hint_y: None
                    height: self.minimum_height
                    # padding: "10dp"
                    spacing: "20dp"
                    orientation: 'horizontal'    

                    MDTextField:  

                        id: password
                        hint_text: "password"
                        helper_text: "Enter a password"
                        # icon_right: "eye-off"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        pos_hint: {"center_x": .5}
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']
                        password:True

                    MDTextField:  

                        id: input_text
                        hint_text: "retype password"
                        helper_text: "retype password"
                        # icon_right: "eye-off"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        pos_hint: {"center_x": .5}
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']
                        password:True

                MDTextField:  

                    id: phone_no
                    hint_text: "Phone Number"
                    helper_text: "Enter your Phone Number"
                    # icon_left: "phone"
                    helper_text_mode: "on_focus"
                    specific_text_color: "#ffffff"
                    pos_hint: {"center_x": .5}
                    multiline: False
                    radius: (20, 20, 20, 20)
                    mode: "rectangle"
                    color_active: 1, 1, 1, 1
                    normal_color: app.theme_cls.accent_color
                    line_color_normal: colors['Gray']['500']    


                BoxLayout:

                    size_hint_y: None
                    height: self.minimum_height
                    # padding: "10dp"
                    spacing: "20dp"
                    orientation: 'horizontal'    

                    MDTextField:  

                        id: aadhar_card
                        hint_text: "Aadhar Number"
                        helper_text: "Aadhar Card Number"
                        # icon_left: "aadhaar_icon"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        text_size:self.size
                        pos_hint: {"center_x": .5}
                        # size_hint_x: None
                        # width: self.parent.width - dp(58)
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']

                    MDTextField:  

                        id: pan_card
                        hint_text: "Pan Number"
                        helper_text: "Pan Card Number"
                        # icon_left: "pan_icon"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        pos_hint: {"center_x": .5}
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']

                BoxLayout:

                    size_hint_y: None
                    height: self.minimum_height
                    # padding: "10dp"
                    spacing: "20dp"
                    orientation: 'horizontal'    

                    MDTextField:  

                        id: address_1
                        hint_text: "Address 1"
                        helper_text: "Enter your address"
                        # icon_left: "map-marker"
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

                        id: address_2
                        hint_text: "Address 2"
                        helper_text: "Enter your address"
                        # icon_left: "map-marker"
                        helper_text_mode: "on_focus"
                        specific_text_color: "#ffffff"
                        pos_hint: {"center_x": .5}
                        multiline: False
                        radius: (20, 20, 20, 20)
                        mode: "rectangle"
                        color_active: 1, 1, 1, 1
                        normal_color: app.theme_cls.accent_color
                        line_color_normal: colors['Gray']['500']              


                Widget:
                    size_hint_y: None
                    height: '4dp'

                MDRectangleFlatButton:
                    id:confirm_id
                    text: "CONFIRM"
                    pos_hint: {"center_x":.5}
                    on_release: root.signup()
                    size_hint: 1, None
                    height: dp(48)
                    radius: [40, 40, 40, 40]
                    md_bg_color: app.theme_cls.primary_color
                    opacity: 1
                    text_color: 1, 1, 1, 1
                    font_name:'Roboto-Bold'
                    disabled:True

                # Widget:
                #     size_hint_y: None
                #     height: '2dp'    

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1.1,None
                    height: self.minimum_height
                    spacing: dp(1) 

                    Widget:
                        size_hint_x: None
                        height: '2dp'

                    Widget:
                        size_hint_x: None
                        width: dp(24)

                    MDLabel:
                        text: "By confirming you agree to all"
                        font_size: "10sp"
                        theme_text_color: "Primary"
                        halign: 'right'
                        height: self.texture_size[1] + dp(2)

                    MDTextButton:
                        text: " terms"
                        font_size: "11sp"
                        halign: 'center'
                        underline:True
                        size_hint_y: None
                        height: self.texture_size[1] + dp(2)  # Adjust padding
                        bold:True
                        theme_text_color: "Custom"
                        text_color: 0.117, 0.459, 0.725, 1
                        # on_press: 

                    Widget:
                        size_hint_y: None
                        height: dp(10)


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
                        text: "Already have an account?"
                        font_size: "10sp"
                        theme_text_color: "Primary"
                        halign: 'right'
                        height: self.texture_size[1] + dp(2)


                    MDTextButton:
                        text: "  Sign In"
                        font_size: "11sp"
                        halign: 'center'
                        underline:True
                        size_hint_y: None
                        height: self.texture_size[1] + dp(2)  # Adjust padding
                        bold:True
                        theme_text_color: "Custom"
                        text_color: 0.117, 0.459, 0.725, 1
                        on_press: root.nav_sign_in()

                    Widget:
                        size_hint_y: None
                        height: dp(10)


                Widget:
                    size_hint_y: None
                    height: dp(30)
                        #on_touch_down: root.manager.current = 'signin' if self.collide_point(*args[1].pos) else False



'''
Builder.load_string(KV)


class SignUpScreen(Screen):
    verification_state = "initial"
    email = StringProperty('')
    user_otp = StringProperty('')

    def go_back(self):
        existing_screen = self.manager.get_screen('signup')
        self.manager.current = 'landing'
        self.manager.remove_widget(existing_screen)

    def nav_verify(self):
        # Create a modal view for the loading animation
        self.current_screen = self.manager.get_screen('signup')
        self.email = self.current_screen.ids.gmail.text
        print(self.email)
        modal_view = ModalView(size_hint=(None, None), size=(300, 150), background_color=[0, 0, 0, 0])

        # Create a BoxLayout to hold the loading text
        box_layout = BoxLayout(orientation='vertical')

        # Create a label for the loading text
        loading_label = MDLabel(
            text="Loading...",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            font_size="20sp",
            bold=True
        )

        # Add the label to the box layout
        box_layout.add_widget(loading_label)

        # Add the box layout to the modal view
        modal_view.add_widget(box_layout)

        # Open the modal view
        modal_view.open()

        # Perform the actual action (e.g., navigating to userdetails screen)
        Clock.schedule_once(lambda dt: self.show_verify(modal_view), 1)

    def show_verify(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the UserDetailsScreen
        userdetails_screen = Factory.VerifyScreen(name='verify')

        # Add the UserDetailsScreen to the existing ScreenManager
        sm.add_widget(userdetails_screen)

        # Switch to the UserDetailsScreen
        sm.current = 'verify'

    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.verify_code = ''

    import re
    import validators  # Consider using validators for more robust checks
    from socket import gethostbyname

    def is_valid_email_format(self, email):
        """
        Check if the email format is valid.
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None


    def is_real_email(self, email):

        if not self.is_valid_email_format(email):
            return False
        domain = email.split('@')[1]
        if not self.has_mx_records(domain):
            return False
        return self.verify_email_smtp(email)

    def send_email(self):
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text

        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.user_otp = self.verification_code
        subject = "Verification Code for Email Confirmation"
        html_content = f"Hello,<br><br>Your verification code is: <strong>{self.verification_code}</strong><br><br>Thank you!"
        sender_email = "shubrathdevadiga6421@gmail.com"
        api_key = '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'

        message = Mail(
            from_email=sender_email,
            to_emails=gmail,
            subject=subject,
            html_content=html_content)

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            # self.show_dialog("Verification Code Sent", "A verification code has been sent to your email address.")
            self.enable_verification_code_input()
            self.nav_verify()
            # current_screen.ids.verify_button.on_release = ''

            # self.verification_state = "verifying"
            # self.current_button.text = "Verifying..."  # Update button text


        except Exception as e:
            print(str(e))

            self.show_dialog("Error", "Failed to send verification email. Please try again.")
            current_screen.ids.gmail.text = ''
            
            
    def enable_verification_code_input(self):
        current_screen = self.manager.get_screen('signup')
        # self.verificationCode.disabled = False
        current_screen.ids.verify_button.disabled = False

    def show_dialog(self, title, text):
        # Function to show dialogs with title and message
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def get_generated_verification_code(self):
        # Replace with your logic to generate and return the verification code
        # For simplicity, returning a hardcoded code here
        return "ABC123"  # Replace with your actual code generation logic



    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def signup(self):
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.user_name.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = f"{current_screen.ids.address_1.text}+, {current_screen.ids.address_2.text}"
        # self.account_details(phone_no)
        # self.add_money(phone_no)
        # self.transactions(phone_no)
        print(f"{gmail, username, password, phone_no, aadhar_card, pan_card, address}")
        try:
            if self.is_phone_number_registered(phone_no):

                toast("Phone number already exists. Choose another.").open()
                # self.manager.show_notification('Alert!','Phone number already exists. Choose another.')
                return

            else:  # Add user data to the 'login' collection in Anvil
                app_tables.wallet_users.add_row(
                    users_email=gmail,
                    users_username=username,
                    users_password=password,
                    users_phone=float(phone_no),
                    users_aadhar=float(aadhar_card),
                    users_pan=pan_card,
                    users_address=address,
                    users_usertype="customer",
                    users_banned=False,
                )

                # Show a popup with a success message
                # dialog = MDDialog(
                #     title="Alert",
                #     buttons=[
                #         MDFlatButton(
                #             text="OK",
                #             on_release=lambda *args: (dialog.dismiss(), self.dismiss_and_navigate())
                #         )
                #     ]
                # )
                # dialog.text = f"Successfully signed up."
                # dialog.open()
                self.manager.show_notification('Success','Successfully signed up.')
                self.dismiss_and_navigate()

                self.ids.address.text = ''
                self.ids.pan_card.text = ''
                self.ids.aadhar_card.text = ''
                self.ids.phone_no.text = ''
                self.ids.password.text = ''
                self.ids.username.text = ''
                self.ids.gmail.text = ''
        except Exception as e:
            print(e)

    @anvil.server.callable
    def is_phone_number_registered(self, phone_number):
        user = app_tables.wallet_users.get(users_phone=float(phone_number))
        return user is not None

    def dismiss_and_navigate(self):
        existing_screen = self.manager.get_screen('signup')
        self.manager.add_widget(Factory.SignInScreen(name='signin'))
        self.manager.current = 'signin'
        self.manager.remove_widget(existing_screen)

    def nav_sign_in(self):
        self.manager.add_widget(Factory.SignInScreen(name='signin'))
        self.manager.current = 'signin'
