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
            self.card_distribution(self.player_decks, self.deck)
            self.check_quartet(self.player_decks, self.deck)


    def create_deck(self): 
        deck = []
        for letter in self.cards:
            [deck.append((letter,i)) for i in range(4)]
        return deck

    def display_state(self,player_decks):
        for player in player_decks.keys():
            print(player,':', self.display_cards(player_decks[player]))

    def display_cards(self,cards_list):
        extract_list = [c+'-'+str(v) for c, v in cards_list]
        display = ', '.join(extract_list).replace(',','')
        return display

    def check_cards_left(self, deck): 
        return len(deck)

    def card_distribution(self, player_deck, deck):
        for player in self.players:
            picked_cards = random.sample(deck,4)
            self.player_decks[player]= picked_cards
            [self.deck.remove(x) for x in picked_cards]
        return self.player_decks, self.deck

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