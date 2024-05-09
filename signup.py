import anvil
from anvil.tables import app_tables
from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivy.base import EventLoop

KV = '''
<SignUpScreen>:
    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            title: "Sign Up"   
            anchor_title:'left'
            elevation: 2


        ScrollView:

            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                padding: "10dp"
                spacing: "20dp"
                orientation: 'vertical'
                
                MDTextField:
                    mode: "rectangle"
                    id: user_name
                    hint_text: " Username"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                    
                    
                MDTextField:
                    mode: "rectangle"
                    id: gmail
                    hint_text: " Email Address"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                    
                    
                MDTextField:
                    mode: "rectangle"
                    id: password
                    hint_text: " Password"
                    password: True
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                    
                MDTextField:
                    mode: "rectangle"
                    id: re_password
                    hint_text: " Retype your password"
                    password: True
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                                

                MDTextField:
                    mode: "rectangle"
                    id: phone_no
                    hint_text: " Phone Number"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]

                MDTextField:
                    mode: "rectangle"
                    id: aadhar_card
                    hint_text: " Aadhar Card Number"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]

                MDTextField:
                    mode: "rectangle"
                    id: pan_card
                    hint_text: " PAN Card Number"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]

                MDTextField:
                    mode: "rectangle"
                    id: address_1
                    hint_text: " Address Line 1"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                    
                MDTextField:
                    mode: "rectangle"
                    id: address_2
                    hint_text: " Address Line 2"
                    line_color_normal: (0.5, 0.5, 0.5, 1)
                    # required: True
                    radius: [50, 50, 50, 50]
                Widget:
                    size_hint_y: None
                    height: '4dp'
                MDFillRoundFlatButton:
                    text: "Sign Up"
                    pos_hint: {"center_x": .5}
                    on_release: root.signup()
                    halign:"center"
                    size_hint: .3, None
                Widget:
                    size_hint_y: None
                    height: '2dp'    


                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None

                    height: self.minimum_height
                    spacing: dp(20) 
                    Widget:
                        size_hint_x: None
                        height: '10dp'
                    MDLabel:
                        text: "Already have an account?"
                        font_size: "11sp"
                        theme_text_color: "Primary"
                        halign: 'right'
                        height: self.texture_size[1] + dp(2)
                    MDLabel:
                        text: "Sign In"
                        font_size: "12sp"
                        halign: 'left'
                        size_hint_y: None
                        height: self.texture_size[1] + dp(2)  # Adjust padding
                        bold:True
                        theme_text_color: "Custom"
                        text_color: 0.117, 0.459, 0.725, 1
                        #on_touch_down: root.manager.current = 'signin' if self.collide_point(*args[1].pos) else False



'''
Builder.load_string(KV)


class SignUpScreen(Screen):

    def go_back(self):
        existing_screen = self.manager.get_screen('signup')
        self.manager.current = 'landing'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def signup(self):
        current_screen = self.manager.get_screen('signup')
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.user_name.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = f"{current_screen.ids.address_1.text}+, {current_screen.ids.address_2.text}"
        # self.account_details(phone_no)
        # self.add_money(phone_no)
        # self.transactions(phone_no)
        try:
            if self.is_phone_number_registered(phone_no):

                toast("Phone number already exists. Choose another.").open()
                # self.manager.show_notification('Alert!','Phone number already exists. Choose another.')
                return

            else:  # Add user data to the 'login' collection in Anvil
                app_tables.wallet_users.add_row(
                    email=gmail,
                    username=username,
                    password=password,
                    phone=float(phone_no),
                    aadhar=float(aadhar_card),
                    pan=pan_card,
                    address=address,
                    usertype="customer",
                    banned=False,
                )

                # Show a popup with a success message
                dialog = MDDialog(
                    title="Alert",
                    buttons=[
                        MDFlatButton(
                            text="OK",
                            on_release=lambda *args: (dialog.dismiss(), self.dismiss_and_navigate())
                        )
                    ]
                )
                dialog.text = f"Successfully signed up."
                dialog.open()
                self.manager.show_notification('Success','Successfully signed up.')

                self.ids.address.text = ''
                self.ids.pan_card.text = ''
                self.ids.aadhar_card.text = ''
                self.ids.phone_no.text = ''
                self.ids.password.text = ''
                self.ids.username.text = ''
                self.ids.gmail.text = ''
        except Exception as e:
            print(e)

    @anvil.server.callable
    def is_phone_number_registered(self, phone_number):
        user = app_tables.wallet_users.get(phone=float(phone_number))
        return user is not None

    def dismiss_and_navigate(self):
        existing_screen = self.manager.get_screen('signup')
        self.manager.add_widget(Factory.SignInScreen(name='signin'))
        self.manager.current = 'signin'
        self.manager.remove_widget(existing_screen)
