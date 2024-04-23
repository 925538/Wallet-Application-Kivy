import base64
import io
import traceback

from kivy.uix.screenmanager import SlideTransition
from kivy.utils import platform
import qrcode
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.storage.jsonstore import JsonStore
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivymd.material_resources import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from anvil.tables import app_tables
from kivy.core.window import Window
from addPhone import AddPhoneScreen
from transfer import TransferScreen
from withdraw import WithdrawScreen
from accmanage import AccmanageScreen
from addAccount import AddAccountScreen
from complaint import ComplaintScreen
from help import HelpScreen
from settings import SettingsScreen
from transaction import Transaction
from viewprofile import Profile
from Wallet import AddMoneyScreen
from loadingScreen import loadingScreen
from checkbalance import BalanceScreen
from selftransfer import SelftransferScreen
from referfriend import ReferFriendScreen
from autotopup import AutoTopupScreen
#from qrscanner import ScanScreen
from newQR import QRCodeScreen
from kivy.core.image import  Image as CoreImage
import tempfile
from io import BytesIO
from PIL import Image as imga
navigation_helper = """
<DashBoardScreen>:
    MDNavigationLayout:
    
        MDScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.1
                    pos_hint:{"top":1}
                    #md_bg_color: "#fe5016"

                    MDTopAppBar:
                        title: "[b][color=#ffffff]G WALLET[/color][/b]"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        elevation: 1
                        pos_hint: {"center_y": 1}
                        md_bg_color: "#148EFE"
                        specific_text_color: "#000000"
                        elevation: 1
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]
                        right_action_items: [["account-circle", lambda x: root.manage_acc()]] 
                    
                    MDBoxLayout:
                        orientation: "vertical"                   
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: 0.1
                    pos_hint: {"top":0.9}


                    MDCard:
                        orientation: "vertical"
                        size_hint: None, None
                        size: "320dp", "30dp"
                        md_bg_color: "#C4E3FF"
                        radius: [dp(15), dp(15), dp(15), dp(15)]
                        pos_hint: {"center_y": 1, "center_x": 0.5}

                        MDLabel:
                            text: "Search in G Wallet"
                            theme_text_color: "Custom"  # Disable theme color
                            md_bg_color: 0, 0, 0, 0
                            text_color: 0, 0, 0, 1
                            # size_hint_y:None
                            pos_hint: {"center_x": 0.8, "center_y": 0.5}
                            font_size: "15sp"

                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint: None, None
                        size: "320dp", "20dp"
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.5
                    pos_hint:{"top":0.8}
                    #md_bg_color: "#1650fe"

                    MDBoxLayout:
                        orientation: "vertical"
                        pos_hint: {"center_x": 0.5,"center_y":0.5}
                        #md_bg_color: "#fe168a"
                        size_hint_y: 1
                        size_hint_x: 1


                        MDGridLayout:
                            cols: 3
                            rows: 3
                            spacing: dp(25)
                            size_hint: (None, None)  # Set size_hint to None
                            width: self.minimum_width  # Set width explicitly
                            height: self.minimum_height  # Set height explicitly
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}


                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.nav_transfer()

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    #spacing: dp(-12)

                                    Image:
                                        source: "images/money-transfer.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"   
                                    MDLabel:
                                        text: "Transfer"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"


                                    MDLabel:
                                        text: "Money"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1
                                on_release: root.Add_Money()
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/wallet.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Your"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                                    MDLabel:
                                        text: "Wallet"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None 
                                # elevation: 1
                                on_release: root.nav_withdraw()       
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/cash-withdrawal.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Withdraw"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"
                                    MDLabel:
                                        text: "  Money"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"  
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.nav_addPhone()       
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/phone.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Pay"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                                    MDLabel:
                                        text: "contacts"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"   

                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                #elevation: 1 
                                on_release: root.nav_auto_topup()

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/topup.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Auto"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"
                                    MDLabel:
                                        text: "Topup"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"   
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1 
                                on_release: root.bank_account()         
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/museum.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Bank"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                                    MDLabel:
                                        text: "Accounts"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"    
                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                # elevation: 1
                                on_release: root.nav_self_transfer()  
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/self-transfer.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Self"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                                    MDLabel:
                                        text: "Transfer"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"  

                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                on_release: root.nav_refer()
                                # elevation: 1        
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/refer.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}

                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Refer a"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                                    MDLabel:
                                        text: "friend"
                                        color: 20/255, 142/255, 254/255,1 
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"  

                            MDCard:
                                orientation: "vertical"
                                size_hint: None, None
                                size: "90dp", "90dp"
                                md_bg_color: 0, 0, 0, 0
                                radius: [dp(20), dp(20), dp(20), dp(20)]
                                pos_hint_y: None
                                pos_hint_x:  None
                                #on_release: root.nav_Scanner()
                                # elevation: 1        
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: dp(-12)

                                    Image:
                                        source: "images/scanner.png"
                                        size_hint: (0.4, 1)
                                        pos_hint:{"center_x":0.5,"center_y":0.2}
                                MDBoxLayout:
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "30dp"    
                                    MDLabel:
                                        text: "Scan a"
                                        color: 20/255, 142/255, 254/255,1
                                        font_size: "12sp"
                                        halign: "center"
                                        bold: True
                                    MDLabel:
                                        text: "QR Code"
                                        color: 20/255, 142/255, 254/255,
                                        font_size: "12sp"
                                        bold: True 
                                        halign: "center"

                        MDBoxLayout:
                            orientation: "vertical"
                            #md_bg_color: "#fefe16"

                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y :0.4
                    pos_hint:{"center_y":0.12}
                    md_bg_color: "#C4E3FF"
                    spacing: dp(-10)

                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y :0.28
                        pos_hint:{"center_y":1}

                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.generate_qr_code()  
                            Image:
                                source: "images/qr-code.png"
                                size_hint: (0.5, 0.5)
                                pos_hint:{"center_x":0.1}

                            MDLabel:
                                text: "Receive money from QR code"
                                theme_text_color: "Custom"  # Disable theme color
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)        
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.go_to_transaction()  
                            Image:
                                source: "images/history.png"
                                size_hint: (0.5, 0.5)

                            MDLabel:
                                text: "See transaction history"
                                theme_text_color: "Custom"  
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.nav_check_balance()
                            Image:
                                source: "images/balance.png"
                                size_hint: (0.5, 0.5)
                            MDLabel:
                                text: "Check balance"
                                theme_text_color: "Custom"  
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.1
                            md_bg_color: "#C4E3FF"
                            on_release: root.nav_settings()  
                            Image:
                                source: "images/setting.png"
                                size_hint: (0.5, 0.5)

                            MDLabel:
                                text: "Settings"
                                theme_text_color: "Custom" 
                                text_color: 0, 0, 0, 1
                                font_size: "13sp"
                                pos_hint:{"center_y":0.25}
                            Image:
                                source: "images/right-chevron.png"
                                size_hint: (0.4, 0.4)    
                    MDBoxLayout:
                        orientation: "vertical" 
                        size_hint_y:0.12     

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 10, 10, 0)
            md_bg_color: "#F5F5F5"
            padding: 0 
            spacing: 0
            ContentNavigationDrawer:
                ScrollView: 
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y: 1.2
                        
                        padding:dp(2)
                        spacing:dp(5)
                        
                        MDCard:
                            orientation: "horizontal"
                            size_hint_y :0.13
                            
                            radius: [15, 15, 15, 15]
                            on_release: root.nav_settings() 
                            spacing:dp(102)
                            padding:dp(10)
                            md_bg_color: "#F5F5F5"
                            
                            
                            
                            MDIcon:
                                icon:"arrow-left"
                                theme_text_color: 'Custom'
                                text_color: 0, 0, 0, 1
                                pos_hint:{"center_y":0.5}
                                theme_text_color: "Custom"
                                
                            MDLabel:
                                text: "Profile"
                                theme_text_color: "Custom" 
                                text_color: 0, 0, 0, 1
                                font_size: "18sp"
                                size_hint_x: None
                                pos_hint:{"center_x":0.5}
                            
                            
                            
                            
                        MDBoxLayout: 
                            orientation: "vertical"
                            size_hint_y: 0.29
                            
                            size_hint_x: None
                            height: dp(20)
                            width:dp(270)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.99}
                            padding: dp(10)  
                            spacing:dp(10)
                
                            canvas:
                                Color:
                                    rgba: 1, 1, 1, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [dp(15), dp(15), dp(15), dp(15)]
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.5
                                radius: [15, 15, 15, 15]
                                
                                spacing:dp(65)
                                padding:dp(10)
                            
                                
                                
                                
                                
                                MDIcon:
                                    icon:"qrcode-scan"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5}
                                    theme_text_color: "Custom"
                                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                    size_hint: None, None  # Disable size hint
                                    size: dp(60), dp(60) 
                                    on_touch_down: root.generate_qr_code() if self.collide_point(*args[1].pos) else None
                                    
                                Image:
                                    id: user_image
                                    source: "images/user.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(60), dp(60)  # Set custom size
                                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        
                                MDIcon:
                                    icon:"export-variant"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5}
                                    theme_text_color: "Custom"
                                    pos_hint: {"center_x": 0.9, "center_y": 0.5}
                                    on_touch_down: root.manager.logout() if self.collide_point(*args[1].pos) else None
                                    size: dp(20), dp(20)
                        
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                size_hint_x: 0.5
                                pos_hint: {"center_x": 0.5}
                                spacing:dp(20)
                        
                                MDLabel:
                                    text: "[b]your name[/b]"
                                    id: username_label
                                    markup: True
                                    theme_text_color: "Custom" 
                                    font_name:"Roboto-Bold"
                                    font_size: "18sp"
                                    pos_hint: {"center_x": 0.9}
                                MDLabel:
                                    text: "[b]Email[/b]"
                                    id:email_label
                                    markup: True
                                    theme_text_color: "Custom"  
                                    
                                    font_size: "15sp"
                                    pos_hint:{"center_x":0.58}
                              
                                MDCard:
                                    orientation: "horizontal"
                                    size_hint: None, None
                                    size: "230dp", "30dp"
                                    md_bg_color: "#C4E3FF"
                                    radius: [dp(15), dp(15), dp(15), dp(15)]
                                    pos_hint: {"center_y": 1, "center_x": 0.5}
                                    padding:dp(76)
            
                                    MDLabel:
                                        text: "Edit Profile"
                                        theme_text_color: "Custom"  # Disable theme color
                                        md_bg_color: 0, 0, 0, 0
                                        text_color: 0, 0, 0, 1
                                        size_hint_y:None
                                        pos_hint: {"center_x": 1.4, "center_y": 0.5}
                                        font_size: "15sp"
                                    
                                        
                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            size_hint_x: None
                            height: dp(60)
                            width:dp(270)
                            pos_hint: {'center_x': 0.5, 'center_y': 0.07}
                            padding: dp(20)  
                            spacing:dp(10)
                            
                
                            canvas:
                                Color:
                                    rgba: 115/255, 191/255, 250/255, 1
                                RoundedRectangle:
                                    pos: self.pos
                                    size: self.size
                                    radius: [20, 20, 20, 20] 
                            

                            MDGridLayout:
                                cols:2
                                MDLabel:
                                    text: "[b]Invite Your Friends[/b] \\nEarn $20 both of you"
                                    markup: True
                                    theme_text_color: "Custom"  
                                    md_bg_color: 0, 0, 0, 0
                                    text_color: 0, 0, 0, 1
                                    pos_hint: {"center_x": 0.8, "center_y": 0.5}
                                    font_size: "15sp"

                                MDIcon:
                                    icon: "chevron-right"
                                    pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                                    on_touch_down: root.nav_refer() if self.collide_point(*args[1].pos) else None
                                    theme_text_color: "Custom"
                                    text_color: 0, 0, 0, 1
                        MDBoxLayout: #for features
                            orientation: "vertical"
                            size_hint_y: 0.65
                            pos_hint: {"top":0.8}
                            spacing:dp(25)
                            padding:dp(10)
    
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.generate_qr_code()
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                
                                Image:
                                    source: "images/qr-code.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20) 
                                    pos_hint:{"center_x":0.1}
                                    pos_hint:{"center_y":0.5} 
                                MDLabel:
                                    text: "Your QR code"
                                    theme_text_color: "Custom"  
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    pos_hint:{"center_y":0.5} 
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5} 
                                    theme_text_color: "Custom"
                                    
                                    
    
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.nav_settings() 
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                Image:
                                    source: "images/setting.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20)
                                    pos_hint:{"center_y":0.5}
                                MDLabel:
                                    text: "Settings"
                                    theme_text_color: "Custom" 
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    
                                    pos_hint:{"center_y":0.5}
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5}
                                    theme_text_color: "Custom"
                                    
    
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.nav_auto_topup()
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                Image:
                                    source: "images/topup.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20)
                                    pos_hint:{"center_y":0.5} 
                                MDLabel:
                                    text: "Auto topup"
                                    theme_text_color: "Custom"  
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    pos_hint:{"center_y":0.5}   
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5}   
                                    theme_text_color: "Custom"
                                         
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.profile_view()
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                Image:
                                    
                                    source: "images/account.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20)
                                    pos_hint:{"center_y":0.5} 
                                MDLabel:
                                    text: "Manage account"
                                    theme_text_color: "Custom"  
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    pos_hint:{"center_y":0.5} 
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5}   
                                    theme_text_color: "Custom"
                                    
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.nav_help()
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                Image:
                                    source: "images/help.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20)
                                    pos_hint:{"center_y":0.5} 
                                MDLabel:
                                    text: "Get help"
                                    theme_text_color: "Custom"  
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    pos_hint:{"center_y":0.5} 
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5} 
                                    theme_text_color: "Custom"
                                    
    
                            MDCard:
                                orientation: "horizontal"
                                size_hint_y :0.13
                                radius: [15, 15, 15, 15]
                                on_release: root.nav_complaint()
                                md_bg_color: "#F5F5F5"
                                spacing:dp(40)
                                padding:dp(20)
                                
                                Image:
                                    source: "images/report.png"
                                    size_hint: None, None  # Disable size hint
                                    size: dp(20), dp(20)
                                    pos_hint:{"center_y":0.5} 
                                MDLabel:
                                    text: "Raise a complaint"
                                    theme_text_color: "Custom"  
                                    text_color: 0, 0, 0, 1
                                    font_size: "15sp"
                                    pos_hint:{"center_y":0.5} 
                                MDIcon:
                                    icon:"chevron-right"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5} 
                                    theme_text_color: "Custom"
                                    
    
                            
                                    
                            MDCard:
                                orientation: "horizontal"
                                size_hint: None, None
                                size: "130dp", "33dp"
                                md_bg_color: 115/255, 191/255, 250/255, 1
                                radius: [dp(15), dp(15), dp(15), dp(15)]
                                pos_hint: {"center_y": 1, "center_x": 0.5}
                                padding:dp(30)
                                on_release: root.manager.logout()
                                
                                MDIcon:
                                    icon:"logout"
                                    theme_text_color: 'Custom'
                                    text_color: 0, 0, 0, 1
                                    pos_hint:{"center_y":0.5} 
                                    theme_text_color: "Custom"
                                MDLabel:
                                    text: "Logout"
                                    theme_text_color: "Custom"  # Disable theme color
                                    md_bg_color: 0, 0, 0, 0
                                    text_color: 0, 0, 0, 1
                                    size_hint_y:None
                                    pos_hint: {"center_x": 0.99, "center_y": 0.5}
                                    font_size: "15sp"
                                    
                                    
                                
                        MDBoxLayout:
                            orientation:"vertical"
                            size_hint_y: 0.15
                            #md_bg_color: "#fefe16"

"""
Builder.load_string(navigation_helper)


class BottomAppBar(FloatLayout):
    pass


class MDCardBoxLayout(BoxLayout):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    pass


class DashBoardScreen(Screen):

    def on_enter(self, *args):

        self.ids.email_label.text = str(JsonStore('user_data.json').get('user')['value']['email'])
        self.ids.username_label.text = JsonStore('user_data.json').get('user')['value']['username']
        store = JsonStore('user_data.json').get('user')['value']['phone']
        table = app_tables.wallet_users.get(phone=store)
        image_stored = table['profile_pic']
        if image_stored:
            decoded_image_bytes = base64.b64decode(image_stored)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                temp_file_path = temp_file1.name
                # Write the decoded image data to the temporary file
                temp_file1.write(decoded_image_bytes)
                # Close the file to ensure the data is flushed and saved
                temp_file1.close()
            self.ids.user_image.source = temp_file_path

    def get_username(self):
        store = JsonStore('user_data.json').get('user')['value']
        return store["username"]

    def nav_addPhone(self):
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

        # Perform the actual action (e.g., adding a phone)
        Clock.schedule_once(lambda dt: self.show_addphone_screen(modal_view), 1)

    def show_addphone_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the AddPhoneScreen
        addphone_screen = Factory.AddPhoneScreen(name='addphone')

        # Add the AddPhoneScreen to the existing ScreenManager
        sm.add_widget(addphone_screen)

        # Switch to the AddPhoneScreen
        sm.current = 'addphone'

    def fetch_and_update_addPhone(self):
        store = JsonStore('user_data.json').get('user')['value']
        # Update labels in ComplaintScreen
        addPhone_screen = self.get_screen('addPhone')


    def profile_view(self):
        # Show loading animation
        self.show_loading_screen()

        # Schedule fetching and updating profile data
        Clock.schedule_once(lambda dt: self.fetch_and_update_profile(), 1)

    def fetch_and_update_profile(self):
        # Get user data from the JsonStore
        store = JsonStore('user_data.json').get('user')['value']
        username = store["username"]
        gmail = store["email"]
        phone = store["phone"]
        aadhaar = store["aadhar"]
        address = store["address"]
        pan = store["pan"]

        # Add the Profile screen to the ScreenManager if not added already
        if 'profile' not in self.manager.screen_names:
            self.manager.add_widget(Factory.Profile(name='profile'))

        # Get the instance of the 'Profile' screen
        profile_screen = self.manager.get_screen('profile')

        # Update the labels with user data
        profile_screen.ids.username_label.text = f"Username: {username}"
        profile_screen.ids.email_label.text = f"Email: {gmail}"

        profile_screen.ids.aadhaar_label.text = f"Aadhar: {aadhaar}"
        profile_screen.ids.pan_label.text = f"Pan no: {pan}"
        profile_screen.ids.address_label.text = f"Address: {address}"

        # Dismiss the loading animation
        self.dismiss_loading_screen()

        # Navigate to the 'Profile' screen
        self.manager.current = 'profile'

    def show_loading_screen(self):
        # Create a modal view for the loading animation
        self.modal_view = ModalView(size_hint=(None, None), size=(300, 150), background_color=[0, 0, 0, 0])

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

        # Create a progress bar for the loading animation
        loading_progress = ProgressBar()

        # Add the components to the box layout
        box_layout.add_widget(loading_label)
        box_layout.add_widget(loading_progress)

        # Add the box layout to the modal view
        self.modal_view.add_widget(box_layout)

        # Open the modal view
        self.modal_view.open()

        # Animate the loading text to the center
        Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.5).start(loading_label)

    def dismiss_loading_screen(self):
        # Dismiss the loading animation modal view
        if self.modal_view:
            self.modal_view.dismiss()

    def account_details_exist(self, phone):
        try:
            return app_tables.wallet_users_account.search(phone=phone)  # Returns a list of accounts
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return False

    def nav_withdraw(self):
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
        Clock.schedule_once(lambda dt: self.show_withdraw_screen(modal_view), 1)

    def show_withdraw_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Get phone number from JsonStore
        phone = JsonStore('user_data.json').get('user')['value']["phone"]

        # Check if account details exist
        account_details = self.account_details_exist(phone)

        if account_details:
            # Create a new instance of the WithdrawScreen
            withdraw_screen = Factory.WithdrawScreen(name='withdraw')

            # Add the WithdrawScreen to the existing ScreenManager
            sm.add_widget(withdraw_screen)

            # Switch to the WithdrawScreen
            sm.current = 'withdraw'
        else:
            # If account details do not exist, show the add account dialog
            self.show_add_account_dialog()

    def nav_transfer(self):
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
        Clock.schedule_once(lambda dt: self.show_transfer_screen(modal_view), 1)

    def show_transfer_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Get phone number from JsonStore
        phone = JsonStore('user_data.json').get('user')['value']["phone"]

        # Check if account details exist
        account_details = self.account_details_exist(phone)

        if account_details:
            # Create a new instance of the TransferScreen
            transfer_screen = Factory.TransferScreen(name='transfer')

            # Add the TransferScreen to the existing ScreenManager
            sm.add_widget(transfer_screen)

            # Switch to the TransferScreen
            sm.current = 'transfer'
        else:
            # If account details do not exist, show the add account dialog
            self.show_add_account_dialog()

    def nav_self_transfer(self):
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
        Clock.schedule_once(lambda dt: self.show_self_transfer_screen(modal_view), 1)

    def show_self_transfer_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Get phone number from JsonStore
        phone = JsonStore('user_data.json').get('user')['value']["phone"]

        # Check if account details exist
        account_details = self.account_details_exist(phone)

        if account_details:
            # Create a new instance of the TransferScreen
            transfer_screen = Factory.SelftransferScreen(name='self_transfer')

            # Add the TransferScreen to the existing ScreenManager
            sm.add_widget(transfer_screen)

            # Switch to the TransferScreen
            sm.current = 'self_transfer'
        else:
            # If account details do not exist, show the add account dialog
            self.show_add_account_dialog()

    def show_add_account_dialog(self):
        dialog = MDDialog(
            title="Bank Account Not Found",
            text="You don't have a bank account associated with your phone number. "
                 "Would you like to add a bank account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda *args: (dialog.dismiss(), setattr(self.manager, 'current', 'dashboard'))),
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args:
                    self.add_account_screen(dialog)),
            ],
        )
        dialog.open()

    def add_account_screen(self, dialog):
        dialog.dismiss()
        new_screen = Factory.AddAccountScreen(name='addaccount')
        self.manager.add_widget(new_screen)
        self.manager.current = 'addaccount'

    def go_to_transaction(self):
        # Call on_start to show the loading animation
        self.on_start()

        # Schedule the transition to the transaction screen
        Clock.schedule_once(lambda dt: self.show_transaction_screen(), 1)

    def show_transaction_screen(self):
        # Dismiss the loading animation
        self.dismiss_loading_screen()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the Transaction screen
        transaction_screen = Factory.Transaction(name='transaction')

        # Add the Transaction screen to the existing ScreenManager
        sm.add_widget(transaction_screen)

        # Switch to the Transaction screen
        sm.current = 'transaction'

    def on_start(self):
        # Show the loading animation
        self.show_loading_screen()

        # Perform the actual action (e.g., getting transaction history)
        Clock.schedule_once(lambda dt: self.get_transaction_history(), 1)

    def show_loading_screen(self):
        # Create a modal view for the loading animation
        self.modal_view = ModalView(size_hint=(None, None), size=(300, 150), background_color=[0, 0, 0, 0])

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
        self.modal_view.add_widget(box_layout)

        # Open the modal view
        self.modal_view.open()

        # Animate the loading text to the center
        Animation(pos_hint={'center_x': 0.5, 'center_y': 0.5}, duration=0.5).start(loading_label)

    def dismiss_loading_screen(self):
        # Dismiss the loading animation modal view
        if self.modal_view:
            self.modal_view.dismiss()

    def get_transaction_history(self):
        try:
            # Get the phone number from the JSON file
            store = JsonStore('user_data.json').get('user')['value']
            phone = store['phone']
            # Query the 'transactions' table to fetch the transaction history
            transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
            self.manager.add_widget(Factory.Transaction(name='transaction'))
            trans_screen = self.manager.get_screen('transaction')
            trans_screen.ids.transaction_list.clear_widgets()

            current_date = ""

            # Create a dictionary to store transactions grouped by date
            transactions_by_date = {}

            for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
                                      reverse=True):
                transaction_datetime = transaction['date']
                transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                transaction_date = transaction_date_str.split(' ')[0]
                transactions_text = f"{transaction['receiver_phone']}"
                fund_text = f"{transaction['fund']}"

                # Add transaction to transactions_by_date dictionary
                transactions_by_date.setdefault(transaction_date, []).append(transaction)

            for date, transactions_for_date in transactions_by_date.items():
                # Check if there are any transactions with non-None fund for this date
                if any(transaction['fund'] is not None for transaction in transactions_for_date):
                    header_text = f"[b]{date}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )
                    trans_screen.ids.transaction_list.add_widget(list1)

                    for transaction in transactions_for_date:
                        if transaction['fund'] is not None:
                            transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                            # Add transaction details
                            transaction_item_widget = OneLineListItem(text=f"{transactions_text}",
                                                                      theme_text_color='Custom',
                                                                      text_color=[0, 0, 0, 1], divider=None)
                            transaction_container.add_widget(transaction_item_widget)

                            transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                            if transaction['transaction_type'] == 'Credit':
                                fund_color = [0, 0.5, 0, 1]
                                sign = '+'
                            else:
                                fund_color = [1, 0, 0, 1]
                                sign = '-'

                            fund_label = MDLabel(text=f"{sign}₹{fund_text}", theme_text_color='Custom',
                                                 text_color=fund_color,
                                                 halign='right', padding=(15, 15))
                            transaction_container.add_widget(fund_label)

                            trans_screen.ids.transaction_list.add_widget(transaction_container)

        except Exception as e:
            print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")

    menu = None  # Add this line to declare the menu attribute
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }

    def show_currency_options(self, button):
        currency_options = ["INR", "GBP", "USD", "EUR"]
        self.menu_list = [
            {"viewclass": "OneLineListItem", "text": currency, "on_release": lambda x=currency: self.menu_callback(x)}
            for currency in currency_options
        ]

        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=button,
            items=self.menu_list,
            width_mult=4
        )
        self.menu.open()

    def menu_callback(self, instance_menu_item):
        print(f"Selected currency: {instance_menu_item}")
        store = JsonStore('user_data.json')
        phone_no = store.get('user')['value']["phone"]
        total_balance = self.manager.get_total_balance(phone_no, instance_menu_item)
        # Convert the total balance to the selected currency

        self.ids.balance_lbl.text = f'balance: {total_balance} '
        print(total_balance)
        self.ids.options_button.icon = self.options_button_icon_mapping.get(instance_menu_item, "currency-inr")
        self.menu.dismiss()

    def generate_qr_code(self):
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

        # Perform the actual action (e.g., showing the add money screen)
        Clock.schedule_once(lambda dt: self.show_qr(modal_view), 1)

    def show_qr(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the screen for adding money
        qr_screen = Factory.QRCodeScreen(name='qrcode')

        # Add the screen for adding money to the existing ScreenManager
        sm.add_widget(qr_screen)

        # Switch to the screen for adding money
        sm.current = 'qrcode'

    def nav_addContact(self):
        self.manager.current = 'addcontact'

    def Add_Money(self):
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

        # Perform the actual action (e.g., showing the add money screen)
        Clock.schedule_once(lambda dt: self.show_addmoney_screen(modal_view), 1)


    def show_addmoney_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the screen for adding money
        add_money_screen = Factory.WalletScreen(name='WalletScreen')

        # Add the screen for adding money to the existing ScreenManager
        sm.add_widget(add_money_screen)

        # Switch to the screen for adding money
        sm.current = 'WalletScreen'

    def bank_account(self):
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

        # Perform the actual action (e.g., opening the bank account screen)
        Clock.schedule_once(lambda dt: self.show_bankaccount_screen(modal_view), 1)

    def show_bankaccount_screen(self, modal_view):
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

    def nav_settings(self):
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

        # Perform the actual action (e.g., opening the settings screen)
        Clock.schedule_once(lambda dt: self.show_settings_screen(modal_view), 1)

    def show_settings_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the SettingsScreen
        settings_screen = Factory.SettingsScreen(name='settings')

        # Add the SettingsScreen to the existing ScreenManager
        sm.add_widget(settings_screen)

        # Switch to the SettingsScreen
        sm.current = 'settings'

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

    def nav_complaint(self):
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

        # Perform the actual action (e.g., opening the complaint screen)
        Clock.schedule_once(lambda dt: self.show_complaint_screen(modal_view), 1)

    def show_complaint_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the ComplaintScreen
        complaint_screen = Factory.ComplaintScreen(name='complaint')

        # Add the ComplaintScreen to the existing ScreenManager
        sm.add_widget(complaint_screen)

        # Switch to the ComplaintScreen
        sm.current = 'complaint'

    def nav_Scanner(self):
        # Check if the platform is Android
        # if platform == 'android':
        #     from android.permissions import request_permission, Permission
        #     def callback(permissions, grant_results):
        #         if all(grant_results):
        #             self.show_scanner_modal()
        #         else:
        #             # Permission denied
        #             # Handle permission denial here (e.g., display error message)
        #             self.manager.current = "dashboard"
        #             pass
        #
        #     request_permission(Permission.CAMERA, callback)
        # else:
        #     # For non-Android platforms, directly open the scanner modal
        self.show_scanner_modal()

    def show_scanner_modal(self):
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

        # Perform the actual action (e.g., opening QR scanner)
        Clock.schedule_once(lambda dt: self.show_scanner_screen(modal_view), 1)

    def show_scanner_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the QRCodeScannerScreen
        qr_scanner_screen = Factory.ScanScreen(name='qrscanner')

        # Add the QRCodeScannerScreen to the existing ScreenManager
        sm.add_widget(qr_scanner_screen)

        # Switch to the QRCodeScannerScreen
        sm.current = 'qrscanner'

    def nav_check_balance(self):
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

        # Perform the actual action (e.g., checking balance)
        Clock.schedule_once(lambda dt: self.show_check_balance_screen(modal_view), 1)

    def show_check_balance_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the BalanceScreen
        balance_screen = Factory.BalanceScreen(name='checkbalance')

        # Add the BalanceScreen to the existing ScreenManager
        sm.add_widget(balance_screen)

        # Switch to the BalanceScreen
        sm.current = 'checkbalance'

    def nav_refer(self):
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

        # Perform the actual action (e.g., showing the add money screen)
        Clock.schedule_once(lambda dt: self.show_refer_screen(modal_view), 1)

    def show_refer_screen(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the screen for adding money
        refer_screen = Factory.ReferFriendScreen(name='refer')

        # Add the screen for adding money to the existing ScreenManager
        sm.add_widget(refer_screen)

        # Switch to the screen for adding money
        sm.current = 'refer'

    def nav_auto_topup(self):
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

        # Perform the actual action (e.g., showing the add money screen)
        Clock.schedule_once(lambda dt: self.show_auto_topup(modal_view), 1)

    def show_auto_topup(self, modal_view):
        # Dismiss the loading animation modal view
        modal_view.dismiss()

        # Retrieve the screen manager
        sm = self.manager

        # Create a new instance of the screen for adding money
        auto_topup = Factory.AutoTopupScreen(name='auto_topup')

        # Add the screen for adding money to the existing ScreenManager
        sm.add_widget(auto_topup)

        # Switch to the screen for adding money
        sm.current = 'auto_topup'



    def manage_acc(self):
        screen = self.manager
        profile_screen = Factory.Profile(name="profile")
        screen.add_widget(profile_screen)
        screen.current = 'profile'
