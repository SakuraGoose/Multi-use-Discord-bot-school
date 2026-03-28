<h1 align="center">Hugo's Au Pair</h1>
<p align="center">
  This project is a school project, for the purpose of Polymorphism. The bot is not made for production in mind, and will not be maintained.
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

2. Create a `.env` file with your Discord bot token and MySQL credentials:
   ```
   Discord_Bot_Token=your_token_here
   
   MYSQL_HOST=your_mysql_host
   MYSQL_PORT=3306
   MYSQL_USER=your_database_user
   MYSQL_PASSWORD=your_database_password
   MYSQL_DATABASE=your_database_name
   ```

3. Run the bot:
   ```bash
   python core.py
   ```

The bot will automatically connect to your MySQL database and create the necessary tables.

