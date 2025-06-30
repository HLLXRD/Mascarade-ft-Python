import random

class Character:
    def __init__(self, name, gender, ID):
        self.gender = gender
        self.name = name
        self.ID = ID


class King(Character):
    name = "king" # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = ["King success"]
    list_fail = ["King fail"]

    def __init__(self,ID):
        super().__init__(King.name, King.gender, ID)
        self.list_success = King.list_success
        self.list_fail = King.list_fail

    @classmethod
    def activate(cls, player,game):
        # print(f"{cls.name} triggered")
        player.money += 3
        game.affected_dict["affected"].add(player.ID)

class Queen(Character):
    name = "queen"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "female"
    label_messages = None
    list_success = ["Queen success"]
    list_fail = ["Queen fail"]
    def __init__(self, ID):
        super().__init__(Queen.name, Queen.gender, ID)
        self.list_success = Queen.list_success
        self.list_fail = Queen.list_fail
    @classmethod
    def activate(cls, player,game):
        # print(f"{cls.name} triggered")
        player.money += 2

        game.affected_dict["affected"].add(player.ID)

class Thief(Character):
    name = "thief"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = ["Thief success"]
    list_fail = ["Thief fail"]

    def __init__(self,ID):
        super().__init__(Thief.name, Thief.gender, ID)
        self.list_success = Thief.list_success
        self.list_fail = Thief.list_fail
    @classmethod
    def activate(cls, player, game):
        # print(f"{cls.name} triggered")
        player.money += 2
        the_thief_ID = player.ID
        the_stolen_IDs = [player.ID - 1, (player.ID + 1) % len(game.players_dict)]
        for i in the_stolen_IDs:
            if i == -1:
                i = len(game.players_dict) - 1
            game.players_dict[i].money -= 1
        #The affected target is the thief and two robbered players
        if -1 in the_stolen_IDs:
            the_stolen_IDs.remove(-1)
            the_stolen_IDs.append(len(game.players_dict) - 1)
        game.affected_dict["affected"].add(the_thief_ID)
        game.affected_dict["affected"].update(the_stolen_IDs)

class Judge(Character):
    name = "judge"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = ["Judge success"]
    list_fail = ["Judge fail"]
    def __init__(self,ID):
        super().__init__(Judge.name, Judge.gender, ID)
        self.list_success = Judge.list_success
        self.list_fail = Judge.list_fail
    @classmethod
    def activate(cls, player, game):
        # print(f"{cls.name} triggered")
        player.money += game.court
        # player.money = 15
        game.court = 0

        ###minus money code here
        game.affected_dict["affected"].add(player.ID)
        game.affected_dict["affected"].add("court")


class Widow(Character):
    name = "widow"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "female"
    label_messages = None
    list_success = ["Widow success"]
    list_fail = ["Widow fail"]
    def __init__(self, ID):
        super().__init__(Widow.name, Widow.gender, ID)
        self.list_success = Widow.list_success
        self.list_fail = Widow.list_fail
    @classmethod
    def activate(cls, player,game):
        # print(f"{cls.name} triggered")
        if player.money < 10:
            player.money = 10
        game.affected_dict["affected"].add(player.ID)



class Bishop(Character):
    name = "bishop"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None ###We can add this for the tie situation
    list_success = ["Bishop success"]
    list_fail = ["Bishop fail"]
    def __init__(self, ID):
        super().__init__(Bishop.name, Bishop.gender, ID)
        self.list_success = Bishop.list_success
        self.list_fail = Bishop.list_fail


    @classmethod
    def activate(cls, player,game):
        # print(f"{cls.name} triggered")
        money_dict = {}
        for i in game.players_dict:
            money_dict.setdefault(game.players_dict[i].money, []).append(i)

        #Get the max-money-holder list
        max_money_list = money_dict[max(money_dict)]

        if max(money_dict) == player.money and len(max_money_list) >= 2:
            max_money_list.remove(player.ID)

        #If only one person on the max list, take 2 coin from them
        if len(max_money_list) == 1:
            chosen_ID = max_money_list[0]
        else:
            chosen_ID = random.choice(max_money_list)
        chosen_player = game.players_dict[chosen_ID]

        #Take 2 coins from chosen one
        chosen_player.money -= 2
        player.money += 2

        game.affected_dict["affected"].add(player.ID)
        game.affected_dict["affected"].add(chosen_player.ID)
class Courtesan(Character):
    name = "courtesan"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "female"
    label_messages = None
    list_success = ["Courtesan success"]
    list_fail = ["Courtesan fail"]

    def __init__(self,ID):
        super().__init__(Courtesan.name, Courtesan.gender, ID)
        self.list_success = Courtesan.list_success
        self.list_fail = Courtesan.list_fail
    @classmethod
    def activate(cls, player, game, *args):
        # print(f"{cls.name} triggered")
        the_courtesan_ID = player.ID
        the_customer_ID = (the_courtesan_ID + 1) % len(game.players_dict)

        if game.players_dict[the_customer_ID].get_card().gender == "male":
            game.players_dict[the_customer_ID].money -= 3
            player.money += 3
        #The affected target is the courtesan and her customer
        game.affected_dict["affected"].add(the_courtesan_ID)
        game.affected_dict["affected"].add(the_customer_ID)


        #If there is UI, show the cards

        #Update the UI to show the cards
        if len(args) != 0:
            print("courtesan condition met")
            game_screen = args[0]
            game_screen.special_activate_UI('courtesan', the_customer_ID)

class Cheat(Character):
    name = "cheat"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = ["Cheat success"]
    list_fail = ["Cheat fail"]

    def __init__(self,ID):
        super().__init__(Cheat.name, Cheat.gender, ID)
        self.list_success = Cheat.list_success
        self.list_fail = Cheat.list_fail
    @classmethod
    def activate(cls, player, game):
        # print(f"{cls.name} triggered")
        if player.money >= 10:
            player.money = 13
        #The affected target is the courtesan and her customer
        game.affected_dict["affected"].add(player.ID)

### Necromancer, Gambler, Chester, Cheater