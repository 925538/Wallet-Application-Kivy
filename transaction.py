from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivymd.uix.screen import Screen
from kivy.properties import DictProperty
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
from datetime import date
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.label import MDIcon
from kivy.uix.anchorlayout import AnchorLayout
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


'''
Builder.load_string(KV)


class Transaction(Screen):
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
        print(self.type_filt_credit)
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
        print(self.type_filt_debit)
        self.debit_type_add=type
        if hasattr(type, 'selected') and type.selected:
            print('yes inside slected')
            type.bg_color = (0,0,0,0)
            type.selected = False
            self.type_filt_debit = ''
        else:
            print('yes not selected')
            type.bg_color = '#148efe'
            type.selected = True
        
    
    
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
                # if transaction['']
                if transaction_date != current_date :
                    
                    current_date = transaction_date
                    header_text = f"[b]{transaction_date}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                    self.ids.transaction_list.add_widget(list1)
                
                transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                # Add transaction details
                if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited':
                    print('inside cond')
                    uer = app_tables.wallet_users.get(users_phone = phone)
                    transactions_text = uer['users_username']
                if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                    user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                    transactions_text = user['users_username']
                transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                        text_color=[0, 0, 0, 1], divider=None)
                transaction_container.add_widget(transaction_item_widget)

                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                if transaction['users_transaction_type'] == 'Credit':
                    fund_color = [0, 0.5, 0, 1]
                    sign = '+'
                elif transaction['users_transaction_type'] == 'Deposited':
                    fund_color = [0, 0.5, 0, 1]
                    sign = '+'
                else:
                    fund_color = [1, 0, 0, 1]
                    sign = '-'

                icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                    size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, 'top': 0.7})
                        
                sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                    halign='right')
                fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                    halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                
                transaction_container.add_widget(sign_label)
                transaction_container.add_widget(icon)
                transaction_container.add_widget(fund_label)
                self.ids.transaction_list.add_widget(transaction_container)
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
                        # if transaction_date != current_date:
                        #     current_date = transaction_date
                            

                        transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                        # Add transaction details
                        if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited':
                            print('inside cond')
                            uer = app_tables.wallet_users.get(users_phone = phone)
                            transactions_text = uer['users_username']
                        if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                            user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                            transactions_text = user['users_username']
                        if transaction_date_str == str(self.start_date):
                            print('yes inside')
                            transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                    text_color=[0, 0, 0, 1], divider=None)
                            transaction_container.add_widget(transaction_item_widget)

                            transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                            if transaction['users_transaction_type'] == 'Credit':
                                fund_color = [0, 0.5, 0, 1]
                                sign = '+'
                            elif transaction['users_transaction_type'] == 'Deposited':
                                fund_color = [0, 0.5, 0, 1]
                                sign = '+'
                            else:
                                fund_color = [1, 0, 0, 1]
                                sign = '-'

                            icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                            size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, 'top': 0.7})
                                
                            sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                                halign='right')
                            fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                                halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                            
                            transaction_container.add_widget(sign_label)
                            transaction_container.add_widget(icon)
                            transaction_container.add_widget(fund_label)
                            self.ids.transaction_list.add_widget(transaction_container)
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

                        if str(self.start_date) <= transaction_date_str <= str(self.end_date):
                            if transaction_date != current_date:
                                current_date = transaction_date
                                header_text = f"[b]{transaction_date}[/b]"
                                list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                                        text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                                self.ids.transaction_list.add_widget(list1)

                            transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                            # Add transaction details
                            if transaction['users_transaction_type'] == 'Withdrawn' or transaction['users_transaction_type'] == 'Deposited':
                                print('inside cond')
                                uer = app_tables.wallet_users.get(users_phone = phone)
                                transactions_text = uer['users_username']
                            if transaction['users_transaction_type'] == 'Credit' or transaction['users_transaction_type'] == 'Debit':
                                user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'] )
                                transactions_text = user['users_username']
                            if str(self.start_date) <= transaction_date_str <= str(self.end_date):
                                transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                        text_color=[0, 0, 0, 1], divider=None)
                                transaction_container.add_widget(transaction_item_widget)

                                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                                if transaction['users_transaction_type'] == 'Credit':
                                    fund_color = [0, 0.5, 0, 1]
                                    sign = '+'
                                elif transaction['users_transaction_type'] == 'Deposited':
                                    fund_color = [0, 0.5, 0, 1]
                                    sign = '+'
                                else:
                                    fund_color = [1, 0, 0, 1]
                                    sign = '-'

                                icon = MDIcon(icon=fund_currency1, theme_text_color='Custom', text_color=fund_color,
                                            size_hint=(None, None), size=(dp(5), dp(5)), pos_hint={'center_y': 0.5, 'top': 0.7})
                                
                                sign_label =  MDLabel(text=f"{sign}", theme_text_color='Custom', text_color=fund_color,
                                                    halign='right')
                                fund_label = MDLabel(text=f"{fund_text}", theme_text_color='Custom', text_color=fund_color,
                                                    halign='left', padding=(15, 15),size_hint_x= None,width = '100dp',adaptive_width = True)
                                
                                transaction_container.add_widget(sign_label)
                                transaction_container.add_widget(icon)
                                transaction_container.add_widget(fund_label)
                                self.ids.transaction_list.add_widget(transaction_container)
            except Exception as e:
                print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")
                self.manager.show_notification('Alert!','An error occurred. Please try again.')

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