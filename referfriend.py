from anvil.tables import app_tables
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
import random
import string
import pyperclip
from kivy.storage.jsonstore import JsonStore
from kivy.base import EventLoop
from kivymd.uix.textfield import MDTextField
from kivy.factory import Factory
from kivy.uix.modalview import ModalView
import tempfile
Builder.load_string('''
# <ReferFriendScreen>:
#     Screen:
#         MDTopAppBar:
#             title: 'Referral'
#             anchor_title:'left'
#             elevation: 2
#             left_action_items: [['arrow-left', lambda x: root.go_back()]]
#             md_bg_color: "#148EFE"
#             specific_text_color: "#ffffff"
#             pos_hint: {'top':1}
#         BoxLayout:
#             orientation: 'vertical'
#             pos_hint:{'center_y':.91}
#             padding:dp(10)
            
#             # Widget:
#             #     size_hint_y: None
#             #     height:dp(15)    
#             MDLabel:
#                 text: "Invite friends to GWallet"
#                 size_hint_y: None
#                 height: self.texture_size[1]
#                 # halign: 'left'  
#                 pos_hint:{'center_x':.5,'center_y':.78}
#                 font_size: dp(20)
                
#             Widget:
#                 size_hint_y: None
#                 height:dp(10)
                     
#             MDLabel:
#                 text: "Invite friends to GWallet and get ₹100 and when your friends make their first payment they get ₹50!"
#                 size_hint_y: None
#                 height: self.texture_size[1]
#                 # halign: ''
#                 theme_text_color: "Secondary"
#                 font_size: dp(15)
#             BoxLayout:
#                 orientation: 'horizontal'
#                 size_hint_y: None
#                 height: dp(100)
#                 # padding:dp(10)
#                 spacing: dp(20)
    
#                 MDTextField:
#                     id: textinput1
#                     hint_text: "userfullname"
#                     font_size: 24
#                     color: 0, 0, 0, 1
#                     size_hint_x: 0.5
    
#                 MDTextField:
#                     id: textinput2
#                     hint_text: "usercode"
#                     font_size: 24
#                     color: 0, 0, 0, 1
#                     size_hint_x: 0.5
            
#             MDRectangleFlatButton:
#                 text: 'Copy Code'
#                 pos_hint: {'center_x': 0.5, 'center_y': 0.5}
#                 size_hint: (0.4, None)  # Increase button size
#                 on_release: root.copy_code()
#                 text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
#                 line_color: [0, 0, 0, 0]  # Set line color to transparent
    
#             MDRoundFlatButton: 
#                 id: button2
#                 text: 'Search Contacts'
#                 pos_hint: {'center_x': 0.5, 'center_y': 0.7}
#                 size_hint: (0.8, None)  # Increase button size
#                 theme_text_color: "Custom"  # Use custom text color
#                 text_color: (67 / 255, 67 / 255, 67 / 255, 1)  # Set text color to rgba(67, 67, 67, 1)
#                 md_bg_color: (217 / 255, 217 / 255, 217 / 255, 1)  # Set background color to rgba(217, 217, 217, 1)
#                 line_color: [0, 0, 0, 0]  # Set line color to transparent    
#             MDList:
#                 id: contacts_list
#                 OneLineListItem:
#                     text: "Contact number 1"
#                 OneLineListItem:
#                     text: "Contact number 2"
#lines 416 422 426 282
#:import MDIconButton kivymd.uix.button.MDIconButton
            
<ReferFriendScreen>:
    Screen:
        BoxLayout:
            orientation: 'vertical'
            pos_hint:{"center_x":0.5}
            
            # MDTopAppBar:
            #     title: 'Referral'
            #     anchor_title: 'left'
            #     elevation: 2
            #     left_action_items: [MDIconButton(icon='arrow-left', on_press=lambda x: root.go_back(), pos_hint={'x': 0.1})]
            #     right_action_items: [MDIconButton(icon='magnify', on_press=lambda x: root.open_search()), MDIconButton(icon='dots-vertical')]
            #     md_bg_color: "#148EFE"
            #     specific_text_color: "#ffffff"
            #     pos_hint: {'top': 1}
            
            MDCard:
            
                size_hint_x:None
                size_hint_y:None
                
                width:root.width*1
                height:root.height*0.1
                
                radius:[0,0,0,0]
                
                md_bg_color: "#148EFE"
                elevation:2

                
                MDBoxLayout:
                
                    size_hint_x:None
                    size_hint_y:None
                    
                    width:self.parent.width
                    height:self.parent.height
                    
                    
                    
                    
                    
                    AnchorLayout:
                        
                        pos_hint:{"center_x":0.1,"center_y":0.5}
                        size_hint_y:None
                        size_hint_x:None
                        
                        width:dp(40)
                        height:dp(20)
                        anchor_x:"left"
                        MDIconButton:
                            
                            icon:"arrow-left"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            on_release:root.go_back()
                        
                    Widget:
                        size_hint_x:None
                        width:dp(10)
                        
                    AnchorLayout:
                        
                        pos_hint:{"center_x":0.1}
                        MDLabel:
                            
                            text:"Referral"
                            # bold:True
                            theme_text_color: 'Custom'
                            font_size:"22sp"
                            text_color:1,1,1,1
                
                    Widget:
                        size_hint_x:None
                        width:root.width*0.3
                    
                    MDBoxLayout:
                        pos_hint:{"center_x":0.8}
                    
                        AnchorLayout:
                            pos_hint:{"center_x":1}
                            # anchor_x:"right"
                            
                            
                            MDIconButton:
                                
                                icon:"magnify"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                on_release:root.open_search()
                
                
                        AnchorLayout:
                            
                            # pos_hint:{"center_x":0.99,"center_y":0.5}
                            anchor_x:"right"
                            
                            MDIconButton:
                                
                                icon:"dots-vertical"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                        
                    
                        
                        
                    
                    

                            
                            
            Widget:
                size_hint_y:None
                height:dp(5)    
                
            BoxLayout:
                orientation: 'vertical'
                pos_hint:{'center_y':.1}
                padding:dp(10)

                MDLabel:
                    text: "Invite friends to GWallet"
                    size_hint_y: None
                    height: self.texture_size[1]
                    # halign: 'left'  
                    pos_hint:{'center_x':.5,'center_y':.78}
                    font_size: dp(25)
    
                Widget:
                    size_hint_y: None
                    height:dp(10)
    
                MDLabel:
                    text: "Invite friends to GWallet and get ₹100 and when your friends make their first payment they get ₹50!"
                    size_hint_y: None
                    height: self.texture_size[1]
                    # halign: ''
                    theme_text_color: "Secondary"
                    font_size: dp(15)
                BoxLayout:
                    pos_hint: {"center_y": 0.9}

                    Widget:
                        size_hint_x:None
                        width:dp(5)


                    Image:
                        id:user_image
                        source: "images/user.png"
                        size_hint_x: None
                        width: dp(48)
                        size_hint_y:None
                        height:dp(48)
                        pos_hint: {"center_x":0.5,"center_y": 0.4}


                    TwoLineListItem:
                        id:textinput1
                        text: "No result"
                        secondary_text: " "
                        on_release: root.on_number_click(float(root.ids.search_text_card.text))
                        pos_hint:{"center_y":0.4}
                        valign: "center"
                        divider: None
                    
                        MDTextButton:
                            text: "Share"
                            font_size: "15sp"
                            # halign: 'center'
                            # underline:True
                            bold:True
                            theme_text_color: 'Custom'
                            text_color: 0.117, 0.459, 0.725, 1
                            pos_hint:{"center_x":0.9,"center_y":0.47}
                            padding_x:dp(10)
                            

                MDSeparator:
                    height: '1dp'
                    

                Widget:
                    size_hint_y:None
                    height:dp(150)
            BoxLayout:
                orientation: 'vertical'
                pos_hint:{"center_y":0.1}
    
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: dp(40)
                    spacing:dp(5)

                    Widget:
                        size_hint_y:None
                        height: dp(3)

                    MDTextField:
                        id: search_text_card
                        line_color_normal: app.theme_cls.colors['Gray']['500']
                        fill_color_normal: 1, 1, 1, 1
                        text:""
                        hint_text: 'Search Name or Mobile No.'
                        icon_left: "magnify"
                        hint_text_color_normal: 0, 0, 0, 0.7
                        # bold:True
                        mode: 'rectangle'
                        multiline: False
                        size_hint_x: 0.9
                        size_hint_y: None
                        height: dp(40)
                        radius: [10,10,10,10]
                        padding: dp(10)
                        on_text_validate: root.on_search_text_entered()
                        pos_hint: {"center_y": 0.7, 'x': 0.05}  # Adjust the value to move it down   
                        
                Widget:
                    size_hint_y: None
                    height: "40dp"
                # 
                # MDCard:
                #     orientation: "vertical"
                #     size_hint: None, None
                #     width: root.width * 0.9
                #     height: root.height * 0.13
                #     elevation: 1
                #     md_bg_color: (1, 1, 1, 1)
                #     pos_hint: {"center_x": 0.5, "center_y": 0.3}
                # 



                BoxLayout:
                    md_bg_color:1,1,0,1
                    pos_hint: {"center_y": 0.4,"center_x":0.54}
                    size_hint_x:None
                    width:root.width*0.97

                    # Widget:
                    #     size_hint_x:None
                    #     width:dp(5)

                    BoxLayout:
                        # md_bg_color:1,1,0,1
                        pos_hint: {"center_y": 0.4,"center_x":0.3}
                        Image:
                            id: image_id
                            source: ""
                            size_hint_x: None
                            width: dp(48)
                            size_hint_y: None
                            height: dp(48)
                            pos_hint: {"center_x":0.5,"center_y": 0.3}
    
    
                        TwoLineListItem:
                            id: search_result_item
                            text: "No result"
                            secondary_text: " "
                            # on_release: root.on_number_click(float(root.ids.search_text_card.text))
                            pos_hint:{"center_y":0.3}
                            valign: "center"
                            # divider:None
                            md_bg_color:0,1,1,1
                            size_hint_x:None
                            width:root.width*0.8
                            
                            BoxLayout:
                                orientation: 'horizontal'
                                size_hint_y: None
                                height: dp(30)
                                pos_hint: {"center_x":0.55,"center_y": 0.3}
                                # spacing: dp(10)
                                
                                MDLabel:
                                    id: phone_number
                                    text:""
                                    halign: 'left'
                                    valign: 'middle'
                                    size_hint_x: None
                                    width: dp(90)
                                    theme_text_color: 'Custom'
                                    text_color: 0.5, 0.5, 0.5, 1
                                    
                                AnchorLayout:
                                    anchor_x:"left"
                                    # pos_hint:{"center_x":0.0}
                                
                                    MDTextButton:
                                        id:invite
                                        text: " "
                                        bold:True
                                        font_size: "15sp"
                                        # halign: 'center'
                                        # underline:True
                                        theme_text_color: 'Custom'
                                        text_color: 0.117, 0.459, 0.725, 1
                                        # pos_hint:{"center_x":0.01,"center_y":0.3}
                                    # padding_x:dp(10)
                                
                                # Widget:
                                #     size_hint_x:None
                                #     height:dp(150)
    
                            MDIcon:
                                id:logo_id
                                icon:""
                                theme_text_color: 'Custom'
                                text_color: 0.145, 0.827, 0.4, 1
                                pos_hint:{"center_x":0.9,"center_y":0.47}
                                theme_text_color: "Custom"
                                
                                padding_x:dp(10)

                    Widget:
                        size_hint_y: None
                        height: "120dp"
                    # Widget:
                    #     size_hint:None,None
                    #     height:dp(20)
                Widget:
                    size_hint:None,None
                    height:dp(350)
                   
        Widget:
            size_hint_y: None
            height: "180dp"
''')

class CustomLabel(Label):
    pass

class ReferFriendScreen(Screen):

    def __init__(self, **kwargs):
        super(ReferFriendScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        phone = JsonStore('user_data.json').get('user')['value']['users_phone']
        username = JsonStore('user_data.json').get('user')['value']['users_username']
        self.ids.textinput1.text = username
        user = app_tables.wallet_users.get(users_phone=phone)
        if user['users_profile_pic']:
                try:
                    decoded_image_bytes =user['users_profile_pic'].get_bytes()
                    # core_image =  CoreImage(BytesIO(decoded_image_bytes), ext='png',filename='image.png')
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                        temp_file_path = temp_file1.name
                        # Write the decoded image data to the temporary file
                        temp_file1.write(decoded_image_bytes)
                        # Close the file to ensure the data is flushed and saved
                        temp_file1.close()
                    self.ids.user_image.source=temp_file_path
                except Exception as e:
                    print(e)
        else:
            self.ids.user_image.source = "images/user.png"

        if not user['users_referral']:
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.ids.textinput1.secondary_text = random_code
            user.update(users_referral=random_code)
        else:
            self.ids.textinput1.secondary_text = f"[size=21]{user['users_referral']}[/size]"

    def copy_code(self):
        from kivy.utils import ask
        code_to_copy = self.ids.textinput2.text
        pyperclip.copy(code_to_copy)

    def go_back(self):
        existing_screen = self.manager.get_screen('refer')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def on_search_text_entered(self):
        number = float(self.ids.search_text_card.text)
        try:
            userdata = app_tables.wallet_users.get(users_phone=number)

            username = userdata['users_username']
            print(f'username in SearchField:{username}')
            self.ids.search_result_item.disabled = False
            self.ids.search_result_item.text = username
            self.ids.phone_number.text = str(int(number))
            self.ids.invite.text = ". Invite"
            # self.ids.contact_label.text = number
            self.ids.search_result_item.children[0].icon = "whatsapp"
            if userdata['users_profile_pic']:
                    try:
                        decoded_image_bytes =userdata['users_profile_pic'].get_bytes()
                        # core_image =  CoreImage(BytesIO(decoded_image_bytes), ext='png',filename='image.png')
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                            temp_file_path = temp_file1.name
                            # Write the decoded image data to the temporary file
                            temp_file1.write(decoded_image_bytes)
                            # Close the file to ensure the data is flushed and saved
                            temp_file1.close()
                        self.ids.image_id.source=temp_file_path
                    except Exception as e:
                        print(e)
            else:
                self.ids.image_id.source = "images/user.png"
            # self.ids.image_id.size = (44, 44)
            # self.ids.image_id.allow_stretch= True
            # self.ids.image_id.keep_ratio= True

            return username

        except Exception as e:
            print(e)
            self.manager.show_notification('Alert!', 'User not found.')
            self.ids.search_text_card.text = ""
            self.ids.search_result_item.text = "No result"
            self.ids.image_id.source = ""
            self.ids.phone_number.text = ""
            self.ids.invite.text = ""
            self.ids.logo_id.text = ""

            return {}

    def on_number_click(self, number):
        phone_number = self.ids.search_text_card.text
        if phone_number:
            username = self.ids.search_result_item.text
            self.manager.add_widget(Factory.UserDetailsScreen(name='userdetails'))
            self.manager.current = 'userdetails'
            user_details_screen = self.manager.get_screen('userdetails')
            user_details_screen.username = username
            user_details_screen.phone_number = phone_number
            user_details_screen.current_user_phone = self.current_user_phone
            print(self.current_user_phone)

            # Fetch the user details from the database
            user_data = app_tables.wallet_users.get(phone=number)

            if user_data:
                user_details_screen.current_user_phone = self.current_user_phone
                print(self.current_user_phone)
                user_details_screen.searched_user_phone = str(
                    user_data['users_phone'])  # Adjust this based on your data structure
                print(f"{user_data['users_phone']}")
            else:
                print(f"User with phone number {number} not found in the database")
                self.manager.show_notification('Alert!', 'User not found.')
    
    def open_search(self):
        search_view = ModalView(size_hint=(0.8, 0.2), auto_dismiss=True)
        search_field = MDTextField(
            hint_text="Search...",
            size_hint=(1, None),
            height="40dp",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            multiline=False,
        )
        search_view.add_widget(search_field)
        search_view.open()