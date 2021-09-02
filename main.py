import random
import sys


class Quartet:
    def __init__(self):
        self.deck = []
        self.score = {}
        self.players = ["Anna", "Bert", "Claudia", "Dan"]
        self.player_decks = {}
        self.cards = ["A", "B", "C", "D", "E"]
        self.player = random.choice(self.players)  # player who is playing the turn
        self.requestable_cards = {}

    def run(self):
        """run the game"""
        self.create_deck()
        self.card_distribution()
        running_game = True
        while running_game:
            self.check_quartet(self.player_decks, self.player)
            self.display_cards(self.player_decks)
            self.whos_turn(self.player)
            self.cards_can_be_asked(self.players, self.player_decks)
            self.card_asking(self.requestable_cards, self.player)
            self.card_exchange(
                card_to_ask, player_to_ask, self.player, self.player_decks
            )

    def create_deck(self):
        """ generate a deck of 4 cards for each letters defined in self.cards """
        self.deck = []
        for letter in self.cards:
            for num in range(4):
                self.deck.append((letter, num))

    def card_distribution(self):
        """ randomly distribute cards equally between players """
        for player in self.players:
            self.score[player] = 0
            picked_cards = random.sample(self.deck, 5)
            self.player_decks[player] = picked_cards
            [self.deck.remove(x) for x in picked_cards]

    def check_quartet(self, player_decks, player):
        """
        check if a player have 4 cards of the same type to remove
        from the deck and score 1 point
        """
        letters_owned = [card[0][0] for card in player_decks[player]]
        for letter in self.cards:
            if letters_owned.count(letter) == 4:
                self.score[player] += 1
                print(player, "has a quartet!")
                quartet_cards = []
                for cards in player_decks[player]:
                    if cards[0] == letter:
                        quartet_cards.append(cards)
                player_decks[player] = [
                    card for card in player_decks[player] if card not in quartet_cards
                ]  # remove quartet cards from player hand
                down = [letter + "-" + str(i) for i in range(4)]
                print(player, "is putting down {} {} {} {}".format(*down))
        if len(player_decks[player]) == 0:
            self.end_game(player, self.score)

    def display_cards(self, player_decks):
        """ turn tuple into a prettier print """
        for player in player_decks:
            tuple_to_list = [c + "-" + str(v) for c, v in player_decks[player]]
            display_from_list = (
                player + " : " + ", ".join(tuple_to_list).replace(",", "")
            )
            print(display_from_list)

    def whos_turn(self, player):
        """ print the player who's playing """
        return print("It's {}'s turn".format(player))

    def cards_can_be_asked(self, players, player_decks):
        """ return only cards that can be asked by the actual player """
        letters_owned = {}
        for player in players:
            all_cards = player_decks.copy()
            letters_owned[player] = list(
                set([card[0][0] for card in all_cards[player]])
            )  # extract only card letters owned by each player
            all_cards.pop(player)
            self.requestable_cards[player] = [
                card
                for card_list in all_cards.values()
                for card in card_list
                if card[0] in letters_owned[player]
            ]  # keep only cards that match with letters owned

    def card_asking(self, requestable_cards, player):
        """ Randomly ask a card within requestable_cards and print it """
        list_can_be_asked = requestable_cards[player]
        nb_cards_to_ask = len(list_can_be_asked)
        if nb_cards_to_ask == 0:
            return self.end_game(player, self.score)
        print("There are {0} cards {1} can ask for".format(nb_cards_to_ask, player))
        global card_to_ask, player_to_ask, display_card_to_ask  # globals var to reuse it this turn
        card_to_ask = random.choice([card for card in list_can_be_asked])
        display_card_to_ask = "{}-{}".format(*card_to_ask)
        player_to_ask = self.players.copy()
        player_to_ask.remove(player)
        player_to_ask = random.choice(player_to_ask)
        print(
            "{} is asking for {} from {}".format(
                player, display_card_to_ask, player_to_ask
            )
        )

    def card_exchange(self, card_to_ask, player_to_ask, player, player_decks):
        """ Check if the requested card is owned by the asked player

        Args
        ----------
        card_to_ask : tuple
            Number and letter of card asked by the actual player to another
        player_to_ask : str
            The name of the player asked
        player : str
            The name of the actual player
        player_decks : dict
            All players with there cards owned

        Returns
        -------
        print:
            If the asked player has card, print the exchange,
            remove card from his hand and add it to the actual player
            Else, print he doesn't have the card and change the player's turn
        """
        if card_to_ask in player_decks[player_to_ask]:
            print("{} gets {}-{} from {}".format(player, *card_to_ask, player_to_ask))
            player_decks[player_to_ask].remove(card_to_ask)
            player_decks[player].append(card_to_ask)
        else:
            print("{} does not have {}-{}".format(player_to_ask, *card_to_ask))
            self.player = player_to_ask

    def end_game(self, player, score):
        """ print when a player has ended the game. If he's the last one, print the score"""
        print("{} is out of cards".format(player))
        try:
            self.players.remove(player)
        except ValueError:  # in case of all players are already deleted
            pass
        if len(self.players) == 0:
            print("All players out of cards - game is over!")
            for player, score in self.score.items():
                print("{} has {} quartet(s)".format(player, score))
            return sys.exit(0)
        self.player = random.choice(self.players)


if __name__ == "__main__":
    Quartet().run()
