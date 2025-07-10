from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.audio import SoundLoader


import os
from math import cos, sin, pi
import random

from .game_brain import Game
from .sidebar_widget import ActionSidebar, CharSelectingSidebar, PlayerSelectingSidebar, SwapOrNotSidebar, BlockSelectingSidebar, PlayerWidget, CourtWidget, PauseOverlay
from .player_and_action import swap, char_selected



'''
Here, we will have some lines to discuss about the text_size, texture_size, label_size, since understanding these slightly-different things thoroughly is really important to manipulate the Labek better:

*text_size: The maximum box that the text can reach, it's a thing that can be predefined by the user, and it's like a deadline designated by a boss (us) to his workder (kivy).

*texture_size: The actual box that the text takes up after being rendered, this is like the actual time when a task is completed, it can only be specified once the task is done, and it cannot be set just like the text_size, it will be set by kivy instead.

*label_size: the size of the label, the label here is like a background, layout information holder for the text.

**The cases to apply them:.
+text_size = label_size: This will ensure that the text wont go out the label, since we have made the maximum text box size = size of the label
+label_size = texture_size: This will make the label fit perfectly to the size of the text_box.
+label_size = text_size: This usually used when we want the background a little bit wide around the text box


'''
#Make the image clickable
class ClickableImage(ButtonBehavior, Image):
    pass
class LimitedTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        max_chars = 12  # Set your limit here
        allowed = substring[:max_chars - len(self.text)]
        return super().insert_text(allowed, from_undo=from_undo)
class MenuScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'
        self.app = app
        self.image_general_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_general')

    def on_enter(self, *args):
        self.clear_widgets()
        self.image_general_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_general')
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")
        # Main layout
        self.main_layout = FloatLayout()
        self.background = Image(source = os.path.join(self.image_general_folder, 'background_menu.png'),
                                size_hint = (1,1),
                                pos_hint = {'center_x': 0.5, 'center_y': 0.5},
                                keep_ratio=False,
                                allow_stretch=True
                                )

        self.main_layout.add_widget(self.background)



        self.label_img = Image(source = os.path.join(self.image_general_folder, 'title_font.png'), size_hint = (1033/1333,193/750), pos_hint = {'center_x': 0.5, 'center_y': 209/300})
        self.main_layout.add_widget(self.label_img)


        # layout = BoxLayout(orientation='vertical', spacing=20, padding=50)


        # Start Game button
        self.start_btn = FloatLayout(size_hint = (494/ 1333,21/125), pos_hint = {'center_x': 925/1333, 'center_y': 178/375})

        self.start_btn_img = ClickableImage(
            source = os.path.join(self.image_general_folder, 'button.png'),
            size_hint = (1,1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )

        self.start_btn_img.bind(on_press=self.start_game)

        self.start_btn_text = Label(text = "Start game", font_size = self.size[1] // (12402/575) * 36/23, size_hint = (1,1), pos_hint = {'center_x': 0.5, 'center_y': 0.5}, valign = "center", halign = "center", font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),color=[192 / 255, 135 / 255, 74 / 255, 1])
        self.start_btn_text.bind(size = self.update_font_size)

        self.start_btn.add_widget(self.start_btn_img)
        self.start_btn.add_widget(self.start_btn_text)

        # Option button
        self.option_btn = FloatLayout(size_hint=(494 / 1333, 21 / 125),
                                     pos_hint={'center_x': 925 / 1333, 'center_y': 217/750})

        self.option_btn_img = ClickableImage(
            source=os.path.join(self.image_general_folder, 'button.png'),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )

        self.option_btn_img.bind(on_press=self.go_to_options)

        self.option_btn_text = Label(text="Option", font_size=self.size[1] // (12402 / 575) * 36 / 23, size_hint=(1, 1),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5}, valign = "center", halign = "center", font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                     color=[192 / 255, 135 / 255, 74 / 255, 1])
        self.option_btn_text.bind(size=self.update_font_size)

        self.option_btn.add_widget(self.option_btn_img)
        self.option_btn.add_widget(self.option_btn_text)

        #Exit
        self.exit_btn = FloatLayout(size_hint=(494 / 1333, 21 / 125),
                                     pos_hint={'center_x': 925 / 1333, 'center_y': 77 / 750})

        self.exit_btn_img = ClickableImage(
            source=os.path.join(self.image_general_folder, 'button.png'),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )

        self.exit_btn_img.bind(on_press=self.exit_game)

        self.exit_btn_text = Label(text="Exit", font_size=self.size[1] // (12402 / 575) * 36 / 23, size_hint=(1, 1),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5}, valign = "center", halign = "center", font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                   color=[192 / 255, 135 / 255, 74 / 255, 1])
        self.exit_btn_text.bind(size=self.update_font_size)

        self.exit_btn.add_widget(self.exit_btn_img)
        self.exit_btn.add_widget(self.exit_btn_text)


        self.main_layout.add_widget(self.start_btn)
        self.main_layout.add_widget(self.option_btn)
        self.main_layout.add_widget(self.exit_btn)

        self.add_widget(self.main_layout)




    def start_game(self, instance):
        print("Starting game...")
        self.app.game = Game(player_num = self.app.player_num)
        print(f"++++{Window.size}+++++++")
        self.manager.current = 'off_name_typing'
        # You can switch to game screen here later


    def go_to_options(self, instance):
        self.manager.current = 'options'

    def exit_game(self, instance):
        App.get_running_app().stop()

    def update_font_size(self,instance, value):
        instance.font_size = self.size[1] // (12402/575) * 36/23
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': 0.5, 'center_y': 0.5}




class OptionsScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = 'options'
    def on_enter(self, *args):
        self.clear_widgets()
        self.player_num = 3  # Default number of players
        self.speed = 1
        # Main layout
        self.layout = FloatLayout(size_hint = (1,1))

        self.img_general_folder = os.path.join(os.path.dirname(__file__), "img_general")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        self.background_path = os.path.join(self.img_general_folder, "option_background.png")
        self.background = Image(source = self.background_path, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        # Title
        # Title
        self.title = Label(text="Option",
                           font_size=self.layout.size[1] * 72/23 // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[191 / 255, 144 / 255, 0 / 255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 620 / 689},  ## ADJUST LATER
                           size_hint=(278 / 399, 126 / 689)
                           )
        print(self.title.pos_hint)
        self.title_shade = Label(text=self.title.text,
                                 font_size=self.layout.size[1]* 72/23 // (12402 / 575),
                                 halign='center',
                                 valign='center',
                                 font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                 color=[116 / 255, 47 / 255, 6 / 255, 1],
                                 pos_hint={'center_x': self.title.pos_hint["center_x"] * (1 - 12 / 995),
                                           'center_y': self.title.pos_hint["center_y"] * (1 - 1 / 150)},
                                 ## ADJUST LATER
                                 size_hint=self.title.size_hint
                                 )
        self.title_shade.shade_of = self.title

        self.title.text_size = self.title.size

        self.title.bind(size=self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.layout.add_widget(self.title_shade)
        self.layout.add_widget(self.title)

        # Player count section

        # Player count label
        self.player_label = Label(text=f'Number of Players: {self.player_num}',
                                  font_size=self.layout.size[1]* 36/23 // (12402 / 575),
                                  color = [191 / 255, 144 / 255, 0 / 255, 1],
                                  pos_hint={'center_x': 0.5, 'center_y': 0.75},
                                  font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                  size_hint = (1, 0.1),
                                  valign='center',
                                  halign='center')


        self.player_label.bind(size=self.update_button_font)

        self.layout.add_widget(self.player_label)

        # Player count slider
        self.player_slider = Slider(min=3, max=8, step=1, size_hint=(0.7, 0.02),
                background_horizontal='',  # Transparent background image
                value_track=True,
                value_track_color=(1, 0.2, 0.2, 1),  # No bg image
                background_disabled_horizontal='',  # No disabled bg image
                # background_vertical='',  # Same for vertical sliders
                # background_disabled_vertical='',
                background_width=0,
                # Light red fill color
                value_track_width=4,
                cursor_image= os.path.join(self.img_general_folder, "court.png"),
                pos_hint = {'center_x': 0.5, 'center_y': 0.65},
                )
        with self.player_slider.canvas.before:
            # self.texture = Image(source = r"D:\Em yêu những môn học này\OOP\Mascarade\kivy\src\img_general\raw\widget_background_copy.png").texture

            Color(0.5, 0, 0, 1)  # Dark red color (values 0–1)
            self._slider_bg = RoundedRectangle(pos=self.player_slider.pos,
                                        size=self.player_slider.size,
                                        radius=[(20, 20), (20, 20), (20, 20), (20, 20)],
                                        segments=24,
                                        # texture = self.texture
                                        )

        self.player_slider.bind(value=self.on_player_count_change)
        # Update rectangle when slider moves or resizes
        self.player_slider.bind(pos=self._update_slider_bg,
                                size=self._update_slider_bg)
        self.layout.add_widget(self.player_slider)

        # Speed count slider

        # Player count label
        self.speed_label = Label(text=f'Speed: x{1/self.speed}',
                                  font_size=self.layout.size[1] * 36 / 23 // (12402 / 575),
                                  color=[191 / 255, 144 / 255, 0 / 255, 1],
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                  font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                  size_hint=(1, 0.1),
                                  valign='center',
                                  halign='center')

        self.speed_label.bind(size=self.update_button_font)

        self.layout.add_widget(self.speed_label)
        self.speed_slider = Slider(min=0.2, max=1.5, step=0.1, value = 1, size_hint=(0.7, 0.02),
                                    background_horizontal='',  # Transparent background image
                                    value_track=True,
                                    value_track_color=(1, 0.2, 0.2, 1),  # No bg image
                                    background_disabled_horizontal='',  # No disabled bg image
                                    # background_vertical='',  # Same for vertical sliders
                                    # background_disabled_vertical='',
                                    background_width=0,
                                    # Light red fill color
                                    value_track_width=4,
                                    cursor_image=os.path.join(self.img_general_folder, "court.png"),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                    )
        with self.speed_slider.canvas.before:
            # self.texture = Image(source = r"D:\Em yêu những môn học này\OOP\Mascarade\kivy\src\img_general\raw\widget_background_copy.png").texture

            Color(0.5, 0, 0, 1)  # Dark red color (values 0–1)
            self._sslider_bg = RoundedRectangle(pos=self.speed_slider.pos,
                                               size=self.speed_slider.size,
                                               radius=[(20, 20), (20, 20), (20, 20), (20, 20)],
                                               segments=24,
                                               # texture = self.texture
                                               )

        self.speed_slider.bind(value=self.on_speed_change)
        # Update rectangle when slider moves or resizes
        self.speed_slider.bind(pos=self._update_sslider_bg,
                                size=self._update_sslider_bg)
        self.layout.add_widget(self.speed_slider)


        # Back button
        self.back_btn_img = ClickableImage(source = os.path.join(self.img_general_folder, "button.png"), size_hint = (468/1333, 39/250), pos_hint = {'center_x': 342/1333, 'center_y': 271/1500}, allow_stretch = True, keep_ratio = False)
        self.back_btn_text = Label(text='Back', font_size=self.layout.size[1]* 36/23 // (12402 / 575),
                            color = [192 / 255, 0 / 255, 0 / 255, 1],
                            halign = 'center',
                            valign = 'center',
                            font_name = os.path.join(self.font_folder, "ManufacturingConsent-Regular.ttf"),
                            pos_hint = {'center_x': self.back_btn_img.pos_hint["center_x"], "center_y": self.back_btn_img.pos_hint["center_y"]},
                            size_hint = (1, 1)
                            )
        self.back_btn_img.bind(on_press=self.back_to_menu)
        self.back_btn_text.bind(size = self.update_button_font)

        # Apply button
        self.apply_btn_img = ClickableImage(source=os.path.join(self.img_general_folder, "button.png"),
                                      size_hint=(468/1333, 39/250),
                                      pos_hint={'center_x': 1007/1333, 'center_y': 271/1500}, allow_stretch = True, keep_ratio = False)
        self.apply_btn_text = Label(text='Apply', font_size=self.layout.size[1] * 36 / 23 // (12402 / 575),
                          color=[233 / 255, 188 / 255, 21 / 255, 1],
                          halign='center',
                          valign='center',
                          font_name=os.path.join(self.font_folder, "ManufacturingConsent-Regular.ttf"),
                          pos_hint={'center_x': self.apply_btn_img.pos_hint["center_x"], "center_y": self.apply_btn_img.pos_hint["center_y"]},
                          size_hint=(1, 1)
                          )
        self.apply_btn_img.bind(on_press=self.apply_settings)
        self.apply_btn_text.bind(size=self.update_button_font)

        self.layout.add_widget(self.apply_btn_img)
        self.layout.add_widget(self.back_btn_img)
        self.layout.add_widget(self.apply_btn_text)
        self.layout.add_widget(self.back_btn_text)

        self.add_widget(self.layout)

    def _update_slider_bg(self, instance, value):
        self._slider_bg.pos = instance.pos
        self._slider_bg.size = instance.size

    def _update_sslider_bg(self, instance, value):
        self._sslider_bg.pos = instance.pos
        self._sslider_bg.size = instance.size

    def update_title_font(self, instance, value):
        instance.font_size = self.layout.size[1]* 72/23//(12402/575)
        instance.text_size = instance.size

    def update_button_font(self, instance, value):
        instance.font_size = self.layout.size[1]* 36/23 // (12402 / 575)
        instance.text_size = instance.size # Dont add this if we dont have a proper size hint, since we dont manually set a size hint, the label size, since we dont set, the size is (100, 100), and it can make the text_size shrink, wrap awkwardly
        # instance.size = instance.texture_size
    def update_title_shade_font(self, instance, value):
        instance.font_size = self.layout.size[1] * 72/23 // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-12/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)}

    def on_player_count_change(self, instance, value):
        self.player_num = int(value)
        self.player_label.text = f'Number of Players: {self.player_num}'

    def on_speed_change(self, instance, value):
        self.speed = value
        self.speed_label.text = f'Speed: x{round(1/self.speed, 1)}'

    def apply_settings(self, instance):
        self.app.player_num = self.player_num
        print(f"Applied settings: {self.player_num} players")
        self.manager.current = 'menu'
        # Here you can save the settings to your game

    def back_to_menu(self, instance):
        self.manager.current = 'menu'


class OffNameScreen(Screen):

    def __init__(self,app, **kwargs):
        super().__init__(**kwargs)
        print(Window.size)
        self.app = app
        self.name = 'off_name_typing'
        self.img_general_folder = os.path.join(os.path.dirname(__file__), "img_general")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

    def on_enter(self, *args):
        self.clear_widgets()
        #Get the layout
        self.layout = FloatLayout(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.background = Image(source=os.path.join(self.img_general_folder, "castle_view.png"), keep_ratio = False, allow_stretch = True, size_hint = (1,1))


        self.layout.add_widget(self.background)

        self.letter = Image(source = os.path.join(self.img_general_folder, "Name_background.png"), keep_ratio = False, allow_stretch = True, size_hint = (2.5/5,1),
                            pos_hint = {'center_x': 0.5, 'center_y': 2/5})
        self.layout.add_widget(self.letter)


        name_layout = BoxLayout(size_hint=(1, 0.7))

        name_input = LimitedTextInput(
            hint_text="Enter your name",
            multiline=False,
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.6, 'center_y': 0.1},
            background_color=(0, 0, 0, 0),  # Fully transparent
            foreground_color=(0, 0, 0, 1),  # White text
            cursor_color=(1, 1, 1, 1),  # White cursor
            halign="center",
            # valign="center",
            font_name = os.path.join(self.font_folder, "ManufacturingConsent-Regular.ttf"),
            font_size = 50
        )
        name_input.bind(on_text_validate=self.on_name_entered)

        name_layout.add_widget(name_input)
        self.layout.add_widget(name_layout)
        self.add_widget(self.layout)

    def on_name_entered(self, instance):
        name = [instance.text]
        self.app.game.take_player_names(name)
        self.app.game.game_build()
        self.manager.current = 'off_game'

class OffGameScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = 'off_game'
        # self.layout_initialized = False

        #Start the turn-counting indices, also initialize the win condition

        self.play_turn_index = 0
        self.block_turn_index = 0

        #To manage the widget, create a dict to store it correspondingly to the ID
        self.widgets_dict = {}

        #Initialize the sidebars
        self.sidebar = None
        self.player_sidebar = None
        self.char_sidebar = None
        self.block_sidebar = None
        self.swap_or_not_sidebar = None

        # Add sound
        self.sound_folder = os.path.join(os.path.dirname(__file__), "img_general")
        #Load the sounds
        self.sound = SoundLoader.load(os.path.join(self.sound_folder,r'Masquerade Waltz - Andreas Benhaut (mp3cut.net).mp3'))  # Can be .mp3, .ogg, .wav

    def on_pre_enter(self, **kwargs):
        # Initialize the sidebars
        self.sidebar = None
        self.player_sidebar = None
        self.char_sidebar = None
        self.block_sidebar = None
        self.swap_or_not_sidebar = None
        #Resert all the value that will be created later
        self.clear_widgets()
        self.win_condition = False
        self.time_ratio = self.app.time_ratio

        #Add sound
        # self.sound_folder = os.path.join(os.path.dirname(__file__), "img_general")
        # #Load the sounds
        # self.sound = SoundLoader.load('Masquerade Waltz - Andreas Benhaut (mp3cut.net).mp3')  # Can be .mp3, .ogg, .wav
        #
        if self.sound:
            print(f"Sound length: {self.sound.length} seconds")
            self.sound.loop = True
            self.sound.play()
        # if not self.layout_initialized:
        self.general_folder = os.path.join(os.path.dirname(__file__), "img_general")
        self.layout = FloatLayout()

        self.background = Image(
                                source=os.path.join(self.general_folder,'ingame_background_cropped.jpg'),     # <- Replace with your image path
                                allow_stretch=True,
                                keep_ratio=False,
                                size_hint=(1, 1),
                                pos_hint={'x': 0, 'y': 0}
                            )
        self.layout.add_widget(self.background)

        #Add the button for the sound
        self.mute_sound_btn = ClickableImage(source=os.path.join(self.general_folder, "mute.png"),
                                            pos_hint={"center_x": 0.05, "center_y": 0.1}, keep_ratio=True,
                                            size_hint=(0.1, 0.1))

        self.mute_sound_btn.bind(on_press = self.mute_sound)

        self.layout.add_widget(self.mute_sound_btn)

        # Add the button for the sound
        self.play_sound_btn = ClickableImage(source=os.path.join(self.general_folder, "sound.png"),
                                        pos_hint={"center_x": 0.05, "center_y": 0.1}, keep_ratio=True,
                                        size_hint=(0.1, 0.1))

        self.play_sound_btn.bind(on_press=self.play_sound)

        # self.layout.add_widget(self.play_sound_btn)

        self.player_num = self.app.player_num
        center_x = 0.5
        center_y = 0.5
        radius = 0.4
        ratio = 1/(Window.width / Window.height)

        for i in range(self.player_num):
            angle = -pi / 2 + 2 * pi * i / self.player_num
            if self.player_num == 8 :
                if i == 5 or i == 1:
                    angle += pi/18
                elif i == 3 or i == 7:
                    angle -= pi/18
            if self.player_num == 7:
                if i == 1:
                    angle += pi/18
                elif i == 6:
                    angle -= pi/18
            x = center_x + radius * cos(angle) * ratio
            y = center_y + radius * sin(angle)

            if angle == -pi / 2:
                position = "bottom"
            elif angle == pi/2:
                position = "top"
            elif -pi/2 < angle < pi/2:
                position = "right"
            else:
                position = "left"

            player_space = PlayerWidget(self, self.app.game.players_dict[i], position,
                                        pos_hint={'center_x': x, 'center_y': y})

            self.widgets_dict[i] = player_space
            self.layout.add_widget(player_space)

            # player_space.init_action()
        #For the court
        self.court_background = Image(
            source=os.path.join(self.general_folder, 'court.png'),  # <- Replace with your image path
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.court_background)

        self.court_widget = CourtWidget(self.app)
        self.layout.add_widget(self.court_widget)
        self.widgets_dict['court'] = self.court_widget



        #Init the hands on the widget
        for i in self.widgets_dict:
            if type(i) == int:
                self.widgets_dict[i].init_claim()


        # #For the pause button
        # self.pause_button = Button(text="Pause", size_hint=(0.05,0.05), pos_hint={'right': 1})
        # self.pause_button.bind(on_press = self.pause )
        # self.add_widget(self.pause_button)


        self.add_widget(self.layout)
        # self.layout_initialized = True

    def on_leave(self):
        self.sound.stop()

    def mute_sound(self, instance):
        self.layout.remove_widget(self.mute_sound_btn)
        if self.sound:
            self.sound.stop()
        self.layout.add_widget(self.play_sound_btn)

    def play_sound(self, instance):
        self.layout.remove_widget(self.play_sound_btn)
        if self.sound:
            self.sound.play()
        self.layout.add_widget(self.mute_sound_btn)



    def minimize_window(self, instance):
        Window.minimize()

    def toggle_maximize(self, instance):
        if Window.borderless:
            Window.borderless = False
            Window.fullscreen = False
        elif Window.fullscreen:
            Window.fullscreen = False
        else:
            Window.fullscreen = 'auto'

    def close_app(self, instance):
        App.get_running_app().stop()

    # def pause(self,instance):
    #     pause_overlay = PauseOverlay()
    #     Clock.unschedule(self.play_turn)
    #     self.add_widget(pause_overlay)

    def on_enter(self, **kwargs):
        for i in self.widgets_dict:
            if type(i) == int:
                self.widgets_dict[i].reveal_card()
                Clock.schedule_once(self.widgets_dict[i].hide_card, 5 * self.player_num/4 * self.time_ratio)
        Clock.schedule_once(self.play_turn, (5 * self.player_num/4 + 0.5) * self.time_ratio)

    def play_turn(self, dt):
        ###Since the game.check() only to check after a claim
        # if not self.app.game.check() == 0: ###Resolve the winning match
        #     print("Game over")
        #     return


        curr_turn = self.play_turn_index % self.app.player_num
        print(f"========Start of Player {curr_turn}'s turn========")
        curr_player = self.app.game.players_dict[curr_turn]

        if curr_player.type == "bot":
            result = curr_player.decide_play(self)
            # self.play_turn_index += 1
            # ###Update giảm revealed cards mỗi cuối lượt
            # Clock.schedule_once(self.play_turn, 1)
            if result[0] == 0:
                agent_ID = result[1]
                patient_ID = result[2]
                decision = result[3]

                self.widgets_dict[agent_ID].show_action(0, patient_ID)

                swap(agent_ID, patient_ID, decision, self)

            elif result[0] == 1:
                player_ID = result[1]
                role_ID = result[2]

                char_selected("dummy", player_ID, role_ID, self)

            elif result[0] == 2:
                player_ID = result[1]

                #Show action
                self.widgets_dict[curr_turn].show_action(2)

                #If peek, update itself probability
                curr_player.reveal_update([(curr_turn, curr_player.get_card().ID)], "normal")

                #Store to the history
                self.app.game.history.append({'mode': 2, "player": player_ID})

                #Endturn
                self.end_turn("dummy")


        else:
            self.call_for_decision(curr_turn)

    def block_turn(self,dt, first_ID, role_ID):
        self.block_turn_index += 1
        # print(f"====={self.block_turn_index}=====")
        if self.block_turn_index == self.app.game.player_num: #Finish resolve
            print(self.layout.size)

            #Resolve the claim phase, also update all the bots based on the revealed cards
            self.resolve_claim() # This need approaximately 1.8s to finish

            if not (self.app.game.chars_dict[role_ID] in self.app.game.special_activate): #and self.app.game.affected_dict["status"] == 1): #
                '''
                The approach "if not the situation that the special activate is actually activated" will make the system trigger the Courtesan strangely.
                Since the checking condition of the status is not triggering immediately but it waits for some sec (find the line Clock.schedule_once(lambda dt, p = player_ID, c = card_ID, r = role_ID, w = widget:update_claim(dt, p, c, r, w), 1.4))
                This makes the status is not updated enough fast, so the activate of the special will be trigger as the normal beside its own method, this make the game bomboclaaat
                '''
                print("Complete claim due to normal role, not special!!!")
                Clock.schedule_once(self.complete_claim, 2.1 * self.time_ratio)

        else:
            # self.block_turn_index += 1
            curr_turn = (self.block_turn_index + first_ID) % self.app.game.player_num
            print(f"-------Block Turn {curr_turn}-------")
            curr_player = self.app.game.players_dict[curr_turn]

            if curr_player.type == "bot":
                curr_player.decide_block(self, first_ID)
            else:
                self.call_for_block(first_ID, role_ID)



    def resolve_claim(self):
        game = self.app.game

        #Get the role_claimed
        role_ID = game.affected_dict['role_ID']
        role_claimed = game.chars_dict[role_ID]

        game.affected_dict['affected'].update(game.decide_dict["yes"])

        if len(game.decide_dict["yes"]) == 1:
            first_ID = game.decide_dict["yes"][0]
            first = game.players_dict[first_ID]
            first_widget = self.widgets_dict[first_ID]

            for player_ID in game.players_dict:
                widget = self.widgets_dict[player_ID]
                widget.parent.remove_widget(widget.bubble_chat)
                widget.bubble_chat = None

            #If there is only one, make the glove with the mask fade, and replace the transparent card with the cardback
            Clock.schedule_once(first_widget.hide_card, 0 * self.time_ratio)

            first_widget.claim_anim_out.start(first_widget.hand_mask_normal) # This take 0.6s to complete

            def one_yes(dt):

                game.affected_dict["status"] = 1

                game.dict_for_history["claimers"].append((first_ID, role_ID))

                if game.chars_dict[role_ID] not in self.app.game.special_activate:
                    game.chars_dict[role_ID].activate(first, self.app.game)
                    print(f">>{role_claimed.name} triggered")

                else:
                    game.chars_dict[role_ID].activate(first, game, self)
                    print(f">>{role_claimed.name} triggered")

            Clock.schedule_once(one_yes, 0.8 * self.time_ratio)
            ###This update for the situation everyone agree may cause the bot assume that player is the real role, while we can solve this by just raise the probability to 0.5
        else:
            #If there is more than 1 players claim, add the court to the affected
            game.affected_dict["affected"].add("court")
            true_IDs = [] #For the farmers
            game.wrong_IDs = []

            #Remove all the bubbles chat from the claiming yes or no phase
            for player_ID in game.players_dict:
                widget = self.widgets_dict[player_ID]
                widget.parent.remove_widget(widget.bubble_chat)
                widget.bubble_chat = None

            print(f"====={game.decide_dict["yes"]}")
            for player_ID in game.decide_dict["yes"]:
                widget = self.widgets_dict[player_ID]
                player = game.players_dict[player_ID]
                card_ID = player.get_card().ID

                #Reveal the card, show the animation of the hand, which will take 1,2s in total
                widget.claim_anim_out.start(widget.hand_mask_normal)
                Clock.schedule_once(lambda dt,w = widget: w.claim_anim_in.start(w.hand_mask_rotated), 0.6 * self.time_ratio)
                widget.reveal_card()

                def update_claim(dt, player_ID, card_ID, role_ID, widget):
                    print(f"^^^^^{player_ID, card_ID}^^^^^ ")
                    #Update revealed
                    game.players_dict[player_ID].revealed = len(self.app.game.players_dict) // 2 + 1  # Always +1 since this turn revealed cards decreased the confidence, the players inside the yes wont be decreased


                    if card_ID == role_ID:
                        game.affected_dict["status"] = 1
                        true_IDs.append(player_ID)
                        widget.pop_bubble_chat(f"{random.choice(game.chars_dict[role_ID].list_success)}")

                    else:
                        game.wrong_IDs.append(player_ID)
                        widget.pop_bubble_chat(f"{random.choice(game.players_dict[player_ID].get_card().list_fail)}")

                    game.dict_for_history["claimers"].append((player_ID, card_ID))

                Clock.schedule_once(lambda dt, p = player_ID, c = card_ID, r = role_ID, w = widget:update_claim(dt, p, c, r, w), 1.4 * self.time_ratio)

            #Activate the role on the true player
            def activ(dt):
                if len(true_IDs) != 0:
                    true_ID = true_IDs[0]
                    true_player = game.players_dict[true_ID]

                    if game.chars_dict[role_ID] not in self.app.game.special_activate:
                        game.chars_dict[role_ID].activate(true_player, self.app.game)
                        print(f">>{role_claimed.name} triggered")

                    else:
                        game.chars_dict[role_ID].activate(true_player, game, self)
                        print(f">>{role_claimed.name} triggered")

            Clock.schedule_once(activ,1.6 * self.time_ratio)


        #Add the dictionary to the history
        def update_his(dt):
            game.history.append(game.dict_for_history)

        Clock.schedule_once(update_his, 1.8 * self.time_ratio)


    def penalize(self):
        game= self.app.game
        # Penalize the role on the wrong player(s)
        for i in game.wrong_IDs:
            player = game.players_dict[i]
            player.money -= 1
            game.court += 1
    def update_UI_and_check(self):
        # print(f"\n\n\n {self.app.game.court}")
        print(f"====={self.app.game.affected_dict["affected"]}=====")


        for i in self.app.game.affected_dict["affected"]:
            #Since the widgets_dict has both 'court' (str) and 0,1,2,3,4,5(int), we can just update money for all players
            self.widgets_dict[i].update_money()

        print(f"The yes dict when update the UI: {self.app.game.decide_dict["yes"]}")

        if len(self.app.game.decide_dict["yes"]) > 1:
            for i in self.app.game.decide_dict["yes"]:
                Clock.schedule_once(self.widgets_dict[i].hide_card, 2 * self.time_ratio) ###We can just add 0.5 + i * delta_time so that the cards are hid gradually
                def remove_widget(dt, widget_ID):
                    print(f"Removing Bubble Chat of the Player {widget_ID}")
                    self.widgets_dict[widget_ID].parent.remove_widget(self.widgets_dict[widget_ID].bubble_chat)
                Clock.schedule_once(lambda dt ,widget_ID = i: remove_widget(dt, widget_ID), 2 * self.time_ratio)
                def none_bubble_chat(dt, widget_ID):
                    print(f"Removing Chat of the Player {widget_ID} from the parent")
                    self.widgets_dict[widget_ID].bubble_chat = None

                Clock.schedule_once(lambda dt, widget_ID = i: none_bubble_chat(dt, widget_ID), 2 * self.time_ratio)

        #Remove all the gloves for claim then check the result
        def delayed_check_remove_hand(dt):
            for i in self.app.game.decide_dict["yes"]:
                if self.widgets_dict[i].hand_mask_rotated.opacity != 0:
                    self.widgets_dict[i].hand_mask_rotated.opacity = 0
            check_result = self.app.game.check("real")
            if check_result == 0:
                return
            elif 0 in check_result :  # You won
                self.app.sm.current = "win_scene"
                self.win_condition = True
            else:
                self.app.sm.current = "lose_scene"
                self.win_condition = True
        Clock.schedule_once(delayed_check_remove_hand, 2.3 * self.time_ratio)



    # def special_activate_UI(self, mode, *args):
        # if mode == "courtesan":
        #     print("Updating courtesan...")
        #     customer_ID = args[0]
        #
        #     # The customers of the Courtesan will reveal to show their gender, also increase the revealed
        #     self.widgets_dict[customer_ID].reveal_card()
        #     self.app.game.players_dict[customer_ID].revealed = len(self.app.game.players_dict) // 2 + 1
        #
        #     #All the bots will update the customer's card into its memory
        #     for i in self.app.game.bots_dict:
        #         self.app.game.bots_dict[i].reveal_update([(customer_ID, self.app.game.players_dict[customer_ID].get_card().ID)], "normal")
        #
        #     Clock.schedule_once(self.widgets_dict[customer_ID].hide_card, 2 * self.time_ratio)
        #
        #     Clock.schedule_once(self.complete_claim, 3 * self.time_ratio)

        # if mode == "witch":
        #     spell_caster_ID = args[0]
        #
        #     decision = None
        #     if self.app.game.players_dict[spell_caster_ID].type == "bot":
        #         decision = self.app.game.players_dict[spell_caster_ID].decide_cards(mode = "witch")
        #
        #     elif self.app.game.players_dict[spell_caster_ID].type == "human":


    def complete_claim(self, dt):
        print("Complete the claim of the turn!")
        #Penalize the wrong players after complete
        self.penalize()
        # Update the UI, and also check if the win condition has met
        self.update_UI_and_check()  # This takes approximately 2.5s to fully completed

        def end_turn_check_win(dt): # If here, we wrap the endturn in the clock, not the entire condition-checking, it will get error since the update_UI_and_check require 2.3s to complete
            if self.win_condition == True:
                pass
            else:
                # Endturn, reduce the confidence
                Clock.schedule_once(self.end_turn, 0 * self.time_ratio)

        Clock.schedule_once(end_turn_check_win, 3 * self.time_ratio)


    def end_turn(self, dt):
        print("=======End Turn======")
        #Remove all the actions
        # for i in self.widgets_dict:
        #     if type(i) == int:
        #         Clock.schedule_once(self.widgets_dict[i].clear_action, 1)
        #If there is the letter from the last swapping, clear it
        if self.app.game.history[-1]["mode"] == 0:
            agent_ID = self.app.game.history[-1]["agent"]

            agent_widget = self.widgets_dict[agent_ID]

            if agent_widget.object != None:
                agent_widget.parent.remove_widget(agent_widget.object)
                agent_widget.object = None
            if agent_widget.bubble_chat != None:
                agent_widget.parent.remove_widget(agent_widget.bubble_chat)
                agent_widget.bubble_chat = None

        elif self.app.game.history[-1]["mode"] == 2:
            player_ID = self.app.game.history[-1]["player"]
            player_widget = self.widgets_dict[player_ID]

            if player_widget.peek_widget != None:
                player_widget.layout.remove_widget(player_widget.peek_widget)
                player_widget.peek_widget = None

            if player_widget.bubble_chat != None:
                player_widget.parent.remove_widget(player_widget.bubble_chat)
                player_widget.bubble_chat = None

        #Update the action
        self.app.game.update()
        for i in self.app.game.players_dict:
            player = self.app.game.players_dict[i]
            if player.revealed >= 1:
                player.revealed -= 1

        #Update the revealed
        for i in self.widgets_dict:
            if type(i) == int:
                self.widgets_dict[i].update_revealed()


        self.play_turn_index += 1
        Clock.schedule_once(self.play_turn, 1.5 * self.time_ratio)

    def call_for_decision(self, player_ID):
        if self.sidebar is None:
            self.sidebar = ActionSidebar(self, player_ID)
        if self.sidebar.parent is None:
            self.layout.add_widget(self.sidebar)
    def call_for_choose_char(self):
        if self.char_sidebar is None:
            self.char_sidebar = CharSelectingSidebar(self, "claim")
        if self.char_sidebar.parent is None:
            self.layout.add_widget(self.char_sidebar)
    def call_for_block(self, first_ID, role_ID):
        if self.block_sidebar is None:
            self.block_sidebar = BlockSelectingSidebar(self, first_ID, role_ID)
        if self.block_sidebar.parent is None:
            self.layout.add_widget(self.block_sidebar)
    def call_for_choose_player(self, mode, *args):
        if len(args) == 0: # We only remove the sidebar (ActionSideBar) if it is not a rollback call
            if self.sidebar.parent is not None:
                self.layout.remove_widget(self.sidebar)
            if self.sidebar is not None:
                self.sidebar = None

        if self.player_sidebar is None:
            self.player_sidebar = PlayerSelectingSidebar(self, mode)
        if self.player_sidebar.parent is None:
            self.layout.add_widget(self.player_sidebar)


    def call_for_swap_or_not(self, agent_ID, patient_ID, *args):
        if len(args) == 0: # We only remove the player_sidebar if it is not a rollback call
            if self.player_sidebar.parent is not None:
                self.layout.remove_widget(self.player_sidebar)
            if self.player_sidebar is not None:
                print("debug")
                self.player_sidebar = None
        if self.swap_or_not_sidebar is None:
            self.swap_or_not_sidebar = SwapOrNotSidebar(self, agent_ID, patient_ID)
        if self.swap_or_not_sidebar.parent is None:
            self.layout.add_widget(self.swap_or_not_sidebar)

    def hide_all_sidebars(self):
        # Hide action selection sidebar
        if self.sidebar and self.sidebar.parent:
            self.layout.remove_widget(self.sidebar)
            self.sidebar = None
        # Hide character selection sidebar
        if self.char_sidebar and self.char_sidebar.parent:
            self.layout.remove_widget(self.char_sidebar)
            self.char_sidebar = None
        # Hide block selection sidebar
        if self.block_sidebar and self.block_sidebar.parent:
            self.layout.remove_widget(self.block_sidebar)
            self.block_sidebar = None
        # Hide player selection sidebar
        if self.player_sidebar and self.player_sidebar.parent:
            self.layout.remove_widget(self.player_sidebar)
            self.player_sidebar = None
        # Hide swap selection sidebar
        if self.swap_or_not_sidebar and self.swap_or_not_sidebar.parent:
            self.layout.remove_widget(self.swap_or_not_sidebar)
            self.swap_or_not_sidebar = None

class WinScene(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "win_scene"

        self.image_general_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_general')

        self.layout = FloatLayout(size_hint = (1,1))

        self.background_path = os.path.join(self.image_general_folder, "winscreen.png")
        self.background = Image(source = self.background_path, size_hint = (1,1), allow_stretch = True, keep_ratio = False)
        self.layout.add_widget(self.background)

        self.main_menu_btn = ClickableImage(source = os.path.join(self.image_general_folder, "return_button.png"), pos_hint = {"center_x": 0.05, "center_y": 0.1}, keep_ratio = True, size_hint = (0.1, 0.1))
        self.main_menu_btn.bind (on_press=self.return_to_menu)

        # main_menu_btn = Button(text="Return to Main Menu", font_size=24, size_hint=(1, 0.2))
        # main_menu_btn.bind(on_press=self.return_to_menu)
        self.layout.add_widget(self.main_menu_btn)

        self.add_widget(self.layout)

    def return_to_menu(self, instance):
        self.app.sm.current = "menu"




class LoseScene(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "lose_scene"

        self.image_general_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_general')

        self.layout = FloatLayout(size_hint=(1, 1))

        self.background_path = os.path.join(self.image_general_folder, "loosescreen.png")
        self.background = Image(source=self.background_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.background)

        self.main_menu_btn = ClickableImage(source=os.path.join(self.image_general_folder, "return_button.png"),
                                            pos_hint={"center_x": 0.05, "center_y": 0.1}, keep_ratio=True, size_hint = (0.1, 0.1))
        self.main_menu_btn.bind(on_press=self.return_to_menu)

        # main_menu_btn = Button(text="Return to Main Menu", font_size=24, size_hint=(1, 0.2))
        # main_menu_btn.bind(on_press=self.return_to_menu)
        self.layout.add_widget(self.main_menu_btn)

        self.add_widget(self.layout)

    def return_to_menu(self, instance):
        self.app.sm.current = "menu"