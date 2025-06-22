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


import os
from math import cos, sin, pi
import random

from .game_brain import Game
from .sidebar_widget import ActionSidebar, CharSelectingSidebar, PlayerSelectingSidebar, SwapOrNotSidebar, BlockSelectingSidebar, PlayerWidget, CourtWidget, PauseOverlay
from .player_and_action import swap, char_selected
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
        start_btn = Button(text='Start Game',bold=True, font_size=24, size_hint=(1, 0.2))
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
        self.app.game = Game(player_num = self.app.player_num)
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


            #For the pause button
            self.pause_button = Button(text="Pause", size_hint=(0.05,0.05), pos_hint={'right': 1})
            self.pause_button.bind(on_press = self.pause )
            self.add_widget(self.pause_button)


            self.add_widget(self.layout)
            self.layout_initialized = True

            # # Init the hands on the widget
            # for i in self.widgets_dict:
            #     if type(i) == int:
            #         self.widgets_dict[i].pop_bubble_chat("Ohmni!")

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
                Clock.schedule_once(self.widgets_dict[i].hide_card, 5 * self.player_num/4)
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
            self.resolve_claim()

            if not (self.app.game.chars_dict[role_ID] in self.app.game.special_activate and self.app.game.affected_dict["status"] == 1): #If not the situation that the special activate is actually activated

                Clock.schedule_once(self.complete_claim, 2.1)

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
            Clock.schedule_once(first_widget.hide_card, 0)

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

            Clock.schedule_once(one_yes, 0.8)
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
                Clock.schedule_once(lambda dt,w = widget: w.claim_anim_in.start(w.hand_mask_rotated), 0.6)
                widget.reveal_card()

                def update_claim(dt, player_ID, card_ID, role_ID, widget):
                    print(f"^^^^^{player_ID, card_ID}^^^^^ ")
                    #Update revealed
                    game.players_dict[player_ID].revealed = len(self.app.game.players_dict) // 2 + 1  # Always +1 since this turn revealed cards decreased the confidence, the players inside the yes wont be decreased


                    if card_ID == role_ID:
                        print("^^^^^Debug^^^^^ ")
                        game.affected_dict["status"] = 1
                        true_IDs.append(player_ID)
                        widget.pop_bubble_chat(f"{random.choice(game.chars_dict[role_ID].list_success)}")

                    else:
                        game.wrong_IDs.append(player_ID)
                        widget.pop_bubble_chat(f"{random.choice(game.players_dict[player_ID].get_card().list_fail)}")

                    game.dict_for_history["claimers"].append((player_ID, card_ID))

                Clock.schedule_once(lambda dt, p = player_ID, c = card_ID, r = role_ID, w = widget:update_claim(dt, p, c, r, w), 1.4)

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

            Clock.schedule_once(activ,1.6)


        #Add the dictionary to the history
        def update_his(dt):
            game.history.append(game.dict_for_history)

        Clock.schedule_once(update_his, 1.8)


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

        if len(self.app.game.decide_dict["yes"]) > 1:
            for i in self.app.game.decide_dict["yes"]:
                Clock.schedule_once(self.widgets_dict[i].hide_card, 2) ###We can just add 0.5 + i * delta_time so that the cards are hid gradually
                Clock.schedule_once(lambda dt ,widget_ID = i: self.widgets_dict[widget_ID].parent.remove_widget(self.widgets_dict[widget_ID].bubble_chat), 2)
                def none_bubble_chat(dt, widget_ID):
                    self.widgets_dict[widget_ID].bubble_chat = None

                Clock.schedule_once(lambda dt, widget_ID = i: none_bubble_chat(dt, widget_ID), 2)

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
            else:
                self.app.sm.current = "lose_scene"
        Clock.schedule_once(delayed_check_remove_hand, 2.3)



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
        # for i in self.widgets_dict:
        #     if type(i) == int:
        #         Clock.schedule_once(self.widgets_dict[i].clear_action, 1)
        #If there is the letter from the last swapping, clear it
        if self.app.game.history[-1]["mode"] == 0:
            agent_ID = self.app.game.history[-1]["agent"]

            agent_widget = self.widgets_dict[agent_ID]

            if agent_widget.letter != None:
                agent_widget.parent.remove_widget(agent_widget.letter)
                agent_widget.letter = None
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

class WinScene(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "win_scene"

        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        self.label = Label(text=" You Win! ", font_size=36, size_hint=(1, 0.3))
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

        self.label = Label(text=" You Lose! ", font_size=36, size_hint=(1, 0.3))
        layout.add_widget(self.label)

        main_menu_btn = Button(text="Return to Main Menu", font_size=24, size_hint=(1, 0.2))
        main_menu_btn.bind(on_press=self.return_to_menu)
        layout.add_widget(main_menu_btn)

        self.add_widget(layout)

    def return_to_menu(self, instance):
        self.app.sm.current = "menu"