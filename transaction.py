from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivymd.uix.screen import Screen
from kivy.properties import DictProperty,StringProperty
from kivy.base import EventLoop
from anvil.tables import app_tables
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory
from kivymd.uix.list import OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
import traceback
from kivy.uix.widget import Widget
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from datetime import date,datetime
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.label import MDIcon
from kivy.uix.anchorlayout import AnchorLayout
import tempfile
from kivy.uix.image import Image
from kivymd.uix.card import MDSeparator
KV = '''
<Transaction>:
    Screen:
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            pos_hint:{'top':1}

            MDTopAppBar:
                title: 'Transaction History'
                elevation: 3
                left_action_items: [['arrow-left', lambda x: root.go_back()]]
                md_bg_color: "#148EFE"
                specific_text_color: "#ffffff"
                pos_hint: {'top': 1}

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(20)
                padding: dp(5),0,dp(5),0

                # Removed unnecessary MDLabel

                MDIconButton:
                    icon: "filter-variant"
                    pos_hint: {"center_x": 0.95}
                    theme_text_color: "Custom"
                    text_color: 0, 0, 1, 1  # Blue color for the icon
                    on_release: root.open_sort_filter()    

                ScrollView:
                    effect_kludge: True
                    MDList:
                        id: transaction_list
            # MDBoxLayout:
            #     size_hint_y: None
            #     height: '80dp'
    
            #     canvas.before:
            #         Color:
            #             rgba: (0.078,0.557,0.996,1)
            #         RoundedRectangle:
            #             size: self.size
            #             pos: self.pos
            #             radius: [40, 40, 0, 0]
                        
            #     MDGridLayout:
    
            #         cols:5
    
            #         spacing:'30dp'
            #         padding: '20dp'
            #         pos_hint:{"center_x":0.5}
            #         size_hint:None,None
            #         width:self.parent.width
            #         md_bg_color:
    
            #         MDIconButton:
            #             id:wallet_icon
            #             icon: 'wallet'
            #             theme_text_color:"Custom"
            #             text_color: root.get_button_color('wallet')
            #             icon_size:"40dp"
            #             size_hint: (0.1, 0.1)
            #             on_release:root.nav_your_wallet()
    
    
    
            #         MDIconButton:
            #             icon: 'history'
            #             theme_text_color:"Custom"
            #             text_color: root.get_button_color('transaction')
            #             icon_size:"40dp"
            #             size_hint: (0.1, 0.1)
            #             on_release:root.nav_your_transaction_history()
    
    
            #         MDIconButton:
            #             icon: 'qrcode-scan'
            #             theme_text_color:"Custom"
            #             text_color: root.get_button_color('qr')
            #             icon_size:"40dp"
            #             size_hint: (0.1, 0.1)
            #             on_release:root.nav_qr_scan()
    
            #         MDIconButton:
            #             icon: 'contacts'
            #             theme_text_color:"Custom"
            #             text_color: root.get_button_color('addphone')
            #             icon_size:"40dp"
            #             size_hint: (0.1, 0.1)
            #             on_release:root.nav_your_pay_contacts()
    
            #         MDIconButton:
            #             icon: 'account-circle'
            #             theme_text_color:"Custom"
            #             icon_size:"40dp"
            #             text_color: root.get_button_color('profile')
            #             size_hint: (0.1, 0.1)
            #             on_release:root.nav_your_profile()

'''
Builder.load_string(KV)


class Transaction(Screen):
    # current_page = StringProperty('transaction')
    # filter_dialog = ObjectProperty(None)
    def go_back(self):
        existing_screen = self.manager.get_screen('transaction')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(Transaction, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False
    

    dynamic_ids_currency = DictProperty({})
    dynamic_ids_type = DictProperty({})
    currency=''
    type_filt_debit=''
    type_filt_credit=''
    start_date=''
    end_date=''
    
    icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }
    options_button_icon_mapping = ['INR','GBP','EUR','USD']

    def open_sort_filter(self):
        # if not self.filter_dialog:
        self.filter_dialog = MDDialog(
            title="Filter Payments",
            type="custom",
            content_cls=MDList(),
            buttons=[
                MDFlatButton(
                    text="APPLY",on_release = lambda x:self.get_transaction_history()),
                    MDFlatButton(
                    text="CLEAR ALL",on_release = lambda x:self.clear_all())],
        )
        grid = GridLayout(cols = 3,size_hint_y= None,height='60dp',padding='2dp')
        col1 = AnchorLayout(size_hint_x='100dp')
        col1.add_widget(MDLabel(text=''))
        grid.add_widget(col1)
        col2 = AnchorLayout(pos_hint={'center_x':0.5,'center_y':0.5},size_hint_x = '15dp')
        col2.add_widget(MDIconButton(icon='currency-inr',on_release = (lambda x:self.filter_currency(x))),)
        grid.add_widget(col2)
        col3 = AnchorLayout(pos_hint={'center_x':0.5,'center_y':0.5},size_hint_x = '15dp')
        col3.add_widget(MDIconButton(icon='calendar',on_release=lambda x: self.pick_date()),)
        grid.add_widget(col3)

        items = [
            grid,
            OneLineListItem(text='All',on_release =(lambda x:self.get_transaction_history())),
            OneLineListItem(id= 'Credit',text="Credit",on_release = (lambda x:self.type_filter_credit(x))),  # Text for Status option
            OneLineListItem(id='Debit',text="Debit",on_release = (lambda x:self.type_filter_debit(x))),
            # OneLineListItem(text="Currency",on_release = (lambda x:self.filter_currency())),  # Text for Type option
            # OneLineListItem(text='Date', on_release=lambda x: self.pick_date()),
        ]
        for i in range(len(items)):
            self.filter_dialog.content_cls.add_widget(items[i])

        self.filter_dialog.open()
        if (self.currency or self.type_filt_credit or self.type_filt_debit or self.start_date or self.end_date) :
            print('has values')
            self.currency=''
            self.type_filt_debit=''
            self.type_filt_credit=''
            self.start_date=''
            self.end_date=''

    # def all_func(self):
    #     self.clear_all()
        
        
    def clear_all(self):
        self.currency=''
        self.type_filt_debit=''
        self.type_filt_credit=''
        self.start_date=''
        self.end_date=''
        return
        # self.credit_type_add.bg_color=(0,0,0,0)
        # self.debit_type_add.bg_color = (0,0,0,0)

    def filter_currency(self,main_button):
        print('printing',main_button)
        self.filt_currency = MDDialog(
            title="Filter Payments",
            type="custom",
            content_cls=MDList(),
            # buttons=[
            #     MDFlatButton(
            #         text="APPLY",on_release = lambda x:self.get_transaction_history(currency = self.currency)
            #     ),
            # ],
            )
        for currency in self.options_button_icon_mapping:
            id = currency
            item = OneLineListItem( id=id,text = currency,on_release = lambda x,main_insta=main_button:self.selected_currency(x,main_insta))
            self.filt_currency.content_cls.add_widget(item)
            self.dynamic_ids_currency[id] = item
        self.filt_currency.open()
    

    def selected_currency(self,instance,main_inst):
        # print(instance.id,instance)
        main_inst.icon = self.icon_mapping[instance.id]
        self.currency = instance.id
        print(self.currency)
        for i in self.dynamic_ids_currency:
            if i == instance.id :
                self.dynamic_ids_currency[instance.id].bg_color='#148efe'
            else:
                self.dynamic_ids_currency[i].bg_color = '#ffffff'    
        self.filt_currency.dismiss()

        
    def type_filter_credit(self,type):
        self.type_filt_credit = type.text
        self.credit_type_add = type
        print('transaction',self.type_filt_credit)
        if hasattr(type, 'selected') and type.selected:
            type.bg_color = (0,0,0,0)
            type.selected = False
            self.type_filt_credit = ''
        else:
            type.bg_color = '#148efe'
            type.selected = True
        
        # def color_change(self,type):
        #     type.bg_color = (0,0,0,0)
        # self.type_filt = MDDialog(
        #     title="Filter Payments",
        #     type="custom",
        #     content_cls=MDList(),
        #     buttons=[
        #         MDFlatButton(
        #             text="APPLY",on_release = lambda x:self.get_transaction_history(trans_type = self.type_filt1))],

        # )
        # for typee in ['Credit','Debit']:
        #     id = typee
        #     item = OneLineListItem( id=id,text = typee,on_release = lambda x:self.type_filter_selected(x))
        #     self.type_filt.content_cls.add_widget(item)
        #     self.dynamic_ids_type[id] = item
        # # print(self.dynmaic_ids.items())
        # self.type_filt.open()

    def type_filter_debit(self,type):
        self.type_filt_debit = type.text
        print('transaction',self.type_filt_debit)
        if hasattr(type, 'selected') and type.selected:
            print('yes inside slected')
            type.bg_color = (0,0,0,0)
            type.selected = False
            self.type_filt_debit = ''
        else:
            print('yes not selected')
            type.bg_color = '#148efe'
        
    
    
    def pick_date(self):
        self.date_p = MDDatePicker(mode="range")
        self.date_p.bind(on_save = self.selected_date)
        self.date_p.open()

    def selected_date(self,instance,value,daterange):
        print(instance)
        print(value)
        self.start_date = daterange[0]
        print('yes',self.start_date)
        self.end_date = daterange[-1]
        you=''
        if you:
            print('tRue')
        else:print('False')
        # self.get_transaction_history_date(start_date = start_date,last_date = end_date)
    
    # def type_filter_selected(self,instance):
    #     self.type_filt1 = instance.id
    #     for i in self.dynamic_ids_type:
    #         if i == instance.id :
    #             self.dynamic_ids_type[instance.id].bg_color='#148efe'
    #         else:
    #             self.dynamic_ids_type[i].bg_color = '#ffffff'
            
    #     return self.type_filt1


    def get_transaction_history(self):
        store = JsonStore('user_data.json').get('user')['value']
        phone = store['users_phone']
        if self.filter_dialog:
            self.filter_dialog.dismiss()
        # if self.type_filt:
        #     self.type_filt.dismiss()
        
        
        
        filters = {'users_transaction_phone':phone,}
        
        # transaction = []
        if self.currency:
            filters['users_transaction_currency']=self.currency
            # transaction = list(app_tables.wallet_users_transaction.search(phone=phone,currency = currency ))
        if self.type_filt_credit:
            filters['users_transaction_type']=self.type_filt_credit
            # transaction = list(app_tables.wallet_users_transaction.search(phone=phone,transaction_type = transaction_type ))
        # if 'no_filter' in arguements.keys():
        #     print('yes no filter')
        #     transaction = list(app_tables.wallet_users_transaction.search(phone=phone))
        #     for i in transaction:
        #         print(i['receiver_phone'])
        if self.type_filt_debit:
            filters['users_transaction_type']=self.type_filt_debit
        if self.type_filt_credit and self.type_filt_debit:
            del filters['users_transaction_type']
            print(filters.items())
                    
        # if self.currency == None or self.type_filt1 ==None:
        #     transaction = list(app_tables.wallet_users_transaction.search(phone=phone))
        
        try:
            # Query the 'transactions' table to fetch the transaction history
            transactions = list(app_tables.wallet_users_transaction.search(**filters))
            self.ids.transaction_list.clear_widgets()
            current_date = ""

            for transaction in sorted(filter(lambda x: x['users_transaction_date'] is not None, transactions), key=lambda x: x['users_transaction_date'],
                                    reverse=True):
                transaction_datetime = transaction['users_transaction_date']
                transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                transaction_date = transaction_date_str.split(' ')[0]
                transactions_text = f"{transaction['users_transaction_receiver_phone']}"
                fund_text = f"{round(transaction['users_transaction_fund'], 2)}"
                fund_currency = f"{transaction['users_transaction_currency']}"
                lowered_currency = fund_currency.lower()
                fund_currency1 = f"currency-{lowered_currency}"
                transaction_datetime_obj = str(transaction_datetime).split(" ")
                transaction_time = str(transaction_datetime_obj[1]).split(".")
                transaction_time = transaction_time[0]
                time_obj = datetime.strptime(transaction_time, "%H:%M:%S")
                am_pm = "AM" if time_obj.hour < 12 else "PM"
                formatted_time = time_obj.strftime("%I:%M: ") + am_pm
                # if transaction['']
                if transaction_date != current_date :
                    
                    current_date = transaction_date
                    header_text = f"[b]{transaction_date}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                    self.ids.transaction_list.add_widget(list1)
                main_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(46))
                timing_label = MDLabel(text=f"{formatted_time}", font_style="Caption", pos_hint={"center_x": 0.62})
                transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(46))

                # Add transaction details
                if transaction['users_transaction_type'] == 'Withdrawn' :
                    # print('inside cond')
                    # uer = app_tables.wallet_users.get(users_phone = phone)
                    transactions_text = 'Withdrawn'
                
                if transaction['users_transaction_type'] == 'Deposited':
                    transactions_text = 'Deposit'
                if transaction['users_transaction_type'] == 'Auto Topup':
                    transactions_text = 'Auto topup'

                if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                    user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                    print('yeshere',transaction['users_transaction_receiver_phone'])
                    transactions_text = user['users_username']
                
                
                    #ids.user_image.texture = core_image.texture
                imagee = Image(size_hint_y=None,height='44dp',size_hint_x=None,width='30dp',pos_hint={'center_x':0.5})
                if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                    details = app_tables.wallet_users.get(users_phone = phone)
                    print(phone)
                    try:
                        if details['users_profile_pic'] is not None:
                            print('coming')
                            decoded_image_bytes =details['users_profile_pic'].get_bytes()
                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                temp_file_path = temp_file1.name
                                # Write the decoded image data to the temporary file
                                temp_file1.write(decoded_image_bytes)
                                # Close the file to ensure the data is flushed and saved
                                temp_file1.close()
                            imagee.source=temp_file_path
                        else:
                            imagee.source='images/user.png'
                    except Exception as e:
                        print(e)

                elif transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                    details = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'])
                    try:
                        if details['users_profile_pic'] is not None:
                            print('coming')
                            decoded_image_bytes =details['users_profile_pic'].get_bytes()
                            decoded_image_bytes =details['users_profile_pic'].get_bytes()
                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                temp_file_path = temp_file1.name
                                # Write the decoded image data to the temporary file
                                temp_file1.write(decoded_image_bytes)
                                # Close the file to ensure the data is flushed and saved
                                temp_file1.close()
                            imagee.source=temp_file_path
                        else:
                            imagee.source='images/user.png'
                    except Exception as e:
                        print(e)

                transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                        text_color=[0, 0, 0, 1], divider=None)
                

                transaction_container.add_widget(imagee)
                transaction_container.add_widget(transaction_item_widget)

                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                    fund_color = [0, 0.5, 0, 1]
                    sign = '+'
                # elif transaction['users_transaction_type'] == 'Debit' or :
                #     fund_color = [0, 0.5, 0, 1]
                #     sign = '+'
                else:
                    fund_color = [1, 0, 0, 1]
                    sign = '-'

                icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                    size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, })
                        
                sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                    halign='right')
                fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                    halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                
                transaction_container.add_widget(sign_label)
                transaction_container.add_widget(icon)
                transaction_container.add_widget(fund_label)
                main_container.add_widget(transaction_container)
                main_container.add_widget(timing_label)
                self.ids.transaction_list.add_widget(main_container)
                self.ids.transaction_list.add_widget(Widget(size_hint_y=None,height=dp(10)))
                self.ids.transaction_list.add_widget(MDSeparator(height = dp(1)))
        except Exception as e:
            print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')
        
        if self.start_date or self.end_date:
            try:
            # Get the phone number from the JSON file
            
            # Query the 'transactions' table to fetch the transaction history
                if self.start_date == self.end_date:
                    transactions = list(app_tables.wallet_users_transaction.search(**filters))
                    self.ids.transaction_list.clear_widgets()
                    header_text = f"[b]{str(self.start_date)}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                                    text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )
                    self.ids.transaction_list.add_widget(list1)
                    for transaction in sorted(filter(lambda x: x['users_transaction_date'] is not None , transactions), key=lambda x: x['users_transaction_date'],
                                            reverse=True):
                        transaction_datetime = transaction['users_transaction_date']
                        transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                        transaction_date = transaction_date_str.split(' ')[0]
                        transactions_text = f"{transaction['users_transaction_receiver_phone']}"
                        fund_text = f"{round(transaction['users_transaction_fund'], 2)}"
                        fund_currency = f"{transaction['users_transaction_currency']}"
                        lowered_currency = fund_currency.lower()
                        fund_currency1 = f"currency-{lowered_currency}"
                        print(fund_text,transaction_date_str)
                        transaction_datetime_obj = str(transaction_datetime).split(" ")
                        transaction_time = str(transaction_datetime_obj[1]).split(".")
                        transaction_time = transaction_time[0]
                        time_obj = datetime.strptime(transaction_time, "%H:%M:%S")
                        am_pm = "AM" if time_obj.hour < 12 else "PM"
                        formatted_time = time_obj.strftime("%I:%M: ") + am_pm
                        # if transaction_date != current_date:
                        #     current_date = transaction_date
                            
                        main_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(46))
                        timing_label = MDLabel(text=f"{formatted_time}", font_style="Caption", pos_hint={"center_x": 0.62})
                        transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(46))

                        # Add transaction details
                        
                        if transaction['users_transaction_type'] == 'Withdrawn' :
                            transactions_text = 'Withdrawn'
                            
                        if transaction['users_transaction_type'] == 'Deposited':
                            transactions_text = 'Deposit'

                        if transaction['users_transaction_type'] == 'Auto Topup':
                            transactions_text = 'Auto topup'


                        if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                            user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                            transactions_text = user['users_username']
                            print(transaction['users_transaction_receiver_phone'])

                        if transaction_date_str == str(self.start_date):
                            print('yes inside')
                            imagee = Image(size_hint_y=None,height='44dp',size_hint_x=None,width='30dp',pos_hint={'center_x':0.5})
                            if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                                details = app_tables.wallet_users.get(users_phone = phone)
                                try:
                                    if details['users_profile_pic'] is not None:
                                        print('coming')
                                        decoded_image_bytes =details['users_profile_pic'].get_bytes()
                                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                            temp_file_path = temp_file1.name
                                            # Write the decoded image data to the temporary file
                                            temp_file1.write(decoded_image_bytes)
                                            # Close the file to ensure the data is flushed and saved
                                            temp_file1.close()
                                        imagee.source=temp_file_path
                                    else:
                                        imagee.source='images/user.png'
                                except Exception as e:
                                    print(e)

                            if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                                details = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'])
                                try:
                                    if details['users_profile_pic'] is not None:
                                        decoded_image_bytes =details['users_profile_pic'].get_bytes()
                                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                            temp_file_path = temp_file1.name
                                            # Write the decoded image data to the temporary file
                                            temp_file1.write(decoded_image_bytes)
                                            # Close the file to ensure the data is flushed and saved
                                            temp_file1.close()
                                        imagee.source=temp_file_path
                                    else:
                                        imagee.source='images/user.png'
                                except Exception as e:
                                    print(e)

                            transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                    text_color=[0, 0, 0, 1], divider=None)
                            transaction_container.add_widget(imagee)
                            transaction_container.add_widget(transaction_item_widget)

                            transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                            if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                                fund_color = [0, 0.5, 0, 1]
                                sign = '+'
                            # elif transaction['users_transaction_type'] == 'Debit' or :
                            #     fund_color = [0, 0.5, 0, 1]
                            #     sign = '+'
                            else:
                                fund_color = [1, 0, 0, 1]
                                sign = '-'

                            icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                            size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5})
                                
                            sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                                halign='right')
                            fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                                halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                            
                            transaction_container.add_widget(sign_label)
                            transaction_container.add_widget(icon)
                            transaction_container.add_widget(fund_label)
                            main_container.add_widget(transaction_container)
                            main_container.add_widget(timing_label)
                            self.ids.transaction_list.add_widget(main_container)
                            self.ids.transaction_list.add_widget(Widget(size_hint_y=None,height=dp(10)))
                            self.ids.transaction_list.add_widget(MDSeparator(height = dp(1)))
                if self.start_date != self.end_date:
                    transactions = list(app_tables.wallet_users_transaction.search(**filters))
                    self.ids.transaction_list.clear_widgets()
                    current_date = ""

                    for transaction in sorted(filter(lambda x: x['users_transaction_date'] is not None, transactions), key=lambda x: x['users_transaction_date'],
                                            reverse=True):
                        transaction_datetime = transaction['users_transaction_date']
                        transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                        transaction_date = transaction_date_str.split(' ')[0]
                        transactions_text = f"{transaction['users_transaction_receiver_phone']}"
                        fund_text = f"{round(transaction['users_transaction_fund'], 2)}"
                        fund_currency = f"{transaction['users_transaction_currency']}"
                        lowered_currency = fund_currency.lower()
                        fund_currency1 = f"currency-{lowered_currency}"
                        transaction_datetime_obj = str(transaction_datetime).split(" ")
                        transaction_time = str(transaction_datetime_obj[1]).split(".")
                        transaction_time = transaction_time[0]
                        time_obj = datetime.strptime(transaction_time, "%H:%M:%S")
                        am_pm = "AM" if time_obj.hour < 12 else "PM"
                        formatted_time = time_obj.strftime("%I:%M: ") + am_pm
                        if str(self.start_date) <= transaction_date_str <= str(self.end_date):
                            if transaction_date != current_date:
                                current_date = transaction_date
                                header_text = f"[b]{transaction_date}[/b]"
                                list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                                        text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                                self.ids.transaction_list.add_widget(list1)

                            main_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(46))
                            timing_label = MDLabel(text=f"{formatted_time}", font_style="Caption", pos_hint={"center_x": 0.62})
                            transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(46))

                            # Add transaction details
                            
                            if transaction['users_transaction_type'] == 'Withdrawn' :
                                transactions_text = 'Withdrawn'
                                
                            if transaction['users_transaction_type'] == 'Deposited':
                                transactions_text = 'Deposit'

                            if transaction['users_transaction_type'] == 'Auto Topup':
                                transactions_text = 'Auto topup'
                            

                            if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                                user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                                transactions_text = user['users_username']
                                print(transaction['users_transaction_receiver_phone'])

                            if str(self.start_date) <= transaction_date_str <= str(self.end_date):
                                imagee = Image(size_hint_y=None,height='44dp',size_hint_x=None,width='30dp',pos_hint={'center_x':0.5})
                                try:
                                    if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                                        details = app_tables.wallet_users.get(users_phone = phone)
                                        if details['users_profile_pic'] is not None:
                                            decoded_image_bytes =details['users_profile_pic'].get_bytes()
                                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                                temp_file_path = temp_file1.name
                                                # Write the decoded image data to the temporary file
                                                temp_file1.write(decoded_image_bytes)
                                                # Close the file to ensure the data is flushed and saved
                                                temp_file1.close()
                                            imagee.source=temp_file_path
                                        else:
                                            imagee.source='images/user.png'
                                except Exception as e:
                                    print(e)

                                if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                                    details = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'])
                                    try:
                                        if details['users_profile_pic'] is not None:
                                            decoded_image_bytes =details['users_profile_pic'].get_bytes()
                                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                                                temp_file_path = temp_file1.name
                                                # Write the decoded image data to the temporary file
                                                temp_file1.write(decoded_image_bytes)
                                                # Close the file to ensure the data is flushed and saved
                                                temp_file1.close()
                                            imagee.source=temp_file_path
                                        else:
                                            imagee.source='images/user.png'
                                    except Exception as e:
                                        print(e)
                                transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                        text_color=[0, 0, 0, 1], divider=None)
                                transaction_container.add_widget(imagee)
                                transaction_container.add_widget(transaction_item_widget)

                                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                                if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Deposited' or transaction['users_transaction_type'] == 'Auto Topup':
                                    fund_color = [0, 0.5, 0, 1]
                                    sign = '+'
                                # elif transaction['users_transaction_type'] == 'Debit' or :
                                #     fund_color = [0, 0.5, 0, 1]
                                #     sign = '+'
                                else:
                                    fund_color = [1, 0, 0, 1]
                                    sign = '-'

                                icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                            size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5})
                                
                                sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                                    halign='right')
                                fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                                    halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                                
                                transaction_container.add_widget(sign_label)
                                transaction_container.add_widget(icon)
                                transaction_container.add_widget(fund_label)
                                main_container.add_widget(transaction_container)
                                main_container.add_widget(timing_label)
                                self.ids.transaction_list.add_widget(main_container)
                                self.ids.transaction_list.add_widget(Widget(size_hint_y=None,height=dp(10)))
                                self.ids.transaction_list.add_widget(MDSeparator(height = dp(1)))
            except Exception as e:
                print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')

    # def get_button_color(self, page):
    #     return (0, 0, 0, 0.7) if self.current_page == page else (1, 1, 1, 1)

    # def nav_your_wallet(self):
    #     self.manager.add_widget(Factory.AddMoneyScreen(name='addmoney'))
    #     self.manager.current = 'addmoney'
    #     self.current_page = 'wallet'

    # def nav_your_transaction_history(self):
    #     self.manager.add_widget(Factory.Transaction(name='transaction'))
    #     self.manager.current = 'transaction'
    #     self.current_page = 'transaction'

    # def nav_qr_scan(self):
    #     self.manager.add_widget(Factory.ScanScreen(name='qrscanner'))
    #     self.manager.current = 'qrscanner'
    #     self.current_page = 'qr'

    # def nav_your_pay_contacts(self):
    #     self.manager.add_widget(Factory.AddPhoneScreen(name='addphone'))
    #     self.manager.current = 'addphone'
    #     self.current_page = 'addphone'

    # def nav_your_profile(self):
    #     self.manager.add_widget(Factory.Profile(name='profile'))
    #     self.manager.current = 'profile'
    #     self.current_page = 'profile'
    #transaction history by date
    # def get_transaction_history_date(self,**args):
    #     store = JsonStore('user_data.json').get('user')['value']
    #     phone = store['phone']
    #     if self.filter_dialog:
    #         self.filter_dialog.dismiss()
        
        
    #     arguements = args
      
    #     # if 'start_date' in arguements.keys()
    #     try:
    #         # Get the phone number from the JSON file
            
    #         # Query the 'transactions' table to fetch the transaction history
    #         if 'start_date' in arguements.keys() and 'last_date' not in arguements.keys() and arguements['start_date'] != arguements['last_date']:
    #             transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
    #             self.ids.transaction_list.clear_widgets()
    #             header_text = f"[b]{arguements['start_date']}[/b]"
    #             list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
    #                                             text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )
    #             self.ids.transaction_list.add_widget(list1)
    #             for transaction in sorted(filter(lambda x: x['date'] is not None , transactions), key=lambda x: x['date'],
    #                                     reverse=True):
    #                 transaction_datetime = transaction['date']
    #                 transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
    #                 transaction_date = transaction_date_str.split(' ')[0]
    #                 transactions_text = f"{transaction['receiver_phone']}"
    #                 fund_text = f"{round(transaction['fund'], 2)}"
    #                 fund_currency = f"{transaction['currency']}"
    #                 lowered_currency = fund_currency.lower()
    #                 fund_currency1 = f"currency-{lowered_currency}"
    #                 print(fund_text,transaction_date_str)
    #                 # if transaction_date != current_date:
    #                 #     current_date = transaction_date
                        

    #                 transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

    #                 # Add transaction details
    #                 if transaction_date_str == str(arguements['start_date']):
    #                     print('yes inside')
    #                     transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
    #                                                             text_color=[0, 0, 0, 1], divider=None)
    #                     transaction_container.add_widget(transaction_item_widget)

    #                     transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

    #                     if transaction['transaction_type'] == 'Credit':
    #                         fund_color = [0, 0.5, 0, 1]
    #                         sign = '+'
    #                     else:
    #                         fund_color = [1, 0, 0, 1]
    #                         sign = '-'

    #                     icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
    #                                     size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, 'top': 0.7})
                            
    #                     sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
    #                                         halign='right')
    #                     fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
    #                                         halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                        
    #                     transaction_container.add_widget(sign_label)
    #                     transaction_container.add_widget(icon)
    #                     transaction_container.add_widget(fund_label)
    #                     self.ids.transaction_list.add_widget(transaction_container)
    #         if 'start_date' in arguements.keys() and 'last_date' in arguements.keys():
    #             transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
    #             self.ids.transaction_list.clear_widgets()
    #             current_date = ""

    #             for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
    #                                     reverse=True):
    #                 transaction_datetime = transaction['date']
    #                 transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
    #                 transaction_date = transaction_date_str.split(' ')[0]
    #                 transactions_text = f"{transaction['receiver_phone']}"
    #                 fund_text = f"{round(transaction['fund'], 2)}"
    #                 fund_currency = f"{transaction['currency']}"
    #                 lowered_currency = fund_currency.lower()
    #                 fund_currency1 = f"currency-{lowered_currency}"

    #                 if str(arguements['start_date']) <= transaction_date_str <= str(arguements['last_date']):
    #                     if transaction_date != current_date:
    #                         current_date = transaction_date
    #                         header_text = f"[b]{transaction_date}[/b]"
    #                         list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
    #                                                 text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

    #                         self.ids.transaction_list.add_widget(list1)

    #                     transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

    #                     # Add transaction details
    #                     if str(arguements['start_date']) <= transaction_date_str <= str(arguements['last_date']):
    #                         transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
    #                                                                 text_color=[0, 0, 0, 1], divider=None)
    #                         transaction_container.add_widget(transaction_item_widget)

    #                         transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

    #                         if transaction['transaction_type'] == 'Credit':
    #                             fund_color = [0, 0.5, 0, 1]
    #                             sign = '+'
    #                         else:
    #                             fund_color = [1, 0, 0, 1]
    #                             sign = '-'

    #                         icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
    #                                     size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, 'top': 0.7})
                            
    #                         sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
    #                                             halign='right')
    #                         fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
    #                                             halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                            
    #                         transaction_container.add_widget(sign_label)
    #                         transaction_container.add_widget(icon)
    #                         transaction_container.add_widget(fund_label)
    #                         self.ids.transaction_list.add_widget(transaction_container)
    #     except Exception as e:
    #         print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")
    #         self.manager.show_notification('Alert!','An error occurred. Please try again.')