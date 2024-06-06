import base64
import io
from kivy.uix.image import Image
import qrcode
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.base import EventLoop
from kivy.core.window import Window
navigation_helper = """
<NavbarScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"

                MDTopAppBar:
                    title: ""
                    elevation: 1
                    pos_hint: {"top": 1}
                    md_bg_color: "#ffffff"
                    specific_text_color: "#000000"
                        
                    # Adding a logo to the left of the text
                    BoxLayout:
                        spacing: dp(10)
                        MDIconButton:
                            icon: 'menu'
                            on_release: root.go_back()
                            pos_hint: {'center_y': 0.7}

                        Image:
                            source:'images/2.png'  # Replace with the actual path to your logo
                            size_hint: None, None
                            size: dp(30), dp(28)
                            pos_hint: {'center_y': 0.7}
                            
                        MDLabel:
                            text: "G-wallet"
                            font_size: '24sp'
                            bold: True
                            pos_hint: {'center_y': 0.7, 'center_x': 0.7}
                ScrollView:
                    BoxLayout:  
                        size_hint_y: None
                        height: dp(510)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '8dp'   
                            padding: '15dp'   
                        
                            MDLabel:
                                id: username_label
                                text:''
                                font_style:"H6"
                                size_hint_y:None
                                bold: True
                                height: self.texture_size[1]


                            MDLabel:
                                id: email_label
                                text:''
                                font_style:"Body1" 
                                size_hint_y:None
                                #bold: True
                                height: self.texture_size[1]

                            MDLabel:
                                id: contact_label  
                                text: ''
                                font_style: "Body1" 
                                size_hint_y: None
                                #bold: True
                                height: self.texture_size[1]    


                            BoxLayout: 
                                size_hint_y: None
                                height: dp(400)
                                pos_hint: {'center_x': 0.45, 'y': 220}        

                                BoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: self.minimum_height
                                    spacing: '4dp'

                                    OneLineIconListItem:
                                        text: "Your QR Code"
                                        on_release: root.generate_qr_code()
                                        IconLeftWidget:
                                            icon: "qrcode-scan"
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb")  
                                    # OneLineIconListItem:
                                    #     text: "Auto Topup"
                                    #     IconLeftWidget:
                                    #         icon: "autorenew" 
                                    #         theme_text_color: 'Custom'
                                    #         text_color: get_color_from_hex("#3489eb") 
                                    OneLineIconListItem:
                                        text: "Settings"
                                        on_release: root.manager.nav_settings()
                                        IconLeftWidget:
                                            icon: "cog-outline"
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb")                      
                                    OneLineIconListItem:
                                        text: "Profile"
                                        on_release: root.profile_view()
                                        IconLeftWidget:
                                            icon: "face-man-profile" 
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb")
                                    OneLineIconListItem:
                                        text: "Account Management"
                                        on_release: root.manager.nav_accmanage()
                                        IconLeftWidget:
                                            icon: "bank"
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb")
                                    # OneLineIconListItem:
                                    #     text: "Get Help"
                                    #     on_release: root.manager.nav_help()
                                    #     IconLeftWidget:
                                    #         icon: "help-circle"
                                    #         theme_text_color: 'Custom'
                                    #         text_color: get_color_from_hex("#3489eb")
                                    OneLineIconListItem:
                                        text: "Raise a Complaint"
                                        on_release: root.manager.nav_complaint()
                                        IconLeftWidget:
                                            icon: "alert"  
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb")        
                                    OneLineIconListItem:
                                        text: "Log-out"
                                        on_release: root.manager.logout()
                                        IconLeftWidget:
                                            icon: "logout"  
                                            theme_text_color: 'Custom'
                                            text_color: get_color_from_hex("#3489eb") 
                       
"""
Builder.load_string(navigation_helper)

class NavbarScreen(Screen):
    def go_back(self):
        self.manager.current = 'dashboard'

    def __init__(self, **kwargs):
        super(NavbarScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)


    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27,9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
    
    def fetch_and_update_navbar(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in NavbarScreen
        navbar_screen = self.get_screen('navbar')
        navbar_screen.ids.username_label.text = store["users_username"]
        navbar_screen.ids.email_label.text = store["users_email"]
        navbar_screen.ids.contact_label.text = store["users_phone"] 

    def generate_qr_code(self):
        phone = JsonStore('user_data.json').get('user')['value']["users_phone"]
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(phone)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_data = buffer.getvalue()
        self.show_qr(png_data)

    def show_qr(self, png_data):
        qr_code_popup = Popup(title='Your QR Code', size_hint=(0.8, 0.8))
        qr_code_image = Image()
        qr_code_image.source = 'data:image/png;base64,' + base64.b64encode(png_data).decode('utf-8')
        qr_code_popup.add_widget(qr_code_image)
        qr_code_popup.open()     
    
    def profile_view(self):
        store = JsonStore('user_data.json').get('user')['value']
        username = store["users_username"]
        gmail = store["users_email"]
        phone = store["users_phone"]
        aadhaar = store["users_Aadhaar"]
        address = store["users_address"]
        pan = store["users_pan"]
        profile_screen = self.manager.get_screen('profile')
        profile_screen.ids.username_label.text = f"{username}"  # Assuming username is at index 1
        profile_screen.ids.email_label.text = f"{gmail}"  # Assuming email is at index 0
        profile_screen.ids.contact_label.text = f"{phone}"
        profile_screen.ids.aadhaar_label.text = f"{aadhaar}"
        profile_screen.ids.pan_label.text = f"{pan}"
        profile_screen.ids.address_label.text = f"{address}"
        # Navigate to the 'Profile' screen
        self.manager.current = 'profile'

 