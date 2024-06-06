import requests
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import Screen
from kivy.base import EventLoop
from kivy.core.window import Window

KV = """
<ComplaintScreen>
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: 'Report a bug'
            elevation: 3
            anchor_title:'left'
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint: {'top': 1}

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                padding: ["10dp", "1dp", "10dp", "1dp"]
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'top': 1, 'center_x': 0.5}

                #1
                BoxLayout:
                    orientation: "horizontal" 
                    spacing: "10dp"
                    padding: ["10dp", "1dp", "10dp", "1dp"]
                    size_hint_y: None
                    height: self.minimum_height
                    pos_hint: {'top': 1, 'center_x': 0.5}

                    MDLabel:
                        text: "Email:"  
                        font_size:"15sp"
                        height:"18dp"
                        size_hint_x: None
                        width: "100dp"  # Adjust the width as needed

                    MDTextField:
                        id: email_label
                        multiline: False
                        readonly: True

                #2
                BoxLayout:
                    orientation: "horizontal" 
                    spacing: "10dp"
                    padding: ["10dp", "1dp", "10dp", "1dp"]
                    size_hint_y: None
                    height: self.minimum_height
                    pos_hint: {'top': 1, 'center_x': 0.5}

                    MDLabel:
                        text: "Issue Name:"  
                        font_size:"15sp"
                        height:"18dp"
                        size_hint_x: None
                        width: "100dp"  # Adjust the width as needed

                    MDTextField:
                        multiline: False

                #3
                BoxLayout:
                    orientation: "horizontal" 
                    spacing: "10dp"
                    padding: ["10dp", "1dp", "10dp", "1dp"]
                    size_hint_y: None
                    height: self.minimum_height
                    pos_hint: {'top': 1, 'center_x': 0.5}

                    MDLabel:
                        text: "Specific Issues:"  
                        font_size:"15sp"
                        height:"18dp"
                        size_hint_x: None
                        width: "100dp"  # Adjust the width as needed

                    MDTextField:
                        multiline: False   

                #4
                BoxLayout:
                    orientation: "horizontal" 
                    spacing: "10dp"
                    padding: ["10dp", "1dp", "10dp", "1dp"]
                    size_hint_y: None
                    height: self.minimum_height
                    pos_hint: {'top': 1, 'center_x': 0.5}

                    MDLabel:
                        text: "Description:"  
                        font_size:"15sp"
                        height:"18dp"
                        size_hint_x: None
                        width: "100dp"  # Adjust the width as needed

                    MDTextField:
                        multiline: True        

                MDRectangleFlatButton:
                    text: "Submit"
                    on_release: root.Submit()
                    size_hint_x: None
                    width: "150dp"
                    pos_hint: {'center_x': 0.5}                        

"""
Builder.load_string(KV)


class ComplaintScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('complaint')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(ComplaintScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def fetch_and_update_complaint(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        complaint_screen = self.get_screen('complaint')
        complaint_screen.ids.email_label.text = store["users_email"]

    def Submit(self):
        # self.show_popup("Your Report has been submited. \nOur Technical Executive will respond you shortly.")
        self.manager.show_notification('Alert!','Report submited.\nOur Technical Executive will respond you shortly.')
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
