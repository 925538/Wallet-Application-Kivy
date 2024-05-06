from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import mainthread, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from camera4kivy import Preview
from PIL import Image as PILImage
from pyzbar.pyzbar import decode
from kivy.base import EventLoop
Builder.load_string("""
<ScanScreen>:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Scan QR Code"
            anchor_title:'left'
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            elevation: 2
        
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: root.height - dp(56)  # Adjust for top app bar height
            
            ScanAnalyze:
                id: preview
                aspect_ratio: '16:9'
                extracted_data: root.got_result
""")


class ScanScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ScanScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def go_back(self):
        self.ids.preview.disconnect_camera()
        existing_screen = self.manager.get_screen('qrscanner')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def on_kv_post(self, obj):
        self.ids.preview.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
    @mainthread
    def got_result(self, result):
        decoded_data = result.data.decode('utf-8')  # Decode bytes to string
        print("Decoded Data:", decoded_data)
        self.nav_to_transfer(decoded_data)

    def nav_to_transfer(self, data):
        # Create a modal view for the loading animation
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

        # Perform the actual action (e.g., checking account details and navigating)
        Clock.schedule_once(lambda dt: self.show_transfer_screen(modal_view, data), 1)

    def show_transfer_screen(self, modal_view, data):
        # Dismiss the loading animation modal view
        modal_view.dismiss()
        self.ids.preview.disconnect_camera()
        # Retrieve the screen manager
        self.manager.add_widget(Factory.TransferScreen(name='transfer'))
        transfer_scr = self.manager.get_screen('transfer')
        transfer_scr.ids.mobile_no_field.text = data
        self.manager.current = 'transfer'


class ScanAnalyze(Preview):
    extracted_data = ObjectProperty(None)

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):
        pimage = PILImage.frombytes(mode='RGBA', size=image_size, data=pixels)
        list_of_all_barcodes = decode(pimage)

        if list_of_all_barcodes:
            if self.extracted_data:
                self.extracted_data(list_of_all_barcodes[0])
            else:
                print("Not found")
                self.manager.show_notification('Alert!',"An error occured. Please try again.")
