import discord
from client import tree
import client
import asyncio

intents = discord.Intents.all()
intents.messages = True


def MainEmbed(interaction: discord.Interaction):
    HelpEmbed = discord.Embed(
        color=discord.Colour.green(),
        title="",
        type="rich",
        description="",
    )
    HelpEmbed.set_footer(text="backend ❇️ your best economy bot!")
    HelpEmbed.set_author(name=client.user.name, icon_url=f"https://discord.com/users/{client.user.id}")
    return interaction.response.send_message(embed=HelpEmbed)


@tree.command(
    name="help",
    description="List of bot commands",
)
async def help(interaction: discord.Interaction):
    await MainEmbed(interaction)
