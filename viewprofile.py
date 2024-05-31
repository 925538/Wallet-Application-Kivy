# from ast import Store
# from ctypes import sizeof
# from fileinput import filename
# import imp
# from logging import root
# from operator import imod
# from os import path
from ast import Global
import platform
import anvil
from certifi import where
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import Screen
from kivy.uix.camera import Camera
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from PIL import Image, ImageDraw
from io import BytesIO
from kivy.core.image import Image as CoreImage
import tempfile
from kivymd.uix.boxlayout import MDBoxLayout
import os
from anvil.tables import app_tables
import base64
from kivy.uix.button import Button
from os.path import join

KV = """
<Profile>:
    Screen:
        MDScreen:
            BoxLayout:
                orientation: "vertical"
                MDTopAppBar:
                    title: 'Profile'
                    elevation: 3
                    left_action_items: [['arrow-left', lambda x: root.go_back()]]
                    md_bg_color: "#148EFE"
                    specific_text_color: "#ffffff"
                # Scrollable part
                ScrollView:
                    BoxLayout: 
                        size_hint_y: None
                        height: dp(580)
                        pos_hint: {'center_x': 0.45, 'y': 280}
                        spacing:dp(15)
                        padding:dp(12)        

                        BoxLayout:
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(15)
                            padding: dp(12)

                            MDIconButton:
                                id:profile 
                                icon:'camera'
                                spacing:dp(15)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primary_color
                                # hint_text_color_normal: "#484848"
                                # text_color_normal:"#484848"
                                # icon_left_color_normal:"#484848"
                                # line_color_normal:"#484848"
                                md_bg_color: "#e1eaea"
                                size_hint_y: None
                                height: 200
                                pos_hint: {'center_x': 0.5, 'center_y': 0.9}
                                on_release: root.open_camera()

                            # Profile Details
                            MDTextField:
                                hint_text:'Username'
                                spacing:dp(15)
                                id: username_label
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                icon_left_color_normal:"#148efe"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                icon_left: "account"
                                mode: "rectangle"
                                readonly: True

                            # BoxLayout:
                            #     orientation: 'horizontal'
                            #     size_hint_y: None
                            #     height: dp(66)
                            #     padding: dp(3)
                            #     spacing: dp(15)
                            MDTextField:
                                spacing:dp(15)
                                id: email_label
                                hint_text:'Email'
                                text_color_normal:"#484848"
                                hint_text_color_normal: "#148efe"
                                icon_left_color_normal:"#148efe"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                mode: "rectangle"
                                icon_left: "email"
                                readonly: True
                                theme_text_color: "Custom"
                                text_color: '#000000'  # Set text color to black
                                font_style: "Button"
                                bold: True
                                # MDIconButton:
                                #     icon: "pencil"
                                #     pos_hint: {'center_y': 0.5}
                                #     on_release: root.enable_email_edit()  

                            # BoxLayout:
                            #     orientation: 'horizontal'
                            #     size_hint_y: None
                            #     height: dp(66)
                            #     padding: dp(2.8)
                            #     spacing: dp(15)
                            MDTextField:
                                spacing: dp(15)
                                id: contact_label
                                hint_text:"Contact"
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                line_color_normal:"#148efe"
                                radius:[30,30,30,30]
                                mode: "rectangle"
                                icon_left: "phone"
                                readonly: True
                                theme_text_color: "Custom"
                                text_color: '#000000'  # Set text color to black
                                icon_left_color_normal:"#148efe"
                                font_style: "Button"
                                bold: True
                                # MDIconButton:
                                #     icon: "pencil"
                                #     pos_hint: {'center_y': 0.5}
                                #     on_release: root.enable_contact_edit() 

                            MDTextField:
                                spacing:dp(15)
                                id: aadhaar_label
                                hint_text_color_normal: "#148efe"
                                line_color_normal:"#148efe"
                                text_color_normal:"#484848"
                                hint_text:'Aadhaar'
                                radius:[30,30,30,30]
                                icon_left: "fingerprint"
                                icon_left_color_normal:"#148efe"
                                mode: "rectangle"
                                readonly: True

                            MDTextField:
                                spacing:dp(15)
                                id: pan_label
                                text_color_normal:"#484848"
                                hint_text_color_normal: "#148efe"
                                line_color_normal:"#148efe"
                                hint_text:'Pan'
                                radius:[30,30,30,30]
                                icon_left: "credit-card"
                                icon_left_color_normal:"#148efe"
                                #mode: "rectangle"
                                mode: "rectangle"
                                readonly: True

                            MDTextField:

                                hint_text:'Address'
                                hint_text_color_normal: "#148efe"
                                text_color_normal:"#484848"
                                line_color_normal:"#148efe"
                                # mode:'persistent'
                                text_color:0,0,0,1
                                # line_color_focus:1,0,0,1
                                font_color:0,0,0,1
                                id: address_label
                                icon_left: "map-marker"
                                icon_left_color_normal:"#148efe"
                                mode: "rectangle"
                                radius:[30,30,30,30]
                                readonly: True


                            MDRaisedButton:
                                spacing:dp(15)
                                id: edit_save_button
                                text: "Edit Profile"
                                size_hint: None, None
                                size: dp(150), dp(50)
                                pos_hint: {'center_x': 0.5}  
                                on_release: root.edit_profile()   

"""
Builder.load_string(KV)

from kivy.animation import Animation


class Profile(Screen):
    # current_user_data = None
    # editing_mode = False  # Initialize editing_mode attribute
    # email_editing = False  # Attribute to track email editing

    def animate_textfield(self):
        Animation(background_color=(1, 0.9, 0.9, 1)).start(self)

    def __init__(self, **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.editing_mode = False  # Initialize editing_mode in the __init__ method
        self.email_editing = False  # Initialize email_editing
        EventLoop.window.bind(on_keyboard=self.on_key)
    # def enable_email_edit(self):
    #     self.ids.email_label.readonly = False  # Enable email editing
    #     self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
    #     self.email_editing = True  # Set email_editing flag to True

    # def save_email(self, new_email):
    #     self.ids.email_label.text = new_email  # Update the label with the new email
    #     self.update_email(new_email)  # Save the new email to the JSON file
    #     self.disable_email_edit()  # Disable email editing after saving

    # def disable_email_edit(self):
    #     self.ids.email_label.readonly = True  # Disable email editing
    #     self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
    #     self.email_editing = False  # Set email_editing flag to False

    def edit_profile(self):
        self.manager.add_widget(Factory.EditUser(name='edituser'))
        edit_screen = self.manager.get_screen('edituser')
        store = JsonStore('user_data.json').get('user')['value']
        edit_screen.ids.username.text = store["username"]
        edit_screen.ids.email.text = store["email"]
        edit_screen.ids.phone.text = str(store["phone"])
        # edit_screen.ids.password.text = store["password"]
        edit_screen.ids.aadhaar.text = str(store["aadhar"])
        edit_screen.ids.pan.text = store["pan"]
        edit_screen.ids.address.text = store["address"]
        self.manager.current = 'edituser'

    # def save_profile(self):
    #     self.editing_mode = False  # Switch back to edit mode after saving

    # def update_email(self, new_email):
    #     # Update email in the JSON file
    #     store = JsonStore('user_data.json')  # Load the JSON store
    #     if store.exists('user'):
    #         user_data = store.get('user')
    #         user_data['value']['gmail'] = new_email  # Update the 'gmail' field with the new value
    #         store.put('user', **user_data)  # Put the updated data back into the JSON store
    #         self.fetch_and_update_navbar()
    #         self.fetch_and_update_complaint()
    #         print('new gmail updated')

    # def fetch_and_update_navbar(self):
    #     store = JsonStore('user_data.json').get('user')['value']
    #     # Update labels in NavbarScreen
    #     navbar_screen = self.manager.get_screen('navbar')
    #     navbar_screen.ids.username_label.text = store["username"]
    #     navbar_screen.ids.email_label.text = store["gmail"]
    #     navbar_screen.ids.contact_label.text = store["phone"]

    # def fetch_and_update_complaint(self):
    #     store = JsonStore('user_data.json').get('user')['value']
    #     # Update labels in ComplaintScreen
    #     complaint_screen = self.manager.get_screen('complaint')
    #     complaint_screen.ids.email_label.text = store["gmail"]

    # def edit_save_profile(self):
    #     if self.email_editing:
    #         new_email = self.ids.email_label.text  # Get the updated email from the UI
    #         self.update_email(new_email)  # Update email in the JSON file
    #         self.disable_email_edit()  # Disable email editing mode
    #         self.save_profile()  # If in email editing mode, save the email
    #     else:
    #         # Toggle between 'Edit Profile' and 'Save' for other fields
    #         if self.editing_mode:
    #             self.save_profile()  # If in save mode, save the profile
    #             self.ids.edit_save_button.text = "Edit Profile"  # Change button text to 'Edit Profile'
    #         else:
    #             self.edit_profile()  # If in edit mode, perform editing actions
    #             self.ids.edit_save_button.text = "Save"  # Change button text to 'Save'
    #         self.editing_mode = not self.editing_mode  # Toggle editing mode
    #         on_release: root.save_edit()

    def go_back(self):
        self.manager.current = 'dashboard'



    def on_key(self, window, key, scancode, codepoint, modifier):
        # 27 is the key code for the back button on Android
        if key in [27, 9]:
            self.go_back()
            return True  # Indicates that the key event has been handled
        return False

    def open_camera(self):
        # setting the path
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            from android.storage import primary_external_storage_path
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            # app_dir = App.get_running_app().user_data_dir
            from os.path import join
            app_dir=App.get_running_app().user_data_dir
            # Path = join(app_dir,"DCIM")
            global Path
            # Path=primary_external_storage_path()
            Path = join(app_dir,"/storage/emulated/0/")

        else:
            Path = r'/'
        file_chooser1 = FileChooserListView(path=Path)
        file_chooser1.bind(on_submit=self.selected_file)
        # Create and open a Popup containing the file chooser
        self.popup = Popup(title='Select a file', content=file_chooser1, size_hint=(1, 1), pos_hint={'top': 1, })
        boxlayoutt = MDBoxLayout(orientation='vertical', spacing=5, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5})
        button = Button(text='Cancel', size=(1, 1), pos_hint={'center_x': 0.5, 'bottom': 0.35})
        button.bind(on_release=self.cancel)
        boxlayoutt.add_widget(button)
        self.popup.open()
        self.popup.content.add_widget(boxlayoutt)
    def cancel(self, inst):
        self.popup.dismiss()

    def selected_file(self, instance, value, dummy):
        print(value[0])
        print(dummy)
        print(instance)
        image_path = value[0]  # after clicking we get the image path here
        try:
            # Open the image

            with Image.open(image_path) as img:
                dashboard_screen = self.manager.get_screen('dashboard')
                siz = img.size
                print('size: ', siz)
                # resizing the image
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                # img.crop((0,200,250,250))
                mask = Image.new('L', (250, 250), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 250, 250), fill=255)

                # apply mask to image
                img.putalpha(mask)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    temp_image_path = temp_file.name
                    img.save(temp_image_path)

                # save circular thumbnail image

                # img.save('circular1.png')

                # showing the image using show() function
                # img.show()

                def is_tilted(image_path):
                    try:
                        # Open the image
                        with Image.open(image_path) as img:
                            # Check if the image has Exif data

                            if hasattr(img, '_getexif'):
                                print('yes in hasat')
                                exif_data = img._getexif()
                                # Check if the image has orientation metadata (tag 274)
                                if exif_data and 274 in exif_data:
                                    # print('yes in exif data')
                                    orientation = exif_data[274]
                                    # print(orientation)
                                    # Check if the orientation requires rotation
                                    if orientation in [2, 3, 4, 5, 7, 6, 8]:
                                        # print('yes in orientation')
                                        return True
                                    else:
                                        # print('in inside else')
                                        return False
                                else:
                                    # print('else outside part')
                                    return False
                                    # if orientation in [1,2]:
                    except Exception as e:
                        print(f"Error: {e}")

                store = JsonStore('user_data.json').get('user')['value']['phone']
                table = app_tables.wallet_users.get(phone=store)
                # Rotate the image by 90 degrees clockwise
                if is_tilted(image_path):
                    # print('returned true')
                    with Image.open(image_path) as imgg:
                        # print('1')
                        exif_data = imgg._getexif()
                        # print('2')
                        orientate = exif_data[274]
                        # print('3')
                    rotations = {2: 0, 3: 180, 4: 180, 5: 90, 6: 270, 7: 90, 8: 90}
                    for i in rotations.keys():
                        # print('4')
                        if orientate == i:
                            global rotated_img
                            if orientate == 2:
                                img.flip_horizontal = True
                            if orientate == 4:
                                img.flip_vertical = True
                                rotated_img = img.rotate(rotations[orientate], expand=True)
                            if orientate == 5:
                                img.flip_vertical = True
                                rotated_img = img.rotate(rotations[orientate], expand=True)
                            if orientate == 7:
                                img.flip_vertical = True
                                rotated_img = img.rotate(rotations[orientate], expand=True)
                            print('5')

                            rotated_img = img.rotate(rotations[orientate], expand=True)
                            # print('6')
                            # print('7')
                            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                                # print('8')
                                temp_image_path1 = temp_file.name
                                rotated_img.save(temp_image_path1)
                            # print(type(rotated_img))
                            with BytesIO() as byte_stream:
                                rotated_img.save(byte_stream, format='PNG')
                                # print('yoo man')
                                image_bytes = byte_stream.getvalue()
                                byte_stream.seek(0)
                                # byte_stream.seek(0)
                                # image_data = byte_stream.read()
                                # byte_stream.seek(0)
                                
                            # print('before saving')
                            dashboard_screen.ids.user_image.source = temp_image_path1   #texture = CoreImage(BytesIO(image_data), ext='png',
                                                                                            #filename='image.png').texture
                            self.ids.profile.icon = temp_image_path1
                            # image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                            
                            pic = anvil.BlobMedia(content_type="image/png", content=image_bytes)
                            table.update(profile_pic = pic)
                            # dashboard_screen.user_pic()
                            print('yes updated')
                            break
                else:
                    try:
                        with Image.open(temp_image_path) as img:
                            with BytesIO() as byte_stream:
                                img.save(byte_stream, format='PNG')
                                imagee_byte = byte_stream.getvalue()
                                # byte_stream.seek(0)
                                # imagee_data = byte_stream.read()
                                # byte_stream.seek(0)
                                # print('yes continued ')
                        # converting to base64
                        # imagee_base64 = base64.b64encode(imagee_byte).decode('utf-8')
                        print('yes 2')
                        # clearing previous data
                        
                        # print('yes 3')
                        # updating table  in database
                        picc = anvil.BlobMedia(content_type="image/png", content=imagee_byte)
                        table.update(profile_pic = picc)
                        print('yes updated1')
                        # print('yes 4')
                        # providing image to the dashboard screen
                        dashboard_screen.ids.user_image. source=temp_image_path
                        self.ids.profile.icon = temp_image_path
                    except Exception as e:
                        print(e)
                        self.manager.show_notification('Alert!','An error occured.  Please try again.')
            # Continue with further processing...
        except Exception as e:
            print(f"Error opening image: {e}")
            self.manager.show_notification('Alert!','An error occured.  Please try again.')
        self.popup.dismiss()

    def on_pre_enter(self):
        store = JsonStore('user_data.json').get('user')['value']['phone']
        table = app_tables.wallet_users.get(phone=store)
        image_stored = table['profile_pic']
        if image_stored:
            decoded_image_bytes =image_stored.get_bytes()
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file1:
                temp_file_path = temp_file1.name
                # Write the decoded image data to the temporary file
                temp_file1.write(decoded_image_bytes)
                # Close the file to ensure the data is flushed and saved
                temp_file1.close()
            self.ids.profile.icon = temp_file_path
