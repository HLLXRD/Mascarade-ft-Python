from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.cache import Cache
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window

import os
import random
import pyglet
import copy

from .player_and_action import char_selected, swap
from .char import Witch, Princess



class ClickableImage(ButtonBehavior, Image):
    pass

class ActionSidebar(FloatLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 0.9])

    def __init__(self, game_screen, player_ID, **kwargs):
        super().__init__(size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)
        #Take the general folder
        self.img_action_folder = os.path.join(os.path.dirname(__file__), "img_actions/sidebar")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        self.game_screen = game_screen
        self.player_ID = player_ID
        self.player = self.game_screen.app.game.players_dict[self.player_ID]

        self.background_path = os.path.join(self.img_action_folder, "sidebar_background.png")
        print(self.background_path)
        self.background = Image(source=self.background_path, pos_hint={'center_x': 0.5, "center_y": 0.5},
                                size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)
        # # Transparent-ish background
        # with self.canvas.before:
        #     Color(*self.background_color)
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        #
        # self.bind(size=self._update_rect, pos=self._update_rect)
        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1), pos_hint={'center_x': 0.5, "center_y": 0.5})

        # # Title
        # title = Label(text="Your Turn", font_size=24, size_hint=(1, 0.1))
        # self.main_layout.add_widget(title)
        # Add background

        #########Test Title#######
        self.title = Label(text = "Your move, noble one. What shall it be?",
                           font_size = self.size[1]//(12402/575),
                           halign='center',
                           valign='center',
                           font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color = [192/255, 135/255, 74/255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 593/689}, ## ADJUST LATER
                           size_hint = (278/399, 88/689)
                           )
        print(self.title.pos_hint)
        self.title_shade = Label(text="Your move, noble one. What shall it be?",
                           font_size=self.size[1] // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[116 / 255, 47 / 255, 6 / 255, 1],
                           pos_hint={'center_x': self.title.pos_hint["center_x"] * (1-18/995), 'center_y': self.title.pos_hint["center_y"] * (1-1/150)},  ## ADJUST LATER
                           size_hint=(278 / 399, 88 / 689)
                           )
        self.title_shade.shade_of = self.title

        self.title.text_size = self.title.size

        self.title.bind(size = self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.add_widget(self.title_shade)
        self.add_widget(self.title)



        ############################

        # Action buttons
        # swap_btn = Button(text="Swap", font_size=18, size_hint=(1, 0.15))
        # swap_btn.bind(on_press=self.on_swap_cards)
        # self.main_layout.add_widget(swap_btn)
        # Swap buttons
        self.swap_btn_img = ClickableImage(
                          size_hint  =(268/399, 9/53),
                          source = os.path.join(self.img_action_folder, "best_frame.png"),
                          pos_hint = {"center_x": 0.5, "center_y": 913/1378},
                          keep_ratio = False,
                          allow_stretch = True)
        self.swap_btn_label = Label(text="Swap",
                                    font_size=self.size[1] * 28/23 // (12402/575),
                                    font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                    size_hint  =(268/399, 9/53),
                                    pos_hint = {"center_x": 0.5, "center_y": 913 / 1378},
                                    valign='center',
                                    halign='center',
                                    color = [192/255, 135/255, 74/255, 1])
        self.swap_btn_label.text_size = self.swap_btn_label.size


        self.swap_btn_img.bind(on_press=self.on_swap_cards, size = lambda instance, value, pos = 0: self.update_button_img(instance,value, pos))
        self.swap_btn_label.bind(size= self.update_button_label)

        self.add_widget(self.swap_btn_img)
        self.add_widget(self.swap_btn_label)




        # If the revealed is 0 and the total turns played are more than 2, show the claim
        if self.player.revealed == 0 and self.game_screen.play_turn_index > 2:
            #Claim button
            self.claim_btn_img = ClickableImage(
                size_hint=(268 / 399, 9 / 53),
                source=os.path.join(self.img_action_folder, "best_frame.png"),
                pos_hint={"center_x": 0.5, "center_y": 913 / 1378 - 7000/ 35139},
                keep_ratio=False,
                allow_stretch=True)
            self.claim_btn_label = Label(text="Claim",
                                        font_size=self.size[1] * 28 / 23 // (12402 / 575),
                                        font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                        size_hint=(268 / 399, 9 / 53),
                                        pos_hint={"center_x": 0.5, "center_y": 913 / 1378 - 7000/ 35139},
                                        valign='center',
                                        halign='center',
                                        color=[192 / 255, 135 / 255, 74 / 255, 1])
            self.claim_btn_label.text_size = self.claim_btn_label.size

            self.claim_btn_img.bind(on_press=self.on_claim_role, size = lambda instance, value, pos = 7000/ 35139: self.update_button_img(instance,value, pos))
            self.claim_btn_label.bind(size=self.update_button_label)

            self.add_widget(self.claim_btn_img)
            self.add_widget(self.claim_btn_label)
        ######
        #Peek button
        self.peek_btn_img = ClickableImage(
            size_hint=(268 / 399, 9 / 53),
            source=os.path.join(self.img_action_folder, "best_frame.png"),
            pos_hint={"center_x": 0.5, "center_y": 913 / 1378 - 7000/ 35139},
            keep_ratio=False,
            allow_stretch=True)
        self.peek_btn_label = Label(text="Peek cards",
                                     font_size=self.size[1] * 28 / 23 // (12402 / 575),
                                     font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                     size_hint=(268 / 399, 9 / 53),
                                     pos_hint={"center_x": 0.5, "center_y": 913 / 1378 - 2 * 7000/ 35139},
                                     valign='center',
                                     halign='center',
                                     color=[192 / 255, 135 / 255, 74 / 255, 1])
        self.peek_btn_label.text_size = self.peek_btn_label.size

        self.peek_btn_img.bind(on_press=self.on_look_at_card,
                                size=lambda instance, value, pos=2 * 7000/ 35139: self.update_button_img(instance, value,
                                                                                                      pos))
        self.peek_btn_label.bind(size=self.update_button_label)

        self.add_widget(self.peek_btn_img)
        self.add_widget(self.peek_btn_label)

        #Roll back button
        self.rollback_btn_img = ClickableImage(
            size_hint=(61/399,61/689),
            source=os.path.join(self.img_action_folder, "return_button_flip.png"),
            pos_hint={"center_x": 0.5, "center_y": 137/1378},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_btn_img.bind(on_press=self.on_rollback_sidebar)
        self.add_widget(self.rollback_btn_img)

        #Rollback again button
        self.rollback_again_btn_img = ClickableImage(
            size_hint=(61/1333,61/689),
            source=os.path.join(self.img_action_folder, "return_button.png"),
            pos_hint={"center_x": 1 - 99/1378, "center_y": 0.5 },
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_again_btn_img.bind(on_press=self.on_rollback_again_sidebar)


        # Spacer
        # self.main_layout.add_widget(Label(text="", size_hint=(1, 0.3)))

        # Add the boxlayout into the FloatLayout
        # self.add_widget(self.main_layout)

        # # End turn button
        # end_turn_btn = Button(text="End Turn", font_size=20, size_hint=(1, 0.15))
        # end_turn_btn.bind(on_press=self.on_end_turn)
        # self.add_widget(end_turn_btn)
    def update_title_font(self, instance, value):
        instance.font_size = self.size[1]//(12402/575)
        instance.text_size = instance.size

    def update_title_shade_font(self, instance, value):
        instance.font_size = self.size[1] // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-18/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)} #'center_x': self.title.pos_hint["center_x"] * (1-4/995) #'center_y': self.title.pos_hint["center_y"] * (1-1/24)

    def update_button_img (self, instance, value, pos):
        instance.size_hint = (268/399, 9/53)
        instance.pos_hint = {"center_x": 0.5, "center_y": 913/1378 - pos}
    def update_button_label(self, instance, value):
        instance.font_size = self.size[1] * 28/23 // (12402/575)  # Since the font of the button size 28 and the font of the title is 23
        instance.text_size = instance.size



    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_swap_cards(self, instance):
        print("Player chose: Swap Cards")
        # Add your swap cards logic here
        print(self.game_screen.size)
        self.game_screen.call_for_choose_player('swap')
    def on_look_at_card(self, instance):
        print("Player chose: Peek at Card")
        # Add your look at card logic here  # Hide sidebar after action
        self.game_screen.hide_all_sidebars()
        widget = self.game_screen.widgets_dict[self.player_ID]
        #Show action
        widget.show_action(2)
        widget.reveal_card()

        #After 3s, hide it
        Clock.schedule_once(widget.hide_card, 3 * self.game_screen.time_ratio)

        #Save to the history
        self.game_screen.app.game.history.append({"mode": 2, "player": self.player_ID})

        #Endturn
        Clock.schedule_once(self.game_screen.end_turn, 4* self.game_screen.time_ratio) #Set the time after all the action works

    def on_claim_role(self, instance):
        print("Player chose: Claim Role")
        # Add your claim role logic here
        self.game_screen.call_for_choose_char()

    def on_rollback_sidebar(self, instance):
        if self.game_screen.sidebar and self.game_screen.sidebar.parent:
            self.game_screen.layout.remove_widget(self.game_screen.sidebar)
            self.game_screen.sidebar = None
        if not self.rollback_again_btn_img.parent:
            self.game_screen.add_widget(self.rollback_again_btn_img)


    def on_rollback_again_sidebar(self, instance):
        self.game_screen.call_for_decision(self.player_ID)

        self.game_screen.remove_widget(self.rollback_again_btn_img)




    # def on_end_turn(self, instance):
    #     print("Player chose: End Turn")
    #     # Add your end turn logic here=  # Hide sidebar after action

class CharSelectingSidebar(FloatLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen , mode,  player_ID = 0, **kwargs):
        super().__init__(
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.mode = mode
        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.player_ID = player_ID

        # Take the general folder
        self.img_action_folder = os.path.join(os.path.dirname(__file__), "img_actions/sidebar")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        self.background_path = os.path.join(self.img_action_folder, "sidebar_background.png")
        print(self.background_path)
        self.background = Image(source=self.background_path, pos_hint={'center_x': 0.5, "center_y": 0.5},
                                size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        self.mask_revealed_path = os.path.join(self.img_action_folder, "mask_revealed.png")
        self.mask_revealed = Image(source = self.mask_revealed_path,
                                  pos_hint = {'center_x': 0.5, "center_y": 245/689},
                                  size_hint = (320/399,426/689),
                                   allow_stretch=True, keep_ratio=False, opacity = 0.59)
        self.add_widget(self.mask_revealed)

        self.mode_actions_dict = {
            "claim": char_selected
            # "usurper": self.execute_usurper,
            # "inquisitor": self.execute_inquisitor,
        }

        # Transparent-ish background

        self.title_action_dict = {
            "claim": "Show yourself, lord. Who hides beneath that gilded mask?"
        }
        # Title
        self.title = Label(text=self.title_action_dict[mode],
                           font_size=self.size[1] // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[192 / 255, 135 / 255, 74 / 255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 573 / 689},  ## ADJUST LATER
                           size_hint=(278 / 399, 126 / 689)
                           )
        print(self.title.pos_hint)
        self.title_shade = Label(text=self.title_action_dict[mode],
                                 font_size=self.size[1] // (12402 / 575),
                                 halign='center',
                                 valign='center',
                                 font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                 color=[116 / 255, 47 / 255, 6 / 255, 1],
                                 pos_hint={'center_x': self.title.pos_hint["center_x"] * (1 - 18 / 995),
                                           'center_y': self.title.pos_hint["center_y"] * (1 - 1 / 150)},
                                 ## ADJUST LATER
                                 size_hint=self.title.size_hint
                                 )
        self.title_shade.shade_of = self.title

        self.title.text_size = self.title.size

        self.title.bind(size=self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.add_widget(self.title_shade)
        self.add_widget(self.title)

        # Scroll
        scroll = ScrollView(size_hint=(109/133, 320/689), do_scroll_x=False, pos_hint = {"center_x": 0.5, "center_y": 304/689})

        # Add the layout grid
        layout = GridLayout(cols=1, spacing=17/689 * self.size[1],padding=[0,0,0,0], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'), size = self.update_spacing)

        img_folder = os.path.join(os.path.dirname(__file__), 'img_chars')
        for i in self.character_dict:
            path = os.path.join(img_folder, f"{self.character_dict[i].name}.png")
            img = ClickableImage(
                source=path,
                size_hint_y=None,
                height = 91 / 689 * self.size[1],
                allow_stretch=True,
                keep_ratio=False
            )
            print(path)
            img.bind(on_press=lambda instance, char_ID=i, player_ID = self.player_ID: self.mode_actions_dict[self.mode](instance, player_ID,char_ID, self.game_screen), size = self.update_button_height) # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
            # Add just-created widget into the grid layout
            layout.add_widget(img)

        # Add the whole grid layout into the scroll
        scroll.add_widget(layout)

        # Add the scroll to the total layout
        self.add_widget(scroll)

        # Roll back button
        self.rollback_btn_img = ClickableImage(
            size_hint=(61 / 399, 61 / 689),
            source=os.path.join(self.img_action_folder, "return_button_flip.png"),
            pos_hint={"center_x": 0.5, "center_y": 137 / 1378},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_btn_img.bind(on_press=self.on_rollback_sidebar)
        self.add_widget(self.rollback_btn_img)


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_title_font(self, instance, value):
        instance.font_size = self.size[1]//(12402/575)
        instance.text_size = instance.size

    def update_title_shade_font(self, instance, value):
        instance.font_size = self.size[1] // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-18/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)} #'center_x': self.title.pos_hint["center_x"] * (1-4/995) #'center_y': self.title.pos_hint["center_y"] * (1-1/24)

    def update_spacing(self, instance, value):
        instance.spacing = self.size[1] * 17/689

    def update_button_height(self, instance, value):
        instance.height = self.size[1] * 91 / 689

    def on_rollback_sidebar(self, instance):

        if self.game_screen.char_sidebar and self.game_screen.char_sidebar.parent:
            self.game_screen.layout.remove_widget(self.game_screen.char_sidebar)
            self.game_screen.char_sidebar = None

        if not self.game_screen.sidebar:
            self.game_screen.call_for_decision(self.player_ID)
class PlayerSelectingSidebar(FloatLayout):


    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen, mode, player_ID=0, **kwargs):  ###OOO Remove the default for player_ID for online mode
        super().__init__(
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)
        self.mode = mode
        self.game_screen = game_screen
        self.players_dict = self.game_screen.app.game.players_dict
        self.chars_dict = self.game_screen.app.game.chars_dict
        # self.label = f"{random.choice(self.game_screen.app.game.label_messages_dict[self.mode])}"
        self.player_ID = player_ID

        self.img_action_folder = os.path.join(os.path.dirname(__file__), r"img_actions/sidebar")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        self.mode_actions_dict = {
            "swap": self.execute_swap,
            "witch": self.execute_witch,
            "princess": self.execute_princess,
            #"joker": self.execute_joker,
        }
        self.mode_title_dict = {"swap": "A whispered invitation to dance… who shall receive it?",
                                "witch": "The charm is cast in silence… who shall bear its mark?",
                                "princess": "Should she raise her hand once more… who shall feel its grace?"}

        #Add background
        self.background_path = os.path.join(self.img_action_folder, "sidebar_background.png")
        print(self.background_path)
        self.background = Image(source=self.background_path, pos_hint={'center_x': 0.5, "center_y": 0.5},
                                size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)


        #Image of the selecting action
        self.title_image = Image(source = os.path.join(self.img_action_folder, f"{mode}.png"), size_hint = (86/133, 194/689),
                                 pos_hint = {"center_x":0.5, "center_y":19/23}, keep_ratio=False, allow_stretch=True, opacity = 0.59)
        self.add_widget(self.title_image)

        #Title of the selecting action
        self.title = Label(text=self.mode_title_dict[mode],
                           font_size=self.size[1] // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[192 / 255, 135 / 255, 74 / 255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 412/689},  ## ADJUST LATER
                           size_hint=(39/57, 126/689)
                           )
        self.title_shade = Label(text=self.mode_title_dict[mode],
                                 font_size=self.size[1] // (12402 / 575),
                                 halign='center',
                                 valign='center',
                                 font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                 color=[116 / 255, 47 / 255, 6 / 255, 1],
                                 pos_hint={'center_x': self.title.pos_hint["center_x"] * (1 - 18 / 995),
                                           'center_y': self.title.pos_hint["center_y"] * (1 - 1 / 150)},
                                 ## ADJUST LATER
                                 size_hint=self.title.size_hint
                                 )
        self.title_shade.shade_of = self.title
        self.title.text_size = self.title.size

        self.title.bind(size=self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.add_widget(self.title_shade)
        self.add_widget(self.title)

        # Scroll
        self.scroll = ScrollView(size_hint=(337/399, 190/689), do_scroll_x=False,  # 337
                                 pos_hint={'center_x': 0.5, "center_y": 240 / 689})

        # Create a list of buttons so that we can update all the size together
        self.scroll.list_buttons = []

        # Add the layout grid
        self.grid_layout = GridLayout(cols=1, spacing=18 / 689 * self.size[1], padding=[0, 0, 0, 0],
                                      size_hint_y=None)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'), size = self.update_spacing)

        for i in range(self.game_screen.player_num):
            if i != self.player_ID:  # Ensure that the player wont have a chance to swap with himself
                print(self.size, "mimimi")
                layout = FloatLayout(height=86/689 * self.size[1], size_hint_y=None)
                button_img = ClickableImage(
                    source=os.path.join(self.img_action_folder, "frame_listing.png"),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    keep_ratio=False,
                    allow_stretch=True,
                    size_hint_y=None,
                    height=layout.height,
                )
                layout.bind(size = self.update_button_height)
                button_img.bind(size = self.update_button_height)

                button_text = Label(
                    text=self.game_screen.app.game.players_dict[i].player_name,
                    font_size=self.size[1] // (12402 / 575),
                    color=[192 / 255, 135 / 255, 74 / 255, 1],
                    halign='center',
                    valign='center',
                    font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                    pos_hint={'center_x': 0.5, "center_y": 0.5},
                    size_hint=(1, 1)
                )
                button_text.text_size = button_text.size
                button_text.bind(size=self.update_title_font)

                button_img.bind(on_press=lambda instance, patient_ID=i: self.mode_actions_dict[self.mode](instance,
                                                                                                          patient_ID))  # We can still use the function like that, take the value and put (...) after it, we can safely sepecify the arguments put inside the function, like the self.mode_actions_dict[self.mode] just a reference, until with the () after it, it becomes real function run
                # Add just-created widget into the grid layout
                layout.add_widget(button_img)
                layout.add_widget(button_text)

                # Append the layout to the list
                self.scroll.list_buttons.append(layout)

                self.grid_layout.add_widget(layout)

        # Add the whole grid layout into the scroll
        self.scroll.add_widget(self.grid_layout)

        # Add all of them to the parent
        self.add_widget(self.scroll)


        # Roll back button
        self.rollback_btn_img = ClickableImage(
            size_hint=(61 / 399, 61 / 689),
            source=os.path.join(self.img_action_folder, "return_button_flip.png"),
            pos_hint={"center_x": 0.5, "center_y": 137 / 1378},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_btn_img.bind(on_press=self.on_rollback_sidebar)
        self.add_widget(self.rollback_btn_img)
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


    def update_title_font(self, instance, value):
        instance.font_size = self.size[1]//(12402/575)
        instance.text_size = instance.size

    def update_title_shade_font(self, instance, value):
        instance.font_size = self.size[1] // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-18/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)} #'center_x': self.title.pos_hint["center_x"] * (1-4/995) #'center_y': self.title.pos_hint["center_y"] * (1-1/24)
    def execute_swap(self, instance, patient_ID):
        self.game_screen.call_for_swap_or_not(self.player_ID, patient_ID)

    def execute_witch(self, instance, patient_ID):
        result = patient_ID
        Witch.execute(self.game_screen.app.game.players_dict[self.player_ID], result, self.game_screen.app.game, self.game_screen)

        self.game_screen.layout.remove_widget(self.game_screen.player_sidebar)
        self.game_screen.player_sidebar = None

    def execute_princess(self, instance, patient_ID):
        result = patient_ID
        Princess.execute(self.game_screen.app.game.players_dict[self.player_ID], result, self.game_screen.app.game, self.game_screen, "offline")

        self.game_screen.layout.remove_widget(self.game_screen.player_sidebar)
        self.game_screen.player_sidebar = None


    def update_button_height(self, instance, value):
        instance.height = self.size[1] * 86/689

    def update_spacing(self, instance,value):
        instance.spacing = 18 / 689 * self.size[1]

    def on_rollback_sidebar(self, instance):

        if self.game_screen.player_sidebar and self.game_screen.player_sidebar.parent:
            self.game_screen.layout.remove_widget(self.game_screen.player_sidebar)
            self.game_screen.player_sidebar = None

        if not self.game_screen.sidebar:
            self.game_screen.call_for_decision(self.player_ID)



class SwapOrNotSidebar(FloatLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])

    def __init__(self, game_screen, agent_ID, patient_ID, **kwargs):  ###OOO Remove the default for player_ID for online mode
        super().__init__(
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.label = "Do you want to swap actually?"
        self.agent_ID = agent_ID
        self.patient_ID = patient_ID

        self.img_action_folder = os.path.join(os.path.dirname(__file__), "img_actions\sidebar")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        # # Transparent-ish background
        # with self.canvas.before:
        #     Color(*self.background_color)
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        #
        # self.bind(size=self._update_rect, pos=self._update_rect)
        # Add background
        self.background_path = os.path.join(self.img_action_folder, "sidebar_background.png")
        self.background = Image(source=self.background_path, pos_hint={'center_x': 0.5, "center_y": 0.5},
                                size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        #Add the couple in the background
        self.background_couple_path = os.path.join(self.img_action_folder, "background_couple.png")
        self.background_couple = Image(source = self.background_couple_path, pos_hint={'center_x': 73/133, "center_y": 0.5}, size_hint = (1, 0.9), opacity = 0.41,allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_couple)
        # Title
        # Title of the selecting action
        self.title = Label(text="An alluring dance beneath hazy candlelight... shall their fates truly be entwined?",
                           font_size=self.size[1] // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[192 / 255, 135 / 255, 74 / 255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 491 / 689},  ## ADJUST LATER
                           size_hint=(52 / 57, 126 / 689)
                           )
        self.title_shade = Label(text="An alluring dance beneath hazy candlelight... shall their fates truly be entwined?",
                                 font_size=self.size[1] // (12402 / 575),
                                 halign='center',
                                 valign='center',
                                 font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                 color=[116 / 255, 47 / 255, 6 / 255, 1],
                                 pos_hint={'center_x': self.title.pos_hint["center_x"] * (1 - 18 / 995),
                                           'center_y': self.title.pos_hint["center_y"] * (1 - 1 / 150)},
                                 ## ADJUST LATER
                                 size_hint=self.title.size_hint
                                 )
        self.title_shade.shade_of = self.title
        self.title.text_size = self.title.size

        self.title.bind(size=self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.add_widget(self.title_shade)
        self.add_widget(self.title)
        # Scroll
        # scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        #
        # # Add the layout grid
        # layout = GridLayout(cols=1, spacing=20, padding=[10, 10, 10, 10], size_hint_y=None)
        # layout.bind(minimum_height=layout.setter('height'))
        #
        # for i in ["yes", "no"]:
        #     button = Button(
        #         text=i,
        #         font_size=20,
        #         size_hint_y=None,  # remove size_hint_y
        #         height=60  # set a fixed height
        #     )
        #
        #     button.bind(on_press=lambda instance, decision=i: self.swap_decided(instance,
        #                                                                                                    self.agent_ID,
        #                                                                                                    self.patient_ID,
        #                                                                                                    decision,
        #                                                                                                    self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
        #     # Add just-created widget into the grid layout
        #     layout.add_widget(button)
        #
        # # Add the whole grid layout into the scroll
        # scroll.add_widget(layout)
        #
        # # Add the scroll to the total layout
        # self.add_widget(scroll)

        #For the Yes button
        self.yes_button = FloatLayout(
                                            pos_hint={'center_x': 0.5, "center_y": 352 / 689},
                                            size_hint=(337 / 399, 86 / 689)
                                        )
        self.yes_button_img = ClickableImage(source = os.path.join(self.img_action_folder, "frame_listing.png"),
                                             pos_hint = {'center_x': 0.5, "center_y": 0.5},
                                             size_hint = (1,1),
                                             allow_stretch = True,
                                             keep_ratio = False)
        self.yes_button_img.bind(on_press=lambda instance, decision="yes": self.swap_decided(instance,
                                                                                       self.agent_ID,
                                                                                       self.patient_ID,
                                                                                       decision,
                                                                                       self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
        self.yes_button_text = Label(text="Yes",
                                     font_size=self.size[1] // (12402 / 575),
                                     halign='center',
                                     valign='center',
                                     font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                     color=[192 / 255, 135 / 255, 74 / 255, 1],
                                     pos_hint={'center_x': 0.5, "center_y": 0.5},  ## ADJUST LATER
                                     size_hint=(1,1)
        )

        self.yes_button_text.bind(size=self.update_title_font)

        self.yes_button.add_widget(self.yes_button_img)
        self.yes_button.add_widget(self.yes_button_text)

        self.add_widget(self.yes_button)


        #For the no button
        self.no_button = FloatLayout(
            pos_hint={'center_x': 0.5, "center_y": 227 / 689},
            size_hint=(337 / 399, 86 / 689)
        )
        self.no_button_img = ClickableImage(source=os.path.join(self.img_action_folder, "frame_listing.png"),
                                             pos_hint={'center_x': 0.5, "center_y": 0.5},
                                             size_hint=(1, 1),
                                             allow_stretch=True,
                                             keep_ratio=False)
        self.no_button_img.bind(on_press=lambda instance, decision="yes": self.swap_decided(instance,
                                                                                             self.agent_ID,
                                                                                             self.patient_ID,
                                                                                             decision,
                                                                                             self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
        self.no_button_text = Label(text="No",
                                     font_size=self.size[1] // (12402 / 575),
                                     halign='center',
                                     valign='center',
                                     font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                     color=[192 / 255, 135 / 255, 74 / 255, 1],
                                     pos_hint={'center_x': 0.5, "center_y": 0.5},  ## ADJUST LATER
                                     size_hint=(1, 1)
                                     )

        self.no_button_text.bind(size=self.update_title_font)

        self.no_button.add_widget(self.no_button_img)
        self.no_button.add_widget(self.no_button_text)

        self.add_widget(self.no_button)

        # Roll back button
        self.rollback_btn_img = ClickableImage(
            size_hint=(61 / 399, 61 / 689),
            source=os.path.join(self.img_action_folder, "return_button_flip.png"),
            pos_hint={"center_x": 0.5, "center_y": 137 / 1378},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_btn_img.bind(on_press=self.on_rollback_sidebar)
        self.add_widget(self.rollback_btn_img)




    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    def update_title_font(self, instance, value):
        instance.font_size = self.size[1]//(12402/575)
        instance.text_size = instance.size

    def update_title_shade_font(self, instance, value):
        instance.font_size = self.size[1] // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-18/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)} #'center_x': self.title.pos_hint["center_x"] * (1-4/995) #'center_y': self.title.pos_hint["center_y"] * (1-1/24)

    ### Build Idea: Create the swap then we build the selected for each role like Witch, Inquisitor
    def swap_decided(self, instance, agent_ID, patient_ID, decision, game_screen):

        #Hide sidebars, update actions UI
        game_screen.hide_all_sidebars()
        game_screen.widgets_dict[agent_ID].show_action(0, patient_ID)

        swap(agent_ID, patient_ID, decision, game_screen)

    def on_rollback_sidebar(self, instance):

        if self.game_screen.swap_or_not_sidebar and self.game_screen.swap_or_not_sidebar.parent:
            self.game_screen.layout.remove_widget(self.game_screen.swap_or_not_sidebar)
            self.game_screen.swap_or_not_sidebar = None

        if not self.game_screen.sidebar:
            self.game_screen.call_for_choose_player("swap", "rollback")

class BlockSelectingSidebar(FloatLayout):
    # background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen, first_ID, role_ID, player_ID=0, **kwargs): ###OOO Remove the default for player_ID for online mode
        super().__init__(
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.label = f"Are you the real {self.game_screen.app.game.chars_dict[role_ID].name}?"
        self.player_ID = player_ID

        self.img_action_folder = os.path.join(os.path.dirname(__file__), "img_actions\sidebar")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        #This is to start the next block turn
        self.first_ID = first_ID
        self.role_ID = role_ID

        # Add background
        self.background_path = os.path.join(self.img_action_folder, "sidebar_background.png")
        self.background = Image(source=self.background_path, pos_hint={'center_x': 0.5, "center_y": 0.5},
                                size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Add the couple in the background
        self.broken_mask_path = os.path.join(self.img_action_folder, "broken_mask.png")
        self.broken_mask = Image(source=self.broken_mask_path,
                                       pos_hint={'center_x': 0.5, "center_y": 237/689}, size_hint=(347/399, 6/13),
                                       opacity=0.23, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.broken_mask)

        # Title
        # Title
        # Title of the selecting action
        self.title = Label(text=f"Someone dares to unveil the secret as The [color=FFD966]{self.game_screen.app.game.chars_dict[self.role_ID].name.capitalize()}[/color]… But beneath it—truth, or yet another mask? Noble one, do you possess the courage to step forward and challenge it?",
                           font_size=self.size[1] // (12402 / 575),
                           halign='center',
                           valign='center',
                           font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                           color=[192 / 255, 135 / 255, 74 / 255, 1],
                           pos_hint={'center_x': 0.5, "center_y": 1019/1378},  ## ADJUST LATER
                           size_hint=(50 / 57, 281 / 689),
                           markup = True
                           )
        self.title_shade = Label(
            text=f"Someone dares to unveil the secret as The {self.game_screen.app.game.chars_dict[self.role_ID].name.capitalize()}… But beneath it—truth, or yet another mask? Noble one, do you possess the courage to step forward and challenge it?",
            font_size=self.size[1] // (12402 / 575),
            halign='center',
            valign='center',
            font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
            color=[116 / 255, 47 / 255, 6 / 255, 1],
            pos_hint={'center_x': self.title.pos_hint["center_x"] * (1 - 18 / 995),
                      'center_y': self.title.pos_hint["center_y"] * (1 - 1 / 150)},
            ## ADJUST LATER
            size_hint=self.title.size_hint
            )
        self.title_shade.shade_of = self.title
        self.title.text_size = self.title.size

        self.title.bind(size=self.update_title_font)
        self.title_shade.bind(size=self.update_title_shade_font)

        self.add_widget(self.title_shade)
        self.add_widget(self.title)


        #Yes button
        self.yes_button = FloatLayout(
            pos_hint={'center_x': 0.5, "center_y": 302 / 689},
            size_hint=(337 / 399, 86 / 689)
        )
        self.yes_button_img = ClickableImage(source=os.path.join(self.img_action_folder, "frame_listing.png"),
                                             pos_hint={'center_x': 0.5, "center_y": 0.5},
                                             size_hint=(1, 1),
                                             allow_stretch=True,
                                             keep_ratio=False)
        self.yes_button_img.bind(on_press=lambda instance, decision="yes", player_ID=self.player_ID: self.block_decided(instance,
                                                                                                       self.first_ID,
                                                                                                       self.role_ID,
                                                                                                       player_ID,
                                                                                                       decision,
                                                                                                       self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
        self.yes_button_text = Label(text="Yes",
                                     font_size=self.size[1] // (12402 / 575),
                                     halign='center',
                                     valign='center',
                                     font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                     color=[192 / 255, 135 / 255, 74 / 255, 1],
                                     pos_hint={'center_x': 0.5, "center_y": 0.5},  ## ADJUST LATER
                                     size_hint=(1, 1)
                                     )

        self.yes_button_text.bind(size=self.update_title_font)

        self.yes_button.add_widget(self.yes_button_img)
        self.yes_button.add_widget(self.yes_button_text)

        self.add_widget(self.yes_button)

        # For the no button
        self.no_button = FloatLayout(
            pos_hint={'center_x': 0.5, "center_y": 191 / 689},
            size_hint=(337 / 399, 86 / 689)
        )
        self.no_button_img = ClickableImage(source=os.path.join(self.img_action_folder, "frame_listing.png"),
                                            pos_hint={'center_x': 0.5, "center_y": 0.5},
                                            size_hint=(1, 1),
                                            allow_stretch=True,
                                            keep_ratio=False)
        self.no_button_img.bind(
            on_press=lambda instance, decision="no", player_ID=self.player_ID: self.block_decided(instance,
                                                                                                   self.first_ID,
                                                                                                   self.role_ID,
                                                                                                   player_ID,
                                                                                                   decision,
                                                                                                   self.game_screen))
        self.no_button_text = Label(text="No",
                                    font_size=self.size[1] // (12402 / 575),
                                    halign='center',
                                    valign='center',
                                    font_name=os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
                                    color=[192 / 255, 135 / 255, 74 / 255, 1],
                                    pos_hint={'center_x': 0.5, "center_y": 0.5},  ## ADJUST LATER
                                    size_hint=(1, 1)
                                    )

        self.no_button_text.bind(size=self.update_title_font)

        self.no_button.add_widget(self.no_button_img)
        self.no_button.add_widget(self.no_button_text)

        self.add_widget(self.no_button)

        # Roll back button
        self.rollback_btn_img = ClickableImage(
            size_hint=(61 / 399, 61 / 689),
            source=os.path.join(self.img_action_folder, "return_button_flip.png"),
            pos_hint={"center_x": 0.5, "center_y": 137 / 1378},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_btn_img.bind(on_press=self.on_rollback_sidebar)
        self.add_widget(self.rollback_btn_img)

        # Rollback again button
        self.rollback_again_btn_img = ClickableImage(
            size_hint=(61 / 1333, 61 / 689),
            source=os.path.join(self.img_action_folder, "return_button.png"),
            pos_hint={"center_x": 1 - 99 / 1378, "center_y": 0.5},
            keep_ratio=False,
            allow_stretch=True)

        self.rollback_again_btn_img.bind(on_press=self.on_rollback_again_sidebar)


        # for i in ["yes", "no"]:
        #     button = Button(
        #         text=i,
        #         font_size=20,
        #         size_hint_y=None,  # remove size_hint_y
        #         height=60  # set a fixed height
        #     )
        #
        #     button.bind(on_press=lambda instance, decision = i, player_ID=self.player_ID: self.block_decided(instance,
        #                                                                                                     self.first_ID,
        #                                                                                                     self.role_ID,
        #                                                                                                     player_ID,
        #                                                                                                     decision,
        #                                                                                                     self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
        #     # Add just-created widget into the grid layout
        #     layout.add_widget(button)
        #
        # # Add the whole grid layout into the scroll
        # scroll.add_widget(layout)
        #
        # # Add the scroll to the total layout
        # self.add_widget(scroll)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    ### Build Idea: Create the swap then we build the selected for each role like Witch, Inquisitor

    def update_title_font(self, instance, value):
        instance.font_size = self.size[1]//(12402/575)
        instance.text_size = instance.size

    def update_title_shade_font(self, instance, value):
        instance.font_size = self.size[1] // (12402 / 575)
        instance.text_size = instance.size
        instance.pos_hint = {'center_x': instance.shade_of.pos_hint["center_x"] * (1-18/995), 'center_y': instance.shade_of.pos_hint["center_y"] * (1-1/150)} #'center_x': self.title.pos_hint["center_x"] * (1-4/995) #'center_y': self.title.pos_hint["center_y"] * (1-1/24)
    def block_decided (self, instance, first_ID, role_ID, player_ID, decision, game_screen ):

        game_screen.app.game.decide_dict[decision].append(player_ID)

        #Hide all sidebars, update UI actions widget
        game_screen.hide_all_sidebars()
        game_screen.widgets_dict[player_ID].show_action(3, decision, first_ID, role_ID)

    def on_rollback_sidebar(self, instance):

        if self.game_screen.block_sidebar and self.game_screen.block_sidebar.parent:
            self.game_screen.layout.remove_widget(self.game_screen.block_sidebar)
            self.game_screen.block_sidebar = None

        if not self.rollback_again_btn_img.parent:
            self.game_screen.add_widget(self.rollback_again_btn_img)

    def on_rollback_again_sidebar(self, instance):
        self.game_screen.call_for_block(self.first_ID, self.role_ID)

        self.game_screen.remove_widget(self.rollback_again_btn_img)


class PlayerWidget(BoxLayout):
    def __init__(self, game_screen,player, position, **kwargs):
        super().__init__(orientation='vertical', size_hint=(0.15, 9/52), **kwargs) # (0.13, 0.15)

        # Define the folders to get the general, the card images and the action images
        self.img_card_folder = os.path.join(os.path.dirname(__file__), 'img_cards')
        self.img_action_folder = os.path.join(os.path.dirname(__file__), 'img_actions')
        self.img_general_folder = os.path.join(os.path.dirname(__file__), "img_general")
        self.font_folder = os.path.join(os.path.dirname(__file__), "fonts")

        #Take the position side of the bubble_chat
        self.position = position

        #Initialize the bubble_chat
        self.bubble_chat = None
        if self.position == "top":
            self.bubble_chat_hint_x = self.pos_hint["center_x"]
            self.bubble_chat_hint_y = self.pos_hint["center_y"] - (167/206) * self.size_hint[1]
            self.bubble_chat_size_hint_x = self.size_hint[0] * (118/87)
            self.bubble_chat_size_hint_y = self.size_hint[1] * (46/103)

        elif self.position == "bottom":
            self.bubble_chat_hint_x = self.pos_hint["center_x"]
            self.bubble_chat_hint_y = self.pos_hint["center_y"] + (167/206) * self.size_hint[1]
            self.bubble_chat_size_hint_x = self.size_hint[0] * (118/87)
            self.bubble_chat_size_hint_y = self.size_hint[1] * (46/103)


        elif self.position == "left":
            self.bubble_chat_hint_x = self.pos_hint["center_x"] - (107/87) * self.size_hint[0]
            self.bubble_chat_hint_y = self.pos_hint["center_y"] + (65/206) * self.size_hint[1]
            self.bubble_chat_size_hint_x = self.size_hint[0] * (40/29)
            self.bubble_chat_size_hint_y = self.size_hint[1] * (42/103)

        elif self.position == "right":
            self.bubble_chat_hint_x = self.pos_hint["center_x"] + (107 / 87) * self.size_hint[0]
            self.bubble_chat_hint_y = self.pos_hint["center_y"] + (65 / 206) * self.size_hint[1]
            self.bubble_chat_size_hint_x = self.size_hint[0] * (40 / 29)
            self.bubble_chat_size_hint_y = self.size_hint[1] * (42 / 103)

        self.bubble_chat_path = os.path.join(self.img_action_folder, f"bubble_chat_{self.position}.png")


        #Initialize the object to send
        self.object = None




        #For the size of the font
        # def adjust_font_size(label, size, ratio):
        #     label.font_size = size[1] * ratio  # Set font to 50% of label height

        #A float layout is to make sure that the background is behind the content
        self.layout = FloatLayout()

        self.background = Image(
            source=os.path.join(self.img_general_folder, 'player_widget_background_framed.png'),
            # <- Replace with your image path
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.layout.add_widget(self.background)

        #Create a main box layout to manage the information inside it
        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1,1), pos_hint={'x': 0, 'y': 0}, padding=10)

        #Attributize the game_screen and the chars_dict (which can be used in the call later)
        self.game_screen = game_screen
        self.chars_dict = self.game_screen.app.game.chars_dict

        self.information_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        # self.action_layout = BoxLayout(orientation='horizontal', spacing = 10,  size_hint=(1,0.25))

        #Define the folders to get the card images and the action images
        self.img_card_folder = os.path.join(os.path.dirname(__file__), 'img_cards')
        self.img_action_folder = os.path.join(os.path.dirname(__file__), 'img_actions')

        #Define the player
        self.player = player

        #Take the cardback
        self.card = os.path.join(self.img_card_folder,f"card_back.png") # Filename of the card image

        self.card_image = Image(source=self.card, size_hint=(0.5, 0.96),pos_hint = {"center_y": 0.5, "x": 0}, allow_stretch=True,keep_ratio=False)
        #self.action_image = Image(source=self.action, size_hint = (1,1))
        self.information_layout.add_widget(self.card_image)



        #Create layout of other information
        self.layout_right = BoxLayout(orientation='vertical', spacing=0, size_hint=(0.6, 1))

        #This is for the label of the role, which is red in color
        font_size = Window.system_size[1] * self.size_hint[1] * 0.22
        self.label_role = Label(
            markup = True,
            text = f"[color=8E1616]Masked[/color]", #{player.get_card().name.capitalize()}
            size_hint=(1, 0.05),
            halign='center',
            valign='top',
            color = [0, 0, 0, 1],
            font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
            font_size = font_size
        )

        self.label_id = Label(
            text = str(player.ID),
            size_hint=(1, 0.05),
            halign='center',
            valign='top',
            color = [0, 0, 0, 1]
        )
        # self.label_id.bind(size = lambda label, size, ratio=0.8: adjust_font_size(label, size, ratio))

        self.label_name = Label(
            text=player.player_name,
            size_hint=(1, 0.05),
            halign='center',
            valign='top',
            color = [0, 0, 0, 1]
        )
        # self.label_name.bind(size=lambda label, size, ratio=0.8: adjust_font_size(label, size, ratio))


        # Enable text wrapping
        self.label_name.bind(size=self.label_name.setter('text_size'))
        self.layout_right.add_widget(self.label_role)
        self.layout_right.add_widget(self.label_id)
        self.layout_right.add_widget(self.label_name)

        #This is for the revealed
        self.label_revealed = Label(text=f"{player.revealed} turn(s)", size_hint=(1, 0.05), color = [0, 0, 0, 1],
                                 pos_hint={'center_x': 0.5, 'center_y': 0.2})
        # self.label_revealed.bind(size = lambda label, size, ratio = 0.8: adjust_font_size(label,size,ratio))
        self.layout_right.add_widget(self.label_revealed)
        #This is for the money
        self.label_money = Label(text=f"{player.money}g", size_hint=(1, 0.05),color = [0, 0, 0, 1], pos_hint = {'center_x': 0.5, 'center_y': 0.1})
        # self.label_money.bind(size=lambda label, size, ratio=0.8: adjust_font_size(label, size, ratio))
        self.layout_right.add_widget(self.label_money)


        #Add all to the information's widget
        self.information_layout.add_widget(self.layout_right)

        #Add the information and the action widget to the player widget
        # self.main_layout.add_widget(self.action_layout)
        self.main_layout.add_widget(self.information_layout)

        #Add the main contain into the float layout
        self.layout.add_widget(self.main_layout)

        #Add all the float layout to the biggest widget
        self.add_widget(self.layout)



        # #Add the hand mask normal and hand mask rotated to the specify position
        # self.hand_mask_normal_path = os.path.join(self.img_action_folder, "img_actions/big_mask4_cropped.png")
        # size_hint_x = self.size_hint[0] * 440/591
        # size_hint_y = self.size_hint[1] * 183/190
        # hint_x = self.pos_hint["center_x"] - self.size_hint[0] * 377/1182
        # hint_y = self.pos_hint["center_y"] + self.size_hint[1] * 18/95
        # self.hand_mask_normal = Image(source=self.hand_mask_normal_path, size_hint=(size_hint_x, size_hint_y),pos_hint = {"center_x": hint_x, "center_y": hint_y}, allow_stretch=True,keep_ratio=False)
        #
        # self.parent.add_widget(self.hand_mask_normal)

    def init_claim(self, **kwargs):
        # Set up the animation for the swap, the claim, the peek
        self.claim_anim_in = Animation(opacity=1, duration=0.6 * self.game_screen.time_ratio)
        self.claim_anim_out = Animation(opacity=0, duration=0.6 * self.game_screen.time_ratio)
        # Add the hand mask normal to the specify position
        self.hand_mask_normal_path = os.path.join(self.img_action_folder, "hand_mask_normal.png")
        size_hint_x = self.size_hint[0] * 440 / 591
        size_hint_y = self.size_hint[1] * 183 / 190
        hint_x = self.pos_hint["center_x"] - self.size_hint[0] * 377 / 1182
        hint_y = self.pos_hint["center_y"] + self.size_hint[1] * 18 / 95
        self.hand_mask_normal = Image(source=self.hand_mask_normal_path, size_hint=(size_hint_x, size_hint_y),
                                      pos_hint={"center_x": hint_x, "center_y": hint_y}, allow_stretch=True,
                                      keep_ratio=False, opacity = 0)

        self.parent.add_widget(self.hand_mask_normal)

        # Add the hand mask rotated to the specify position
        self.hand_mask_rotated_path = os.path.join(self.img_action_folder, "hand_mask_rotated.png")
        size_hint_x = self.size_hint[0] * 364/591
        size_hint_y = self.size_hint[1] * 451/380
        hint_x = self.pos_hint["center_x"] - self.size_hint[0] * 509/1182
        hint_y = self.pos_hint["center_y"] + self.size_hint[1] * 211/760
        self.hand_mask_rotated = Image(source=self.hand_mask_rotated_path, size_hint=(size_hint_x, size_hint_y),
                                      pos_hint={"center_x": hint_x, "center_y": hint_y}, allow_stretch=True,
                                      keep_ratio=False, opacity = 0)

        self.parent.add_widget(self.hand_mask_rotated)

    def reveal_card(self, *args):
        '''
        The args is to support for the role want to reveal, to make the affect to know which role is being claimed
        '''
        if len(args) == 0:
            self.card = os.path.join(self.img_card_folder,f"{self.player.get_card().name}.png")
            self.label_role.text = f"[color=8E1616]{self.player.get_card().name.capitalize()}[/color]"
        else:
            role_ID = args[0]
            self.card = os.path.join(self.img_card_folder,f"{self.game_screen.app.game.chars_dict[role_ID].name}.png")

        # Remove old texture from cache
        Cache.remove('kv.image', self.card + '|False|0')
        Cache.remove('kv.texture', self.card + '|False|0')

        self.card_image.source = self.card
        self.card_image.opacity = 1
        if len(args) == 1:
            self.card_image.opacity = 0.5
        self.card_image.reload()  # Refresh the image
        ###Nhớ reveal trong 1 khoảng tgian

    def hide_card(self, dt):
        self.card = os.path.join(self.img_card_folder,"card_back.png")
        self.label_role.text = f"[color=8E1616]Masked[/color]"

        # Remove old texture from cache
        Cache.remove('kv.image', self.card + '|False|0')
        Cache.remove('kv.texture', self.card + '|False|0')

        self.card_image.source = self.card
        self.card_image.opacity = 1
        self.card_image.reload()  # Refresh the image

    def update_money(self):
        self.label_money.text = f"{self.player.money}g"

    def update_revealed(self):
        self.label_revealed.text = f"{self.player.revealed} turn(s)"

    def show_action(self, action_id, *args):
        '''

        action_id types:
        0: swap *args is the patient_ID
        1: claim: *args is the role_ID
        2: peek
        3: block *args "yes" or "no", the first_ID, and the role_ID

        For important information, we all use the dark red 8E1616 to highlight it
        '''
        if action_id == 0: #this is for the swap option

            # Set up the patient, the widget
            patient_ID = args[0]

            # self.pop_bubble_chat((f"Shall we dance, "
            #                       f"[color=8E1616]Player {patient_ID}[/color]?"))
            self.pop_bubble_chat((f"Shall we dance, "
                                  f"[color=8E1616]Player {self.game_screen.app.game.players_dict[patient_ID].player_name}[/color]"
                                  ))
            self.give(patient_ID, "love_letter") #This takes more than 1.5s to finish it



        elif action_id == 1: #this is for the claim option
            # Show the action bubble chat
            role_ID_claim = args[0]
            self.pop_bubble_chat((f"I'm the "
                                 f"[color=8E1616]{self.game_screen.app.game.chars_dict[role_ID_claim].name.capitalize()}[/color]!"))
            #Show the hand with the mask
            self.claim_anim_in.start(self.hand_mask_normal)
            # Show the card vaguely
            self.reveal_card(role_ID_claim)


        elif action_id == 2: #this is for the peek option
            #Pop the bubble chat
            self.pop_bubble_chat((f"A glimpse beneath the veil..."))
            #Set up the peek widget
            peek_path = os.path.join(self.img_action_folder, "eyes.png")
            self.peek_widget = Image(source=peek_path, size_hint=(0.5, 1),pos_hint = {"x":0, "y":0}, keep_ratio = False, allow_stretch = True, opacity = 0.6)

            #Add widget to the action_layout
            self.layout.add_widget(self.peek_widget)
        elif action_id == 3: #this is for the block option
            decision = args[0]
            first_ID = args[1]
            role_ID = args[2]

            if decision == "yes":
                self.claim_anim_in.start(self.hand_mask_normal)
                # self.pop_bubble_chat(f"Not you! I'm the actual one!")
                self.pop_bubble_chat(f"[color=8E1616]Treachery![/color] I'm the true one!")

            else:
                self.pop_bubble_chat((
                    f"As you say, " # The parts without the color specified by markup will be in the font color of the label, here it will be black
                    f"[color=8E1616]{self.game_screen.app.game.chars_dict[role_ID].name.capitalize()}[/color]."))


            #Continue the block turn
            Clock.schedule_once(lambda dt: self.game_screen.block_turn(dt, first_ID, role_ID), 2 * self.game_screen.time_ratio)

    def pop_bubble_chat(self, text):
        print(f"======{self.parent.size}=======")
        # font_size = Window.system_size[1] * self.size_hint[1] * 0.22
        if self.bubble_chat == None:
            # self.bubble_chat = Image(source = self.bubble_chat_path,size_hint = (self.bubble_chat_size_hint_x, self.bubble_chat_size_hint_y), pos_hint = {"center_x": self.bubble_chat_hint_x, "center_y": self.bubble_chat_hint_y}) #text = text, bubble_chat_path= self.bubble_chat_path)
            self.bubble_chat = BubbleChat(size_hint = (self.bubble_chat_size_hint_x, self.bubble_chat_size_hint_y), pos_hint = {"center_x": self.bubble_chat_hint_x, "center_y": self.bubble_chat_hint_y}, text = text, bubble_chat_path= self.bubble_chat_path, position = self.position) #font_size = font_size
        if self.bubble_chat.parent == None:
            self.parent.add_widget(self.bubble_chat)
        print(f"bubble_chat added! Content: {text}")

    def give (self, patient_ID, mode): #Note that the pos, and the size of x and y in pixel are super trustworthy, while the size of the window system width height is not
        patient_widget = self.game_screen.widgets_dict[patient_ID]

        size_hint_x_letter = patient_widget.size_hint[0] * 21/58
        size_hint_y_letter = patient_widget.size_hint[1] * 41/103

        old_left_edge = self.pos[0] + self.size[0]*( 1 - 21/58)//2
        old_bottom_edge = self.pos[1] + self.size[1]*( 1 - 41/103)//2


        new_left_edge = patient_widget.pos[0] + patient_widget.size[0]*( 1 - 21/58)//2
        new_bottom_edge = patient_widget.pos[1] + patient_widget.size[1]*( 1 - 41/103)//2

        #Let the letter appear
        if self.object == None:
            self.object = Image(source = os.path.join( self.img_action_folder,f"{mode}.png"), size_hint = (size_hint_x_letter, size_hint_y_letter), pos = (old_left_edge, old_bottom_edge))
        if self.object.parent == None:
            self.parent.add_widget(self.object)

        #Give it to the patient
        move_anim = Animation(pos = (new_left_edge, new_bottom_edge), duration = 1.6 * self.game_screen.time_ratio, t='out_quad')
        move_anim.start(self.object)


    def clear_action(self, dt):
        self.action_layout.clear_widgets()

class BubbleChat(BoxLayout):
    def __init__(self, text, bubble_chat_path, position,  **kwargs):
        super().__init__(**kwargs)

        self.main_layout = FloatLayout(size_hint = (1,1))
        self.font_folder = os.path.join(os.path.dirname(__file__),"fonts")

        # Background image (your speech bubble)
        self.bubble = Image(
            source=bubble_chat_path,  # your image
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_layout.add_widget(self.bubble)

        if position == "right":
            self.text_pos_hint = {'x': 1/48, 'center_y': 0.5}
            self.text_size_hint = (47/48,1)

        elif position == "left":
            self.text_pos_hint = {'x': 0, 'center_y': 0.5}
            self.text_size_hint = (47 / 48, 1)

        elif position == "bottom":
            self.text_pos_hint = {'center_x': 0.5, 'y': 5/46}
            self.text_size_hint = (1, 21/23)
        elif position == "top":
            self.text_pos_hint = {'center_x': 0.5, 'y': 0}
            self.text_size_hint = (1, 21/23)
        # Text on top
        self.label = Label(
            markup = True,
            text=text,
            font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),  # black text
            size_hint=self.text_size_hint,
            pos_hint=self.text_pos_hint,
            shorten = False, #False

            # split_str=''
            # line_height = 1.5
            # font_size = self.font_size
        )


        self.label.font_size = self.label.size[1] * 0.37
        self.label.text_size = self.label.size
        # self.label.text_size = (self.label.width, None)
        # self.label.bind(size=lambda inst, size: setattr(inst, 'text_size', (size[0], None)))
        # self.label.line_height = self.label.size[1]*0.013 # Using this to customize the line spacing is kinda good but it will affect the alignment of the text somehow
        self.label.bind(size = self.update_font_size)

        # #Draw a white rectangle to test the size of the rectangle
        # with self.label.canvas.before:
        #     Color(1, 1, 1, 1)
        #     self._bg_rect = Rectangle(pos = self.label.pos, size=self.label.size)
        # # Keep the rectangle in sync at runtime
        # self.label.bind(pos=self._update_bg, size=self._update_bg)

        self.label.bind(size=self.label.setter('text_size'))  # Enable wrapping
        self.main_layout.add_widget(self.label)

        print(self.label.size)

        self.add_widget(self.main_layout)

    def update_font_size(self, instance, value):
        self.label.font_size = instance.size[1] * 0.37
        # self.label.line_height = instance.size[1]*0.013
        self.label.text_size = value  # (width, height)
        # self.label.text_size = (value[0], value[1]) # font_size specifies how large the text itself is, while texture_size refers to the actual rendered size of that text, including wrapping, line breaks, and visual padding.
        # self.label.height = self.label.texture_size[1]

    # def _update_bg(self, instance, value):
    #     self._bg_rect.pos = instance.pos
    #     self._bg_rect.size = instance.size

class CourtWidget(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', spacing=0, size_hint=(1, 0.15), pos_hint={"center_x":0.5, "center_y":0.5})
        self.app = app
        self.font_folder = os.path.join(os.path.dirname(__file__),"fonts")

        self.court_name = Label(text="Court", font_size=0.3 * self.size[1], size_hint=(1, 0.3), font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"), color = (0,0,0,1)) #### 35
        self.court_money = Label(text = f"{self.app.game.court}g", font_size=0.7 * self.size[1], size_hint=(1, 0.3), font_name = os.path.join(self.font_folder, "UnifrakturCook-Bold.ttf"), color = (0,0,0,1)) #### 60
        self.bind(size = self.update_font_size)
        self.add_widget(self.court_name)
        self.add_widget(self.court_money)

    def update_money(self):
        new_gold = self.app.game.court
        self.court_money.text = f"{new_gold}g"

    def update_font_size(self, instance, value):
        self.court_name.font_size = 0.3 * instance.size[1]
        self.court_money.font_size = 0.7 * instance.size[1]


class PauseOverlay(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.pos_hint = {'x': 0, 'y': 0}
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)  # semi-transparent black
            Rectangle(pos=self.pos, size=self.size)

        # Pause label
        self.add_widget(Label(text="Paused", font_size=40, pos_hint={"center_x": 0.5, "center_y": 0.6}))

        # Resume button
        resume_btn = Button(text="Resume", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.4})
        resume_btn.bind(on_press=self.resume_game)
        self.add_widget(resume_btn)

    def resume_game(self, *args):
        self.parent.play_turn()
        self.parent.remove_widget(self)