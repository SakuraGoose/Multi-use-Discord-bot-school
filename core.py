import os
import random
import time

import aiohttp
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from database import init_db, SQLiteEco

load_dotenv()

Token = os.getenv("Discord_Bot_Token")
economy_db = SQLiteEco()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

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
        bot.status_server_started = True
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

class CoinflipView(discord.ui.View):
    def __init__(self, bet: int, user_id: int, economy_db, *, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.bet = bet
        self.user_id = user_id
        self.economy_db = economy_db
        self.used = False

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.primary)
    async def heads_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This coinflip isn't yours.", ephemeral=True
            )
            return
        await self._resolve(interaction, "Heads")

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.primary)
    async def tails_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This coinflip isn't yours.", ephemeral=True
            )
            return
        await self._resolve(interaction, "Tails")

    async def _resolve(self, interaction: discord.Interaction, choice: str):
        if self.used:
            await interaction.response.defer()
            return
        self.used = True
        result = random.choice(["Heads", "Tails"])
        await self.economy_db.add_balance(self.user_id, -self.bet)
        if choice == result:
            win_amount = self.bet * 2
            await self.economy_db.add_balance(self.user_id, win_amount)
            new_balance = await self.economy_db.get_balance(self.user_id)
            outcome = f"**{result}** — You won! +**{win_amount}** (Balance: **{new_balance}**)"
            color = discord.Color.green()
        else:
            new_balance = await self.economy_db.get_balance(self.user_id)
            outcome = f"**{result}** — You lost **{self.bet}**. (Balance: **{new_balance}**)"
            color = discord.Color.red()
        embed = discord.Embed(
            title="🪙 Coinflip",
            description=f"Bet: **{self.bet}**\nYou chose **{choice}**\n\n{outcome}",
            color=color,
        )
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        if self.used:
            return
        for item in self.children:
            item.disabled = True
        if self.message:
            embed = discord.Embed(
                title="🪙 Coinflip",
                description=f"Bet: **{self.bet}**\n\n*Timed out — pick faster next time!*",
                color=discord.Color.dark_gray(),
            )
            try:
                await self.message.edit(embed=embed, view=self)
            except discord.NotFound:
                pass


@bot.tree.command(name="coinflip", description="Flip a coin - heads or tails (optional bet for 2x payout)")
@app_commands.describe(bet="Amount to bet (leave empty to flip without betting)")
async def coinflip(interaction: discord.Interaction, bet: int | None = None):
    if bet is None:
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"🪙 **{result}**")
        return
    if bet <= 0:
        await interaction.response.send_message("Bet must be positive.", ephemeral=True)
        return
    await economy_db.ensure_user(interaction.user.id)
    balance = await economy_db.get_balance(interaction.user.id)
    if balance < bet:
        await interaction.response.send_message(
            f"Not enough balance. You have **{balance}**.", ephemeral=True
        )
        return
    embed = discord.Embed(
        title="🪙 Coinflip",
        description=f"Bet: **{bet}**\n\nPick your side:",
        color=discord.Color.blue(),
    )
    view = CoinflipView(bet=bet, user_id=interaction.user.id, economy_db=economy_db)
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="balance", description="View a user's balance from the database")
@app_commands.describe(user="The user to check (leave empty for yourself)")
async def balance(interaction: discord.Interaction, user: discord.User | None = None):
    target = user or interaction.user
    await economy_db.ensure_user(target.id)
    balance = await economy_db.get_balance(target.id)
    embed = discord.Embed(
        title=f"{target.display_name}'s balance",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Balance", value=f"**{balance}**", inline=True)
    await interaction.response.send_message(embed=embed)

# --- TESTING ONLY (start) - Remove or disable for production ---
@bot.tree.command(name="admin-balance", description="Admin: give, remove, or set a user's balance")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    action="Action to perform (give, remove, or set)",
    user="The user to modify",
    amount="The amount"
)
@app_commands.choices(action=[
    app_commands.Choice(name="give", value="give"),
    app_commands.Choice(name="remove", value="remove"),
    app_commands.Choice(name="set", value="set"),
])
async def admin_balance(
    interaction: discord.Interaction,
    action: app_commands.Choice[str],
    user: discord.User,
    amount: int,
):
    if amount < 0:
        await interaction.response.send_message("Amount must be positive.", ephemeral=True)
        return
    await economy_db.ensure_user(user.id)
    if action.value == "give":
        await economy_db.add_balance(user.id, amount)
        new_balance = await economy_db.get_balance(user.id)
        await interaction.response.send_message(
            f"Gave **{amount}** to {user.display_name}. New balance: **{new_balance}**"
        )
    elif action.value == "remove":
        await economy_db.add_balance(user.id, -amount)
        new_balance = await economy_db.get_balance(user.id)
        await interaction.response.send_message(
            f"Removed **{amount}** from {user.display_name}. New balance: **{new_balance}**"
        )
    else:
        await economy_db.set_balance(user.id, amount)
        await interaction.response.send_message(
            f"Set {user.display_name}'s balance to **{amount}**"
        )
# --- TESTING ONLY (end) ---

bot.run(Token)