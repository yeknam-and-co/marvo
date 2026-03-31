import discord
from helpers.db import delete_ticket
import asyncio

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete Ticket", style=discord.ButtonStyle.danger, custom_id="delete_ticket")
    async def delete_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Deleting ticket...", ephemeral=True)
        await asyncio.sleep(1)
        
        await delete_ticket(interaction.client.conn, interaction.channel.id)
        await interaction.channel.delete()
