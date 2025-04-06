from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
import math
import time
from kivy.utils import platform
from plyer import accelerometer  
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.screen import MDScreen

class NotePopupContent(BoxLayout):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.padding = dp(10)
        self.size_hint_y = None
        self.height = dp(200)

        self.title_field = MDTextField(
            hint_text="Title",
            mode="rectangle",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )
        self.add_widget(self.title_field)

        self.description_field = MDTextField(
            hint_text="Description",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )
        self.add_widget(self.description_field)

        self.description_field.bind(height=self.adjust_height)

    def adjust_height(self, instance, value):
        self.height = self.title_field.height + self.description_field.height + dp(20)


class GuestHomeScreen(Screen):
    notes = ListProperty([])

    def __init__(self, **kwargs):  # Fixed __init__
        super().__init__(**kwargs)
        self.dialog = None
        self.notes = []
        self._shake_threshold = 20
        self._last_reading = [0, 0, 0]
        self._shake_event = None
        self.shake_times = []

    def on_enter(self):
        Clock.schedule_once(self._load_notes)
        if platform == 'android':
            try:
                accelerometer.enable()
                self._shake_event = Clock.schedule_interval(self.detect_shake, 0.2)
            except:
                print("Accelerometer not supported.")

            
    def change_screen(self, screen_name):
        self.manager.current = screen_name
        
    def on_leave(self):
        if platform == 'android':
            try:
                accelerometer.disable()
                if self._shake_event:
                    self._shake_event.cancel()
            except:
                pass

    def change_screen(self, screen_name):
        self.manager.current = screen_name
        
    def detect_shake(self, dt):
        try:
            values = accelerometer.acceleration
            if not values:
                return

            x, y, z = values
            magnitude = math.sqrt(x**2 + y**2 + z**2)

            # Shake for clearing notes (multiple quick shakes)
            if magnitude > self._shake_threshold:
                now = time.time()
                self.shake_times.append(now)
                self.shake_times = [t for t in self.shake_times if now - t < 2]

                if len(self.shake_times) >= 3:
                    self.shake_times = []
                    self.clear_notes()

            # Strong horizontal shake for logout
            if abs(x) > 30:  # Tune this value if needed
                self.logout()

        except Exception as e:
            print("Error in detect_shake:", e)

    def nav_to_chatbot(self):
        self.manager.current = "chatbot_screen"

    def nav_to_files(self):
        self.manager.current = "files_screen"

    def nav_to_ocr(self):
        self.manager.current = "ocr_screen"

    def _load_notes(self, dt):
        if hasattr(self.ids, 'notes_list'):
            self.ids.notes_list.clear_widgets()
            for note in self.notes:
                item = OneLineListItem(text=note.get("title", "Untitled"))
                self.ids.notes_list.add_widget(item)

    def show_add_note_popup(self):
        self.dialog = MDDialog(
            title="Add Note",
            type="custom",
            content_cls=NotePopupContent(),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=self.dismiss_popup),
                MDRaisedButton(text="ADD", on_release=self.add_note),
            ],
            size_hint=(0.8, None),
            height=dp(300))
        self.dialog.open()

    def add_note(self, *args):
        content = self.dialog.content_cls
        title = content.title_field.text.strip()
        description = content.description_field.text.strip()
        if title or description:
            note_item = OneLineListItem(
                text=title,
                on_release=lambda x, t=title, d=description: self.show_note_details(t, d))
            self.ids.notes_list.add_widget(note_item)
            self.notes.append({"title": title, "description": description})
        self.dismiss_popup()

    def show_note_details(self, title, description):
        scroll_view = MDScrollView()

        description_label = MDLabel(
            text=description,
            size_hint_y=None,
            height=dp(200),  # Set a height for the label
            valign="top",
            halign="left",
            padding=(dp(10), dp(10)),  # Add padding for better readability
        )
        description_label.bind(texture_size=description_label.setter("size"))  # Adjust size to fit text
        scroll_view.add_widget(description_label)

        dialog = MDDialog(
            title=title,
            text=description,
            buttons=[
                MDFlatButton(text="CLOSE", on_release=lambda x: dialog.dismiss())
            ],
            size_hint=(0.8, None),
        )
        dialog.open()
    

    def dismiss_popup(self, *args):
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()

    def logout(self):
        self.manager.current = "login_screen"