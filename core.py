import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Token = os.getenv("Discord_Bot_Token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"logged in as {bot.user}")

@bot.tree.command(name="8ball", description="Ask the magic 8ball a question")
@app_commands.describe(question="The question you want to ask")

async def eight_ball(interaction: discord.Interaction, question: str):
    response = ["Yes","No","Maybe","Unknown"]
    answer = random.choice(response)
    
    await interaction.response.send_message(f"**Question:** {question} \n** {answer}"
    )

bot.run(Token)