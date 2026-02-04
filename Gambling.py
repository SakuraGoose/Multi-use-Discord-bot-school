import random
import discord
from discord.ext import commands
from discord import app_commands
from abc import ABC, abstractmethod

class Gambling(ABC):
    def __init__(self,user_id:int, bet:int):
        self.bet = bet 
        self.user = user_id

    def valid_bet(bet, balance:int): # waiting for get balance function

    def win(self,bonus:float = 2): 
        return int(self.bet * bonus)
    
    def lose(self):
        return -self.bet 
    @abstractmethod
    def play(self):
        """Must return (result_text, payout)"""
        pass 

