# Marvo
Discord ticket bot for a single guild.

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file:
```
DISCORD_TOKEN=your_token_here
DB_HOST=localhost
DB_NAME=marvo
DB_USER=your_user
DB_PASSWORD=your_password
```
4. Edit `config.json` with your staff role ID and ticket categories
5. Run: `python main.py`

## Config
- `panel_style` — `buttons` or `dropdown`
- `categories` — add as many ticket types as you want, each with a `name`, `description`, and `welcome_message`
- `staffroleid` — role ID that gets access to all tickets