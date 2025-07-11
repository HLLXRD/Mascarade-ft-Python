import random
import numpy as np
import math
import copy

from .char import Character, Judge, King, Queen, Thief, Bishop, Widow, Courtesan, Cheat, Patron, Beggar, Witch, Princess
from .player_and_action import Player, Bot

#__all__ = ['Character', 'Judge', 'Player', 'Game', 'King', 'Queen', 'Thief', 'Judge']




class Game:
    def __init__(self,*, player_num, human = 1, start_court = 0, game_mode = "offline"):
        self.affected_dict = None
        self.history = []
        self.player_num = player_num
        self.human_num = human
        self.bot_num = player_num - human
        ###FIX THE BUG PLAYER TYPE THE AMOUNT OF HUMAN EXCEEDING THE PLAYER_NUM
        self.court = start_court
        self.game_mode = game_mode

        ###Remember to add Inquisitor and the Cheater to somewhere
        self.total_high_impacts = [King, Widow, Queen, Courtesan, Patron]
        self.high_impacts = []
        ###The special_activate includes Courtesan, Usurper, Inquisitor, Princess, Witch, consider add the Bishop to this list
        self.special_activate = [Courtesan, Witch, Princess]
        ###Male role
        self.male = [Judge, King, Thief, Bishop, Cheat, Patron]
        ###Female role
        self.female = [Queen, Widow, Courtesan, Beggar, Witch, Princess]

        ###This decision_activate is only for the bot player when it has to decide whether it should block a claim or not, and it will include the role that requires player to choose something
        self.decision_activate = [Witch, Princess]

    def game_build(self):
        print("Buiding game....")
        #Setup roles
        roles = Character.__subclasses__() #Get all available roles, not the judge

        #Shuffle players with bot
        players_type = []
        for i in range(self.human_num):
            players_type.append("human")
        for i in range(self.bot_num):
            players_type.append("bot")

        #Only shuffle if the mode is online, so that the first player will always be the player
        if not self.game_mode == "offline" :
            random.shuffle(players_type)

        #Select roles
        roles.remove(Judge) #Remove Judge - the obligatory role for every game to select it directly later
        roles_low_impacts = [x for x in roles if x not in self.total_high_impacts] #Takes the low impacts (or cards without the "take from the bank" function or it cannot steal much money from other players)

        #Selecting the nunber of high_impacts cards
        #The number of high impacts will be a half of the number of player, round down
        high_impacts_number = math.floor(self.player_num/2)
        #If the number of players is 3, it will be 2
        if self.player_num == 3:
            high_impacts_number = 2
        self.selected_roles = [Judge]

        self.selected_roles = self.selected_roles + random.sample(self.total_high_impacts, high_impacts_number)+  random.sample(roles_low_impacts, self.player_num-1 - high_impacts_number) #Ensure that it will always have 2 or more cards with take from the bank

        random.shuffle(self.selected_roles)


        print(f"\n\n\n{self.selected_roles}\n\n\n")

        # Set up the dictionary for impacts
        ###Should check the length of the high_impact, the ad-hoc where the high_impact has no roles, this can make the match becomes cannot win
        selected_set = set(self.selected_roles)
        for i in self.total_high_impacts:
            impact_set = set(self.total_high_impacts)

            intersect_set = impact_set.intersection(selected_set)
            self.high_impacts = list(intersect_set)
        print(self.high_impacts)


        #chars_dict will be in format {<card's ID> : <character_class>}

        #Set up players, characters and a dict to control the bots
        self.players_dict = {}
        self.chars_dict = {}
        self.reversed_chars_dict = {}
        self.bots_dict = {}
        self.player_names_dict = {}

        bot = ["HLLXRD", "Chinh", "Khoo", "Sunsea", "Khoa", "Rmie", "Yukino", "QuanNg"]
        trait = ["OOP", "DSA", "ML", "DL", "IT012", "NMLT", "CS", "AI"]
        bot_names = [b + t for b in bot for t in trait]
        random.shuffle(bot_names)
        for i in range(self.player_num):
            if players_type[i] == "human":
                player_name = next(self.player_names_list)
                card = self.selected_roles[i](i)
                print(f"Welcome {player_name}! Your role is {card.name}.")
                self.players_dict[i] = Player(i, player_name, card, 6, 1, 0)

                #Add the roles to the characters dictionary
                self.chars_dict[card.ID] = card.__class__
                self.reversed_chars_dict[card.__class__] = card.ID

                #Add the player's ID to the dict of IDs with the name of the player as the key
                self.player_names_dict[player_name] = i


            elif players_type[i] == "bot":
                bot_name = bot_names[i]
                card = self.selected_roles[i](i)
                print(f"{bot_name} has arrived with the role {card.name}!")
                self.players_dict[i] = Bot(i, bot_name, card, 6, 1, 0)
                self.bots_dict[i] = self.players_dict[i]

                # Add the roles to the characters dictionary
                self.chars_dict[card.ID] = card.__class__
                self.reversed_chars_dict[card.__class__] = card.ID

                # Add the player's ID to the dict of IDs with the name of the player as the key
                self.player_names_dict[bot_name] = i

        #Initialize the bot's memory dictionary
        base_arr = np.zeros((self.player_num,self.player_num))

        for i in self.players_dict:
            current_card_ID = self.players_dict[i].get_card().ID
            current_player_ID = self.players_dict[i].ID
            base_arr[current_card_ID, current_player_ID] = 1 #this is used for all bots


        for i in self.players_dict:
            if self.players_dict[i].type == "human":
                pass
            elif self.players_dict[i].type == "bot":
                self.players_dict[i].memory_card_array = np.array(base_arr)

        print(self.player_names_dict)




    def take_player_names(self, player_names):
        self.player_names_list = iter(player_names)


    def update(self):
        '''
        History is a list of dicts:

        *Swap: (mode's ID: 0)
        - Format: {"mode": 0, "agent": <agent's ID>, "patient": <patient's ID>}
        - Example: {"mode": 0, "agent": 1, "patient": 2}
        -> Player with ID 1 chooses action 'swap' targeting to player with ID 2.

        *Claim: (mode's ID: 1)
        - Format: {"mode": 1, "role": <role's ID>, "claimers": <IDs of the claimers (integer if only one claimer, else list of tuples)>}
        - Example 1: {"mode": 1, "role": 1, "claimers": [3]}
        -> Player with ID 3 assumes that he is the queen, and everyone agrees with it.
        - Example 2: {"mode": 1, "role": 2, "claimers": [(0,3), (1,2), (3,0)]}
        -> Player with ID 0, 1 and 3 assume to be the Robber (ID 2), but only the 1 is the real one, while 0 is actually the Judge, 3 is actually the King.

        *Peek: (mode's ID:2)
        - Format: {"mode": 2, "player": <player's ID>}
        - Example: {"mode": 2, "player": 1}
        -> Player 1 chooses to peek at his/her card.
        '''
        action_dict = self.history[-1]
        if action_dict["mode"] == 0: #This is to update the swap action of the player
            agent_ID = action_dict["agent"]
            patient_ID = action_dict["patient"]
            agent = self.players_dict[agent_ID]
            patient = self.players_dict[patient_ID]

            #Here, update the confidence with the formula: patient_conf = agent_prev * 0.5 , agent_conf = (agent_prev + patient_prev) * 0.5
            agent_prev = agent.confidence
            patient_prev = patient.confidence
            agent.confidence = (agent_prev + patient_prev) * 0.5
            patient.confidence = (patient_prev) * 0.5

            #Also, since a swap appears, we reset the turn of revealed of the players (both agent and patient)
            agent.revealed = 0
            patient.revealed = 0

            #Update the bots' probability
            for bot_ID in self.bots_dict:
                self.bots_dict[bot_ID].swap_update(agent_ID, patient_ID)

        elif action_dict["mode"] == 2: #This is to update the peek action of the player
            player_ID = action_dict["player"]
            player = self.players_dict[player_ID]
            player.confidence = 1

        elif action_dict["mode"] == 1: #This is to update the claim action of the player
            #For each player revealed card, update the probability
            for bot in self.bots_dict:
                self.bots_dict[bot].reveal_update(action_dict["claimers"], "combat")


            ###maybe /2 is not a good choice, can put this into the setting option?
            if len(action_dict["claimers"]) != 1:
                for player_ID,_ in action_dict["claimers"]:
                    player = self.players_dict[player_ID]
                    player.confidence = 1 #Increase confidence



    def check(self, mode):
        winner = []
        money_dict = {} #Will store a dict with the key is the money, each contains a list of people have that amount of money
        '''Note
        If the win condition matched, return a set of winner: for example {0,1,4}: player with ID 0,1,4 will be the winners
        If not, return 0, the game continues
        '''
        for i in self.affected_dict["affected"]:
            if type(i) == int:
                money_dict.setdefault(self.players_dict[i].money, []).append(i)
        #If there is a 0 inside money_dict, the max wins
        if any(x<=0 for x in money_dict):
            winner = winner + money_dict[max(money_dict)]

        #If there is a 13 or more  inside the money_dict, the 13 holder wins
        for i in money_dict:
            if i >= 13:
                winner = winner + money_dict[i]

        if len(winner) == 0:
            #If the game continue, update the high impact dict if some condition is met
            ###The mode is for the cheater, the widow,...


            return 0

        else:
            return set(winner)

    def test_win_condition(self, player_ID, role_test_ID, bot_player):
        #This is just for the start of the block turn
        #Create a clone of the game so that it can check the win condition now
        clone = Game(
            player_num=self.player_num,
            human=self.human_num,
            start_court=self.court,
            game_mode=self.game_mode
        )

        # Manually copy over state
        clone.players_dict = copy.deepcopy(self.players_dict)
        clone.bots_dict = copy.deepcopy(self.bots_dict)
        clone.chars_dict = copy.deepcopy(self.chars_dict)
        clone.affected_dict = copy.deepcopy(self.affected_dict)
        # clone.high_impacts = copy.deepcopy(self.high_impacts)


        #Specify the role that we want to test now
        role_test = clone.chars_dict[role_test_ID]





        #Specify the player that we will test now
        player = clone.players_dict[player_ID]
        # Since the Courtesan is really special in those chars which is not in the decision activation, so we need to base on the bot's own memory about the first player to define the gender of the next player of the first player
        next_player_ID = (player_ID + 1) % len(clone.players_dict)
        next_player = clone.players_dict[next_player_ID] #This MUST take the next player from the clone, dont put self here

        arr = bot_player.memory_card_array
        row = arr[next_player_ID, :]

        max_prob_role_ID = np.argmax(row)
        max_prob_role = clone.chars_dict[max_prob_role_ID]
        next_player_card = next_player.get_card()
        next_player_card.gender = max_prob_role.gender








        #Activate the affected dict
        role_test.activate(player, clone)
        test_result = clone.check("test")

        return test_result

#1: Lưu trữ hoạt động claim hiện tại vào một phần giải quyết, và phần ảnh hưởng. Phần ảnh hưởng sẽ dùng để check tiền win, và cũng dùng để update gold, update revealed. Phần giải quyết để đưa ra quyết định lúc đó cho bot
#affected_dict để update UI khi có combat, và để check chỉ trong affected điều kiện win
#history để update chung cho bot, cả combat, peek và swap
#decide_dict để ra quyết định cho bot và cũng support update UI vì ta sẽ update tiền trước cho tất cả trong affected, và update card bài cho người trong "yes"


###PLease note that the confidence hasn't contain the situation the peeking situation, for example, players A peeked at her card at the prev turn, and then B swaped with A, even the confidence of A is 1, B still dont know anything about that card so his confidence cannot be raised from A's
###The cards probability doesn't consider the situation of the inequality between the roles, for example, the probability that the King is selected (swapped) is not 50% but maybe 80%
###Currently, if the player is agreed by everyone to be a role, that maybe a bluff, but it should at least raise the probability of that player to be that role actually a little bit, this hasn't been included
###If else the bot so that the Cheater always be blocked, maybe the checking the win condition
###The decide function hasn't had the cross-decide: When a player with the high confidence and/or high probability try to block a claimation, the bot will stop trying to block it, too
###The action decide player hasnt considered whether the claim affects their money or not, if a call is useless, maybe they should peek or swap (bishop's or widow's case)
if __name__ == "__main__":
    game=Game(player_num=3, human = 1)
    game.take_player_names(["hohoho!"])
    game.game_build()
    game.history.append({"mode": 0, "agent": 1, "patient": 2})
    game.update()
    for i in game.bots_dict:
        print(game.bots_dict[i].memory_card_array)
    print(game.players_dict[1].confidence, game.players_dict[2].confidence)
    # for i in game.bots_dict:
    #     game.bots_dict[i].reveal_update([(1,2), (0,3)])
    #     print(game.bots_dict[i].memory_card_array)

