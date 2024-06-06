from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
from kivy.base import EventLoop
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from anvil.tables import app_tables

KV = """
<DefaultCurrency>:
    MDBoxLayout:
        orientation:'vertical'
        MDTopAppBar:
            title: 'Set Default Currency'
            anchor_title:'left'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
            
        # padding:dp(10)
        # spacing:dp(8)
        ScrollView:
            pos_hint:{'center_x':0.5}
            MDBoxLayout:
                orientation:'vertical'
                spacing:dp(10)
                size_hint_y: None
                height: self.minimum_height
                padding:dp(10)
                
            
                
                # MDBoxLayout:
                #     orientation:'horizontal'      

"""
# Dynamically generate the KV string for MDCards
for currency in ['INR', 'USD', 'EUR', 'GBP']:
    icon_path = f"images/{currency.lower()}icon.png"
    if os.path.exists(icon_path):
        icon_source = icon_path
    else:
        icon_source = "images/inricon.png"

    card_kv = f'''
                MDCard:
                    id:{currency}
                    orientation: 'vertical'
                    size_hint: None, None
                    size: "350dp", "100dp"
                    pos_hint: {{"center_x": .5}}
                    md_bg_color:'#b0d9f9'     
                    on_press:root.pressed('{currency}')
                    
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: dp(30)
                        size_hint:None,None
                        pos_hint:{{'center_x':0.38,'y':0.6}}
                        AsyncImage:
                            source: f"{icon_source}"
                            size_hint:None,None
                            height:dp(45)
                            width:dp(45)
                            pos_hint:{{'center_x':0.5,'center_y':0.7}}  

                        MDLabel:
                            id: text_label
                            text: '{currency}'
                            font_size:dp(25)
                            theme_text_color: "Secondary"
                            size_hint:None,None
                            width:dp(80)
                            height:dp(30)
                            halign: 'left'
                            valign:'center'
                            pos_hint:{{'center_x':0.5,'center_y':0.7}}

                            
                            # CheckBox:
                            #     id: {currency}
                            #     color:"#0c217b"
                            #     group:'Default currency'
                            #     on_release:root.check_box(self.active,'{currency}')
                            
                            
                            
                             
    '''
    KV += card_kv

Builder.load_string(KV)


class DefaultCurrency(Screen):

    def go_back(self):
        existing_screen = self.manager.get_screen('defaultcurrency')
        self.manager.current = 'dashboard'
        self.manager.remove_widget(existing_screen)

    def __init__(self, **kwargs):
        super(DefaultCurrency, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)
        self.options_button_icon_mapping = {
            "INR": "currency-inr",
            "GBP": "currency-gbp",
            "USD": "currency-usd",
            "EUR": "currency-eur"
        }

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def pressed(self, money):
        currency_options = ['INR', 'USD', 'EUR', 'GBP']
        store = JsonStore("user_data.json").get('user')['value']['users_defaultcurrency']

        for icon_opt in currency_options:
            if icon_opt == money:
                for values in currency_options:
                    if values == money:
                        self.ids[money].md_bg_color = "#148EFE"
                        self.ids[money].elevation = 3
                    else:
                        self.ids[values].md_bg_color = '#b0d9f9'
                        self.ids[values].elevation = 0
                # sm=self.manager
                # wallet details
                # wallet_scr =Factory.AddMoneyScreen(name='addmoney')
                # sm.add_widget(wallet_scr)
                # wallet_details = sm.get_screen('addmoney')

                # withdraw details
                # withdraw_scr = Factory.WithdrawScreen(name='withdraw')
                # sm.add_widget(withdraw_scr)
                # withdraw_details = sm.get_screen('withdraw')

                # setting in wallet
                # wallet_details.ids.options_button.icon = self.options_button_icon_mapping[money]

                # setting in withdraw
                # withdraw_details.ids.options_button.icon = self.options_button_icon_mapping[money]
                # withdraw_details.ids.options_button.text= money

                # setting the currency in database to default
                # updating user data with new currency

                store = JsonStore("user_data.json")
                user = store.get('user')
                phone = user['value']['users_phone']
                user['value']['users_defaultcurrency'] = money
                store.put("user", **user)  # updating the default currency
                # store.save()

                users_curr = app_tables.wallet_users.get(users_phone=phone)
                users_curr.update(users_defaultcurrency=money)
                # users_curr.commit()

            else:
                continue

    def on_enter(self):
        # store=JsonStore("user_data.json").get('user')['value']['defaultcurrency']
        # defaultcurrency=store,
        phone = JsonStore("user_data.json").get('user')['value']['users_phone']
        # print(store)
        user = app_tables.wallet_users.get(users_phone=phone)
        users_default_currency = user['users_defaultcurrency']

        print(user['users_defaultcurrency'])
        # checking if there is default currency for this user
        if users_default_currency != None:
            self.ids[users_default_currency].md_bg_color = "#148EFE"
            self.ids[users_default_currency].elevation = 3
            print('yes store')
            ids_s = list(self.ids.keys())
            print(ids_s)
            # self.ids..active = True
            self.ids[users_default_currency].active = True
            sm = self.manager

            # wallet details
            wallet_scr = Factory.AddMoneyScreen(name='addmoney')
            sm.add_widget(wallet_scr)
            wallet_details = sm.get_screen('addmoney')

            # withdraw details
            withdraw_scr = Factory.WithdrawScreen(name='withdraw')
            sm.add_widget(withdraw_scr)
            withdraw_details = sm.get_screen('withdraw')

            # setting in wallet
            wallet_details.ids.options_button.icon = self.options_button_icon_mapping[
                users_default_currency]  # setting the icon mapping

            # setting in withdraw
            withdraw_details.ids.options_button.icon = self.options_button_icon_mapping[
                users_default_currency]  # setting the icon mapping
            withdraw_details.ids.options_button.text = users_default_currency


class manager(ScreenManager):
    pass


class Myapp(MDApp):
    def build(self):
        scr_mgr = manager()
        scr_mgr.add_widget(DefaultCurrency(name='default'))
        return scr_mgr


if __name__ == "__main__":
    Myapp().run()
