from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

from signin import SignInScreen
from signup import SignUpScreen
class CustomMDRaisedButton(MDRaisedButton):
    radius = ListProperty([25, 25, 25, 25])

Builder.load_string(
    """
<LandingScreen>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.size
            pos: self.pos

    Widget:
        size_hint_y:None
        height:"20dp"

    BoxLayout:
        orientation: "horizontal"
        padding: dp(20)
        # spacing: dp(20)
        # pos_hint:{"top":1}
        minimum_width:100

        Image:
            source: "images/2.png"
            pos_hint: {'center_x': 0.17,'center_y':0.9}
            size_hint: None, None
            size: "60dp", "60dp"


    BoxLayout:
        size_hint: 1, None
        height: self.minimum_height
        padding: "20dp"
        spacing: "20dp"
        orientation: 'vertical'
        pos_hint: {'center_x': 0.5,'center_y':0.32}



        BoxLayout:
            # size_hint: 1, None
            padding: "1dp"
            orientation: 'horizontal'
            # pos_hint: {'center_x': 0.5,'center_y':0.3}
            minimum_width:100

            MDLabel:
                text: "G-Wallet"
                font_size: 50
                # halign: "center"
                bold: True
                # color: 1,1,1,1

                # pos_hint: {'center_x': 0.12}
                # font_name: "Roboto-Bold"


        Widget:
            size_hint_y:None
            height:"30dp"


        MDLabel:
            text: "Seamlessly send and receive money in multiple currencies with just a few taps."
            font_size: 34
            # halign: "center"
            # bold: True
            pos_hint: {'center_x': 0.5}
            multiline:True
            width:"170dp" 
            # color: 1,1,1,1


        Widget:
            size_hint_y:None
            height:"70dp"



        MDFillRoundFlatButton:
            text: "LOGIN"
            on_release: root.nav_sign_in()
            md_bg_color: "#148efe"
            theme_text_color: 'Custom'
            # text_color: 1, 1, 1, 1
            font_size:"18sp"
            size_hint: 1, None
            height: "15dp"
            font_name: "Roboto-Bold"
            radius: [25, 25, 25, 25]

        MDFillRoundFlatButton:
            text: "SIGNUP"
            on_release: root.nav_sign_up()
            md_bg_color: "#148efe"
            size_hint: 1, None
            font_size:"18sp"
            # md_bg_color: app.theme_cls.primary_light
            height: "15dp"
            font_name: "Roboto-Bold"
            radius: [25, 25, 25, 25]
        Widget:
            size_hint_y:None
            height:"190dp"


"""
)


class LandingScreen(Screen):
    def nav_sign_in(self):
        existing_screen = self.manager.get_screen('landing')
        self.manager.add_widget(Factory.SignInScreen(name='signin'))
        self.manager.current = 'signin'
        self.manager.remove_widget(existing_screen)

    def nav_sign_up(self):
        self.manager.add_widget(Factory.SignUpScreen(name='signup'))
        self.manager.current = 'signup'


class WalletApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(LandingScreen(name='landing'))
        return screen_manager