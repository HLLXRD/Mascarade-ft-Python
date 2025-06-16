from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        root = BoxLayout()

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(30):  # Add many buttons to scroll
            btn = Button(text=f'Option {i+1}', size_hint_y=None, height=40)
            layout.add_widget(btn)

        scroll.add_widget(layout)
        root.add_widget(scroll)

        return root

if __name__ == '__main__':
    MyApp().run()