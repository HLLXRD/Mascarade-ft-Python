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

import os
import random

from .player_and_action import char_selected, swap



class ClickableImage(ButtonBehavior, Image):
    pass

class ActionSidebar(BoxLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 0.9])

    def __init__(self, game_screen, player_ID, **kwargs):
        super().__init__(orientation='vertical',
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.game_screen = game_screen
        self.player_ID = player_ID
        self.player = self.game_screen.app.game.players_dict[self.player_ID]

        # Transparent-ish background
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text="Your Turn", font_size=24, size_hint=(1, 0.1))
        self.add_widget(title)

        # Action buttons
        swap_btn = Button(text="Swap Cards", font_size=18, size_hint=(1, 0.15))
        swap_btn.bind(on_press=self.on_swap_cards)
        self.add_widget(swap_btn)

        look_btn = Button(text="Peek at Card", font_size=18, size_hint=(1, 0.15))
        look_btn.bind(on_press=self.on_look_at_card)
        self.add_widget(look_btn)

        # If the revealed is 0 and the total turns played are more than 2, show the claim
        if self.player.revealed == 0 and self.game_screen.play_turn_index > 2:
            claim_btn = Button(text="Claim Role", font_size=18, size_hint=(1, 0.15))
            claim_btn.bind(on_press=self.on_claim_role)
            self.add_widget(claim_btn)

        # Spacer
        self.add_widget(Label(text="", size_hint=(1, 0.3)))

        # # End turn button
        # end_turn_btn = Button(text="End Turn", font_size=20, size_hint=(1, 0.15))
        # end_turn_btn.bind(on_press=self.on_end_turn)
        # self.add_widget(end_turn_btn)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_swap_cards(self, instance):
        print("Player chose: Swap Cards")
        # Add your swap cards logic here
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
        Clock.schedule_once(widget.hide_card, 3)

        #Save to the history
        self.game_screen.app.game.history.append({"mode": 2, "player": self.player_ID})

        #Endturn
        Clock.schedule_once(self.game_screen.end_turn, 4) #Set the time after all the action works

    def on_claim_role(self, instance):
        print("Player chose: Claim Role")
        # Add your claim role logic here
        self.game_screen.call_for_choose_char()

    # def on_end_turn(self, instance):
    #     print("Player chose: End Turn")
    #     # Add your end turn logic here=  # Hide sidebar after action

class CharSelectingSidebar(BoxLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen , label, mode,  player_ID = 0, **kwargs):
        super().__init__(orientation='vertical',
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.mode = mode
        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.label = label
        self.player_ID = player_ID

        self.mode_actions_dict = {
            "claim": char_selected
            # "usurper": self.execute_usurper,
            # "inquisitor": self.execute_inquisitor,
        }

        # Transparent-ish background
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text=self.label, font_size=24, size_hint=(1, 0.1))
        self.add_widget(title)

        # Scroll
        scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)

        # Add the layout grid
        layout = GridLayout(cols=1, spacing=20,padding=[10, 10, 10, 10], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        img_folder = os.path.join(os.path.dirname(__file__), 'img_chars')
        for i in self.character_dict:
            path = os.path.join(img_folder, f"{self.character_dict[i].name}.png")
            img = ClickableImage(
                source=path,
                size_hint_y=None,
                height = 150,
                allow_stretch=True,
                keep_ratio=False
            )
            print(path)
            img.bind(on_press=lambda instance, char_ID=i, player_ID = self.player_ID: self.mode_actions_dict[self.mode](instance, player_ID,char_ID, self.game_screen)) # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
            # Add just-created widget into the grid layout
            layout.add_widget(img)

        # Add the whole grid layout into the scroll
        scroll.add_widget(layout)

        # Add the scroll to the total layout
        self.add_widget(scroll)


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class PlayerSelectingSidebar(BoxLayout):


    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen, mode, player_ID=0, **kwargs):  ###OOO Remove the default for player_ID for online mode
        super().__init__(orientation='vertical',
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)
        self.mode = mode
        self.game_screen = game_screen
        self.players_dict = self.game_screen.app.game.players_dict
        self.chars_dict = self.game_screen.app.game.chars_dict
        self.label = f"{random.choice(self.game_screen.app.game.label_messages_dict[self.mode])}"
        self.player_ID = player_ID

        self.mode_actions_dict = {
            "swap": self.execute_swap
            #"witch": self.execute_witch,
            #"joker": self.execute_joker,
        }

        # Transparent-ish background
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text=self.label, font_size=24, size_hint=(1, 0.1))
        self.add_widget(title)

        # Scroll
        scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)

        # Add the layout grid
        layout = GridLayout(cols=1, spacing=20, padding=[10, 10, 10, 10], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(self.game_screen.player_num):
            if i != self.player_ID: #Ensure that the player wont have a chance to swap with himself
                button = Button(
                    text=str(i),
                    font_size=20,
                    size_hint_y=None,  # remove size_hint_y
                    height=60  # set a fixed height
                )

                button.bind(on_press = lambda instance, patient_ID = i: self.mode_actions_dict[self.mode](instance, patient_ID))  #We can still use the function like that, take the value and put (...) after it, we can safely sepecify the arguments put inside the function, like the self.mode_actions_dict[self.mode] just a reference, until with the () after it, it becomes real function run
                # Add just-created widget into the grid layout
                layout.add_widget(button)

        # Add the whole grid layout into the scroll
        scroll.add_widget(layout)

        # Add the scroll to the total layout
        self.add_widget(scroll)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def execute_swap(self, instance, patient_ID):
        self.game_screen.call_for_swap_or_not(self.player_ID, patient_ID)


class SwapOrNotSidebar(BoxLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])

    def __init__(self, game_screen, agent_ID, patient_ID, **kwargs):  ###OOO Remove the default for player_ID for online mode
        super().__init__(orientation='vertical',
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.label = "Do you want to swap actually?"
        self.agent_ID = agent_ID
        self.patient_ID = patient_ID

        # Transparent-ish background
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text=self.label, font_size=24, size_hint=(1, 0.1))
        self.add_widget(title)

        # Scroll
        scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)

        # Add the layout grid
        layout = GridLayout(cols=1, spacing=20, padding=[10, 10, 10, 10], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in ["yes", "no"]:
            button = Button(
                text=i,
                font_size=20,
                size_hint_y=None,  # remove size_hint_y
                height=60  # set a fixed height
            )

            button.bind(on_press=lambda instance, decision=i: self.swap_decided(instance,
                                                                                                           self.agent_ID,
                                                                                                           self.patient_ID,
                                                                                                           decision,
                                                                                                           self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
            # Add just-created widget into the grid layout
            layout.add_widget(button)

        # Add the whole grid layout into the scroll
        scroll.add_widget(layout)

        # Add the scroll to the total layout
        self.add_widget(scroll)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    ### Build Idea: Create the swap then we build the selected for each role like Witch, Inquisitor
    def swap_decided(self, instance, agent_ID, patient_ID, decision, game_screen):

        #Hide sidebars, update actions UI
        game_screen.hide_all_sidebars()
        game_screen.widgets_dict[agent_ID].show_action(0, patient_ID)

        swap(agent_ID, patient_ID, decision, game_screen)

class BlockSelectingSidebar(BoxLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    def __init__(self, game_screen, first_ID, role_ID, player_ID=0, **kwargs): ###OOO Remove the default for player_ID for online mode
        super().__init__(orientation='vertical',
                         size_hint=(0.3, 1),
                         pos_hint={'right': 1},
                         **kwargs)

        self.game_screen = game_screen
        self.character_dict = self.game_screen.app.game.chars_dict
        self.label = f"Are you the real {self.game_screen.app.game.chars_dict[role_ID].name}?"
        self.player_ID = player_ID

        #This is to start the next block turn
        self.first_ID = first_ID
        self.role_ID = role_ID

        # Transparent-ish background
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title = Label(text=self.label, font_size=24, size_hint=(1, 0.1))
        self.add_widget(title)

        # Scroll
        scroll = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)

        # Add the layout grid
        layout = GridLayout(cols=1, spacing=20, padding=[10, 10, 10, 10], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))


        for i in ["yes", "no"]:
            button = Button(
                text=i,
                font_size=20,
                size_hint_y=None,  # remove size_hint_y
                height=60  # set a fixed height
            )

            button.bind(on_press=lambda instance, decision = i, player_ID=self.player_ID: self.block_decided(instance,
                                                                                                            self.first_ID,
                                                                                                            self.role_ID,
                                                                                                            player_ID,
                                                                                                            decision,
                                                                                                            self.game_screen))  # We have to use the char_id since if we don't, the lambda will look for i until the loop is done, do it so that the i is passed when the lambda is created (by value, not by reference)
            # Add just-created widget into the grid layout
            layout.add_widget(button)

        # Add the whole grid layout into the scroll
        scroll.add_widget(layout)

        # Add the scroll to the total layout
        self.add_widget(scroll)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    ### Build Idea: Create the swap then we build the selected for each role like Witch, Inquisitor
    def block_decided (self, instance, first_ID, role_ID, player_ID, decision, game_screen ):

        game_screen.app.game.decide_dict[decision].append(player_ID)

        #Hide all sidebars, update UI actions widget
        game_screen.hide_all_sidebars()
        game_screen.widgets_dict[player_ID].show_action(3, decision, first_ID, role_ID)


class PlayerWidget(BoxLayout):
    def __init__(self, game_screen,player,ratio, **kwargs):
        super().__init__(orientation='vertical', size_hint=(0.15,0.20), **kwargs)

        #Attributize the game_screen and the chars_dict (which can be used in the call later)
        self.game_screen = game_screen
        self.chars_dict = self.game_screen.app.game.chars_dict

        self.information_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.75))
        self.action_layout = BoxLayout(orientation='horizontal', spacing = 10,  size_hint=(1,0.25))

        #Define the folders to get the card images and the action images
        self.img_card_folder = os.path.join(os.path.dirname(__file__), 'img_cards')
        self.img_action_folder = os.path.join(os.path.dirname(__file__), 'img_actions')

        #Define the player
        self.player = player

        #Take the cardback
        self.card = os.path.join(self.img_card_folder,f"card_back.png") # Filename of the card image
        #self.action = os.path.join(self.img_action_folder,"mask.png")
        ### Just for example

        self.card_image = Image(source=self.card, size_hint=(0.4, 1))
        #self.action_image = Image(source=self.action, size_hint = (1,1))


        self.information_layout.add_widget(self.card_image)



        #Create layout of other information
        self.layout_right = BoxLayout(orientation='vertical', spacing=0, size_hint=(0.6, 1))

        self.label_id = Label(
            text = str(player.ID),
            size_hint=(1, 0.1),
            halign='center',
            valign='top'
        )
        self.label_name = Label(
            text=player.player_name,
            size_hint=(1, 0.3),
            halign='center',
            valign='top'
        )
        # Enable text wrapping
        self.label_name.bind(size=self.label_name.setter('text_size'))
        self.layout_right.add_widget(self.label_id)
        self.layout_right.add_widget(self.label_name)

        #This is for the revealed
        self.label_revealed = Label(text=f"{player.revealed} turn(s)", size_hint=(1, 0.1),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.layout_right.add_widget(self.label_revealed)
        #This is for the money
        self.label_money = Label(text=f"{player.money}g", size_hint=(1, 0.1), pos_hint = {'center_x': 0.5, 'center_y': 0.1})
        self.layout_right.add_widget(self.label_money)


        #Add all to the information's widget
        self.information_layout.add_widget(self.layout_right)

        #Add the information and the action widget to the player widget
        self.add_widget(self.action_layout)
        self.add_widget(self.information_layout)


    def reveal_card(self):
        self.card = os.path.join(self.img_card_folder,f"{self.player.get_card().name}.png")

        # Remove old texture from cache
        Cache.remove('kv.image', self.card + '|False|0')
        Cache.remove('kv.texture', self.card + '|False|0')

        self.card_image.source = self.card
        self.card_image.reload()  # Refresh the image
        ###Nhớ reveal trong 1 khoảng tgian

    def hide_card(self, dt):
        self.card = os.path.join(self.img_card_folder,"card_back.png")

        # Remove old texture from cache
        Cache.remove('kv.image', self.card + '|False|0')
        Cache.remove('kv.texture', self.card + '|False|0')

        self.card_image.source = self.card
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

        '''
        if action_id == 0: #this is for the swap option
            # Set up the swap widget
            swap_path = os.path.join(self.img_action_folder, "swap.png")
            swap_widget = Image(source=swap_path, size_hint=(1, 1))

            # Set up the patient, the widget
            patient_ID = args[0]
            patient_ID_image_path = os.path.join(self.img_action_folder, f"number_{patient_ID}.png")
            patient_widget = Image(source=patient_ID_image_path, size_hint=(1, 1))

            # Add widgets to the action_layout
            self.action_layout.add_widget(swap_widget)
            self.action_layout.add_widget(patient_widget)
        elif action_id == 1: #this is for the claim option
            #Set up the claim widget
            claim_path = os.path.join(self.img_action_folder, "claim.png")
            claim_widget = Image(source=claim_path, size_hint=(1, 1))
            #Set up the role, the widget
            role_ID = args[0]
            role_name = self.chars_dict[role_ID].name
            role_image_path = os.path.join(self.img_action_folder,f"{role_name}.png")
            role_widget = Image(source=role_image_path, size_hint = (1,1))

            # Add widgets to the action_layout
            self.action_layout.add_widget(claim_widget)
            self.action_layout.add_widget(role_widget)
        elif action_id == 2: #this is for the peek option
            #Set up the peek widget
            peek_path = os.path.join(self.img_action_folder, "peek.png")
            peek_widget = Image(source=peek_path, size_hint=(1, 1))

            #Add widget to the action_layout
            self.action_layout.add_widget(peek_widget)
        elif action_id == 3: #this is for the block option
            decision = args[0]
            first_ID = args[1]
            role_ID = args[2]
            #Create widget
            decision_path = os.path.join(self.img_action_folder,f"{decision}.png")
            decision_widget = Image(source=decision_path, size_hint = (1,1))
            #Add widget to the action_layout
            self.action_layout.add_widget(decision_widget)


            #Continue the block turn
            Clock.schedule_once(lambda dt: self.game_screen.block_turn(dt, first_ID, role_ID), 1)

    def clear_action(self, dt):
        self.action_layout.clear_widgets()



class CourtWidget(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', spacing=0, size_hint=(1, 0.1), pos_hint={"center_x":0.5, "center_y":0.5})
        self.app = app

        self.court_name = Label(text="Court", font_size=24, size_hint=(1, 0.3))
        self.court_money = Label(text = f"{self.app.game.court}g", font_size=24, size_hint=(1, 0.3))

        self.add_widget(self.court_name)
        self.add_widget(self.court_money)

    def update_money(self):
        new_gold = self.app.game.court
        self.court_money.text = f"{new_gold}g"


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