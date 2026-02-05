import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from database import init_db, EconomyRepoFactory

load_dotenv()

Token = os.getenv("Discord_Bot_Token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
eco_repo = EconomyRepoFactory.create()

@bot.event
async def on_ready():
    await bot.tree.sync()
    await init_db()
    print(f"logged in as {bot.user}")

@bot.tree.command(name="8ball", description="Ask the magic 8ball a question")
@app_commands.describe(question="The question you want to ask")

async def eight_ball(interaction: discord.Interaction, question: str):
    response = ["Yes","No","Maybe","I don't Know", "Ask your mom"]
    answer = random.choice(response)
    
    await interaction.response.send_message(f"**Question: ** {question} \n**Answer: ** {answer}"
    )

@bot.tree.command(name="ping", description="Ping the bot")

async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="balance", description="Check your balance")

async def balance(interaction: discord.Interaction):
    user_id = interaction.user.id

    await eco_repo.ensure_user(user_id)

    balance = await eco_repo.get_balance(user_id)

    await interaction.response.send_message(
        f"**Money in wallet:** ${balance}"
    )

@bot.tree.command(name="bank", description="Check your balance")

async def bank(interaction: discord.Interaction):
    user_id = interaction.user.id

    await eco_repo.ensure_user(user_id)

    bank = await eco_repo.get_bank(user_id)

    await interaction.response.send_message(
        f"**Account balance:** ${bank}"
    )




bot.run(Token)