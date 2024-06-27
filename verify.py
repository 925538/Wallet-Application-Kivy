import random
import string

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core import window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDTextButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import smtplib
import dns.resolver

Window.size = (380, 640)

KV = '''
<VerifyScreen>:
    MDScreen:
        BoxLayout:
            orientation: 'vertical'
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {"center_x": .05}
                on_release: root.on_back_button()

            Image:
                source: 'images/phone_verification.jpeg'
                size_hint: None, None
                size: dp(100), dp(100)
                pos_hint: {"center_x": .5}
            Widget:
                size_hint_y: None
                height: "30dp"

            MDLabel:
                text: "Enter Email Verification Code"
                halign: 'center'
                theme_text_color: "Primary"
                font_style: "H6"
            Widget:
                size_hint_y: None
                height: "20dp"

                
            MDLabel:
                text: "We have sent you an OTP on"
                halign: 'center'
                theme_text_color: "Secondary"
                font_style: "Body1"

            MDLabel:
                id: email_label
                text: "abc@gmail.com"
                halign: 'center'
                theme_text_color: "Secondary"
                font_style: "Subtitle1"
            Widget:
                size_hint_y: None
                height: "35dp"
                
            # Widget:
            #     size_hint_y: None
            #     height: "20dp"
            BoxLayout:
                orientation: 'horizontal'
                MDLabel:
                    id: timer_label
                    text: "01:00"
                    halign: 'right'
                    # pos_hint:{"center_x":1}
                    theme_text_color: "Primary"
                    font_style: "H6"
                
                Widget:
                    size_hint_x: None
                    width: "35dp"

            MDTextField:
                id: otp_field
                hint_text: "OTP"
                helper_text_mode: "on_focus"
                icon_right: "key"
                pos_hint: {"center_x": .5}
                size_hint_x: .8
                mode: "rectangle"
                
            Widget:
                size_hint_y: None
                height: "30dp"


            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: self.minimum_height
                MDLabel:
                    halign:"center"
                    text: "Still not received OTP?"
                    theme_text_color: "Secondary"
                    font_style: "Body2"
                    size_hint_x:1
                    
                AnchorLayout:
                    anchor_x:"center"
                    MDTextButton:
                        id:resend_id
                        text: "Resend OTP"
                        on_release: root.resend_otp()
                        
            Widget:
                size_hint_y: None
                height: "40dp"
                
            MDFillRoundFlatButton:
                text: "Verify OTP"
                pos_hint: {"center_x": .5}
                on_release: root.verify_otp()
                size_hint: 0.85, None
                height: dp(48)
                
            
                

            Widget:
                size_hint_y: None
                height: "150dp"

'''

Builder.load_string(KV)


class VerifyScreen(Screen, MDApp):
    email = StringProperty('')
    user_otp = StringProperty('')
    timer = NumericProperty(60)
    success = BooleanProperty(False)

    def init(self, **kwargs):
        sign_up_screen = self.manager.get_screen('signup')
        self.email = sign_up_screen.email
        print(self.email, "j=giu")
        self.send_otp(self.email)
        self.root.ids.email_label.text = self.email
        print(self.root.ids.email_label.text)
        super(VerifyScreen, self).init(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

        self.otp_code = None
        self.email = sign_up_screen.email

        self.send_otp(self.email)
        self.root.ids.email_label.text = self.email
        print(self.root.ids.email_label.text)

    def nav_signup(self):
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
        Clock.schedule_once(lambda dt: self.show_signup(modal_view), 1)

    def show_signup(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the UserDetailsScreen
        userdetails_screen = Factory.SignUpScreen(name='signup')

        # Add the UserDetailsScreen to the existing ScreenManager
        sm.add_widget(userdetails_screen)

        # Switch to the UserDetailsScreen
        sm.current = 'signup'

    def start_timer(self):
        Clock.schedule_interval(self.update_timer, 1)
        self.ids.resend_id.disabled = True

    def update_timer(self, dt):
        if self.timer > 0:
            self.timer -= 1
            minutes, seconds = divmod(self.timer, 60)
            self.ids.timer_label.text = f"{minutes:02}:{seconds:02}"
            # self.ids.resend_id.disabled = False
            if self.timer == 0:
                self.ids.resend_id.disabled = False
        else:
            Clock.unschedule(self.update_timer)
            self.otp_code = ''  # Invalidate OTP

    def on_pre_enter(self):

        sign_up_screen = self.manager.get_screen('signup')
        self.email = sign_up_screen.email

        verify_screen = self.manager.get_screen('verify')
        verify_screen.ids.email_label.text = self.email

        self.user_otp = sign_up_screen.user_otp

        self.timer = 60  # Reset timer to 60 seconds
        self.start_timer()

    def on_back_button(self):
        # Handle back button press
        existing_screen = self.manager.get_screen('verify')
        self.manager.current = 'signup'
        self.manager.remove_widget(existing_screen)

    def send_otp(self, email):
        self.otp_code = self.generate_otp()
        self.send_email(email, self.otp_code)

    # def resend_otp(self):
    # self.send_otp(self.email)

    def resend_otp(self):

        # self.timer = 60  # Reset timer to 60 seconds
        # self.start_timer()
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.user_otp = self.verification_code
        subject = "Verification Code for Email Confirmation"
        html_content = f"Hello,<br><br>Your verification code is: <strong>{self.verification_code}</strong><br><br>Thank you!"
        sender_email = "shubrathdevadiga6421@gmail.com"
        api_key = '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'

        message = Mail(
            from_email=sender_email,
            to_emails=self.email,
            subject=subject,
            html_content=html_content)

        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            self.show_dialog("Verification Code Sent", "A verification code has been sent to your email address.")

            self.timer = 60  # Reset timer to 60 seconds
            self.start_timer()

        except Exception as e:
            print(str(e))

            self.show_dialog("Error", "Failed to send verification email. Please try again.")

    def verify_otp(self):

        verify_screen = self.manager.get_screen('verify')
        entered_code = verify_screen.ids.otp_field.text

        if entered_code == self.user_otp and self.timer > 0:
            self.show_dialog("Success", "OTP verified successfully.")
            verify_screen.ids.otp_field.text = ''
            self.success = True
            signup_screen = self.manager.get_screen('signup')
            signup_screen.ids.verify_button.disabled = True
            signup_screen.ids.confirm_id.disabled = False
            self.nav_signup()


        elif entered_code == self.user_otp and not (self.timer > 0):
            self.show_resend_dialog()
            verify_screen.ids.otp_field.text = ''


        else:
            self.show_dialog("Error", "Invalid or expired OTP. Please try again.")
            verify_screen.ids.otp_field.text = ''

    def generate_otp(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def verify_email(self, email):
        domain = email.split('@')[1]

        try:
            # Get MX record for the domain
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(records[0].exchange)

            # SMTP lib setup (use debug level for full output)
            server = smtplib.SMTP()
            server.set_debuglevel(0)

            # SMTP Conversation
            server.connect(mx_record)
            server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
            server.mail('vikrammoger19@gmail.com')  # Use a valid email address for the sender
            code, message = server.rcpt(email)
            server.quit()

            # Assume 250 as Success
            if code == 250:
                return True
            else:
                return False


        except Exception as e:
            # Handle exceptions (e.g., DNS query failed, server not responding)
            print(f"Exception occurred: {e}")
            return False

    # Example usage

    def send_email(self):
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text

        if self.verify_email(gmail):
            print("The email address exists.")
            # else:
            #     print("The email address does not exist.")

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

                # current_screen.ids.verify_button.on_release = ''

                # self.verification_state = "verifying"
                # self.current_button.text = "Verifying..."  # Update button text
                self.nav_verify()

            except Exception as e:
                print(str(e))

                self.show_dialog("Error", "Failed to send verification email. Please try again.")
        else:
            self.show_dialog("invalid emailid", "Email is not verified")

    #

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text='OK', on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def show_resend_dialog(self):
        dialog = MDDialog(
            title="OTP Expired",
            text="Your OTP has expired. Would you like to resend the OTP?",
            buttons=[
                MDFlatButton(text='Resend', on_release=lambda x: (dialog.dismiss(), self.resend_otp())),
                MDFlatButton(text='Cancel', on_release=lambda x: dialog.dismiss())
            ]
        )
        dialog.open()

    # def on_back_button(self):
    #     # Handle back button press
    #     pass
    #
    # def resend_otp(self):
    #     self.root.get_screen('otp_screen').resend_otp()
    #
    # def verify_otp(self):
    #     self.root.get_screen('otp_screen').verify_otp()
