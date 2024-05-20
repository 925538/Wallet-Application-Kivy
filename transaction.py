from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import Screen
from kivy.properties import DictProperty
from kivy.base import EventLoop
from anvil.tables import app_tables
from kivy.storage.jsonstore import JsonStore
from kivy.factory import Factory
from kivymd.uix.list import OneLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
import traceback
from kivy.uix.widget import Widget
from kivymd.material_resources import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from datetime import date
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.label import MDIcon
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

    def open_sort_filter(self):
        # if not self.filter_dialog:
        self.filter_dialog = MDDialog(
            title="Filter Payments",
            type="custom",
            content_cls=MDList(),
        )

        items = [
            OneLineListItem(text='All',on_release =(lambda x:self.get_transaction_history(no_filter = 'no_filter'))),
            OneLineListItem(text="Type",on_release = (lambda x:self.type_filter())),  # Text for Status option
            OneLineListItem(text="Currency",on_release = (lambda x:self.filter_currency())),  # Text for Type option
            OneLineListItem(text='Date', on_release=lambda x: self.pick_date()),
        ]
        for i in range(len(items)):
            self.filter_dialog.content_cls.add_widget(items[i])

        self.filter_dialog.open()
    
        

    dynamic_ids_currency = DictProperty({})
    dynamic_ids_type = DictProperty({})

    def type_filter(self):
        self.type_filt = MDDialog(
            title="Filter Payments",
            type="custom",
            content_cls=MDList(),
            buttons=[
                MDFlatButton(
                    text="CLEAR ALL",
                ),
                MDFlatButton(
                    text="APPLY",on_release = lambda x:self.get_transaction_history(trans_type = self.type_filt1))],

        )
        for typee in ['Credit','Debit']:
            id = typee
            item = OneLineListItem( id=id,text = typee,on_release = lambda x:self.type_filter_selected(x))
            self.type_filt.content_cls.add_widget(item)
            self.dynamic_ids_type[id] = item
        # print(self.dynmaic_ids.items())
        self.type_filt.open()

    def filter_currency(self):
        self.filt_currency = MDDialog(
            title="Filter Payments",
            type="custom",
            content_cls=MDList(),
            buttons=[
                MDFlatButton(
                    text="CLEAR ALL",
                ),
                MDFlatButton(
                    text="APPLY",on_release = lambda x:self.get_transaction_history(currency = self.currency)
                ),
            ],
            )
        for currency in self.options_button_icon_mapping:
            id = currency
            item = OneLineListItem( id=id,text = currency,on_release = lambda x:self.selected_currency(x))
            self.filt_currency.content_cls.add_widget(item)
            self.dynamic_ids_currency[id] = item
        self.filt_currency.open()
    
    def pick_date(self):
        self.date_p = MDDatePicker(mode="range")
        self.date_p.bind(on_save = self.selected_date)
        self.date_p.open()

    def selected_date(self,instance,value,daterange):
        print(instance)
        print(value)
        start_date = daterange[0]
        print('yes',start_date)
        end_date = daterange[-1]
        self.get_transaction_history_date(start_date = start_date,last_date = end_date)
    def type_filter_selected(self,instance):
        self.type_filt1 = instance.id
        for i in self.dynamic_ids_type:
            if i == instance.id :
                self.dynamic_ids_type[instance.id].bg_color='#148efe'
            else:
                self.dynamic_ids_type[i].bg_color = '#ffffff'
            
        return self.type_filt1

    def selected_currency(self,instance):
        # print(instance.id,instance)
        self.currency = instance.id
        # print(self.currency)
        for i in self.dynamic_ids_currency:
            if i == instance.id :
                self.dynamic_ids_currency[instance.id].bg_color='#148efe'
            else:
                self.dynamic_ids_currency[i].bg_color = '#ffffff'
            
        return self.currency

    
    options_button_icon_mapping = ['INR','GBP','EUR','USD']
    filt_currency=''
    type_filt=''
    type_filt1=''
    currency=''

    def get_transaction_history(self,**args):
        store = JsonStore('user_data.json').get('user')['value']
        phone = store['phone']
        if self.filter_dialog:
            self.filter_dialog.dismiss()
        if self.type_filt:
            self.type_filt.dismiss()
        if self.filt_currency:
            self.filt_currency.dismiss()
        
        arguements = args
        print(args)
        global transaction
        if 'currency' in arguements.keys():
            print('yes curre')
            global currency
            currency = arguements['currency'] 
            transaction = list(app_tables.wallet_users_transaction.search(phone=phone,currency = currency ))
        if 'trans_type' in arguements.keys():
            print('yes type')
            global transaction_type
            transaction_type = arguements['trans_type']
            transaction = list(app_tables.wallet_users_transaction.search(phone=phone,transaction_type = transaction_type ))
        if 'no_filter' in arguements.keys():
            print('yes no filter')
            transaction = list(app_tables.wallet_users_transaction.search(phone=phone))
            for i in transaction:
                print(i['receiver_phone'])
        # if self.currency == None or self.type_filt1 ==None:
        #     transaction = list(app_tables.wallet_users_transaction.search(phone=phone))
        try:
            # Get the phone number from the JSON file
            
            # Query the 'transactions' table to fetch the transaction history
            print('yes')
            transactions = transaction
            self.ids.transaction_list.clear_widgets()
            current_date = ""

            for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
                                    reverse=True):
                print('yes 1')
                transaction_datetime = transaction['date']
                transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                transaction_date = transaction_date_str.split(' ')[0]
                transactions_text = f"{transaction['receiver_phone']}"
                fund_text = f"{round(transaction['fund'], 2)}"
                fund_currency = f"{transaction['currency']}"
                lowered_currency = fund_currency.lower()
                fund_currency1 = f"currency-{lowered_currency}"
                print('yes 2')
                if transaction_date != current_date :
                    print('yes 3')
                    current_date = transaction_date
                    header_text = f"[b]{transaction_date}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                    self.ids.transaction_list.add_widget(list1)
                print('yes 5')
                transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                # Add transaction details
                
                transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                        text_color=[0, 0, 0, 1], divider=None)
                transaction_container.add_widget(transaction_item_widget)

                transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                if transaction['transaction_type'] == 'Credit':
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
    def get_transaction_history_date(self,**args):
        store = JsonStore('user_data.json').get('user')['value']
        phone = store['phone']
        if self.filter_dialog:
            self.filter_dialog.dismiss()
        
        
        arguements = args
      
        # if 'start_date' in arguements.keys()
        try:
            # Get the phone number from the JSON file
            
            # Query the 'transactions' table to fetch the transaction history
            if 'start_date' in arguements.keys() and 'last_date' not in arguements.keys() and arguements['start_date'] != arguements['last_date']:
                transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
                self.ids.transaction_list.clear_widgets()
                header_text = f"[b]{arguements['start_date']}[/b]"
                list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                                text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )
                self.ids.transaction_list.add_widget(list1)
                for transaction in sorted(filter(lambda x: x['date'] is not None , transactions), key=lambda x: x['date'],
                                        reverse=True):
                    transaction_datetime = transaction['date']
                    transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                    transaction_date = transaction_date_str.split(' ')[0]
                    transactions_text = f"{transaction['receiver_phone']}"
                    fund_text = f"{round(transaction['fund'], 2)}"
                    fund_currency = f"{transaction['currency']}"
                    lowered_currency = fund_currency.lower()
                    fund_currency1 = f"currency-{lowered_currency}"
                    print(fund_text,transaction_date_str)
                    # if transaction_date != current_date:
                    #     current_date = transaction_date
                        

                    transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                    # Add transaction details
                    if transaction_date_str == str(arguements['start_date']):
                        print('yes inside')
                        transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                text_color=[0, 0, 0, 1], divider=None)
                        transaction_container.add_widget(transaction_item_widget)

                        transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                        if transaction['transaction_type'] == 'Credit':
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
            if 'start_date' in arguements.keys() and 'last_date' in arguements.keys():
                transactions = list(app_tables.wallet_users_transaction.search(phone=phone))
                self.ids.transaction_list.clear_widgets()
                current_date = ""

                for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
                                        reverse=True):
                    transaction_datetime = transaction['date']
                    transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                    transaction_date = transaction_date_str.split(' ')[0]
                    transactions_text = f"{transaction['receiver_phone']}"
                    fund_text = f"{round(transaction['fund'], 2)}"
                    fund_currency = f"{transaction['currency']}"
                    lowered_currency = fund_currency.lower()
                    fund_currency1 = f"currency-{lowered_currency}"

                    if str(arguements['start_date']) <= transaction_date_str <= str(arguements['last_date']):
                        if transaction_date != current_date:
                            current_date = transaction_date
                            header_text = f"[b]{transaction_date}[/b]"
                            list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                                    text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                            self.ids.transaction_list.add_widget(list1)

                        transaction_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(36))

                        # Add transaction details
                        if str(arguements['start_date']) <= transaction_date_str <= str(arguements['last_date']):
                            transaction_item_widget = OneLineListItem(text=f"{transactions_text}", theme_text_color='Custom',
                                                                    text_color=[0, 0, 0, 1], divider=None)
                            transaction_container.add_widget(transaction_item_widget)

                            transaction_container.add_widget(Widget(size_hint_x=None, width=dp(20)))

                            if transaction['transaction_type'] == 'Credit':
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