import random
import discord
from discord.ext import commands
from discord import app_commands
from abc import ABC, abstractmethod

class Gambling(ABC):
    def __init__(self,user_id:int, bet:int):
        self.bet = bet 
        self.user = user_id

#    def valid_bet(bet, balance:int): # waiting for get balance function


    def win(self,bonus:float = 2): 
        return int(self.bet * bonus)
    
    def lose(self):
        return -self.bet 
    
    @abstractmethod
    def play(self) -> (result_text: str, payout:int):
        """Must return (result_text, payout)"""
        pass 

class Coinfilp(Gambling): 
    def __init__(self, user_id: int, bet:int, choice:str):
        super().__init__(user_id, bet)
        self.choice = choice.lower()
    def play(self):
        coin = random.choice(["heads", "tails"])
        if self.choice == coin:
            payout = self.win()
            return f"🪙 Coin landed on **{coin}**. You won {payout}!", payout
        else:
            payout = self.lose()
            return f"🪙 Coin landed on **{coin}**. You lost.", payout
        
class Dice(Gambling): 
    def play(self): 
        roll = random.randint(1,100)
        if roll >= 96:
            payout = self.win(5)
            return f"🎲 You rolled a **{roll}**. You won big time! {payout}", payout
        elif roll >= 61:
            payout = self.win(2)
            return f"🎲 You rolled a **{roll}**. You won! {payout}", payout
        else:
            payout = self.lose()
            return f"🎲 You rolled a **{roll}**. You lost.", payout
class BlackJack(Gambling):
    card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    
    @staticmethod
    def card_value(card: list):
        if card[0] in ['Jack', 'Queen', 'King']:
            return 10
        elif card[0] == 'Ace':
            return 11
        else:
            return int(card[0])
    

    def calculate_score(self, cards):
        score = sum(self.card_value(card) for card in cards)
        # Handle aces: if score > 21 and we have aces, count aces as 1
        aces = sum(1 for card in cards if card[0] == 'Ace')
        while score > 21 and aces > 0:
            score -= 10  # Change ace from 11 to 1
            aces -= 1
            return score
        player_score = self.calculate_score(player_card)
        dealer_score = self.calculate_score(dealer_card)
        if player_score == 21 and dealer_score != 21:
            payout = self.win(2.5)  # Blackjack pays 3:2
            return f"🃏 **Blackjack!** You got {player_card[0][0]} of {player_card[0][1]} and {player_card[1][0]} of {player_card[1][1]} (21). Dealer has {dealer_card[0][0]} of {dealer_card[0][1]} and {dealer_card[1][0]} of {dealer_card[1][1]} ({dealer_score}). You won {payout}!", payout
        elif dealer_score == 21:
            pass
    
    random.shuffle(deck)
    player_card = [deck.pop(), deck.pop()]
    dealer_card = [deck.pop(), deck.pop()]
    def play(self):

        if player_card > dealer_card:
            payout = self.win(2)
            return f"🃏 You got a **{player_card}** and the dealer got a **{dealer_card}**. You won! {payout}", payout
        elif player_card == dealer_card:
            return f"🃏 You got a **{player_card}** and the dealer got a **{dealer_card}**. It's a tie! No win or loss.", 0
        elif: player_card < dealer_card
            payout = self.lose()
            return f"🃏 Dealer won with {dealer_cards[0][0]} of {dealer_cards[0][1]} and {dealer_cards[1][0]} of {dealer_cards[1][1]}. You lost.", payout

        while dealer_score < 17:
            new_card = deck.pop()
            dealer_cards.append(new_card)
            dealer_score = self.calculate_score(dealer_cards)
        
        # Determine winner
        if dealer_score > 21:
            payout = self.win()
            return f"🃏 Dealer busted! Your cards: {', '.join(f'{c[0]} of {c[1]}' for c in player_cards)} ({player_score}). Dealer: {', '.join(f'{c[0]} of {c[1]}' for c in dealer_cards)} ({dealer_score}). You won {payout}!", payout
        elif player_score > dealer_score:
            payout = self.win()
            return f"🃏 You win! Your cards: {', '.join(f'{c[0]} of {c[1]}' for c in player_cards)} ({player_score}). Dealer: {', '.join(f'{c[0]} of {c[1]}' for c in dealer_cards)} ({dealer_score}). You won {payout}!", payout
        elif dealer_score > player_score:
            payout = self.lose()
            return f"🃏 Dealer wins! Your cards: {', '.join(f'{c[0]} of {c[1]}' for c in player_cards)} ({player_score}). Dealer: {', '.join(f'{c[0]} of {c[1]}' for c in dealer_cards)} ({dealer_score}). You lost.", payout
        else:
            return f"🃏 Push! Your cards: {', '.join(f'{c[0]} of {c[1]}' for c in player_cards)} ({player_score}). Dealer: {', '.join(f'{c[0]} of {c[1]}' for c in dealer_cards)} ({dealer_score}). It's a tie.", 0

class GamblingFactory():
    pass