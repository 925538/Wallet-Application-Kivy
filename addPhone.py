from datetime import datetime
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.graphics import Color
from kivy.metrics import dp
from kivy.properties import StringProperty,ListProperty,NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.graphics import RoundedRectangle
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from anvil.tables import app_tables
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.base import EventLoop
from kivy.graphics import Color, Rectangle, Line
from kivymd.uix.card import MDSeparator
from kivymd.uix.button import MDIconButton
import tempfile
KV = '''
<AddPhoneScreen>:
    Screen:
        BoxLayout:
            orientation: 'vertical'

            MDTopAppBar:
                title: root.top_app_bar_title
                halign:'center'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                right_action_items: [["", lambda x:None]]
                md_bg_color: "#148EFE"
                specific_text_color: "#ffffff"
                pos_hint: {'top': 1}

            ScrollView:
                BoxLayout:
                    orientation: 'vertical'

                      # Adjust the height as needed
                    MDCard:
                        size_hint:None,None
                        width:root.width
                        height:root.height
                        orientation:"vertical"

                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: dp(10)
                            spacing:dp(5)

                            Widget:
                                size_hint_y:None
                                height: dp(8)

                            MDTextField:
                                id: search_text_card
                                line_color_normal: app.theme_cls.colors['Gray']['500']
                                fill_color_normal: 1, 1, 1, 1
                                hint_text: 'Search for contacts'
                                icon_left: "magnify"
                                hint_text_color_normal: 0, 0, 0, 0.7
                                # bold:True
                                mode: 'rectangle'
                                multiline: False
                                size_hint_x: 0.9
                                size_hint_y: None
                                height: dp(40)
                                radius: [25,25,25,25]
                                padding: dp(10)
                                on_text_validate: root.on_search_text_entered()
                                pos_hint: {"center_y": 0.4, 'x': 0.05}  # Adjust the value to move it down

                        Widget:  # Spacer
                            size_hint_y: None
                            height: dp(50)  # Adjust the height as needed


                        MDCard:
                            orientation: "vertical"
                            size_hint: None, None
                            width: root.width * 0.9
                            height: root.height * 0.13
                            elevation: 1
                            md_bg_color: (1, 1, 1, 1)
                            pos_hint: {"center_x": 0.5, "center_y": 0.7}
                            
                            
                            
                            
                            BoxLayout:
                                pos_hint: {"center_y": 0.8}
                            
                                Widget:
                                    size_hint_x:None
                                    width:dp(5)
                                    
                                    
                                Image:
                                    id: image_id
                                    source: ""
                                    size_hint_x: None
                                    width: dp(40)
                                    pos_hint: {"center_x":0.5,"center_y": 0.4}
                                
                                    
                                TwoLineListItem:
                                    id: search_result_item
                                    text: "No result"
                                    secondary_text: " "
                                    on_release: root.on_number_click(float(root.ids.search_text_card.text))
                                    pos_hint:{"center_y":0.4}
                                    valign: "center"
                                    disabled: True

                                    MDIcon:
                                        id:logo_id
                                        icon:""
                                        theme_text_color: 'Custom'
                                        text_color: 0, 0, 0, 1
                                        pos_hint:{"center_x":0.9,"center_y":0.47}
                                        theme_text_color: "Custom"
                                        padding_x:dp(10)

                            Widget:
                                size_hint_y: None
                                height: "15dp"





                        Widget:
                            size_hint:None,None
                            height:dp(100)
                    Widget:
                        size_hint:None,None
                        height:dp(400)
                        adaptive_height:True

<UserDetailsScreen>:
    BoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
        
            id: activity_bar
            halign: 'center'
            elevation: 3
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            pos_hint: {'top':1}
            
            
        
            BoxLayout:
                orientation: 'horizontal'
                padding: dp(10)
                spacing: dp(10)
                pos_hint: {'center_x': 0.48, 'center_y': 0.8}
        
                MDIconButton:
                    icon: 'arrow-left'
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    icon_size: "22dp"
                    size_hint: (None, None)
                    size: dp(48), dp(48)
                    on_release: root.go_back()
                    
                Image:
                    id:users_image
                    source: 'images/user.png'
                    allow_stretch: True
                    keep_ratio: True
                    size_hint: None, None
                    size: dp(38), dp(38)
    
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: None
                    width: dp(100)
                    height: dp(48)
                    
        
                    
        
                    Label:
                        id: username_label
                        text: "Username"
                        font_size: '18sp'
                        color: (1, 1, 1, 1)
                        adaptive_width:True
                        pos_hint: {'center_x':0.3}
                    Widget:
                        size_hint_y:None
                        height:"20dp"
        
                    Label:
                        id: phone_number_label
                        text: "Phone Number"
                        font_size: '15sp'
                        color: (1, 1, 1, 1)
                        pos_hint: {'center_x':0.5}
                    Widget:
                        size_hint_y:None
                        height:"10dp"
        
                Widget:
                    size_hint_x: None
                    width: dp(10)
                    
                AnchorLayout:
                    anchor_x: 'right'
                    anchor_y: 'center'
                    # padding: dp(10)
                    
                    Widget:
                        size_hint_x: None
                        width: dp(30)
               
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_x: None
                        width: self.minimum_width
                        # padding: dp(10)
                        spacing: dp(7)
                        
                        
                        
                        MDIconButton:
                            icon: 'phone'
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            icon_size: "22dp"
                            size_hint: (None, None)
                            size: dp(48), dp(48)
                            on_release: root.go_back()
                            # pos_hint: {'center_x': 0.8}
                
                        MDIconButton:
                            icon: 'dots-vertical'
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            icon_size: "22dp"
                            halign:"right"
                            size_hint: (None, None)
                            size: dp(48), dp(48)
                            # pos_hint: {'center_x': 0.9}
                  
            Widget:

                size_hint_y:None
                height:dp(5)
                    
                

                    
        ScrollView:
            MDList:
                id: transaction_list_mdlist

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(50)

            MDTextField:
                id: another_textfield
                hint_text: "Pay amount"
                mode:'round'
                size_hint: None, None
                size: dp(200), dp(60)
                pos_hint: {'center_x': 0.5}  # Position on top
                opacity: 0  # Initially invisible   

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(400)
                spacing: dp(5)
                pos_hint: {'center_x': 0.5}
                padding: 10

                MDFillRoundFlatButton:
                    text: 'Pay'
                    on_release: root.deduct_and_transfer(root.ids.my_text_field.text) 
                    size_hint_x: None
                    width: "150dp"
                    height: "300dp"
                    pos_hint: {'center_x': 0.5}   
                    text_color: "#ffffff"
                    md_bg_color: "#148EFE"

                MDFillRoundFlatButton:
                    text: 'Request'
                    size_hint_x: None
                    width: "150dp"
                    height: "300dp"
                    text_color: 1, 1, 1, 1
                    md_bg_color: "#148EFE"
                    radius: [15]

                CustomMDTextField:
                    id: my_text_field
                    hint_text: "Message..."
                    mode: "round"
                    width: "150dp"
                    height: dp(1)
                    icon_right: "send"
                    padding: dp(5), dp(5)
                    #icon_right_color: app.theme_cls.primary_color
                    line_color_normal: app.theme_cls.primary_color
                    on_text: root.add_another_textfield(self.text)
                    on_text_validate: root.deduct_and_transfer(self.text)

'''

Builder.load_string(KV)

class RoundedBorderIconButton(MDIconButton):
    border_width = NumericProperty(2)
    border_color = ListProperty([1, 1, 1, 1])  # Default to white

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.after.clear()
        with self.canvas.after:
            Color(*self.border_color)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 100), width=self.border_width)



class AddPhoneScreen(Screen):
    top_app_bar_title = "Phone Transfer"
    current_user_phone = ""

    def go_back(self):
        # existing_screen = self.manager.get_screen('addphone')
        self.manager.current = 'dashboard'
        # self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(AddPhoneScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
    

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
    
        
    def fetch_and_update_addPhone(self):
        store = JsonStore('user_data.json').get('user')['value']
        addPhone_screen = self.get_screen('addphone')
        addPhone_screen.ids.contact_label.text = store["users_phone"]
        addPhone_screen.current_user_phone = str(store["users_phone"])

    def on_top_app_bar_title(self, instance, value):
        app = MDApp.get_running_app()
        try:
            self.top_app_bar.title = value
        except AttributeError:
            print("Error: 'top_app_bar' not found")

    def on_search_text_entered(self):
        number = float(self.ids.search_text_card.text)
        try:
            userdata = app_tables.wallet_users.get(users_phone=number)
            username = userdata['users_username']
            print(f'username in SearchField:{username}')
            self.ids.search_result_item.disabled = False
            self.ids.search_result_item.text = username
            self.ids.search_result_item.secondary_text = str(int(number))
            # self.ids.contact_label.text = number
            self.ids.search_result_item.children[0].icon = "chevron-right"
            user_pic=app_tables.wallet_users.get(users_phone=number)
            if user_pic['users_profile_pic']:
                try:
                    decoded_image_bytes =user_pic['users_profile_pic'].get_bytes()
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
            self.manager.show_notification('Alert!','User not found.')
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
            user_data = app_tables.wallet_users.get(users_phone=number)

            if user_data:
                user_details_screen.current_user_phone = self.current_user_phone
                print(self.current_user_phone)
                user_details_screen.searched_user_phone = str(
                    user_data['users_phone'])  # Adjust this based on your data structure
                print(f"{user_data['users_phone']}")
            else:
                print(f"User with phone number {number} not found in the database")
                self.manager.show_notification('Alert!','User not found.')


class RoundedMDLabel(MDLabel):
    md_bg_color = ListProperty([0.7686, 0.8902, 1, 1])  # Default background color
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = [20, ]
        with self.canvas.before:
            self.rect_color = Color(rgba=self.md_bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self.update_rect, size=self.update_rect, md_bg_color=self.on_md_bg_color)

    # def on_size(self, *args):
    #     self.rect.size = self.size
    #     self.rect.pos = self.pos

    # def on_pos(self, *args):
    #     self.rect.pos = self.pos

    # def on_md_bg_color(self, instance, value):
    #     self.rect_color.rgba = value[:4]
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HorizontalLine(BoxLayout):
    def _init_(self, **kwargs):
        super(HorizontalLine, self)._init_(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        self.padding = [dp(10), 0, dp(10), 0]
        self.orientation = 'horizontal'
        with self.canvas:
            Color(0.5, 0.5, 0.5, 1)  # Customize the color as needed
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class CustomMDTextField(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.right_icon_callback = lambda: None

    def on_right_icon(self):
        self.right_icon_callback()
class CustomTitle(BoxLayout):
    def __init__(self, username, phone_number, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text=username, font_size='20sp', color=(1, 1, 1, 1)))
        self.add_widget(Label(text="", font_size='30sp', color=(1, 1, 1, 1)))
        self.add_widget(Label(text=phone_number, font_size='16sp', color=(1, 1, 1, 1)))
        self.add_widget(Label(text="", font_size='30sp', color=(1, 1, 1, 1)))



class UserDetailsScreen(Screen):
    username = ""
    phone_number = StringProperty('')
    
    current_user_phone = 0
    searched_user_phone = ""
    transaction_list_mdlist = None

    # def go_back(self):
    #     existing_screen = self.manager.get_screen('userdetails')
    #     self.manager.current = 'dashboard'
    #     self.manager.remove_widget(existing_screen)

    def check_profile(self):
        print('coming here')
        print(self.phone_number)
        print(type(self.phone_number))
        try:
            user_pic=app_tables.wallet_users.get(users_phone=int(self.phone_number))
            if user_pic['users_profile_pic']:
                decoded_image_bytes =user_pic['users_profile_pic'].get_bytes()
                # core_image =  CoreImage(BytesIO(decoded_image_bytes), ext='png',filename='image.png')
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                    temp_file_path = temp_file1.name
                    # Write the decoded image data to the temporary file
                    temp_file1.write(decoded_image_bytes)
                    # Close the file to ensure the data is flushed and saved
                    temp_file1.close()
                self.ids.users_image.source=temp_file_path
        except Exception as e:
            print(e)

    def on_enter(self, sender=None):
        # Convert phone numbers to integers
        global message, color, align
        current_user_phone1 = JsonStore('user_data.json').get('user')['value']['users_phone']
        self.current_user_phone = current_user_phone1
        print(f'current_user_phone:{self.current_user_phone}')
        searched_user_phone = int(self.searched_user_phone)
        print(f'searched_user_phone:{self.searched_user_phone}')
        searched_user_data = app_tables.wallet_users.get(users_phone=searched_user_phone)
        searched_username = searched_user_data['users_username'] if searched_user_data else 'Unknown User'
        self.ids.username_label.text = searched_username
        self.ids.phone_number_label.text = str(searched_user_phone)
        self.check_profile()
        
        # Get the transaction data between current and searched users
        user_data_1 = app_tables.wallet_users_transaction.search(
            users_transaction_phone=searched_user_phone,
            users_transaction_receiver_phone=current_user_phone1,
            users_transaction_type='Debit'
        )
        user_data_2 = app_tables.wallet_users_transaction.search(
            users_transaction_phone=current_user_phone1,
            users_transaction_receiver_phone=searched_user_phone,
            users_transaction_type='Debit'
        )

        # Convert LiveObjectProxy results to lists
        user_data_1_list = list(user_data_1)
        user_data_2_list = list(user_data_2)

        user_data = user_data_1_list + user_data_2_list

        user_data.sort(key=lambda x: x['users_transaction_date'])

        self.ids.transaction_list_mdlist.clear_widgets()

        # Iterate over the transaction data and display
        for transaction in user_data:
            sender = transaction['users_transaction_phone']
            receiver = transaction['users_transaction_receiver_phone']
            fund = transaction['users_transaction_fund']
            date = transaction['users_transaction_date']

            # Check if date is not None before formatting
            if date is not None:
                date_str = date.strftime('%b %d, %Y %I:%M %p')  # Format the date as desired
                date_only = date.strftime('%b %d, %Y')
            else:
                date_str = "Unknown Date"
                date_only = "Unknown Date"

            searched_user_data = app_tables.wallet_users.get(users_phone=searched_user_phone)
            searched_username = searched_user_data['users_username'] if searched_user_data else 'Unknown User'


            horizontal_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(40),
                spacing=dp(10)
            )

            left_separator = MDSeparator()
            horizontal_layout.add_widget(left_separator)
            date_label = Label(
                text=date_str,
                font_size=16,
                color=(0.3, 0.3, 0.3, 1),
                size_hint_y=None,
                height=dp(40),
                halign='center'
            )

            horizontal_layout.add_widget(date_label)
            
            # Add right separator
            right_separator = MDSeparator()
            horizontal_layout.add_widget(right_separator)
            self.ids.transaction_list_mdlist.add_widget(horizontal_layout)
            # Add a spacer widget for some space between date_label and message_container
            spacer_top = BoxLayout(size_hint=(1, None), height=dp(85))
            self.ids.transaction_list_mdlist.add_widget(spacer_top)

            # Initialize message and color variables
            message = ""
            color = (0, 0, 0, 1)

            message_layout = MDBoxLayout(
                orientation="vertical",
                size_hint=(None, None),
                size=(dp(180), dp(130)),
                padding=[10, 10],
                spacing=100,
            )

            horizontal_layout1 = AnchorLayout(
                anchor_x='right',
                anchor_y='center',
                center_y=0.1,
                size_hint=(None, None),
                width=dp(150),
                height=dp(30)

            )


            # Determine the direction of the message based on sender and receiver
            if sender == current_user_phone1:
                formatted_fund = "{:,.0f}".format(fund)
                message = f"Payment to {searched_username}\n" \
                          f"₹{fund}\n" \
                          f"Paid on {date_only}  "

                background_color = [0.7686, 0.8902, 1, 1]  # [0.8, 0.925, 0.729, 1]
                text_color = (0, 0, 0, 1)
                align = 'right'

            else:
                formatted_fund = "{:,.0f}".format(fund)
                message = f"Payment to you\n" \
                          f"₹{fund}\n" \
                          f"Paid on {date_only}  "

                background_color = [0.7686, 0.8902, 1, 1]  # [0.8, 1, 0.8, 1]
                text_color = (0, 0, 0, 1)
                align = 'left'

            # Inside the loop where you construct the message_label, split the message into parts
            parts = message.split('\n')

            message_container = AnchorLayout(anchor_x=('right' if align == 'right' else 'left'), anchor_y='center')

            # message_layout = MDBoxLayout(
            #     orientation="vertical",
            #     size_hint=(None, None),
            #     size=(dp(170), dp(100)),
            #     padding=[10, 10],
            #     spacing=100,
            # )

            message_label = RoundedMDLabel()
            message_label.text = message
            message_label.font_size = 20
            message_label.md_bg_color = background_color
            message_label.size_hint_y = None
            message_label.height = message_label.texture_size[1] + dp(120)
            message_label.halign = align
            message_label.padding = dp(5)
            message_label.valign = "middle"
            message_label.theme_text_color = "Custom"
            message_label.text_color = text_color

            message_label.markup = True
            formatted_text = f"[size=21]{parts[0]}[/size]"
            for part in parts[1:]:
                formatted_text += f"\n"
                if part.startswith('₹'):
                    formatted_text += f"\n[size=35]{part}[/size]"
                else:
                    formatted_text += f"\n[size=19]{part}[/size]"

            message_label.text = formatted_text

            # Add the message label to the message layout
            message_layout.add_widget(message_label)

            # Add the message layout to the message container
            message_container.add_widget(message_layout)

            # Add the message layout to the transaction list
            self.ids.transaction_list_mdlist.add_widget(message_container)
            self.ids.transaction_list_mdlist.add_widget(horizontal_layout1)
            # Add another spacer widget for some space between message_container and next date_label
            spacer_bottom = BoxLayout(size_hint=(1, None), height=dp(55))
            self.ids.transaction_list_mdlist.add_widget(spacer_bottom)

    def calculate_label_height(self, text):
        lines = text.count("\n") + 1
        return dp(40) * lines
    
    def calculate_label_width(self, text):
        return dp(100)

    def add_another_textfield(self, text):
        if text:
            self.ids.another_textfield.text = text
            self.ids.another_textfield.opacity = 1
        else:
            self.ids.another_textfield.opacity = 0

    def deduct_and_transfer(self, amount):
        print("deduct_and_transfer function called with text:", amount)
        # Convert amount to integer or float
        if amount == '':
            self.manager.show_notification('Alert!','Enter all Fields')
            return
        amount = int(amount)
        date = datetime.now()

        # Fetch current user's data from wallet_users_balance
        current_user_data = app_tables.wallet_users_balance.search(
            users_balance_phone=int(self.current_user_phone),
            users_balance_currency_type='INR'  # Add currency_type condition
        )
        if len(current_user_data) == 1:
            current_user_data = current_user_data[0]
            existing_bal = current_user_data['users_balance']
            if amount > existing_bal:
                # toast("Insufficient Balance.")
                self.manager.show_notification('Alert!','Insufficient Balance.')
            else:
                # Deduct amount from current user's balance
                current_user_data['users_balance'] -= amount
                current_user_data.update()
                print(f'{amount} deduced from {int(self.current_user_phone)}')

                app_tables.wallet_users_transaction.add_row(
                    users_transaction_receiver_phone=int(self.searched_user_phone),
                    users_transaction_phone=int(self.current_user_phone),
                    users_transaction_fund=amount,
                    users_transaction_date=date,
                    users_transaction_type="Debit",
                    users_transaction_status = 'transfered-to',
                    users_transaction_currency = 'INR'
                )

                # Fetch searched user's data from wallet_users_balance
                searched_user_data = app_tables.wallet_users_balance.search(
                    users_balance_phone=int(self.searched_user_phone),
                    users_balance_currency_type='INR'  # Add currency_type condition
                )
                if len(searched_user_data) == 1:
                    searched_user_data = searched_user_data[0]
                    # Add amount to searched user's balance

                    searched_user_data['users_balance'] += amount
                    searched_user_data.update()
                    print(f'{amount} added to {int(self.searched_user_phone)}')

                    app_tables.wallet_users_transaction.add_row(
                        users_transaction_receiver_phone=int(self.current_user_phone),
                        users_transaction_phone=int(self.searched_user_phone),
                        users_transaction_fund=amount,
                        users_transaction_date=date,
                        users_transaction_type="Credit",
                        users_transaction_status = 'received-from',
                        users_transaction_currency='INR'
                    )
                    Clock.schedule_once(lambda dt: self.clear_text_field(), 0.1)

                    # Show a success toast
                    # toast("Money added successfully.")
                    self.manager.show_notification('Success','Money added successfully.')
                    # self.manager.current = 'dashboard'
                    # self.manager.show_balance()
                else:
                    print("Error: More than one row matched for searched user")
                    self.manager.show_notification('Alert!','An error occurred. Please try again.')
        else:
            print("Error: More than one row matched for current user")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')

    def clear_text_field(self):
        self.ids.my_text_field.text = ''

    # def build(self):
    #     custom_text_field = CustomMDTextField()
    #     custom_text_field.right_icon_callback = self.deduct_and_transfer
    #     return custom_text_field

    def go_back(self):
        existing_screen = self.manager.get_screen('userdetails')
        self.manager.add_widget(Factory.AddPhoneScreen(name='addphone'))
        self.manager.current = 'addphone'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(UserDetailsScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False



class WalletApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(AddPhoneScreen(name='add_phone'))
        screen_manager.add_widget(UserDetailsScreen(name='user_details'))
        return screen_manager


if __name__ == '__main__':
    WalletApp().run()