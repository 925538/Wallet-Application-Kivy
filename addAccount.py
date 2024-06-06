from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
from kivy.base import EventLoop
from anvil.tables import app_tables
from kivy.factory import Factory
KV = """
<AddAccountScreen>
    BoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: 'Add Account'
            anchor_title:'left'
            elevation: 3
            left_action_items: [['arrow-left', lambda x: root.go_back()]]
            md_bg_color: "#148EFE"
            specific_text_color: "#ffffff"
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                spacing: "10dp"
                padding: ["10dp", "1dp", "10dp", "1dp"]
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {'top': 1}

                MDTextField:
                    id: account_holder_name
                    hint_text: "  Account Holder's Name"
                    mode: "rectangle"
                    multiline: False 
                    radius: [50, 50, 50, 50]


                MDTextField:
                    id: account_number
                    hint_text: "  Account Number"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]


                MDTextField:
                    id: confirm_account_number
                    hint_text: "  Confirm Account Number"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]

                MDTextField:
                    id: bank_name
                    hint_text: "  Bank Name"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]

                MDTextField:
                    id: branch_name
                    hint_text: "  Branch Name"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]

                MDTextField:
                    id: ifsc_code
                    hint_text: "  IFSC Code"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]


                MDTextField:
                    id: account_type
                    hint_text: "  Account Type"
                    mode: "rectangle"
                    multiline: False
                    radius: [50, 50, 50, 50]


                Widget:
                    size_hint_y: None
                    height: '5dp'    

                MDRaisedButton:
                    #id: edit_save_button
                    text: "Submit"
                    md_bg_color: "#148EFE"
                    size_hint: None, None
                    size: dp(150), dp(50)
                    pos_hint: {'center_x': 0.5}
                    on_release: root.add_account()

"""
Builder.load_string(KV)


class AddAccountScreen(Screen):
    def go_back(self):
        existing_screen = self.manager.get_screen('addaccount')
        self.manager.add_widget(Factory.AccmanageScreen(name='accmanage'))
        self.manager.current = 'accmanage'
        self.ids.account_holder_name.text=''
        self.ids.account_number.text=''
        self.ids.confirm_account_number.text=''
        self.ids.bank_name.text=''
        self.ids.branch_name.text=''
        self.ids.ifsc_code.text=''
        self.ids.account_type.text=''
        self.manager.remove_widget(existing_screen)
        
    def __init__(self, **kwargs):
        super(AddAccountScreen, self).__init__(**kwargs)
        EventLoop.window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def show_popup(self, text):
        dialog = MDDialog(
            title="Alert",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                    # pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
            ]
        )
        dialog.open()

    def add_account(self):
        acc_scr = self.manager.get_screen('addaccount')
        # Retrieve data from text fields
        account_holder_name = acc_scr.ids.account_holder_name.text
        account_number = acc_scr.ids.account_number.text
        confirm_account_number = acc_scr.ids.confirm_account_number.text
        bank_name = acc_scr.ids.bank_name.text
        branch_name = acc_scr.ids.branch_name.text
        ifsc_code = acc_scr.ids.ifsc_code.text
        account_type = acc_scr.ids.account_type.text

        # Check if the account numbers match
        if account_number != confirm_account_number:
            print("Error: Account numbers do not match.")
            # Snackbar("Error: Account number didn't match.").open()
            self.manager.show_notification('Alert!','Account number didnt match.')
            # You might want to handle this case in your UI, e.g., show an error message.
            return

        # Retrieve phone number from user_data.json
        phone = JsonStore('user_data.json').get('user')['value']["users_phone"]
        try:
            accounts_table = app_tables.wallet_users_account

            # Check if the account already exists
            existing_account = accounts_table.get(users_account_number=float(account_number))
            if existing_account:
                print("Error: Account number already exists.")
                # Snackbar(text="Error: Account number already exists.").open()
                self.manager.show_notification('Alert!', 'Account Number Already Exists.')
                return

            # Add a new row to the 'accounts' subcollection
            new_account = accounts_table.add_row(
                users_account_holder_name=account_holder_name,
                users_account_number=float(account_number),
                users_account_bank_name=bank_name,
                users_account_branch_name=branch_name,
                users_account_ifsc_code=ifsc_code,
                users_account_type=account_type,
                users_account_status_confirm=True,
                users_account_phone=phone
            )

            print("Account details added successfully.")
            # toast("account added successfully")
            self.manager.show_notification('Success', "Account details added successfully")
            self.manager.current = 'accmanage'

        except Exception as e:
            print(f"Error adding account details: {e}")
            # toast("error adding account details")
            self.manager.show_notification('Alert!','Error adding account details.')
