from char import Character, Judge, King, Queen, Thief, Bishop, Widow
from math_algorithm import sinkhorn_normalize, random_threshold
import numpy as np
import copy
import random



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
    def action(self, game, action_choose, *args):
        if action_choose.lower() == "swap":
            victim_id = input("Who will be the victim of this? ")
            try:
                victim_id = int(victim_id)
            except:
                for i in game.players_dict:
                    if victim_id.lower() == game.players_dict[i].player_name.lower():
                        victim_id = game.players_dict[i].ID
            finally:
                swap(self, game.players_dict[victim_id])
        elif action_choose.lower() == "claim":
            role_ID = args[0]
            combat(game,self.ID,role_ID)
            game.check()

        elif action_choose.lower() == "peek at card":
            print("You are", self.get_card())

        #Update the action
        game.update()

class Bot(Player):
    def __init__(self, ID, bot_name, card: Character, start_money, confidence, revealed):
        super().__init__(ID, bot_name, card, start_money, confidence, revealed)
        self.memory_card_array = []
        self.type = "bot"

    def swap_update(self, agent_ID, patient_ID):
        agent_row = self.memory_card_array[agent_ID]
        patient_row = self.memory_card_array[patient_ID]

        #Both player card probability will be the average of both of them
        new_row = (agent_row + patient_row) / 2

        #Update the probability
        self.memory_card_array[agent_ID] = new_row
        self.memory_card_array[patient_ID] = new_row


    def reveal_update(self, list_tuple_cases):
        size_array = np.size(self.memory_card_array, 0)
        for player_ID, role_ID in list_tuple_cases:

            #Firstly, convert the column of the card and the row of the player to 0
            self.memory_card_array[player_ID] = np.zeros(size_array)
            self.memory_card_array[:, role_ID] = np.zeros(size_array)

            #Secondly, convert the cell to 1
            self.memory_card_array[player_ID, role_ID] = 1


        self.memory_card_array = sinkhorn_normalize(self.memory_card_array)
        return

    def decide_play(self, game_screen):
        print(f"======Player {self.ID}'s turn=======")
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
        # 3. If the court has 0 money, append Judge to thee useless:
        if game.court == 0:
            useless_self.append(Judge)
        ###Add Cheater

        # Last. Convert all the high_impacts to a list of ID, do the same with the high_impacts_self and the useless_self
        high_impacts_IDs = []
        for i in high_impacts:
            ID = game.reversed_chars_dict[i]
            high_impacts_IDs.append(ID)

        high_impacts_self_IDs = []
        for i in high_impacts_self:
            ID = game.reversed_chars_dict[i]
            high_impacts_self_IDs.append(ID)

        useless_self_IDs = []
        for i in useless_self:
            ID = game.reversed_chars_dict[i]
            useless_self_IDs.append(ID)

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
            mask = (values > 0.25) & (values < 0.4)
            #Check if there is any card with high impacts with probability equal or more than 0.4 inside the matrix
            if np.any(self.memory_card_array[next_player_ID, high_impacts_IDs] >= 0.4):
                #If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result = (0, self.ID, next_player_ID, random.choice(('yes','no')))
                #Else, swap
                else:
                    result = (0, self.ID, next_player_ID, "yes")
            #Cannot use the chain directly
            elif np.any(mask) and 0.7>= next_player.confidence >= 0.5:
                # If it probably keeps high card, random swap or not
                if self.itself_high == 1:
                    result =  (0, self.ID, next_player_ID, random.choice(('yes', 'no')))
                # Else, swap
                else:
                    result =  (0, self.ID, next_player_ID, "yes")
            #If the player confidence is so high, swap
            elif next_player.confidence >= 0.7:
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
            high_impacts_max_prob = np.max(self.memory_card_array[self.ID, high_impacts_self_IDs])
            high_impacts_ID = np.argmax(self.memory_card_array[self.ID, high_impacts_self_IDs]) #If we just do this, it wil

            #Secondly, get the overall max prob, make sure that it wont try to claim useless roles
            if len(useless_self) != 0:
                arr_to_check = np.delete(self.memory_card_array, useless_self_IDs, axis = 1)
            else:
                arr_to_check = self.memory_card_array
            all_max_prob = np.max(arr_to_check[self.ID, :])
            all_max_ID = np.argmax(arr_to_check[self.ID, :])

            #If the max high_impacts probability is high (over 0.35), it will claim it
            if high_impacts_max_prob > 0.35:
                result =  (1, self.ID, high_impacts_ID)
            #If the max all probability is high enough (over 0.5), claim it
            elif all_max_prob >= 0.5:
                result = (1, self.ID, all_max_ID)

            # 2.2 Complex claim, after the basic claim fails to determine the suitable action, it starts to find the player with the least confident but with good cards, swap it
            if result == None:
                min_confidence = 1
                min_ID = 0
                for i in game.players_dict:
                    if game.players_dict[i].confidence <= min_confidence:
                        min_confidence = game.players_dict[i].confidence
                        min_ID = i
                if min_confidence <= 0.35:
                    max_prob_least_confidence = np.max(arr_to_check[min_ID, high_impacts_IDs])
                    max_prob_least_confidence_ID = np.argmax(arr_to_check[min_ID, high_impacts_IDs])
                    if max_prob_least_confidence > 0.4:
                        result = (1, self.ID, max_prob_least_confidence_ID)

        if result == None:
            # 3. If it's fail to claim the role, start to find some valuable cards to swap
            high_confidence = []
            for i in game.players_dict:
                if game.players_dict[i].confidence >= 0.4 and i != self.ID: #Ensure that it won't swap with itself
                    high_confidence.append(i)

            # The player inside the confidence 1 with the highest probability to hold the card inside the column of high impacts will be swapped
            max_prob = 0
            max_prob_player_ID = None
            for i in high_confidence:
                max_current_player = np.max(self.memory_card_array[i, high_impacts_IDs])
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

        return result


    def decide_block(self, game_screen, first_ID):
        #Set up the necessary variable
        role_ID = game_screen.app.game.affected_dict["role_ID"]
        current_yes = game_screen.app.game.decide_dict["yes"] ###Can be removed, maybe used later
        state = None

        #Test the result when the role is triggered by this bot
        self_test_result = game_screen.app.game.test_win_condition(self.ID, role_ID)



        #If the bot's self probability about the role is high, say yes
        if self.memory_card_array[self.ID, role_ID] >= 0.45:
            game_screen.app.game.decide_dict["yes"].append(self.ID)
            state = "yes"

        elif len(game_screen.app.game.decide_dict["yes"]) == 1:
            #If the win condition is trigger after that, say no if this bot included in the winners
            if type(game_screen.app.game.result_test_win_condition) == set:
                if self.ID in game_screen.app.game.result_test_win_condition:
                    game_screen.app.game.decide_dict["no"].append(self.ID)
                    state = "no"

                #Else, say yes if it has more than 1 money
                elif not self.ID in game_screen.app.game.result_test_win_condition and self.money != 1:
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"


        if state == None:
            #If the probability is more than 0.45, say yes
            if self.memory_card_array[self.ID, role_ID] >= 0.45:
                game_screen.app.game.decide_dict["yes"].append(self.ID)
                state = "yes"
            # If the probablity is from 0.3 to 0.45, and claim it can make this bot win, say yes:
            elif 0.25 <= self.memory_card_array[self.ID, role_ID] < 0.45:
                if type(self_test_result) == set:
                    if self.ID in self_test_result:
                        game_screen.app.game.decide_dict["yes"].append(self.ID)
                        state = "yes"
                    # Else, say no
                    else:
                        game_screen.app.game.decide_dict["no"].append(self.ID)
                        state = "no"
                #If the win condition is not triggered but the confidence and the probability of all player in that role is low, and the bot won't lose all the money if it fails, say yes
                elif not any(game_screen.app.game.players_dict[x].confidence >= 0.4 for x in game_screen.app.game.decide_dict["yes"]) and not self.money == 1 and not np.any(self.memory_card_array[:,role_ID] > 0.3):
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"
                else:
                    game_screen.app.game.decide_dict["no"].append(self.ID)
                    state = "no"

            #If the probability is from 0.1 to 0.25
            elif 0.1 < self.memory_card_array[self.ID, role_ID] < 0.25:
                #If the money is 1, say no immediately
                if self.money == 1:
                    game_screen.app.game.decide_dict["no"].append(self.ID)
                    state = "no"

                #The confidence and probablity of this is lower than the before thresholds
                elif not any(game_screen.app.game.players_dict[x].confidence >= 0.3 for x in game_screen.app.game.decide_dict["yes"]) and not np.any(self.memory_card_array[:,role_ID] > 0.15):
                    game_screen.app.game.decide_dict["yes"].append(self.ID)
                    state = "yes"
            #If the probability is lower than 0.1, say no
            else:
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










        #Add to all the card class a separate activate function to test whether the affected player can win with the effect of the card
        #return "yes" or "no"
    def action(self,game):
        pass


def swap(agent, patient):
    decide = input("Would you actually want to swap?")
    if decide.lower() == "yes":
        agent_card = agent.get_card()
        patient_card = patient.get_card()
        agent.set_card(patient_card)
        patient.set_card(agent_card)
        return
    elif decide.lower() == "no":
        return
def combat(game, first_ID, role_ID):
    dict_for_history = {'mode': 1, 'role': role_ID, "claimers": []}
    #Take the role and the first player claiming's ID
    role_claimed = game.chars_dict[role_ID]
    first = game.players_dict[first_ID]
    game.affected_dict = {'role_ID': role_ID, 'status':0, 'affected': {first_ID}} #This is to update the UI later

    #Add the claimed role ID and the activate
    #Take the role's name
    game.decide_dict = {"yes": [first_ID], "no": []} #This is to save to the history when it has all done
    for i in game.players_dict:
        if i == first_ID:
            continue
        else:
            if game.players_dict[i].type == "human":
                pass ### Fix for player
            elif game.players_dict[i].type == "bot":
                decision = game.players_dict[i].block_decide(game.affected, game.decide_dict) #Return "yes" or "no"

                #Append the bot to the corresponding decision list
                game.decide_dict[decision].append(game.players_dict[i])
                #We won't use the "no" later, so we can remove it inside the decide_dict, but "no" can be added as the supportive information for the bot later, for example, if the most likely player to own that card say no, maybe it can try another way to decide

    #Update all the player inside the "yes" into the affected
    game.affected_dict['affected'].update(game.decide_dict["yes"])

    if len(game.decide_dict["yes"]) == 1:
        role_claimed.activate(first)
        game.affected_dict["status"] = 1

        game.dict_for_history["claimers"].append((first_ID, role_ID))
    else:
        for i in game.decide_dict["yes"]:
            if i.get_card().ID == role_ID:
                role_claimed.activate(i, game)
                game.affected_dict["status"] = 1
                game.decide_dict["yes"].remove(i)

                game.dict_for_history["claimers"].append((i.ID, role_ID))
        ###Consider remove the "yes" with the "affected" but the problem appears when we update the affected when activate it so then the yes, or the affected will be polluted
        for i in game.decide_dict["yes"]:
            i.money =- 1
            #Show the card
            print(f"{i.player_name} is the {i.get_card().name}, not the {role_claimed.name}")
            game.court += 1



