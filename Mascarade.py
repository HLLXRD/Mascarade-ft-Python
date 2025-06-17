from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

import os

from src import MenuScreen, OptionsScreen, OffNameScreen, OffGameScreen, WinScene, LoseScene
#Make the image clickable


class GameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_num = 4  # default
        self.game = None

        #Screens
        self.sm = None
        self.off_game_screen = None
    def build(self):

        # Create screen manager
        self.sm = ScreenManager()

        # Create the screens as self attributes
        self.menu_screen = MenuScreen(self)
        self.options_screen = OptionsScreen(self)
        self.off_name_screen = OffNameScreen(self)
        self.off_game_screen = OffGameScreen(self)
        self.win_screen = WinScene(self)
        self.lose_screen = LoseScene(self)

        # Add screens
        self.sm.add_widget(self.menu_screen)
        self.sm.add_widget(self.options_screen)
        self.sm.add_widget(self.off_name_screen)
        self.sm.add_widget(self.off_game_screen)
        self.sm.add_widget(self.win_screen)
        self.sm.add_widget(self.lose_screen)

        return self.sm

    def on_start(self):
        # Set window to fullscreen
        # Window.fullscreen = 'auto'
        pass



if __name__ == '__main__':
    print(os.path.dirname(__file__))
    app = GameApp()
    app.run()

