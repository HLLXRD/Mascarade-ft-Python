

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
        # if platform in ('win', 'linux', 'macosx'):
        #     Window.maximize()
        #     screen_width, screen_height = Window.system_size  # ✅ not Window.size!
        #     print("Real screen resolution:", screen_width, screen_height)
        #     Window.minimize()
        #
        #     # Example: Resize window to 80% of real screen
        #     scale = 0.8
        #     target_width = int(screen_width * scale)
        #     target_height = int(screen_height * scale)
        #
        #     Window.size = (target_width, target_height)
        #     print("Resized Kivy window to:", Window.size)
        # Clock.schedule_interval(self.check_window_resize, 0.2) #Put here will finish this before all the setting below catches up

        # if platform == 'win':
        #     user32 = ctypes.windll.user32
        #     self.system_normal_width = user32.GetSystemMetrics(0)
        #     self.system_normal_height = user32.GetSystemMetrics(1)
        #     #print("Real native screen:", screen_width, screen_height)
        # #self.system_normal_width, self.system_normal_height = Window.system_size
        # print(f"The system size when in normal form is {self.system_normal_width}x{self.system_normal_height}")

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

    # # Alternative: Track size changes more precisely
    # def check_window_resize_precise(self, dt):
    #     current_size = (Window.width, Window.height)
    #
    #     # Store the size when we detect a "large" window
    #     if not hasattr(self, 'last_size'):
    #         self.last_size = current_size
    #         self.prev_maximized = False
    #         return
    #
    #     # Detect significant size changes
    #     width_change = abs(current_size[0] - self.last_size[0])
    #     height_change = abs(current_size[1] - self.last_size[1])
    #
    #     # Large size = maximized, small size = restored
    #     is_now_maximized = current_size[0] > 1400 or current_size[1] > 800
    #
    #     # Only act on significant changes to avoid noise
    #     if width_change > 100 or height_change > 100:
    #         print(f"Size changed: {self.last_size} → {current_size}, Maximized: {is_now_maximized}")
    #
    #         if self.prev_maximized and not is_now_maximized:
    #             print("Detected restore down 🗗 — resizing to custom size")
    #             Window.size = self.custom_restore_size
    #
    #             # Center the window manually
    #             try:
    #                 screen_width, screen_height = Window.system_size
    #                 if screen_width < 1024 or screen_height < 768:
    #                     screen_width, screen_height = 1920, 1080  # fallback
    #             except:
    #                 screen_width, screen_height = 1920, 1080  # fallback
    #
    #             # Calculate center position
    #             window_width, window_height = self.custom_restore_size
    #             center_x = (screen_width - window_width) // 2
    #             center_y = (screen_height - window_height) // 2
    #
    #             # Set window position
    #             Window.left = center_x
    #             Window.top = center_y
    #
    #         self.last_size = current_size
    #         self.prev_maximized = is_now_maximized




if __name__ == '__main__':
    print(os.path.dirname(__file__))
    app = GameApp()
    app.run()

    if platform == 'win':
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        print("Real native screen:", screen_width, screen_height)

