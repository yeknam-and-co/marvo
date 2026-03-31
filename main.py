import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from helpers.db import create_connection, create_table
from helpers.close import TicketView

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    await bot.tree.sync()
    print(f'logging in as marvo')

async def load_cogs():
    for folder in ['cogs', 'events']:
        for filename in os.listdir(f'./{folder}'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'{folder}.{filename[:-3]}')
                    print(f'Loaded: {folder}/{filename[:-3]}')
                except Exception as e:
                    print(f'Failed to load {folder}/{filename[:-3]}: {e}')

async def main():
    bot.conn = await create_connection()
    await create_table(bot.conn)
    await load_cogs()
    await bot.start(discord_token)

if __name__ == "__main__":
    asyncio.run(main())
