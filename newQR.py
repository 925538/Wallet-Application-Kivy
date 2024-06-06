import base64
import io
import qrcode
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.base import EventLoop
kv_string = '''         
<QRCodeScreen>:
    MDFloatLayout:
        md_bg_color:1,1,1,1
        size_hint:(1,1)# Make the size stretchable

        MDTopAppBar:
            md_bg_color:1,1,1,1
            specific_text_color:1/255, 26/255, 51/255, 1
            elevation:0
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            
            pos_hint: {'center_x': 0.5, 'center_y': 0.96}
        
        MDLabel:
            text:"Receive Money"
            pos_hint: {'center_x': 0.6, 'center_y': 0.956}
            size_hint: None,None
            font_size:dp(18)
            height: dp(50)
            width: dp(180)
    MDBoxLayout:
        orientation: "vertical"
        spacing:dp(5)
        padding:dp(30)
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        size_hint: (1.0, None)  # Increase button size
        
        
        
        MDLabel:
            text: "QR code"
            size_hint_y: None
            height: self.texture_size[1]
            # halign: 'left'  
            pos_hint:{'center_x':.5,'center_y':0.5}
            font_size: dp(20)
            

            
        Widget:
            size_hint_y: None
            height:dp(10)
                 
        MDLabel:
            text: "Show this QR code or share magic link to the sender to receive money.It has your account details."
            size_hint_y: None
            height: self.texture_size[1]
            # halign: ''
            theme_text_color: "Secondary"
            font_size: dp(12)
    BoxLayout:
        orientation: 'vertical'
        padding:dp(20)
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: "10dp"
            spacing: "0dp"
            size_hint_y: None
            size_hint_x: None
            height: dp(250)
            width:dp(230)
            
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            
            
            canvas:
                Color:
                    rgba:0,0,0, 1
                
                Line:
                    width: 0.25
            
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 15)
            
            BoxLayout:
                orientation: "vertical"
                padding:dp(30)
                spacing:dp(10)
                
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'center_x': -0.3, 'center_y': -0.6}
                MDRectangleFlatButton:
    
                    line_color:1,1,1,1
                    size_hint: None, None
                    size: dp(50), dp(50)
                    pos_hint: {'center_x': 1.6, 'center_y': 1.3}
                    canvas.before:
                        Color:
                            rgba: 174/255, 214/255, 241/255, 1
                        Ellipse:
                            size: self.size
                            pos: self.pos 
                    
                    Image:
                        size_hint: None, None
                        size: dp(50), dp(50)  # Adjust the size as needed
                        source: "images//profile.png"
                        md_bg_color:217 / 255, 217 / 255, 217 / 255, 1 
            
                
            Image:
                id: qr_code_image
                source: ''
                size_hint: None, None
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size: dp(180), dp(180)
            MDLabel:
                text:""
                size_hint: None, None
                size: dp(10), dp(10)
            
                
    
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(48)
        padding:dp(20)
        spacing:dp(10)
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        
        MDRoundFlatButton:
            text: 'Download QR Code'
            on_release: root.download_qr_code()
            line_color:1,1,1,1
            text_color:0,0,0,1
            md_bg_color:217 / 255, 217 / 255, 217 / 255, 1 
            pos_hint: {'center_y': 0.5}  # Center vertically
        Widget:
            size_hint_y: None
            height: '5dp'
        MDRoundFlatButton:
            text: 'Share QR Code'
            line_color:1,1,1,1
            text_color:1,1,1,1
            on_release: root.share_qr_code()
            md_bg_color:115/255, 191/255, 250/255, 1
            size_hint: None, None
            size: dp(10), dp(10)
            pos_hint: {'center_y': 0.5}  # Center vertically
            

'''

Builder.load_string(kv_string)


class QRCodeScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('qrcode')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)
        
    def __init__(self, **kwargs):
        super(QRCodeScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.generate_qr_code()

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def generate_qr_code(self):
        phone = str(JsonStore('user_data.json').get('user')['value']["users_phone"])
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr_code.add_data(phone)
        qr_code.make(fit=True)

        img = qr_code.make_image(fill_color="#148EFE", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_data = buffer.getvalue()

        # Update QR code image source
        self.ids.qr_code_image.source = 'data:image/png;base64,' + base64.b64encode(png_data).decode('utf-8')

    def download_qr_code(self):
        # Download QR code functionality goes here
        pass

    def share_qr_code(self):
        # Share QR code functionality goes here
        pass


class QRCodeApp(MDApp):
    def build(self):
        return QRCodeScreen()


if __name__ == '__main__':
    QRCodeApp().run()
