from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
from homepage import GuestHomeScreen
Window.size = (360, 640)  # For Pydroid or desktop testing

class LoginScreen(MDScreen):
    pass

class SignupScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def on_kv_post(self, base_widget):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": "Guest", "on_release": lambda x="Guest": self.set_user_type(x)},
            {"viewclass": "OneLineListItem", "text": "Admin", "on_release": lambda x="Admin": self.set_user_type(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.user_type,
            items=menu_items,
            width_mult=3
        )

    def open_menu(self, caller):
        self.menu.open()

    def set_user_type(self, text):
        self.ids.user_type.text = text
        self.menu.dismiss()

    def sign_up(self):
        name = self.ids.full_name.text.strip()
        phone = self.ids.phone_number.text.strip()
        email = self.ids.email.text.strip()
        user_type = self.ids.user_type.text

        if not all([name, phone, email]) or user_type == "Select":
            Snackbar(text="Please fill all fields").open()
            return
        self.manager.current = "otp_screen"

class OTPScreen(MDScreen):
    def verify_otp(self):  # Call this when OTP is validated
        self.manager.current = "guest_home"
        
        
class SignupApp(MDApp):
    def build(self):
        Builder.load_file("UI/auth.kv")  
        Builder.load_file("UI/homepage.kv")    

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(SignupScreen(name='signup_screen'))
        sm.add_widget(OTPScreen(name='otp_screen'))
        sm.add_widget(GuestHomeScreen(name='guest_home'))

        sm.current = "login_screen"  # Show first screen

        return sm


# if __name__ == '__main__':
# SignupApp().run()
