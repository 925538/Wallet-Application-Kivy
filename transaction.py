from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
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
    filter_dialog = ObjectProperty(None)

    def open_sort_filter(self):
        if not self.filter_dialog:
            from kivymd.uix.dialog import MDDialog
            from kivymd.uix.list import MDList, OneLineListItem

            self.filter_dialog = MDDialog(
                title="Filter Payments",
                type="custom",
                content_cls=MDList,
                buttons=[
                    MDFlatButton(
                        text="CLEAR ALL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="APPLY", text_color=self.theme_cls.primary_color
                    ),
                ],
            )

            items = [
                OneLineListItem(text="Status"),  # Text for Status option
                OneLineListItem(text="Type"),  # Text for Type option
            ]
            self.filter_dialog.content_cls.add_widget(items[0])
            self.filter_dialog.content_cls.add_widget(items[1])

        self.filter_dialog.open()

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
    options_button_icon_mapping = {
        "INR": "currency-inr",
        "GBP": "currency-gbp",
        "USD": "currency-usd",
        "EUR": "currency-eur"
    }
    def get_transaction_history(self,currency):
        try:
            # Get the phone number from the JSON file
            store = JsonStore('user_data.json').get('user')['value']
            phone = store['phone']
            # Query the 'transactions' table to fetch the transaction history
            transactions = list(app_tables.wallet_users_transaction.search(phone=phone,currency=currency))
            self.ids.transaction_list.clear_widgets()
            current_date = ""

            for transaction in sorted(filter(lambda x: x['date'] is not None, transactions), key=lambda x: x['date'],
                                    reverse=True):
                transaction_datetime = transaction['date']
                transaction_date_str = transaction_datetime.strftime('%Y-%m-%d')
                transaction_date = transaction_date_str.split(' ')[0]
                transactions_text = f"{transaction['receiver_phone']}"
                fund_text = f"{transaction['fund']}"

                if transaction_date != current_date:
                    current_date = transaction_date
                    header_text = f"[b]{transaction_date}[/b]"
                    list1 = OneLineListItem(text=header_text, height=dp(15), theme_text_color='Custom',
                                            text_color=[0, 0, 0, 1], divider=None, bg_color="#e5f3ff", )

                    self.ids.transaction_list.add_widget(list1)

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

                fund_label = MDLabel(text=f"{sign}{currency} {fund_text}", theme_text_color='Custom', text_color=fund_color,
                                    halign='right', padding=(15, 15))
                transaction_container.add_widget(fund_label)

                self.ids.transaction_list.add_widget(transaction_container)
        except Exception as e:
            print(f"Error getting transaction history: {e} ,{traceback.format_exc()}")
            self.manager.show_notification('Alert!','An error occurred. Please try again.')