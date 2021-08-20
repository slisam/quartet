from collections import defaultdict
import random
import sys


class Quartet:
    def __init__(self):
        self.quartet = {}
        self.score = {}
        self.requestable_cards = {}
        self.player_decks = {}
        self.players = ["Anna", "Bert", "Claudia", "Dan"]
        self.cards = ["A", "B", "C", "D", "E"]
        self.deck = self.create_deck()
        self.ask_log = defaultdict(list)

    def main(self):
        self.create_deck()
        self.card_distribution(self.deck, self.score)
        game = True
        while game is True:
            for player in self.players:
                self.display_cards(self.player_decks)
                self.cards_to_ask(self.players, self.player_decks)
                self.check_quartet(self.player_decks, player)
                self.whos_turn(player)
                self.draw_card(
                    player, self.player_decks, self.ask_log, self.requestable_cards
                )

    def create_deck(self):
        """ generate a deck of 4 cards by letters defined in self.cards """
        self.deck = []
        for letter in self.cards:
            [self.deck.append((letter, num)) for num in range(4)]
        return self.deck

    def card_distribution(self, deck, score):
        """randomly distribute cards equally between players"""
        for player in self.players:
            score[player] = 0
            picked_cards = random.sample(deck, 5)
            self.player_decks[player] = picked_cards
            [self.deck.remove(x) for x in picked_cards]
        return self.player_decks

    def whos_turn(self, player):
        """print the player who's playing"""
        return print("it's {}'s turn".format(player))

    def display_cards(self, cards_list):
        """turn tuple into a prettier print"""
        for player in cards_list:
            tuple_to_list = [c + "-" + str(v) for c, v in cards_list[player]]
            display_from_list = (
                player + " : " + ", ".join(tuple_to_list).replace(",", "")
            )
            print(display_from_list)

    def cards_to_ask(self, players, player_decks):
        letters_owned = {}
        for player in players:
            all_cards = player_decks.copy()
            letters_owned[player] = list(
                set([card[0][0] for card in all_cards[player]])
            )
            all_cards.pop(player)
            self.requestable_cards[player] = [
                card
                for card_list in all_cards.values()
                for card in card_list
                if card[0] in letters_owned[player]
            ]  # keep only cards that match with letters owned
        return self.requestable_cards, letters_owned

    def draw_card(self, player, player_decks, ask_log, requestable_cards):
        """
        determine wich card to ask and log it to avoid same asking
        
        Parameters:
        player (str): Player who's playing this turn

        player_decks (dict): All player's cards

        ask_log (dict): All card's asked at the wrong player

        requestable_cards (dict): Cards that can be ask by the player of this turn

        Returns:
        int:Returning value
        """
        list_can_be_asked = requestable_cards[player]
        nb_cards_to_ask = len(list_can_be_asked)
        if nb_cards_to_ask == 0:
            print("{} is out of cards".format(player))
            self.players.remove(player)
            self.end_game(self.players, self.score)
            return self.players
        print("There are {0} cards {1} can ask for".format(nb_cards_to_ask, player))
        for i in range(15):
            card_to_ask = random.choice([card for card in list_can_be_asked])
            display_card_to_ask = "{}-{}".format(*card_to_ask)
            player_to_ask = self.players.copy()
            player_to_ask.remove(player)
            player_to_ask = random.choice(player_to_ask)
            if len(ask_log) == 0 or [player_to_ask] not in ask_log[player_to_ask]:
                break
            else:
                break
        print(
            "{} is asking for {} from {}".format(
                player, display_card_to_ask, player_to_ask
            )
        )
        if card_to_ask in player_decks[player_to_ask]:
            print("{} gets {}-{} from {}".format(player, *card_to_ask, player_to_ask))
            player_decks[player_to_ask].remove(card_to_ask)
            player_decks[player].append(card_to_ask)
            self.check_quartet(player_decks, player)
            self.display_cards(self.player_decks)
            self.whos_turn(player)
            self.draw_card(player, self.player_decks, self.deck, self.requestable_cards)
        if card_to_ask not in player_decks[player_to_ask]:
            print("{} does not have {}-{}".format(player_to_ask, *card_to_ask))
            self.ask_log[player_to_ask].append(card_to_ask)
            return self.ask_log
        print(
            "{} is asking for {} from {}".format(
                player, display_card_to_ask, player_to_ask
            )
        )
        for player in self.players:
            if not player_decks[player]:
                print("{} is out of cards".format(player))
                self.players.remove(player)
                self.end_game(self, self.players, self.score)

    def check_quartet(self, player_decks, player):
        """check if a player have 4 cards of the same type to remove from the deck and score 1 point"""
        letters_owned = [card[0][0] for card in player_decks[player]]
        for letter in self.cards:
            if letters_owned.count(letter) == 4:
                self.score[player] += 1
                print(player, "has a quartet!")
                quartet_cards = []
                for cards in player_decks[player]:
                    if cards[0] == letter:
                        quartet_cards.append(cards)
                        player_decks[player].remove(cards)
                down = [letter + "-" + str(i) for i in range(4)]
                print(player, "is putting down {} {} {} {}".format(*down))

    def end_game(self, players, score):
        if len(players) == 0:
            print("Player out of cards - game is over!")
            for player, score in self.score.items():
                print("{} has {} quartet(s)".format(player, score))
            return sys.exit(0)


if __name__ == "__main__":
    Quartet().main()
