import random
from kivy.clock import Clock

'''
These are steps to update the new character to the game:
-Step 1: Adjust the name, the gender, the lists of success and fail of it.
-Step 2: Let the file game_brain.py and file player_and_action.py import the new character class.
-Step 3: Add the new character class to the female/male list, high_impacts (if it is) and special_activate (if it is), decision_activate (if it is) list.
-Step 4: Code the skill for it:
 +Step 4.1: If it's the skill with no UI required, the activate doesn't need the *args, and we just need to code it in this char.py file
 +Step 4.2: Else, the activate affects the UI, or need for some decision, we will need to add more things to it, so the activate will require the *args, which will be the game_screen, and the character will need to do the check, update UI and also the end turn itself.
-Step 5: Append the affected player after the skill activation to the affected dict
-Step 6: Add appropriate image of the new character to the folder img_chars and img_cards in folder src.
-Step 7: Code for the bot to think about it (add to useless/ high impacts when, and what to raise the decision). Now, we just code the block claim for the character with decision as random, since we dont know what decision will lead to what, so we just need to random select it'''
class Character:
    def __init__(self, name, gender, ID):
        self.gender = gender
        self.name = name
        self.ID = ID


class King(Character):
    name = "king" # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = [
    "The crown bows to none.",
    "Command is my birthright, not a suggestion.",
    "I do not ask. I decree."
]
    list_fail = [
    "A crown without power is but a hollow band.",
    "Even a king may wear a borrowed crown.",
    "The court no longer listens… how tragic."
]

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
    list_success = [
    "The Queen never weeps — only reigns.",
    "A true queen needs no permission to rule.",
    "My grace is more dangerous than any sword."
]
    list_fail = [
    "Oh... perhaps the throne prefers another.",
    "Even royalty has its missteps.",
    "A rose can still be mistaken for a thorn."
]

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
    list_success = [
    "If it's missing, I probably have it.",
    "One blink, and it's mine.",
    "Some treasures walk into my hands."
]
    list_fail = [
    "Guess someone beat me to it...",
    "Curses… my hand was too slow.",
    "Even shadows have eyes, it seems."
]

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
    list_success = [
    "Justice is blind, but never wrong.",
    "Order must be maintained — by any means.",
    "The gavel falls where it must."
]
    list_fail = [
    "Even the gavel errs... sometimes.",
    "Judgment... withheld.",
    "Law bends when truth hides."
]
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
    list_success = [
    "Heaven smiles upon the righteous.",
    "By divine right, I act — not ask.",
    "Even silence echoes with faith."
]
    list_fail = [
    "Even saints may stumble in shadow.",
    "The light eludes me... for now.",
    "I prayed... but no answer came."
]
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
    list_success = [
    "A whisper from me is worth a king’s decree.",
    "Darling, I always get what I want — eventually.",
    "Desire bends even thrones to my will."
]
    list_fail = [
    "Oops. Wrong bed, wrong crown.",
    "Seems charm doesn't fool everyone.",
    "Not all smiles are sharp enough."
]

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
            print("Updating courtesan...")

            # The customers of the Courtesan will reveal to show their gender, also increase the revealed
            game_screen.widgets_dict[the_customer_ID].reveal_card()
            game_screen.app.game.players_dict[the_customer_ID].revealed = len(game_screen.app.game.players_dict) // 2 + 1

            # All the bots will update the customer's card into its memory
            for i in game_screen.app.game.bots_dict:
                game_screen.app.game.bots_dict[i].reveal_update(
                    [(the_customer_ID, game_screen.app.game.players_dict[the_customer_ID].get_card().ID)], "normal")

            Clock.schedule_once(game_screen.widgets_dict[the_customer_ID].hide_card, 2 * game_screen.time_ratio)

            Clock.schedule_once(game_screen.complete_claim, 3 * game_screen.time_ratio)

class Cheat(Character):
    name = "cheat"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "male"
    label_messages = None
    list_success = [
    "The rules? I wrote them.",
    "Winning is just a matter of perspective.",
    "Nothing's fair — unless I say so."
]
    list_fail = [
    "Hah... caught again? How dull.",
    "Well, even I lose... occasionally.",
    "Too clever for my own trick, huh?"
]

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

class Patron(Character):
    name = "patron"
    gender = "male"
    label_messages = None
    list_success = [
    "Gold is loyal when men are not.",
    "My purse speaks louder than any plea.",
    "Fortune favors those who own it."
]
    list_fail = [
    "Even nobles can misplace a coin.",
    "It seems my wealth was but illusion.",
    "A misstep—costly and unbecoming."
]

    def __init__(self,ID):
        super().__init__(Patron.name, Patron.gender, ID)
        self.list_success = Patron.list_success
        self.list_fail = Patron.list_fail
    @classmethod
    def activate(cls, player, game):
        # print(f"{cls.name} triggered")
        player.money += 3
        the_patron_ID = player.ID
        the_recipient_IDs = [player.ID - 1, (player.ID + 1) % len(game.players_dict)]
        for i in the_recipient_IDs:
            if i == -1:
                i = len(game.players_dict) - 1
            game.players_dict[i].money += 1
        #The affected target is the patron and the two recipients
        if -1 in the_recipient_IDs:
            the_recipient_IDs.remove(-1)
            the_recipient_IDs.append(len(game.players_dict) - 1)
        game.affected_dict["affected"].add(the_patron_ID)
        game.affected_dict["affected"].update(the_recipient_IDs)

class Beggar(Character):
    name = "beggar"
    gender = "female"
    label_messages = None
    list_success = [
    "A coin for the lowly? Bless thee!",
    "Even rags have their revenge.",
    "The gutter remembers, good sir."
]

    list_fail = [
    "No mercy for the wretched, then?",
    "The street offers no favors today.",
    "Even pity's well runs dry."
]
    def __init__(self,ID):
        super().__init__(Beggar.name, Beggar.gender, ID)
        self.list_success = Beggar.list_success
        self.list_fail = Beggar.list_fail
    @classmethod
    def activate(cls, player, game):
        # print(f"{cls.name} triggered")
        the_beggar_ID = player.ID
        i = (the_beggar_ID + 1) % len(game.players_dict)
        while i != the_beggar_ID:
            print(i)
            current_player = game.players_dict[i]
            if current_player.money > player.money:
                print("beggared hehe!!!")
                current_player.money -= 1
                player.money += 1
                game.affected_dict["affected"].add(current_player.ID)
            i = (i+1) % len(game.players_dict)
        game.affected_dict["affected"].add(the_beggar_ID)

class Witch(Character):
    name = "witch"
    gender = "female"
    label_messages = None
    list_success = [
    "The stars told me this would be mine.",
    "Spells weave truth where words falter.",
    "The moon obeys no man’s law."
]

    list_fail = [
    "The winds betrayed my whisper.",
    "Magic falters, but only briefly.",
    "The brew soured mid-spell."
]
    def __init__(self,ID):
        super().__init__(Witch.name, Witch.gender, ID)
        self.list_success = Witch.list_success
        self.list_fail = Witch.list_fail
    @classmethod
    def activate(cls, player, game, *args):
        if len(args) != 0:
            game_screen = args[0]
        # print(f"{cls.name} triggered")
        if player.type == "bot":
            decision = game_screen.app.game.players_dict[player.ID].decide_cards(game_screen=game_screen, mode="witch")
            cls.execute(player, decision, game, game_screen)

        elif player.type == "human":
            game_screen.call_for_choose_player("witch", "witch")


    @classmethod
    def execute(cls, player, decision, game, game_screen):
        spell_caster_ID = player.ID

        victim_ID = decision
        a = game_screen.app.game.players_dict[spell_caster_ID].money
        b = game_screen.app.game.players_dict[victim_ID].money

        game_screen.app.game.players_dict[spell_caster_ID].money = b
        game_screen.app.game.players_dict[victim_ID].money = a

        game.affected_dict["affected"].add(spell_caster_ID)
        game.affected_dict["affected"].add(victim_ID)

        player_widget = game_screen.widgets_dict[spell_caster_ID]

        player_widget.give(victim_ID, "potion")
        delete_time = 1.8
        Clock.schedule_once(lambda dt: player_widget.parent.remove_widget(player_widget.object), delete_time * game_screen.time_ratio) #Remove the potion after

        def set_none(dt):
            player_widget.object = None

        Clock.schedule_once(set_none, (delete_time + 0.1) * game_screen.time_ratio)

        Clock.schedule_once(game_screen.complete_claim, (delete_time+0.5) * game_screen.time_ratio)

class Princess(Character):
    name = "princess"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
    gender = "female"
    label_messages = None
    list_success = [
    "Born to rule, not to beg.",
    "Grace alone wins the day.",
    "Nobility is in deed, not birth alone."
]
    list_fail = [
    "A slip, unbecoming of a royal...",
    "Even roses wilt when plucked too soon.",
    "My crown... misplaced, it seems."
]

    def __init__(self, ID):
        super().__init__(Princess.name, Princess.gender, ID)
        self.list_success = Princess.list_success
        self.list_fail = Princess.list_fail
    @classmethod
    def activate(cls, player,game, *args):
        # print(f"{cls.name} triggered")
        player.money += 2

        game.affected_dict["affected"].add(player.ID)

        if len(args) != 0:
            game_screen = args[0]
            # If the princess is triggered not in the test mode but in the normal mode
            if player.type == "bot":
                decision = game_screen.app.game.players_dict[player.ID].decide_cards(game_screen=game_screen, mode="princess")
                cls.execute(player, decision, game, game_screen, "offline")

            elif player.type == "human":
                game_screen.call_for_choose_player("princess", "princess")

    @classmethod
    def execute(cls, player, decision, game, game_screen, mode):
        princess_ID = player.ID

        victim_ID = decision

        others = [j for j in game.players_dict if j != victim_ID]

        player_there = False

        for i in others:
            if game.players_dict[i].type == "human":
                player_there = True

        if mode == "offline":
            for i in others:
                if game.players_dict[i].type == "bot":
                    game.players_dict[i].reveal_update([(victim_ID, game.players_dict[victim_ID].ID)], "normal")



        player_widget = game_screen.widgets_dict[princess_ID]

        player_widget.give(victim_ID, "blue_rose")

        if mode == "offline":
            if player_there:
                game_screen.widgets_dict[victim_ID].reveal_card()

        delete_time = 1.8
        if mode == "offline":
            if player_there:
                Clock.schedule_once(game_screen.widgets_dict[victim_ID].hide_card, 2 * game_screen.time_ratio)

                delete_time += 2
        Clock.schedule_once(lambda dt: player_widget.parent.remove_widget(player_widget.object),
                            delete_time * game_screen.time_ratio)  # Remove the potion after

        def set_none(dt):
            player_widget.object = None

        Clock.schedule_once(set_none, (delete_time + 0.1) * game_screen.time_ratio)

        Clock.schedule_once(game_screen.complete_claim, (delete_time + 0.5) * game_screen.time_ratio)

# class Necromancer(Character):
#     name = "Necromancer"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
#     gender = "male"
#     label_messages = None
#     list_success = [
#     "necro"
# ]
#     list_fail = [
#     "Necro fail"
# ]
#
#     def __init__(self,ID):
#         super().__init__(Necromancer.name, Necromancer.gender, ID)
#         self.list_success = Necromancer.list_success
#         self.list_fail = Necromancer.list_fail
#     @classmethod
#     def activate(cls, player, game):
#         avail_roles = game.selected_avail_roles
#         total_roles = game.female+game.male
#
#         avail_roles_set = set(avail_roles)
#         total_roles_set = set(total_roles)
#         avail_roles_set.intersection_update(avail_roles_set)
#
#         self.graveyard = avail_roles
# class Gangster(Character):
#     name = "gangster"  # these attributes are belong to the class, not global or any alone instance (the instances share these class attributes, and still access as the King.name)
#     gender = "male"
#     label_messages = None ###We can add this for the tie situation
#     list_success = [
#     "Heaven smiles upon the righteous.",
#     "By divine right, I act — not ask.",
#     "Even silence echoes with faith."
# ]
#     list_fail = [
#     "Even saints may stumble in shadow.",
#     "The light eludes me... for now.",
#     "I prayed... but no answer came."
# ]
#     def __init__(self, ID):
#         super().__init__(Gangster.name, Gangster.gender, ID)
#         self.list_success = Gangster.list_success
#         self.list_fail = Gangster.list_fail
#
#
#     @classmethod
#     def activate(cls, player,game):
#         # print(f"{cls.name} triggered")
#         money_dict = {}
#         for i in game.players_dict:
#             money_dict.setdefault(game.players_dict[i].money, []).append(i)
#
#         #Get the max-money-holder list
#         max_money_list = money_dict[max(money_dict)]
#
#         if max(money_dict) == player.money and len(max_money_list) >= 2:
#             max_money_list.remove(player.ID)
#
#         #If only one person on the max list, take 2 coin from them
#         if len(max_money_list) == 1:
#             chosen_ID = max_money_list[0]
#         else:
#             chosen_ID = random.choice(max_money_list)
#         chosen_player = game.players_dict[chosen_ID]
#
#         #Take 2 coins from chosen one
#         chosen_player.money -= 2
#         player.money += 2
#
#         game.affected_dict["affected"].add(player.ID)
#         game.affected_dict["affected"].add(chosen_player.ID)
