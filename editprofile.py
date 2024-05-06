import requests
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window
from anvil.tables import app_tables
from kivymd.uix.snackbar import Snackbar
from kivy.animation import Animation
from kivy.factory import Factory
KV = """
<EditUser>
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: 'Edit Profile'
            anchor_title:'left'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: "20dp"
                padding: ["20dp", "20dp", "20dp", "20dp"]
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'top': 1}

                MDTextField:
                    id: username
                    text:""
                    text_color:0,0,0,1
                    fill_color_normal: 1,1,1,1
                    md_bg_color:1,1,1,1
                    radius:[21,21,21,21]
                    elevation: dp(2)
                    hint_text: "username"
                    helper_text: "Enter your username"
                    icon_right: "account"
                    mode:'rectangle'
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                MDTextField:
                    id: email
                    elevation: dp(2)
                    text:""
                    hint_text: "Email"
                    helper_text: "Enter your email"
                    icon_right: "email"
                    mode:'rectangle'
                    radius:[21,21,21,21]
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                MDTextField:
                    id: phone
                    elevation: dp(2)
                    text:""
                    hint_text: "Phone Number"
                    helper_text: "Enter your phone number"
                    icon_right: "phone"
                    readonly: False  # Allow editing
                    mode:'rectangle'
                    radius:[21,21,21,21]
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                # MDTextField:
                #     id: password
                #     elevation: dp(2)
                #     text:""
                #     hint_text: "Password"
                #     helper_text: "Enter your password"
                #     icon_right: "lock"
                #     mode:'rectangle'
                #     radius:[21,21,21,21]
                #     hint_text_color_normal: "#148efe"
                #     text_color_normal:"#484848"
                #     icon_right_color_normal:"#148efe"
                #     line_color_normal:"#148efe"
                #     helper_text_color_focus:"#148efe"

                MDTextField:
                    id: aadhaar
                    elevation: dp(2)
                    text:""
                    hint_text: "Aadhaar Number"
                    helper_text: "Enter your Aadhaar number"
                    icon_right: "fingerprint"
                    readonly: True  # Allow editing
                    mode:'rectangle'
                    radius:[21,21,21,21]
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                MDTextField:
                    id: pan
                    elevation: dp(2)
                    text:""
                    hint_text: "PAN Number"
                    helper_text: "Enter your PAN number"
                    icon_right: "credit-card"
                    readonly: True  # Allow editing
                    mode:'rectangle'
                    radius:[21,21,21,21]
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                MDTextField:
                    id: address
                    text:""
                    elevation: dp(2)
                    hint_text: "Address"
                    helper_text: "Enter your address"
                    icon_right: "home"
                    readonly: False  # Allow editing
                    mode:'rectangle'
                    radius:[21,21,21,21]
                    hint_text_color_normal: "#148efe"
                    text_color_normal:"#484848"
                    icon_right_color_normal:"#148efe"
                    line_color_normal:"#148efe"
                    helper_text_color_focus:"#148efe"

                MDRaisedButton:
                    text: "Save Edit"
                    on_release: root.save_edit()
                    pos_hint: {'center_x': 0.5}

"""
Builder.load_string(KV)


class EditUser(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('edituser')
        self.manager.add_widget(Factory.SettingsScreen(name='settings'))
        self.manager.current = 'settings'
        self.manager.remove_widget(existing_screen)


    def __init__(self, **kwargs):
        super(EditUser, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key == 27:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def animate_text_field(self):
        self.anim_duration = 0.2  # Adjust animation duration (in seconds)
        # self.unfocused_border_color = (1, 1, 1, 1)  # Set default border color
        self.focused_border_color = (0, 0.7, 1, 1)
        anim = Animation(border_color=self.focused_border_color, duration=self.anim_duration)
        anim.start(self)
        # animation.bind(on_complete=lambda x, instance=instance: setattr(instance, 'scale', 1))
        

    def save_edit(self):
        edit_scr = self.manager.get_screen('edituser')
        phone = edit_scr.ids.phone.text
        username = edit_scr.ids.username.text
        email = edit_scr.ids.email.text
        # password = edit_scr.ids.password.text
        aadhar = edit_scr.ids.aadhaar.text
        pan = edit_scr.ids.pan.text
        address = edit_scr.ids.address.text

    

        try:
            # Reference to the 'login' table in Anvil
            login_table = app_tables.wallet_users

            # Check if the user exists
            user = login_table.get(phone=float(phone))

            if user is not None:
                # Update the user details
                user.update(
                    username=username,
                    email=email,
                    # password=password,
                    aadhar=float(aadhar),
                    pan=pan,
                    address=address,
                )

                print("User details updated successfully.")
                # self.show_update_success_popup()
                self.manager.show_notification('Sucess','Your profile has been updated successfully. Please log in again.')
            else:
                print(f"User with phone number {phone} does not exist.")
                self.manager.show_notification('Alert!',f"User with phone number {phone} does not exist.")

        except Exception as e:
            print(f"Error updating user details: {e}")
            self.manager.show_notification('Alert!',"An error occured. Please try again.")
    def show_update_success_popup(self):
        dialog = MDDialog(
            title="Update Success",
            text="Your profile has been updated successfully. Please log in again.",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: (dialog.dismiss(), self.manager.logout()),
                )
            ]
        )
        dialog.open()



