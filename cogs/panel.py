from discord.ext import commands
import json
import discord
from discord import app_commands
from helpers.ticketmaker import create_ticket_channel

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Send the ticket panel")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Ticket", description="Select the ticket to be created", color=discord.Color.blue())

        with open("config.json", "r") as f:
            config = json.load(f)

        panel_style = config["panel_style"]
        panel_catagories = config["categories"]
        view = discord.ui.View()

        if panel_style == "buttons":
            for key, category in panel_catagories.items():
                button = discord.ui.Button(
                    label=category["name"],
                    style=discord.ButtonStyle.primary,
                    custom_id=f"ticket_{key}")
                button.callback = self.button_callback
                view.add_item(button)
        elif panel_style == "dropdown":
            options = []
            for key, category in panel_catagories.items():
                options.append(discord.SelectOption(
                    label=category["name"],
                    value=key
                ))
            dropdown = discord.ui.Select(placeholder="Select a ticket type", options=options)
            dropdown.callback = self.dropdown_callback
            view.add_item(dropdown)

        await interaction.response.send_message(embed=embed, view=view)

    async def button_callback(self, interaction: discord.Interaction):
        key = interaction.data["custom_id"].replace("ticket_", "")
        await create_ticket_channel(interaction, key, self.bot.conn)

    async def dropdown_callback(self, interaction: discord.Interaction):
        key = interaction.data["values"][0]
        await create_ticket_channel(interaction, key, self.bot.conn)


async def setup(bot):
    await bot.add_cog(Panel(bot))