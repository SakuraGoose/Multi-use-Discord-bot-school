<p align="center">
  <strong># Hugo's Au Pair</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/endpoint?url=https://shieldsio.sparked.network/badge" alt="Bot status">
  <img src="https://img.shields.io/endpoint?url=https://shieldsio.sparked.network/uptime&cacheSeconds=60" alt="Bot uptime">
</p>

<p align="center">
  A multi-use Discord bot with economy, games, and fun commands.
</p>

---

## Commands

| Command | Description |
|--------|-------------|
| `/ping` | Check if the bot is online. |
| `/8ball <question>` | Ask the magic 8ball a question. |
| `/coinflip [bet]` | Flip a coin — heads or tails. Optional bet for 2× payout. |
| `/balance [user]` | View a user's balance from the database. |
| `/admin-balance <action> <user> <amount>` | *(Admins only)* Give, remove, or set a user's balance. |

### Command details

- **`/ping`** — Replies with "Pong!"
- **`/8ball <question>`** — Ask the magic 8ball a question.
- **`/coinflip [bet]`** — Flip a coin. Add a bet amount to wager for 2× payout (Heads/Tails buttons).
- **`/balance [user]`** — View your or another user's balance (embed).
- **`/admin-balance`** — *(Testing only, admins)* Actions: `give`, `remove`, `set` — e.g. give 100 to a user.

---

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your Discord bot token:
   ```
   Discord_Bot_Token=your_token_here
   ```
3. Run the bot:
   ```bash
   python core.py
   ```
