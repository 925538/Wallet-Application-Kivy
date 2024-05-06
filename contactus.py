from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window

KV = '''
<ContactUsScreen>:
    Screen:
        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: 'Contact Us'
            anchor_title:'left'
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint: {'top':1}

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(200)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}

            Image:
                source: 'images/service.jpg'  # Update with your image file path
                size_hint_y: None
                height: dp(250)  # Adjust the height as needed
                pos_hint: {'center_x': 0.5}

            MDTextField:
                hint_text: "Tell us how we can help you"
                multiline: True


            MDRectangleFlatButton:
                text: "Submit"
                on_release: root.Submit()
                size_hint_x: None
                width: "150dp"
                pos_hint: {'center_x': 0.5}                        

'''
Builder.load_string(KV)


class ContactUsScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('contactus')
        self.manager.current = 'help'
        self.manager.remove_widget(existing_screen)


    def __init__(self, **kwargs):
        super(ContactUsScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def Submit(self):
        # self.show_popup("Your Query has been submited. \nOur Technical Executive will respond you shortly.")
        self.manager.show_notification('Alert!','Query submited.\nOur Technical Executive will respond you shortly.')
        self.manager.current = 'dashboard'

    def show_popup(self, text):
        dialog = MDDialog(
            title="Success",
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
