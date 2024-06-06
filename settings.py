from kivy.animation import Animation
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivy.storage.jsonstore import JsonStore
from paysetting import PaysettingScreen
from addPhone import UserDetailsScreen
from accmanage import AccmanageScreen
from Wallet import AddMoneyScreen
from editprofile import EditUser
from reset import ResetPassword
from gguide import GuideScreen

KV = '''
<SettingsScreen>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Settings'
                    anchor_title:'left'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(260)
                        pos_hint: {'center_x': 0.45, 'y': 220}        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: '4dp'

                            OneLineIconListItem:
                                text: "Payment Settings"
                                on_release: root.nav_paysetting()
                                IconLeftWidget:
                                    icon: "wallet"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")  
                            OneLineIconListItem:
                                text: "Help & Support"
                                on_release: root.nav_help()
                                IconLeftWidget:
                                    icon: "help-circle" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb") 
                            OneLineIconListItem:
                                text: "Profile Settings"
                                on_release: root.edit_profile()  
                                IconLeftWidget:
                                    icon: "account-cog"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")     
                            OneLineIconListItem:
                                text: "App info"
                                on_release: root.nav_guide_screen()
                                IconLeftWidget:
                                    icon: "information-outline" 
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")   
                            OneLineIconListItem:
                                text: "Change password"
                                on_release: root.nav_reset()  
                                IconLeftWidget:
                                    icon: "shield-edit"
                                    theme_text_color: 'Custom'
                                    text_color: get_color_from_hex("#3489eb")          
'''
kv = """
<SettingsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        size_hint_y: 1
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color:"#148EFE"
            size_hint_y: 0.05
            pos_hint:{"top":1}
            MDTopAppBar:
                title: 'Settings'
                anchor_title:'left'
                elevation: 0
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: "#148EFE"
                specific_text_color: "#ffffff" 
                pos_hint:{"top":1}   
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: 0.5
            pos_hint:{"top":0.95}
            
            MDBoxLayout:
                orientation: "vertical"
                spacing: '5dp'
                size_hint_y: 0.9
                MDBoxLayout:
                    orientation: "vertical"
                    OneLineIconListItem:
                        text: "Payment Settings"
                        on_release: root.nav_paysetting()
                        IconLeftWidget:
                            icon: "wallet"
                            theme_text_color: 'Custom'
                            text_color: get_color_from_hex("#3489eb")  
                    OneLineIconListItem:
                        text: "Help & Support"
                        on_release: root.nav_help()
                        IconLeftWidget:
                            icon: "help-circle" 
                            theme_text_color: 'Custom'
                            text_color: get_color_from_hex("#3489eb") 
                    OneLineIconListItem:
                        text: "Profile Settings"
                        on_release: root.edit_profile()  
                        IconLeftWidget:
                            icon: "account-cog"
                            theme_text_color: 'Custom'
                            text_color: get_color_from_hex("#3489eb")
                                       
                    OneLineIconListItem:
                        text: "App info"
                        on_release: root.nav_guide_screen()
                        IconLeftWidget:
                            icon: "information-outline" 
                            theme_text_color: 'Custom'
                            text_color: get_color_from_hex("#3489eb") 
                                                                   
                    OneLineIconListItem:
                        text: "Change password"
                        on_release: root.nav_reset()  
                        IconLeftWidget:
                            icon: "shield-edit"
                            theme_text_color: 'Custom'
                            text_color: get_color_from_hex("#3489eb")
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y:0.3
                
                            
            MDBoxLayout:
                orientation: "vertical"
    
                     
                   
    
"""
Builder.load_string(KV)


class SettingsScreen(Screen):
    def go_back(self):
        # existing_screen = self.manager.get_screen('settings')
        self.manager.current = 'dashboard'
        # self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def edit_profile(self):
        self.manager.add_widget(Factory.EditUser(name='edituser'))
        edit_screen = self.manager.get_screen('edituser')
        store = JsonStore('user_data.json').get('user')['value']
        edit_screen.ids.username.text = store["users_username"]
        edit_screen.ids.email.text = store["users_email"]
        edit_screen.ids.phone.text = str(store["users_phone"])
        # edit_screen.ids.password.text = store["password"]
        edit_screen.ids.aadhaar.text = str(store["users_aadhar"])
        edit_screen.ids.pan.text = store["users_pan"]
        edit_screen.ids.address.text = store["users_address"]
        self.manager.current = 'edituser'

    def nav_paysetting(self):
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

        # Perform the actual action (e.g., navigating to paysetting screen)
        Clock.schedule_once(lambda dt: self.show_paysetting_screen(modal_view), 1)

    def show_paysetting_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the PaysettingScreen
        paysetting_screen = Factory.PaysettingScreen(name='paysetting')

        # Add the PaysettingScreen to the existing ScreenManager
        sm.add_widget(paysetting_screen)

        # Switch to the PaysettingScreen
        sm.current = 'paysetting'

    def nav_accmanage(self):
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

        # Perform the actual action (e.g., navigating to accmanage screen)
        Clock.schedule_once(lambda dt: self.show_accmanage_screen(modal_view), 1)

    def show_accmanage_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the AccmanageScreen
        accmanage_screen = Factory.AccmanageScreen(name='accmanage')

        # Add the AccmanageScreen to the existing ScreenManager
        sm.add_widget(accmanage_screen)

        # Switch to the AccmanageScreen
        sm.current = 'accmanage'

    def nav_userdetails(self):
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

        # Perform the actual action (e.g., navigating to userdetails screen)
        Clock.schedule_once(lambda dt: self.show_userdetails_screen(modal_view), 1)

    def show_userdetails_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the UserDetailsScreen
        userdetails_screen = Factory.UserDetailsScreen(name='userdetails')

        # Add the UserDetailsScreen to the existing ScreenManager
        sm.add_widget(userdetails_screen)

        # Switch to the UserDetailsScreen
        sm.current = 'userdetails'

    def Add_Money(self):
        self.manager.add_widget(Factory.AddMoneyScreen(name='Wallet'))
        self.manager.current = 'Wallet'

    def nav_help(self):
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

        # Animate the loading text to the center
        Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.5).start(loading_label)

        # Perform the actual action (e.g., opening the help screen)
        Clock.schedule_once(lambda dt: self.show_help_screen(modal_view), 1)

    def show_help_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the HelpScreen
        help_screen = Factory.HelpScreen(name='help')

        # Add the HelpScreen to the existing ScreenManager
        sm.add_widget(help_screen)

        # Switch to the HelpScreen
        sm.current = 'help'

    def nav_reset(self):
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

        # Animate the loading text to the center
        Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.5).start(loading_label)

        # Perform the actual action (e.g., opening the help screen)
        Clock.schedule_once(lambda dt: self.show_reset_screen(modal_view), 1)

    def show_reset_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the HelpScreen
        reset_screen = Factory.ResetPassword(name='reset')

        # Add the HelpScreen to the existing ScreenManager
        sm.add_widget(reset_screen)

        # Switch to the HelpScreen
        sm.current = 'reset'

    def nav_guide_screen(self):
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

        # Animate the loading text to the center
        Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.5).start(loading_label)

        # Perform the actual action (e.g., opening the help screen)
        Clock.schedule_once(lambda dt: self.show_guide_screen(modal_view), 1)

    def show_guide_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the HelpScreen
        guide_screen = Factory.GuideScreen(name='guide')

        # Add the HelpScreen to the existing ScreenManager
        sm.add_widget(guide_screen)

        # Switch to the HelpScreen
        sm.current = 'guide'
