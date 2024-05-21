import imp
import anvil
from anvil.tables import app_tables
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.base import EventLoop
KV = """
<ResetPassword>:
    BoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        MDTopAppBar:
            title: "Change Password"
            anchor_title:'left'
            left_action_items: [["arrow-left", lambda x: root.go_back()]]  # Back button
            background_color: (173, 216, 230)  # Light blue color
        BoxLayout:
            orientation: "vertical"
            spacing: "20dp"
            padding: "20dp"

            MDTextField:
                id: old_password_input
                hint_text: "Enter old password"
                password: True
                max_text_length: 20
                multiline: False
                size_hint_y: None
                mode: "rectangle"
                height: "48dp"
                radius: [50, 50, 50, 50]
                line_width: "2dp" 
            MDTextField:
                id: new_password_input
                hint_text: "Enter new password"
                password: True
                max_text_length: 20
                multiline: False
                size_hint_y: None
                mode: "rectangle"
                height: "48dp"
                radius: [50, 50, 50, 50]
                line_width: "2dp" 
            MDTextField:
                id: confirm_password_input
                hint_text: "Enter new password again"
                password: True
                max_text_length: 20
                multiline: False
                size_hint_y: None
                mode: "rectangle"
                height: "48dp"
                radius: [50, 50, 50, 50]
                line_width: "20dp" 

            BoxLayout:
                orientation: "vertical"
                padding: "20dp"
                MDRaisedButton:
                    text: "Submit"  
                    size_hint_y: None
                    height: "48dp"
                    pos_hint:{"center_x":0.5}
                    on_release: root.submit_password()
"""

Builder.load_string(KV)


class ResetPassword(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('reset')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(ResetPassword, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def submit_password(self):
        # Get the current user's phone number from the stored user data
        phone = JsonStore("user_data.json").get("user")["value"]['phone']
        current_user_password = JsonStore("user_data.json").get("user")["value"]["password"]

        # Get the user from the Anvil app_tables.wallet_users
        user = app_tables.wallet_users.get(phone = phone,password=current_user_password)
        try:
            if user:
                # Get the decrypted password from the user's data
                # decrypted_password = anvil.server.call('load_secret_data', current_user_password,
                #                                     self.ids.old_password_input.text)

                if current_user_password == self.ids.old_password_input.text:
                    # Previous password is correct, update with the new password
                    # new_encrypted_password = anvil.server.call("save_secret_data", self.ids.new_password_input.text)
                    user.update(password=self.ids.new_password_input.text)

                    # Show a success pop-up
                    # dialog = MDDialog(
                    #     title="Success",
                    #     text="Password updated successfully!",
                    #     buttons=[
                    #         MDFlatButton(
                    #             text="OK",
                    #             on_release=lambda *args: (dialog.dismiss(), self.go_back())
                    #         )
                    #     ]
                    # )
                    # dialog.open()
                    self.manager.show_notification('Success',"Password updated successfully.")

                else:
                    # Show an error pop-up for incorrect previous password
                    # self.show_error_popup("Incorrect previous password. Please try again.")
                    self.manager.show_notification('Alert!',"Incorrect previous password. Please try again.")
            else:
            # Handle the case where the user is not found
                print("User not found.")
                self.manager.show_notification('Alert!','User not found.')
        except Exception as e:
            print(e)
            self.manager.show_notification('Alert!','An error occured.')
        

    def show_error_popup(self, error_text):
        # Show an error pop-up
        dialog = MDDialog(
            title="Error",
            text=error_text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()
