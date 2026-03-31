import discord
from discord.ext import commands
from helpers.db import get_user_tickets, delete_ticket

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        tickets = await get_user_tickets(self.bot.conn, member.id)
        for ticket in tickets:
            channel_id = ticket[0]
            channel = member.guild.get_channel(channel_id)
            if channel:
                await channel.delete()
            await delete_ticket(self.bot.conn, channel_id)

async def setup(bot):
    await bot.add_cog(JoinLeave(bot))
