import os
import random
import time

import aiohttp
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from database import init_db, EconomyRepoFactory, SQLiteEco

load_dotenv()

Token = os.getenv("Discord_Bot_Token")
economy_db = SQLiteEco()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
eco_repo = EconomyRepoFactory.create()

# --- (Start) Bot status and uptime variables built for the hosted version of the bot, via Sparked hosting. ---
bot_status = {"online": False}
start_time: float | None = None


async def shields_app():
    app = web.Application()

    async def badge(request: web.Request):
        if bot_status["online"]:
            payload = {
                "schemaVersion": 1,
                "label": "Bot status",
                "message": "Online",
                "color": "brightgreen",
            }
        else:
            payload = {
                "schemaVersion": 1,
                "label": "Bot status",
                "message": "Offline",
                "color": "red",
            }
        return web.json_response(payload)

    async def uptime(request: web.Request):
        if not bot_status["online"] or start_time is None:
            msg = "offline"
            color = "lightgrey"
        else:
            seconds = int(time.time() - start_time)
            days, rem = divmod(seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, _ = divmod(rem, 60)
            if days > 0:
                msg = f"{days}d {hours}h"
            elif hours > 0:
                msg = f"{hours}h {minutes}m"
            else:
                msg = f"{minutes}m"
            color = "brightgreen"

        payload = {
            "schemaVersion": 1,
            "label": "Uptime",
            "message": msg,
            "color": color,
        }
        return web.json_response(payload)

    app.router.add_get("/badge", badge)
    app.router.add_get("/uptime", uptime)
    return app


async def start_status_server():
    app = await shields_app()
    runner = web.AppRunner(app)
    await runner.setup()
    # This is built only for the hosted version of the bot, via Sparked hosting.
    # So this will not work on the local running version.
    site = web.TCPSite(runner, host="0.0.0.0", port=25709)
    await site.start()
    print("Shields status server running at http://0.0.0.0:25709/badge")


@bot.event
async def on_connect():
    global start_time
    bot_status["online"] = True
    start_time = time.time()


@bot.event
async def on_ready():
    bot_status["online"] = True
    if not getattr(bot, "status_server_started", False):
        bot.loop.create_task(start_status_server())
        bot.Status_server_started = True
    await bot.tree.sync()
    await init_db()
    print(f"logged in as {bot.user}")


@bot.event
async def on_resumed():
    bot_status["online"] = True


@bot.event
async def on_disconnect():
    bot_status["online"] = False

# --- (End) Bot status and uptime variables built for the hosted version of the bot, via Sparked hosting. ---

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

# @bot.tree.command(name="atm", description="Withdraw or deposit money")
# @app_commands.choices(action[
#     app_commands.Choice(name="Withdraw", value="Withdraw"),
#     app_commands.Choice(name="Deposit", value="Deposit")
# ])

@bot.tree.command(name="bank", description="Check your balance")
async def bank(interaction: discord.Interaction):
    user_id = interaction.user.id

    await eco_repo.ensure_user(user_id)

    bank = await eco_repo.get_bank(user_id)

    await interaction.response.send_message(
        f"**Account balance:** ${bank}"
    )




bot.run(Token)