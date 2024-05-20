from logging import root
from docutils import SettingsSpec
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.list import TwoLineAvatarIconListItem,ThreeLineAvatarIconListItem
from anvil.tables import app_tables
from kivymd.uix.spinner import MDSpinner
from addAccount import AddAccountScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IconRightWidget
from kivy.properties import DictProperty
from kivy.base import EventLoop

KV = '''
<AccmanageScreen>:
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "Account Management"
            anchor_title:'left'
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            right_action_items: [["bank",lambda x: root.nav_account()]]
            elevation:4
        ScrollView:
            GridLayout:
                cols: 1
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
                id: account_details_container
                
        # MDBottomAppBar:
        #     MDTopAppBar:
        #         mode: 'end'
        #         type: 'bottom'
        #         icon: 'bank'
        #         on_action_button: root.nav_account()        
'''
Builder.load_string(KV)


class AccmanageScreen(Screen):
    def go_back(self):
        # existing_screen = self.manager.get_screen('accmanage')
        self.manager.current = 'dashboard'
        # self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(AccmanageScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def on_pre_enter(self, *args):
        # Called before the screen is displayed, show loading animation
        self.show_loading_animation()
        # Use Clock.schedule_once to simulate loading and update details after a delay
        Clock.schedule_once(lambda dt: self.update_details(), 2)

    def show_loading_animation(self):
        # Create and add an MDSpinner to the layout
        self.loading_spinner = MDSpinner(
            size_hint=(None, None),  # Use relative sizing for better scaling
            size=(dp(46), dp(46)),  # Adjust size as needed
            pos=(Window.width / 2 - dp(46) / 2, Window.height / 2 - dp(46) / 2)
        )
        self.ids.account_details_container.add_widget(self.loading_spinner)

    def hide_loading_animation(self):
        # Remove the loading MDSpinner from the layout
        self.ids.account_details_container.remove_widget(self.loading_spinner)

    def nav_account(self):
        self.manager.add_widget(Factory.AddAccountScreen(name='addaccount'))
        self.manager.current = 'addaccount'

    """while creating widgets dynamically cannot access ids as they wont be present in self.ids instead create a dictionary
        and store it in this scenario its dynamic_ids """
    dynmaic_ids = DictProperty({})
    def update_details(self):
        try:
            store = JsonStore('user_data.json')
            phone = store.get('user')['value']["phone"]

            # Call the server function to fetch account details and bank names
            bank_names = app_tables.wallet_users_account.search(phone=phone)
            # bank_names_str = [str(row['bank_name']) for row in bank_names]
            banks= [[str(row['bank_name']),str(row['account_number'])] for row in bank_names]
            print(banks)
            # for i in range(len(banks)):
            #     print(i[0])

            # print(len(bank_names_str))
            # Clear existing widgets in the GridLayout
            account_details_container = self.ids.account_details_container
            account_details_container.clear_widgets()

            # Add OneLineListItems for each bank name
            # right_action= [["dots-vertical", lambda x: self.callback(x)]]
            print(self.ids.keys())
            #if there is only one bank account of the user it will set that account to default
            if len(banks) == 1:
                for bank_name in banks:
                    id=bank_name[1]
                    items=TwoLineAvatarIconListItem(
                                        IconRightWidget(id=id,icon="dots-vertical",on_release =lambda x: self.show_menu(x,bank_name[1])),
                                        id=id, #f'{bank_names_str[0]}',
                                        text=f'{bank_name[0]}',
                                        secondary_text='primary account',
                                        # tertiary_text='primary account',
                                        # on_press=lambda bank_name: self.setting_default_account(f'{bank_name}'),
                                        )
                    account_details_container.add_widget(items)
                print('yes')
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                # phone['default_accout']=str(bank_name[1])
                users = app_tables.wallet_users.get(phone=phone)
                users.update(default_account = bank_name[1])
            #if user has multiple accounts it will show options to select the default account
            if len(banks)>1:
                for bank_name in banks:
                    id = bank_name[1]
                    items=TwoLineAvatarIconListItem(
                                        
                                        IconRightWidget(id=id,icon="dots-vertical",on_release =lambda x: self.show_menu(x,bank_name[1])),
                                        id=id,
                                        text=f'{bank_name[0]}',
                                        # secondary_text = f'{bank_name[1]}'
                                        # on_press=lambda bank_name: self.setting_default_account(f'{bank_name}'),
                                        )
                    # items.add_widget()
                    account_details_container.add_widget(items)
                    self.dynmaic_ids[id] = items
            print(self.dynmaic_ids)
            self.hide_loading_animation()
            # Setting on entering
            if len(banks) == 0:
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                users = app_tables.wallet_users.get(phone=phone)
                users.update(default_account=None)
            if len(banks)>1:
                phone = JsonStore('user_data.json').get('user')['value']['phone']
                users = app_tables.wallet_users.get(phone=phone)
                users_default_account = users['default_account']
                print(users_default_account)
                if users_default_account != None:
                    self.dynmaic_ids[users_default_account].secondary_text='primary account'
        except Exception as e:
            print(f"Error updating details: {e}")
            self.manager.show_notification('Alert!','Some error occured try again.')
            self.hide_loading_animation()
    #checking this code to get bank details
    # def setting_default_account(self,bank):
    #     #gives the bank account
    #     # getting the id of the button pressed in this we are getting the bank names
    #     bank_name = bank.id
    #     # print(bank.id)
    #     print(self.ids.keys())
    #     # print('clicked on the bank')
    #     phone = JsonStore('user_data.json').get('user')['value']['phone']
    #     data_account=app_tables.wallet_users_account.search(phone=phone,bank_name=bank_name)
        
    #     for i in data_account:
    #         print(dict(i))
    
    def show_menu(self,instance,acc_number):
        # print(y)
        store = JsonStore('user_data.json')
        phone = store.get('user')['value']["phone"]

        # Call the server function to fetch account details and bank names
        bank_names = app_tables.wallet_users_account.search(phone=phone)
        # bank_names_str = [str(row['bank_name']) for row in bank_names]
        banks= [[str(row['bank_name']),str(row['account_number'])] for row in bank_names]

        if len(banks)>1:
            menu_items = [
                {
            "text": "set primary",
            "on_release": lambda x=instance: self.set_primary(x),  #,acc_number
                },
                {
            "text": "delete account",
            "on_release": lambda x=instance: self.delete_account(x),
                }
            ]
            self.menu = MDDropdownMenu(items=menu_items)
            self.menu.caller = instance  # Set the button that triggered the menu
            self.menu.open()
        if len(banks)==1:
            menu_items = [
                {
            "text": "delete account",
            "on_release": lambda x=instance: self.delete_account(x),
                }
            ]
            self.menu = MDDropdownMenu(items=menu_items)
            self.menu.caller = instance  # Set the button that triggered the menu
            self.menu.open()

    def delete_account(self,instance):
        phone = JsonStore('user_data.json').get('user')['value']['phone']
        accounts_table = app_tables.wallet_users_account.get(phone = phone,account_number= int(instance.id))
        for i in accounts_table:
            print(i)
            if accounts_table['account_number'] == float(instance.id):
                accounts_table.delete()
                self.menu.dismiss()
                break
            else:
                print('couldnt delete')
                self.manager.show_notification('Alert!',"Couldn't delete account.")
                self.menu.dismiss()

        # print(instance.id)

    def set_primary(self,x):
        # print(acc_number)
        print(x)
        print(x.id)
        print(self.dynmaic_ids[x.id])
         # Print text of each item
        for i in self.dynmaic_ids:
            print(i)
            if i == x.id :
                print('yes',self.dynmaic_ids[i])
                self.dynmaic_ids[i].secondary_text='primary account'
            else:
                self.dynmaic_ids[i].secondary_text=''
                # print(self.dynmaic_ids[i].text)
          
        bank_name=x.id
        phone = JsonStore('user_data.json').get('user')['value']['phone']       
        users = app_tables.wallet_users.get(phone=phone)
        users.update(default_account = bank_name)
        self.menu.dismiss()  
