from kivy.clock import Clock


import numpy as np
import copy
import random
import heapq

from .char import Character, Judge, King, Queen, Thief, Bishop, Widow, Courtesan, Cheat, Patron, Beggar, Witch, Princess
from .math_algorithm import sinkhorn_normalize, random_threshold



class Player:
    def __init__(self, ID, player_name, card: Character, start_money, confidence, revealed):
        self.ID = ID
        self.player_name = player_name
        self.__card = card
        self.money = start_money
        self.type = "human"
        self.confidence = confidence
        self.revealed = revealed
    def get_card(self):
        return self.__card
    def set_card(self, new_card):
        self.__card = new_card
        return

class Bot(Player):
    def __init__(self, ID, bot_name, card: Character, start_money, confidence, revealed):
        super().__init__(ID, bot_name, card, start_money, confidence, revealed)
        self.memory_card_array = []
        self.type = "bot"

    def swap_update(self, agent_ID, patient_ID):

        if agent_ID == self.ID and self.decision_swap == "no":
            pass
        elif agent_ID == self.ID and self.decision_swap == "yes":
            #Switch directly the probability if the swap was its own decision
            self.memory_card_array[[agent_ID, patient_ID]] = self.memory_card_array[[ patient_ID, agent_ID]]

        else:
            agent_row = self.memory_card_array[agent_ID]
            patient_row = self.memory_card_array[patient_ID]

            #Both player card probability will be the average of both of them
            new_row = (agent_row + patient_row) / 2

            #Update the probability
            self.memory_card_array[agent_ID] = new_row
            self.memory_card_array[patient_ID] = new_row


    def reveal_update(self, list_tuple_cases, mode):
        '''
        The mode currently contains two mode:
        - If the mode is combat (the card revealed in a combat), the bot will look that whether list_tuple_case only contains 1 person, it will consider that player possibly bluff, and apply a different metrics to update the probability
        - If the mode is normal (for the peek action, or the cards: Courtesan, the Inquisitor or the Usurper) it will update as normal for all numbers of players, not consider the 1 case
        '''
        size_array = np.size(self.memory_card_array, 0)
        if len(list_tuple_cases) == 1 and mode == "combat":
            for player_ID, role_ID in list_tuple_cases:
                # If the result is the end of a combat, and there is only 1 person claim it, it maybe a bluff so dont convert to 0, and only raise the probability to 0.7
                self.memory_card_array[player_ID, role_ID] = 0.7

        else:
            for player_ID, role_ID in list_tuple_cases:
                #Firstly, convert the column of the card and the row of the player to 0
                self.memory_card_array[player_ID] = np.zeros(size_array)
                self.memory_card_array[:, role_ID] = np.zeros(size_array)

                #Secondly, convert the cell to 1
                self.memory_card_array[player_ID, role_ID] = 1


        self.memory_card_array = sinkhorn_normalize(self.memory_card_array)
        return

    def decide_play(self, game_screen):
        self.decision_swap = None

        game = game_screen.app.game
        # Take the ID of the next player
        next_player_ID = (self.ID + 1) % game.player_num
        next_player = game.players_dict[next_player_ID]
        # I) Make a copy of the list of high-impact cards, so that we can adjust it base on the current state of the game and also the next player
        high_impacts = copy.deepcopy(game.high_impacts)
        high_impacts_self = copy.deepcopy(game.high_impacts)

        useless_self = []



        # 1. If Widow is inside the high_impacts and the player already has 10 golds, remove the Widow from the high_impacts, append it to the useless
        if Widow in high_impacts:
            if next_player.money >= 9:
                high_impacts.remove(Widow)
            if self.money >= 9:
                high_impacts_self.remove(Widow)
                useless_self.append(Widow)

        # 2. If the court of the game holds more than 3 golds, append the Judge to the high_impact
        if game.court >= 3:
            high_impacts.append(Judge)
            high_impacts_self.append(Judge)
        # 3. If the court has 0 or 1 money, append Judge to the useless:
        if game.court <= 1:
            useless_self.append(Judge)
        # 4. If the highest probability role of the next player's gender is female, add the Courtesan to the useless IDs
        if Courtesan in high_impacts:
            next_next_player_ID = (self.ID + 2) % game.player_num

            # Take the female list
            female_list_ID = []
            for i in game.reversed_chars_dict:
                if i in game.female:
                    ID = game.reversed_chars_dict[i]
                    female_list_ID.append(ID)
            #Compare
            if len(female_list_ID) != 0:
                if np.any(self.memory_card_array[next_next_player_ID, female_list_ID] >= random_threshold(0.35)):
                    high_impacts.remove(Courtesan)

                if np.any(self.memory_card_array[self.ID, female_list_ID] >= random_threshold(0.35)):
                    high_impacts_self.remove(Courtesan)
                    useless_self.append(Courtesan)

        # 5. If Cheat is in the game, it will be immediately appended to the high impacts dicts
        if Cheat in game.reversed_chars_dict:
            if next_player.money >= 10:
                high_impacts.append(Cheat)

            if self.money >= 10:
                high_impacts_self.append(Cheat)


            else:
                useless_self.append(Cheat)

        # 6. If Bishop is in the game, and the bot is the player with the most money, add it to the useless
        if Bishop in game.reversed_chars_dict:
            money_dict = {}

            for i in game.players_dict:
                money_dict.setdefault(game.players_dict[i].money, []). append(i)

            max_money_list = money_dict[max(money_dict)]

            if self.ID in max_money_list and len(max_money_list) == 1:
                useless_self.append(Bishop)

        # 7. If Beggar is in the game, and the player is poorer than half of the player, add it to the high_impacts_self, and add it to the useless of the next player or it self
        if Beggar in game.reversed_chars_dict:
            players_list = list(game.players_dict.values())

            money_sort = sorted(players_list, key=lambda x: x.money) #Sort in ascending order (by default)

            if money_sort.index(self) <= game.player_num // 2 - 1:
                high_impacts_self.append(Beggar)
            elif money_sort.index(self) == game.player_num - 1:
                useless_self.append(Beggar)
            elif money_sort.index(next_player) <= game.player_num // 2 - 1:
                high_impacts.append(Beggar) #Consider this, this might be too harsh and violent

        # 8. If Witch is in the game, and the player is poorer than half of the player, add it to the high_impacts_self, and add it to the useless of the next player or it self
        if Witch in game.reversed_chars_dict:
            players_list = list(game.players_dict.values())

            money_sort = sorted(players_list, key=lambda x: x.money)  # Sort in ascending order (by default)

            if money_sort.index(self) <= game.player_num // 2 - 1:
                high_impacts_self.append(Witch)
            if self.money == money_sort[game.player_num - 1].money:
                useless_self.append(Witch)



        ###Add Cheat

        #Print to fix bug
        print(f"Useless of player {self.ID}: {useless_self}")

        # Last. Convert all the high_impacts to a list of ID, do the same with the high_impacts_self and the useless_self
        high_impacts_IDs = []
        for i in high_impacts:
            ID = game.reversed_chars_dict[i]
            high_impacts_IDs.append(ID)

        high_impacts_self_IDs = []
        for i in high_impacts_self:
            ID = game.reversed_chars_dict[i]
            high_impacts_self_IDs.append(ID)


        useful_self_IDs = []
        for i in game.reversed_chars_dict:
            if i not in useless_self:
                ID = game.reversed_chars_dict[i]
                useful_self_IDs.append(ID)

        # II) See if the bot itself has the high_impacts cards
        if np.any(self.memory_card_array[self.ID, high_impacts_IDs] >= 0.3):
            self.itself_high = 1 #One is high, zero is low
        else:
            self.itself_high = 0



        # III) Start thinking
        result = None
        # The swap to block the winning condition is the most important, then we consider when the bot claims its cards
        # 1. First, if the next player has 10 or more golds, and hold the card inside the high_impacts dict with >= 0.5 probability, swap with it
        if next_player.money >= 10:
            # If the probability is not too high, but the confidence is high, still swap
            values = self.memory_card_array[next_player_ID, high_impacts_IDs]
            mask = (values > random_threshold(0.25)) & (values < random_threshold(0.4))
            #Check if there is any card with high impacts with probability equal or more than 0.4 inside the matrix
            if np.any(self.memory_card_array[next_player_ID, high_impacts_IDs] >= random_threshold(0.4)):
                #If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result = (0, self.ID, next_player_ID, np.random.choice(["yes", "no"], p=[0.8, 0.2])) #swap in 80% cases, 20% no swap
                #Else, swap
                else:
                    result = (0, self.ID, next_player_ID, "yes")
            #Cannot use the chain directly
            elif np.any(mask) and random_threshold(0.7) >= next_player.confidence >= random_threshold(0.5):
                # If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result =  (0, self.ID, next_player_ID, random.choice(('yes', 'no')))
                # Else, swap
                else:
                    result =  (0, self.ID, next_player_ID, "yes")
            #If the player confidence is so high, swap
            elif next_player.confidence >= random_threshold(0.7):
                # If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result = (0, self.ID, next_player_ID, random.choice(('yes', 'no')))
                # Else, swap
                else:
                    result = (0, self.ID, next_player_ID, "yes")
        if result == None and self.revealed == 0 and game_screen.play_turn_index > 3:
            # 2. If it is not necessary to block the next player, continue to claim
            # 2.1 Basic claim
            # Firstly, get the args max of the high_impacts in the probability
            if len(high_impacts_self_IDs) >= 1:
                high_impacts_max_prob = np.max(self.memory_card_array[self.ID, high_impacts_self_IDs])
                #high_impacts_ID = np.argmax(self.memory_card_array[self.ID, high_impacts_self_IDs]) #if we just do this, it will return the index after slicing, not the original one
                high_impacts_ID = high_impacts_self_IDs[np.argmax(self.memory_card_array[self.ID, high_impacts_self_IDs])]
                # If the max high_impacts probability is high (over 0.35), it will claim it
                if high_impacts_max_prob > random_threshold(0.2):
                    result = (1, self.ID, high_impacts_ID)

            #Secondly, get the overall max prob, make sure that it wont try to claim useless roles
            if len(useful_self_IDs) >= 1 and result == None:
                all_max_prob = np.max(self.memory_card_array[self.ID, useful_self_IDs])
                all_max_ID = useful_self_IDs[np.argmax(self.memory_card_array[self.ID, useful_self_IDs])] #Fix the shifted ID

                #If the max all probability is high enough (over 0.5), claim it
                if all_max_prob >= random_threshold(0.35):
                    result = (1, self.ID, all_max_ID)

            # 2.2 Complex claim, after the basic claim fails to determine the suitable action, it starts to find the other player with the least confident but with good cards, swap it
            if result == None and len(high_impacts_self_IDs) >= 1:
                min_confidence = 1
                min_ID = 0
                for i in game.players_dict:
                    if game.players_dict[i].confidence <= min_confidence and i != self.ID:
                        min_confidence = game.players_dict[i].confidence
                        min_ID = i
                if min_confidence <= random_threshold(0.35):
                    max_prob_least_confidence = np.max(self.memory_card_array[min_ID, high_impacts_self_IDs])
                    max_prob_least_confidence_ID = high_impacts_self_IDs[np.argmax(self.memory_card_array[min_ID, high_impacts_self_IDs])] #Fix the shifted ID
                    if max_prob_least_confidence >random_threshold(0.4):
                        result = (1, self.ID, max_prob_least_confidence_ID)

        # 3. The Judge is an end-game role, so if the court is too-high, immediately swap with the player has the highest probability to hold it
        if result == None:
            if game.court >= 5:
                judge_ID = game.reversed_chars_dict[Judge]

                other_player_IDs = list(game.players_dict.keys())

                other_player_IDs.remove(self.ID)

                max_ID = other_player_IDs[np.argmax(self.memory_card_array[other_player_IDs, judge_ID])]

                result = (0, self.ID, max_ID, np.random.choice(["yes", "no"], p=[0.7, 0.3]))



        # 4. If it's fail to claim the role, try to sabotage the player with super high_confidence
        if result == None:
            super_high_confidence = []
            for i in game.players_dict:
                if game.players_dict[i].confidence >= 0.9 and i != self.ID:  # Ensure that it won't swap with itself
                    super_high_confidence.append(i)

            if len(super_high_confidence) != 0:
                # #Find the closest player turn that has the super high confidence
                # nearest_ID =  closest_turn_ID(super_high_confidence, self.ID)
                # if nearest_ID == None: #If self is the biggest turn, turn to the next turn (the 0) (turn is rotated)
                #     nearest_ID = super_high_confidence[0]
                nearest_ID = random.choice(super_high_confidence)
                # If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result = (0, self.ID, nearest_ID, np.random.choice(["yes", "no"], p=[0.7, 0.3]))
                # Else, swap
                else:
                    result = (0, self.ID, nearest_ID, "yes")

        # 5. If it still cannot decide, start to find some valuable cards to swap
        if result == None:
            high_confidence = []
            for i in game.players_dict:
                if game.players_dict[i].confidence >= random_threshold(0.4) and i != self.ID: #Ensure that it won't swap with itself
                    high_confidence.append(i)

            # The player inside the confidence 1 with the highest probability to hold the card inside the column of high impacts will be swapped
            if len(high_confidence) >= 1 and len(high_impacts_self_IDs) >= 1:
                max_prob = 0
                max_prob_player_ID = None
                for i in high_confidence:
                    max_current_player = np.max(self.memory_card_array[i, high_impacts_self_IDs])
                    if max_current_player >= max_prob:
                        max_prob = max_current_player
                        max_prob_player_ID = i
                # If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result = (0, self.ID,  max_prob_player_ID, random.choice(('yes', 'no')))
                # Else, swap
                else:
                    result = (0, self.ID,  max_prob_player_ID, "yes")


        if result == None:
            result = (2, self.ID)

        if result[0] == 0:

            if result[3] != None:
                self.decision_swap = result[3]

            elif result[3] == None:
                choices = [i for i in game_screen.app.game.players_dict if i != self.ID]
                choice = random.choice(choices)

                result = list(result)
                result[3] = choice
                result = tuple(result)
                self.decision_swap = result[3]



        return result


    def decide_block(self, game_screen, first_ID):
        #Set up the necessary variable
        role_ID = game_screen.app.game.affected_dict["role_ID"]
        current_yes = game_screen.app.game.decide_dict["yes"] ###Can be removed, maybe used later
        state = None

        if game_screen.app.game.chars_dict[role_ID] in game_screen.app.game.decision_activate:
            if game_screen.app.game.chars_dict[role_ID].name == "witch":
                # If the probability is more than 0.45, say yes
                if self.memory_card_array[self.ID, role_ID] >= random_threshold(0.35):
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"

                elif self.money <= 5 and self.memory_card_array[self.ID, role_ID] >= random_threshold(0.20):
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"

                #Maybe we should add the elif when all the higher prob-holder said no, so the bot is likely the role

        else:
            #Test the result when the role is triggered by this bot
            self_test_result = game_screen.app.game.test_win_condition(self.ID, role_ID, self)

            result_test_win_condition = game_screen.app.game.test_win_condition(first_ID, role_ID, self)



            #If the bot's self probability about the role is high, say yes

            if len(game_screen.app.game.decide_dict["yes"]) == 1:
                #If the win condition is trigger after that, say no if this bot included in the winners
                if type(result_test_win_condition) == set:
                    if self.ID in result_test_win_condition:
                        game_screen.app.game.decide_dict["no"].append(self.ID)
                        state = "no"

                    #Else, say yes if it has more than 1 money
                    elif not self.ID in result_test_win_condition and self.money != 1:
                        game_screen.app.game.decide_dict["yes"].append(self.ID)
                        state = "yes"

                    else:
                        game_screen.app.game.decide_dict["no"].append(self.ID)
                        state = "no"

            if state == None:
                #If the probability is more than 0.45, say yes
                if self.memory_card_array[self.ID, role_ID] >= random_threshold(0.45):
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"
                # If the probablity is from 0.3 to 0.45, and claim it can make this bot win, say yes:
                elif random_threshold(0.25) <= self.memory_card_array[self.ID, role_ID] < random_threshold(0.45):
                    if type(self_test_result) == set:
                        if self.ID in self_test_result:
                            game_screen.app.game.decide_dict["yes"].append(self.ID)
                            state = "yes"
                        # Else, say no
                        else:
                            game_screen.app.game.decide_dict["no"].append(self.ID)
                            state = "no"
                    #If the win condition is not triggered but the confidence and the probability of all player in that role is low, and the bot won't lose all the money if it fails, say yes
                    elif not any(game_screen.app.game.players_dict[x].confidence >= random_threshold(0.4) for x in game_screen.app.game.decide_dict["yes"]) and not self.money == 1 and not np.any(self.memory_card_array[:,role_ID] > random_threshold(0.3)):
                        game_screen.app.game.decide_dict["yes"].append(self.ID)
                        state = "yes"
                    else:

                        game_screen.app.game.decide_dict["no"].append(self.ID)
                        state = "no"

                #If the probability is from 0.1 to 0.25
                elif random_threshold(0.1) < self.memory_card_array[self.ID, role_ID] < random_threshold(0.25):
                    #If the money is 1, say no immediately
                    if self.money == 1:

                        game_screen.app.game.decide_dict["no"].append(self.ID)
                        state = "no"

                    #The confidence and probablity of this is lower than the before thresholds
                    elif not any(game_screen.app.game.players_dict[x].confidence >= random_threshold(0.3) for x in game_screen.app.game.decide_dict["yes"]) and not np.any(self.memory_card_array[:,role_ID] > random_threshold(0.15)):
                        game_screen.app.game.decide_dict["yes"].append(self.ID)
                        state = "yes"
                #If the probability is lower than 0.1, say no
                else:
                    game_screen.app.game.decide_dict["no"].append(self.ID)
                    state = "no"

        if state == None:

            game_screen.app.game.decide_dict["no"].append(self.ID)
            state = "no"

        if state == "no":
            widget = game_screen.widgets_dict[self.ID]
            widget.show_action(3, "no", first_ID, role_ID)
            # print(f"{self.ID} trigger no")


        if state == "yes":
            widget = game_screen.widgets_dict[self.ID]
            widget.show_action(3, "yes", first_ID, role_ID)
            # print(f"{self.ID} trigger yes")

    def decide_cards(self, game_screen, mode):
        if mode == "witch":
            money_dict = {}
            for i in game_screen.app.game.players_dict:
                if i != self.ID:
                    money_dict.setdefault(game_screen.app.game.players_dict[i].money, []).append(i)

            max_money_list = money_dict[max(money_dict)]

            decision = random.choice(max_money_list)

            return decision

        if mode == "princess":
            def find_min_variance_row_except(arr, a):
                variances = np.var(arr, axis=1)

                # Đặt phương sai của hàng a thành inf để loại bỏ khỏi việc tìm min
                variances_masked = np.where(np.arange(len(variances)) != a, variances, np.inf)

                return np.argmin(variances_masked)


            decision = find_min_variance_row_except(self.memory_card_array, self.ID)

            return decision



def char_selected(instance, player_ID, role_ID, game_screen):  # The args take the sidebar boxlayout
    print(f"Player chose: {game_screen.app.game.chars_dict[role_ID].name}")

    # Hide all sidebars after finishing choosing
    game_screen.hide_all_sidebars()

    # Show the action
    game_screen.widgets_dict[player_ID].show_action(1, role_ID)

    ###Maybe we should put those dicts inside another action
    # Start the block_turn
    game_screen.block_turn_index = 0

    # The dict to update the history of the game
    game_screen.app.game.dict_for_history = {'mode': 1, 'role': role_ID, "claimers": []}

    # The dict to update the UI, also to check the money of players
    game_screen.app.game.affected_dict = {'role_ID': role_ID, 'status': 0, 'affected': {player_ID}}

    # The dict to resolve this claim phase, and to support the UI update
    game_screen.app.game.decide_dict = {"yes": [player_ID], "no": []}

    # Make sure that the wrong_IDs is fully cleaned
    game_screen.app.game.wrong_IDs = []



    print(f"++++++Start Block Turn of Player {player_ID}+++++++")
    game_screen.block_turn(0, player_ID, role_ID)


def swap(agent_ID, patient_ID, decision, game_screen): # Since the time here is always needs more than 2 to actually finish, raise the endturn after 2
    time_ratio = game_screen.app.time_ratio
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

    Clock.schedule_once(game_screen.end_turn, 2 * time_ratio)





