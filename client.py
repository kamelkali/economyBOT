import discord
from discord.ext import tasks, commands

intents = discord.Intents.all()
intents.messages = True

client = commands.Bot(
    intents=intents,
    command_prefix="/",
    allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, replied_user=False)

)
tree = client.tree
