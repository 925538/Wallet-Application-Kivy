from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from signin import SignInScreen
from signup import SignUpScreen
Builder.load_string(
    """
<LandingScreen>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos


    BoxLayout:
        orientation: "vertical"
        padding: dp(35)
        spacing: dp(35)  # Adjusted spacing between labels and image

        MDLabel:
            text: ""

            theme_text_color: 'Custom'
            text_color: 0, 0, 0, 1
            bold: True


        Image:
            source: "images/2.png"
            pos_hint: {'center_x': 0.5, 'center_y': 0.85}
            size_hint: None, None
            size: "80dp", "80dp"




        GridLayout:
            cols: 2
            spacing: dp(20)
            padding: dp(20)
            pos_hint: {'center_x': 0.52, 'center_y': 0.8} 
            size_hint: 1, None

            MDRaisedButton:
                md_bg_color: 1,1,1,1
                theme_text_color: 'Custom'
                text_color: 0, 0, 0, 1
                size_hint: 1, None
                height: "50dp"
                line_color: 0, 0, 0, 1  
                line_width: 1

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(10)

                    Image:
                        source: "images/google.png"
                        size_hint: None, None
                        size: "20dp", "25dp"  

                    MDLabel:
                        text: "  Sign In with Google"

                        theme_text_color: 'Custom'
                        text_color: 0, 0, 0, 1
                        pos_hint: {'center_x': 0.8, 'center_y': 0.5}
                        bold: True

        GridLayout:
            cols: 2
            spacing: dp(20)
            padding: dp(20)
            pos_hint: {'center_x': 0.52, 'center_y': 0.7} 
            size_hint: 1, None

            MDRaisedButton:
                rgba: "#1877F2"
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint: 1, None
                height: "50dp"

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10  # Adjust the spacing as needed

                    Image:
                        source: "images/facebook.png"
                        size_hint: None, None
                        size: "20dp", "25dp"
                        allow_stretch: True
                        keep_ratio: True

                    MDLabel:
                        text: "  Sign In with Facebook"
                        theme_text_color: 'Custom'
                        text_color: 1, 1, 1, 1
                        pos_hint: {'center_x': 0.8, 'center_y': 0.5}
                        bold: True

        Label:
            text: ""

        GridLayout:
            cols: 2
            spacing: dp(20)
            padding: dp(20)
            pos_hint: {'center_x': 0.50, 'center_y': 0.6}  # Adjusted y-value
            size_hint: 1, None
            height: "50dp"

            MDRaisedButton:
                text: "Login"
                on_release: root.nav_sign_in()
                rgba: "#1877F2"
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint: 1, None
                height: "50dp"
                font_name: "Roboto-Bold"

            MDRaisedButton:
                text: "Sign Up"
                on_press: root.nav_sign_up()
                rgba: "#1877F2"
                pos_hint: {'right': 1, 'y': 0.5}
                size_hint: 1, None
                height: "50dp"
                font_name: "Roboto-Bold"
        Label:
            text: ""

        Label:
            text: ""
        Label:
            text: ""
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
