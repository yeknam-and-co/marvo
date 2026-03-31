import discord
from discord.ext import commands, tasks
from time import time
from helpers.db import get_ticket, update_last_message, get_inactive_tickets, delete_ticket
import asyncio
class TicketMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_inactive.start()

    def cog_unload(self):
        self.check_inactive.cancel()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        ticket = await get_ticket(self.bot.conn, message.channel.id)
        if ticket:
            await update_last_message(self.bot.conn, message.channel.id)

    @tasks.loop(minutes=30)
    async def check_inactive(self):
        threshold = int(time()) - 86400
        tickets = await get_inactive_tickets(self.bot.conn, threshold)
        for ticket in tickets:
            channel_id = ticket[0]
            for guild in self.bot.guilds:
                channel = guild.get_channel(channel_id)
                if channel:
                    await channel.send("This ticket has been inactive for 24 hours and will now be closed.")
                    await asyncio.sleep(5)

                    await channel.delete()
            await delete_ticket(self.bot.conn, channel_id)

    @check_inactive.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TicketMonitor(bot))
