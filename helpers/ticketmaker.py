import json
import discord
from helpers.db import create_ticket
from helpers.close import TicketView

async def create_ticket_channel(interaction: discord.Interaction, key: str, conn):
    try: 
        with open("config.json", "r") as f:
            config = json.load(f)

        categories = config["categories"]
        category = categories[key]
        guild = interaction.guild
        staff_role = guild.get_role(int(config["staffroleid"]))
        if not staff_role:
            await interaction.response.send_message("Staff role was not found, please use the correct role id in config.json", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
        }

        channel = await guild.create_text_channel(name=f"{key}-{interaction.user.name} - Ticket", overwrites=overwrites)
        await channel.send(category["welcome_message"], view=TicketView())
        
        await interaction.response.send_message(f"Ticket created: {channel.mention}")
        await create_ticket(conn, channel.id, interaction.user.id)
        
    except discord.Forbidden:
        await interaction.response.send_message("please check my permissions and try again.", ephemeral=True)
    except Exception as e:
        print(f"Error creating ticket: {e}")
        await interaction.response.send_message("unexpected error, please try again.", ephemeral=True)
