import json
from base64 import decode

import discord
import django

from asgiref.sync import sync_to_async
from colorama import Fore
from django.core.exceptions import ObjectDoesNotExist
from client import tree, client
from backend.models import discord_users
from asgiref.sync import sync_to_async
from economy.setup_economy import getUserWallet


workJson = json.load(open('./economy/work.json'))




@tree.command(
    name = "work",
    description="debug"
)
async def work(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_exists = await getUserWallet(user_id)
    print(user_exists)