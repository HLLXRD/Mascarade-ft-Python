from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config


import ctypes
import os



from src import MenuScreen, OptionsScreen, OffNameScreen, OffGameScreen, WinScene, LoseScene
#Make the image clickable


class GameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prev_maximized = False
        ####
        self.player_num = 3  # default
        self.game = None

        #Screens
        self.sm = None
        self.off_game_screen = None

        ###Test time ratio
        self.time_ratio = 1

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


        self.normal_width, self.normal_height = Window.size
        print(f"The window size when in normal form is {self.normal_width}x{self.normal_height}")

        Window.maximize()

        self.system_normal_width, self.system_normal_height = Window.system_size

        self.maximum_width = Window.width
        self.maximum_height = Window.height
        print(f"The window maximum size is {self.maximum_width}x{self.maximum_height}")

        self.custom_width = self.maximum_width * 0.7
        self.custom_height = self.maximum_height * 0.7
        print(f"The window custom size is {self.custom_width}x{self.custom_height}")

        self.pos_top = (self.system_normal_height - self.custom_height)//2 + 30 # Fitted
        self.pos_left = (self.system_normal_width - self.custom_width)//2
        print(f"The window position is {self.pos_top}x{self.pos_left}")

        Clock.schedule_interval(self.check_window_resize, 0.2)


    # Better approach: Use absolute size thresholds instead of system_size
    # Better approach: Use absolute size thresholds instead of system_size
    def check_window_resize(self, dt):

        current_width = Window.width
        current_height = Window.height

        # Define what you consider "maximized" based on typical screen sizes
        # Adjust these thresholds based on your target devices

        # Window is maximized if EITHER dimension exceeds threshold
        is_now_maximized = (current_width >= self.maximum_width or
                            current_height >= self.maximum_height)

        # print(f"Current: {current_width}x{current_height}, Maximized: {is_now_maximized}")

        # When it was maximized and now it's not → user clicked "restore down"
        if self.prev_maximized and not is_now_maximized:
            # print("Detected restore down 🗗 — resizing to custom size")
            Window.size = (self.custom_width, self.custom_height)

            # Center the window manually
            # Get screen dimensions (use a reasonable default if system_size is unreliable)
            # try:
            #     screen_width, screen_height = Window.system_size

            #     # If system_size seems too small, use common screen size
            #     if screen_width < 1024 or screen_height < 768:
            #         screen_width, screen_height = 1920, 1080  # fallback
            # except:
            #     screen_width, screen_height = 1920, 1080  # fallback

            # Set window position
            Window.left = self.pos_left
            Window.top = self.pos_top

        self.prev_maximized = is_now_maximized

'''
-Fix the position of the widgets inside the circle (fixed 7, 8)
-Add the card name when revealed --C
-Add return button, pause button
-Add rulebook
-Add empty widget to the layout
-Scale the starting time with the number of players --C
-Reset the changing cards to the victim of the swap cards --C
-Scale the font size with the size of the window game:
    +Fix the font of the Court --C
    +Fix the font inside the widget
        .Scale the font, let the font in two lines if it gets too long --C
        .Counting the number of character (maybe control the capitalized character) so that if the text is short, keep it big in one line
    +Limit the name
    +Dont let some strange symbol goes to the name
    +After done everything, delete the dummy long word in the swap action to fix it
-Shorten the name of the bot
-Clear cache each game --C
-Fixing the problem where the game can have red dot --C
-Fix the problem where the player num in the option is 3, while the game is automatically set to 4 player num --C
-Fix the starting game time --C
-After done everything, just fix the judge, the first limit to claim role
-Fixing the problem that when the first time set up kivy, the game screen is not maximized, why?
-Fix the font on the sidebar, kinda hard to read it
-Add more music to it
'''

'''
important:
-Option screen
-Add sound
-Return to menu
-App logo
-Redesign the playerwidget'''
'''
-Adjust the speed of the game as option.
-Add more players'''


if __name__ == '__main__':
    # while True:
    app = GameApp()
    app.run()


    # if platform == 'win':
    #     user32 = ctypes.windll.user32
    #     screen_width = user32.GetSystemMetrics(0)
    #     screen_height = user32.GetSystemMetrics(1)
    #     print("Real native screen:", screen_width, screen_height)

