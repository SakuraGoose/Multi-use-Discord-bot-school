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
    def play(self):
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
        