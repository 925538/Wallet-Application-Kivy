from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivymd.uix.screen import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import TouchBehavior
from kivy.base import EventLoop
Window.clearcolor = (1, 1, 1, 1)

# Define the Kivy language string
Builder.load_string('''
<GuideScreen>:
    ScrollView:
        size_hint: (1, 1)
        bar_width: 10
        scroll_type: ['bars']
        bar_color: (0.2, 0.2, 0.2, 0.8)

        MDGridLayout:
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(10)
            
            MDTopAppBar:
                id: top_bar
                title: "Welcome to GWallet Guide"
                anchor_title:'left'
                left_action_items: [["arrow-left", lambda x: root.go_back()]] 
                background_color: (173, 216, 230)
                pos_hint: {'top': 1}
        
            MDLabel:
                text: "  Make seamless payments"
                halign: 'left'
                font_style: 'H5'
                size_hint_y: None
                height: self.texture_size[1]  # Adjust the label's height based on text size  
                pos_hint: {'center_x': 0.5, 'center_y': 0.85}  # Center label horizontally and vertically
                
                
            MDGridLayout:
                cols: 2
                rows: 4
                spacing: dp(15)
                size_hint: (None, None)  # Set size_hint to None
                width: self.minimum_width  # Set width explicitly
                height: self.minimum_height  # Set height explicitly
                pos_hint: {"center_x": 0.5, "center_y": 0.68}
        
                MDCard:
                    orientation:"vertical"
                    id: bank_card
                    orientation: "vertical"
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(1)
                    pos_hint: {"center_x": 0.2, "center_y": 0.6}
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/bank.png'  
                            size_hint: (0.2, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.2}
                             
                        MDLabel:
                            text: " Change default Bank Account"
                            size_hint_y: None
                            height: self.texture_size[1]
                            halign: "center"
                            
                MDCard:
                    orientation:"vertical"
                    id: add_bank_card
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(2)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/addbank.png'  
                            size_hint: (0.3, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.1}
                        
                    MDLabel:
                        text:"Add New Bank Account"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
                        
                MDCard:
                    orientation:"vertical"
                    id: transfer_money_card 
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(3)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing:dp(20)
                        Image:
                            source: 'images/moneytransfer.png'  
                            size_hint: (0.2, 1)
                            pos_hint: {"center_x": 0.5, "center_y": 0.5} 
        
                    MDLabel:
                        text: "Transfer Money"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
                        
          
                MDCard:
                    orientation:"vertical"
                    id: check_balance_card
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(4)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/checkbalance.png'  
                            size_hint: (0.2, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.7}
        
                    MDLabel:
                        text: " Check Bank Account Balance"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
                        
                        
            MDLabel:
                text: "  Insurance"
                halign: 'left'
                font_style: 'H5'
                size_hint_y: None
                height: self.texture_size[1]  # Adjust the label's height based on text size  
                pos_hint: {'center_x': 0.5, 'center_y': 0.51}  # Center label horizontally and vertically
        
            MDGridLayout:
                cols: 2
                rows: 1
                spacing: dp(15)
                size_hint: (None, None)  # Set size_hint to None
                width: self.minimum_width  # Set width explicitly
                height: self.minimum_height  # Set height explicitly
                pos_hint: {"center_x": 0.25, "center_y": 0.34}
                adaptive_height:True
                adaptive_width:True
        
                MDCard:
                    orientation:"vertical"
                    id: recharge_card
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(1)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/protect.png' 
                            size_hint: (0.2, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.4}
        
                    MDLabel:
                        text: "  Protect your Payments"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
        
                MDCard:
                    orientation:"vertical"
                    id: electricity_card
                    size_hint: None, None
                    size: "180dp", "150dp"
                    on_press: root.card_clicked(2)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/heart.png'  
                            size_hint: (0.2, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.4}
        
                    MDLabel:
                        text: "Mediclaim Calculator"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
        
                        
            MDLabel:
                text: "  Utilise your Wallet"
                halign: 'left'
                font_style: 'H5'
                size_hint_y: None
                height: self.texture_size[1]  # Adjust the label's height based on text size  
                pos_hint: {'center_x': 0.5, 'center_y': 0.17}  # Center label horizontally and vertically
        
            MDGridLayout:
                cols: 5
                rows: 1
                spacing: dp(15)
                size_hint: (None, None)  # Set size_hint to None
                width: self.minimum_width  # Set width explicitly
                height: self.minimum_height  # Set height explicitly
                pos_hint: {"center_x": 0.16, "center_y": 0}
        
                MDCard:
                    id:wallet_card
                    orientation:"vertical"
                    size_hint: None, None
                    halign: 'left'
                    size: "180dp", "140dp"
                    on_press: root.card_clicked(1)
                    
                    MDBoxLayout:
                        orientation: 'vertical'
                        Image:
                            source: 'images/walletmoney.png'  
                            size_hint: (0.2, 1)
                            pos_hint:{"center_x":0.5,"center_y":0.4}
        
                    MDLabel:
                        text: " Add money to Wallet"
                        size_hint_y: None
                        height: self.texture_size[1]
                        halign: "center"
''')


class GuideScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('guide')
        self.manager.current = 'settings'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(GuideScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def card_clicked(self, card_number):
        print(f"Card {card_number} clicked")


