from collections import defaultdict
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
        self.ask_log = defaultdict(list)
        
    def main(self):
        self.create_deck()
        self.card_distribution( self.deck)
        for i in range(20) :
            for player in self.players:
                self.display_cards(self.player_decks) 
                self.check_quartet(self.player_decks)  
                self.whos_turn(player)
                self.availables_cards(player, self.player_decks, self.ask_log)
        

    def create_deck(self): 
        self.deck = []
        for letter in self.cards:
            [self.deck.append((letter,i)) for i in range(4)]
        return self.deck

    def whos_turn(self,player):
        return print("it's {}'s turn".format(player))

    def display_cards(self,cards_list):
        for player in cards_list:
            tuple_to_list = [c+'-'+str(v) for c, v in cards_list[player]]
            display_from_list = player+" : "+', '.join(tuple_to_list).replace(',','')
            print(display_from_list)

#test affichage des cartes

    def check_cards_left(self, deck): 
        return len(deck)

    def card_distribution(self,  deck):
        for player in self.players:
            picked_cards = random.sample(deck,5)
            self.player_decks[player]= picked_cards
            [self.deck.remove(x) for x in picked_cards]
        return self.player_decks 

    def availables_cards(self,player, player_decks, ask_log):
        available_deck = player_decks.copy()
        available_deck.pop(player)
        # available_deck["stack"] = deck
        letters_owned = []
        [letters_owned.append(k) for k,v in player_decks[player]] # get the letters of cards owned by the player
        cards_can_be_asked = defaultdict(dict)
        for decks in available_deck:
            for owner, cards in available_deck.items():
                cards_match=[]
                for card in cards:
                    if card[0] in letters_owned :
                        cards_match.append(card)
                cards_can_be_asked[owner]=cards_match
        list_can_be_asked = [cards_can_be_asked[x] for x in cards_can_be_asked if isinstance(cards_can_be_asked[x], list)]
        nb_cards_to_ask = sum([len(cards_can_be_asked[x]) for x in cards_can_be_asked if isinstance(cards_can_be_asked[x], list)])
        for i in range(nb_cards_to_ask):
            card_to_ask = random.choice([item for sublist in list_can_be_asked for item in sublist  ]) # make a flat list to choose random tuple
            player_to_ask = self.players.copy()
            player_to_ask.remove(player)
            player_to_ask = random.choice(player_to_ask)
            print(card_to_ask,ask_log,player_to_ask)
            if card_to_ask in ask_log[player_to_ask]: 
                print("already asked")
                print(card_to_ask,player_to_ask, ask_log)
                continue 
            if card_to_ask:
                #trouver la condition qui permet de sortir de la boucle (joueur possède bien la carte demandée)
                break
            else : 
                print("NOTHIINNNG")
        try :
            display_card_to_ask = "{}-{}".format(*card_to_ask)
            print("There are {0} cards {1} can ask for \n{1} is asking for {2} from {3}".format(nb_cards_to_ask, player, display_card_to_ask,player_to_ask))
            self.check_ask(player_to_ask, card_to_ask,self.player_decks, self.ask_log, player) 
        except IndexError:
            print("{} is out of cards".format(player))
            self.players.remove(player)
            if not self.players:
                self.end_game()

    def end_game(self):  
        print("All players out of cards - game is over!")
        for player, score in self.score.items():
            print("{} has {} quartet(s)".format(player, score))


    def check_quartet(self, player_decks):
        for player in player_decks.keys():
            self.score[player]= 0
            cards_count = Counter(elem[0] for elem in player_decks[player])
            for letter, count in cards_count.items():
                if count == 4 :
                    self.score[player]+=1
                    print(player,"has a quartet!")
                    print(player,"is putting down {}-{}-{}-{}".format(*player_decks[player]))  
                    print(self.check_cards_left(player_decks))

    def check_ask(self,player_to_ask,card_to_ask , player_decks, ask_log, player):
        if card_to_ask in player_decks[player_to_ask]  :
            print("{} gets {}-{} from {}".format(player,*card_to_ask, player_to_ask))
            player_decks[player_to_ask].remove(card_to_ask)
            player_decks[player].append(card_to_ask)
            self.display_cards(self.player_decks)
            self.whos_turn(player)
            self.availables_cards(player, self.player_decks, self.deck)
        if card_to_ask in ask_log[player_to_ask]:
                print("card already asked!")
        else : 
            print("{} does not have {}-{}".format(player_to_ask,*card_to_ask))
            ask_log[player_to_ask].append(card_to_ask)
            return self.ask_log

if __name__ == '__main__':
    Quartet().main()