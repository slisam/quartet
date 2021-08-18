import random
from typing import Counter

class Quartet() :

    def __init__(self):
        self.quartet = {}
        self.score = {}
        self.players = ["Anna","Bert","Claudia","Dan"]
        self.player_decks = {}
        self.cards = ["A","B","C","D","E"]
        self.deck =  self.create_deck()
        
    def main(self):
        while True :  
            self.create_deck()
            self.card_distribution( self.deck)
             
            for player in self.players:
                self.display_cards(self.player_decks)   
                self.whos_turn(player)
                self.availables_cards(player, self.player_decks, self.deck)

            break

    def create_deck(self): 
        self.deck = []
        for letter in self.cards:
            [self.deck.append((letter,i)) for i in range(4)]
        return self.deck

    def display_state(self,player_decks):
        for player in player_decks.keys():
            print(player,':', self.display_cards(player_decks[player]))

    def whos_turn(self,player):
        return print("it's {}'s turn".format(player))
    

    def display_cards(self,cards_list):
        for player in self.players:
            extract_list = [c+'-'+str(v) for c, v in cards_list[player]]
            display = player+" : "+', '.join(extract_list).replace(',','')
            print(display)
        return display

    def check_cards_left(self, deck): 
        return len(deck)

    def card_distribution(self,  deck):
        for player in self.players:
            picked_cards = random.sample(deck,4)
            self.player_decks[player]= picked_cards
            [self.deck.remove(x) for x in picked_cards]
        return self.player_decks, self.deck

    def availables_cards(self,player, player_decks, deck):
        available_deck = player_decks.copy()
        available_deck.pop(player)
        available_deck["Deck"] = deck
        player_hand = []
        [player_hand.append(k) for k,v in player_decks[player]] # get the letters of cards owned by the player
        cards_can_be_asked = []
        for decks in available_deck.values():
            for cards in decks : 
                if cards[0] in player_hand :
                    cards_can_be_asked.append(cards)
        nb_cards_to_ask = len(cards_can_be_asked) 
        card_to_ask = random.choice(cards_can_be_asked)
        card_to_ask = "{}-{}".format(*card_to_ask)
        return self.display_asking(player, nb_cards_to_ask,card_to_ask)

    def display_asking(self, player,nb_cards_to_ask,card_to_ask):
        return print("There are {0} cards {1} can ask for \n {1} is asking for {2}".format(nb_cards_to_ask, player, card_to_ask))


    def check_quartet(self, player_decks, deck):
        for player in player_decks.keys():
            self.score[player]= 0
            cards_count = Counter(elem[0] for elem in player_decks[player])
            for letter, count in cards_count.items():
                if count == 4 :
                    self.score[player]+=1
                    print(player,"has a quartet!")
                    print(player,"is putting down", self.display_cards(player_decks[player]))  
                    print(deck)
                    print(self.check_cards_left(player_decks))



if __name__ == '__main__':
    Quartet().main()