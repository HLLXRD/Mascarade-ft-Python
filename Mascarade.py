# import kivy
# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
#
#
# class GameWidget(Widget):
#     pass
#
#
# class GameApp(App):
#     def build(self):
#         return GameWidget()
#
#     def on_start(self):
#         # Set window to fullscreen
#         Window.fullscreen = 'auto'
#
#
# if __name__ == '__main__':
#     GameApp().run()
import os
import random
import main as core
import kivy
from kivy.cache import Cache
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.app import App
from math import cos, sin, pi
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BooleanProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
#Make the image clickable
class ClickableImage(ButtonBehavior, Image):
    pass
class MenuScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.name = 'menu'
        self.app = app

        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Game title
        title = Label(text='My Game', font_size=48, size_hint=(1, 0.3))
        layout.add_widget(title)

        # Buttons layout
        button_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.7))

        # Start Game button
        start_btn = Button(text='Start Game', font_size=24, size_hint=(1, 0.2))
        start_btn.bind(on_press=self.start_game)
        button_layout.add_widget(start_btn)

        # Options button
        options_btn = Button(text='Options', font_size=24, size_hint=(1, 0.2))
        options_btn.bind(on_press=self.go_to_options)
        button_layout.add_widget(options_btn)

        # Exit button
        exit_btn = Button(text='Exit', font_size=24, size_hint=(1, 0.2))
        exit_btn.bind(on_press=self.exit_game)
        button_layout.add_widget(exit_btn)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def start_game(self, instance):
        print("Starting game...")
        self.app.game = core.Game(player_num = self.app.player_num)
        self.manager.current = 'off_name_typing'
        # You can switch to game screen here later


    def go_to_options(self, instance):
        self.manager.current = 'options'

    def exit_game(self, instance):
        App.get_running_app().stop()


class OptionsScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = 'options'
        self.player_num = 3  # Default number of players

        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        # Title
        title = Label(text='Options', font_size=36, size_hint=(1, 0.2))
        layout.add_widget(title)

        # Player count section
        player_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.4))

        # Player count label
        self.player_label = Label(text=f'Number of Players: {self.player_num}', font_size=24)
        player_layout.add_widget(self.player_label)

        # Player count slider
        self.player_slider = Slider(min=3, max=9, step=1, size_hint=(1, 0.3))
        self.player_slider.bind(value=self.on_player_count_change)
        player_layout.add_widget(self.player_slider)

        layout.add_widget(player_layout)

        # Buttons layout
        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.4))

        # Back button
        back_btn = Button(text='Back to Menu', font_size=20)
        back_btn.bind(on_press=self.back_to_menu)
        button_layout.add_widget(back_btn)

        # Apply button
        apply_btn = Button(text='Apply Settings', font_size=20)
        apply_btn.bind(on_press=self.apply_settings)
        button_layout.add_widget(apply_btn)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def on_player_count_change(self, instance, value):
        self.player_num = int(value)
        self.player_label.text = f'Number of Players: {self.player_num}'

    def apply_settings(self, instance):
        self.app.player_num = self.player_num
        print(f"Applied settings: {self.player_num} players")
        # Here you can save the settings to your game

    def back_to_menu(self, instance):
        self.manager.current = 'menu'


class OffNameScreen(Screen):
    def __init__(self,app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = 'off_name_typing'

        #Get the layout
        name_layout = BoxLayout(size_hint=(1, 0.7))

        name_input = TextInput(
            hint_text="Enter your name",
            multiline=False,
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0, 0, 0, 0),  # Fully transparent
            foreground_color=(1, 1, 1, 1),  # White text
            cursor_color=(1, 1, 1, 1),  # White cursor
            halign="center"
        )
        name_input.bind(on_text_validate=self.on_name_entered)

        name_layout.add_widget(name_input)
        self.add_widget(name_layout)

    def on_name_entered(self, instance):
        name = [instance.text]
        self.app.game.take_player_names(name)
        self.app.game.game_build()
        self.manager.current = 'off_game'


#### Added ActionSidebar class for player decision making
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

def char_selected(instance, player_ID,role_ID, game_screen ): #The args take the sidebar boxlayout
    print(f"Player chose: {game_screen.app.game.chars_dict[role_ID].name}")

    # Hide all sidebars after finishing choosing
    game_screen.hide_all_sidebars()

    #Show the action
    game_screen.widgets_dict[player_ID].show_action(1, role_ID)

    ###Maybe we should put those dicts inside another action
    #Start the block_turn
    game_screen.block_turn_index = 0

    #The dict to update the history of the game
    game_screen.app.game.dict_for_history = {'mode': 1, 'role': role_ID, "claimers": []}

    #The dict to update the UI, also to check the money of players
    game_screen.app.game.affected_dict = {'role_ID': role_ID, 'status':0, 'affected': {player_ID}}

    #The dict to resolve this claim phase, and to support the UI update
    game_screen.app.game.decide_dict = {"yes": [player_ID], "no": []}

    #Make sure that the wrong_IDs is fully cleaned
    game_screen.app.game.wrong_IDs = []

    #Take the win condition of the first_player
    game_screen.app.game.result_test_win_condition = game_screen.app.game.test_win_condition(player_ID, role_ID)

    print(f"++++++Start Block Turn of Player {player_ID}+++++++")
    game_screen.block_turn(0, player_ID, role_ID)


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
def swap(agent_ID, patient_ID, decision, game_screen):
    if decision == "no":
        pass
    elif decision == "yes":
        agent = game_screen.app.game.players_dict[agent_ID]
        patient = game_screen.app.game.players_dict[patient_ID]
        agent_card = agent.get_card()
        patient_card = patient.get_card()
        agent.set_card(patient_card)
        patient.set_card(agent_card)

    #Records to a dict to save to history
    dict_for_history = {"mode":0, "agent":agent_ID, "patient":patient_ID}
    game_screen.app.game.history.append(dict_for_history)

    game_screen.end_turn("dummy")

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


class OffGameScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = 'off_game'
        self.layout_initialized = False

        #Start the turn-counting indices
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

    def on_pre_enter(self, **kwargs):
        if not self.layout_initialized:
            # --- Top-right bar for window control ---
            top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.05), pos_hint={'top': 1})
            top_bar.padding = [0, 0, 10, 0]  # Right padding

            # Spacer to push buttons to right
            top_bar.add_widget(Label(size_hint=(0.85, 1)))

            # Minimize button
            min_btn = Button(text='_', font_size=18, size_hint=(0.05, 1))
            min_btn.bind(on_press=self.minimize_window)
            top_bar.add_widget(min_btn)

            # Maximize / Restore button
            max_btn = Button(text='🗖', font_size=18, size_hint=(0.05, 1))
            max_btn.bind(on_press=self.toggle_maximize)
            top_bar.add_widget(max_btn)

            # Close button
            close_btn = Button(text='✕', font_size=18, size_hint=(0.05, 1), background_color=(1, 0, 0, 1))
            close_btn.bind(on_press=self.close_app)
            top_bar.add_widget(close_btn)

            # Add to layout
            self.layout.add_widget(top_bar)
            self.layout = FloatLayout()

            self.player_num = self.app.player_num
            center_x = 0.5
            center_y = 0.5
            radius = 0.2
            ratio = Window.width / Window.height

            for i in range(self.player_num):
                angle = -pi / 2 + 2 * pi * i / self.player_num
                x = center_x + radius * cos(angle)
                y = center_y + radius * sin(angle) * ratio

                player_space = PlayerWidget(self, self.app.game.players_dict[i], ratio,
                                            pos_hint={'center_x': x, 'center_y': y})
                self.widgets_dict[i] = player_space
                self.layout.add_widget(player_space)

            #For the court
            self.court_widget = CourtWidget(self.app)
            self.layout.add_widget(self.court_widget)
            self.widgets_dict['court'] = self.court_widget

            #For the pause button
            self.pause_button = Button(text="Pause", size_hint=(0.05,0.05), pos_hint={'right': 1})
            self.pause_button.bind(on_press = self.pause )
            self.add_widget(self.pause_button)


            self.add_widget(self.layout)
            self.layout_initialized = True

            print(self.widgets_dict)
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
        
    def pause(self,instance):
        pause_overlay = PauseOverlay()
        Clock.unschedule(self.play_turn)
        self.add_widget(pause_overlay)

    def on_enter(self, **kwargs):
        for i in self.widgets_dict:
            if type(i) == int:
                self.widgets_dict[i].reveal_card()
                Clock.schedule_once(self.widgets_dict[i].hide_card, 5)
        Clock.schedule_once(self.play_turn, 5.5)

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
                self.app.game.history.append({'mode': 22, "player": player_ID})

                #Endturn
                self.end_turn("dummy")


        else:
            self.call_for_decision(curr_turn)

    def block_turn(self,dt, first_ID, role_ID):
        self.block_turn_index += 1
        # print(f"====={self.block_turn_index}=====")
        if self.block_turn_index == self.app.game.player_num: #Finish resolve

            #Resolve the claim phase, also update all the bots based on the revealed cards
            self.resolve_claim()

            if not (self.app.game.chars_dict[role_ID] in self.app.game.special_activate and self.app.game.affected_dict["status"] == 1): #If not the situation that the special activate is actually activated


                Clock.schedule_once(self.complete_claim, 0)

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
            game.affected_dict["status"] = 1

            game.dict_for_history["claimers"].append((first_ID, role_ID))

            if game.chars_dict[role_ID] not in self.app.game.special_activate:
                game.chars_dict[role_ID].activate(first, self.app.game)
                print(f">>{role_claimed.name} triggered")

            else:
                game.chars_dict[role_ID].activate(first, game, self)
                print(f">>{role_claimed.name} triggered")
            ###This update for the situation everyone agree may cause the bot assume that player is the real role, while we can solve this by just raise the probability to 0.5
        else:
            #If there is more than 1 players claim, add the court to the affected
            game.affected_dict["affected"].add("court")
            true_IDs = [] #For the farmers
            game.wrong_IDs = []
            for player_ID in game.decide_dict["yes"]:
                player = game.players_dict[player_ID]
                card_ID = player.get_card().ID

                #Reveal the card
                self.widgets_dict[player_ID].reveal_card()

                #Update revealed
                game.players_dict[player_ID].revealed = len(self.app.game.players_dict) // 2 + 1  # Always +1 since this turn revealed cards decreased the confidence, the players inside the yes wont be decreased

                if card_ID == role_ID:
                    game.affected_dict["status"] = 1
                    true_IDs.append(player_ID)
            ###Consider remove the "yes" with the "affected" but the problem appears when we update the affected when activate it so then the yes, or the affected will be polluted
                else:
                    game.wrong_IDs.append(player_ID)

                game.dict_for_history["claimers"].append((player_ID, card_ID))

            #Activate the role on the true player

            if len(true_IDs) != 0:
                true_ID = true_IDs[0]
                true_player = game.players_dict[true_ID]

                if game.chars_dict[role_ID] not in self.app.game.special_activate:
                    game.chars_dict[role_ID].activate(true_player, self.app.game)
                    print(f">>{role_claimed.name} triggered")

                else:
                    game.chars_dict[role_ID].activate(true_player, game, self)
                    print(f">>{role_claimed.name} triggered")


        #Add the dictionary to the history
        game.history.append(game.dict_for_history)


    def penalize(self):
        game= self.app.game
        # Penalize the role on the wrong player(s)
        for i in game.wrong_IDs:
            player = game.players_dict[i]
            player.money -= 1
            game.court += 1
    def update_UI_and_check(self):
        # print(f"\n\n\n {self.app.game.court}")
        for i in self.app.game.affected_dict["affected"]:
            #Since the widgets_dict has both 'court' (str) and 0,1,2,3,4,5(int), we can just update money for all players
            self.widgets_dict[i].update_money()

        for i in self.app.game.decide_dict["yes"]:
            Clock.schedule_once(self.widgets_dict[i].hide_card, 1.5) ###We can just add 0.5 + i * delta_time so that the cards are hid gradually

        check_result = self.app.game.check("real")
        def delayed_check(dt):
            if check_result == 0:
                return
            elif check_result == self.app.game.you_ID:  # You won
                self.app.sm.current = "win_scene"
            else:
                self.app.sm.current = "lose_scene"
        Clock.schedule_once(delayed_check, 2.3)



    def special_activate_UI(self, mode, *args):
        if mode == "courtesan":
            print("Updating courtesan...")
            customer_ID = args[0]

            # The customers of the Courtesan will reveal to show their gender, also increase the revealed
            self.widgets_dict[customer_ID].reveal_card()
            self.app.game.players_dict[customer_ID].revealed = len(self.app.game.players_dict) // 2 + 1

            #All the bots will update the customer's card into its memory
            for i in self.app.game.bots_dict:
                self.app.game.bots_dict[i].reveal_update([(customer_ID, self.app.game.players_dict[customer_ID].get_card().ID)], "normal")

            Clock.schedule_once(self.widgets_dict[customer_ID].hide_card, 2)

            Clock.schedule_once(self.complete_claim, 2.5)

    def complete_claim(self, dt):
        #Penalize the wrong players after complete
        self.penalize()
        # Update the UI, and also check if the win condition has met
        self.update_UI_and_check()  # This takes approximately 2.5s to fully completed

        # Endturn, reduce the confidence
        Clock.schedule_once(self.end_turn, 3)


    def end_turn(self, dt):
        print("=======End Turn======")
        #Remove all the actions
        for i in self.widgets_dict:
            if type(i) == int:
                Clock.schedule_once(self.widgets_dict[i].clear_action, 1)
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
        Clock.schedule_once(self.play_turn, 2)

    def call_for_decision(self, player_ID):
        if self.sidebar is None:
            self.sidebar = ActionSidebar(self, player_ID)
        if self.sidebar.parent is None:
            self.layout.add_widget(self.sidebar)
    def call_for_choose_char(self):
        if self.char_sidebar is None:
            self.char_sidebar = CharSelectingSidebar(self, "Who are you?", "claim")
        if self.char_sidebar.parent is None:
            self.layout.add_widget(self.char_sidebar)
    def call_for_block(self, first_ID, role_ID):
        if self.block_sidebar is None:
            self.block_sidebar = BlockSelectingSidebar(self, first_ID, role_ID)
        if self.block_sidebar.parent is None:
            self.layout.add_widget(self.block_sidebar)
    def call_for_choose_player(self, mode):
        if self.player_sidebar is None:
            self.player_sidebar = PlayerSelectingSidebar(self, mode)
        if self.player_sidebar.parent is None:
            self.layout.add_widget(self.player_sidebar)

    def call_for_swap_or_not(self, agent_ID, patient_ID):
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
class WinScene(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "win_scene"

        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        self.label = Label(text="🎉 You Win! 🎉", font_size=36, size_hint=(1, 0.3))
        layout.add_widget(self.label)

        main_menu_btn = Button(text="Return to Main Menu", font_size=24, size_hint=(1, 0.2))
        main_menu_btn.bind(on_press=self.return_to_menu)
        layout.add_widget(main_menu_btn)

        self.add_widget(layout)

    def return_to_menu(self, instance):
        self.app.sm.current = "menu"


class LoseScene(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "lose_scene"

        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        self.label = Label(text="💀 You Lose! 💀", font_size=36, size_hint=(1, 0.3))
        layout.add_widget(self.label)

        main_menu_btn = Button(text="Return to Main Menu", font_size=24, size_hint=(1, 0.2))
        main_menu_btn.bind(on_press=self.return_to_menu)
        layout.add_widget(main_menu_btn)

        self.add_widget(layout)

    def return_to_menu(self, instance):
        self.app.sm.current = "menu"
        
class GameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_num = 4  # default
        self.game = None

        #Screens
        self.sm = None
        self.off_game_screen = None
    def build(self):
        self.sm = ScreenManager()

        # Add both end scenes
        self.win_scene = WinScene(self)
        self.lose_scene = LoseScene(self)
        self.sm.add_widget(self.win_scene)
        self.sm.add_widget(self.lose_scene)

        # Add other screens
        self.menu_screen = MenuScreen(self)
        self.options_screen = OptionsScreen(self)
        self.off_name_screen = OffNameScreen(self)
        self.off_game_screen = OffGameScreen(self)

        self.sm.add_widget(self.menu_screen)
        self.sm.add_widget(self.options_screen)
        self.sm.add_widget(self.off_name_screen)
        self.sm.add_widget(self.off_game_screen)

        # Start at menu
        self.sm.current = 'menu'

        return self.sm


    def on_start(self):
        # Set window to fullscreen
        # Window.fullscreen = 'auto'
        pass


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





if __name__ == '__main__':
    print(os.path.dirname(__file__))
    app = GameApp()
    app.run()

