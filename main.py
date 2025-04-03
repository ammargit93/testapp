from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = MDLabel(
            text="Hello World",
            halign="center",
            theme_text_color="Primary",
            font_style="H2"
        )
        self.add_widget(label)

class HelloWorldApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return MainScreen()

if __name__ == '__main__':
    HelloWorldApp().run()
