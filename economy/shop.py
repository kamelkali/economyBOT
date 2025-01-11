import discord
from aiohttp.web_response import json_response
from django.core.exceptions import ObjectDoesNotExist
import requests
from scripts.regsetup import description

from client import tree, client
from backend.models import DiscordUsers
from asgiref.sync import sync_to_async

@tree.command(
    name="shop-list",
    description="Displays items in shop"
)
async def shop_list(interaction: discord.Interaction):
    wallet_id = interaction.user.id
    data = {"id": wallet_id}
    response = requests.get("http://127.0.0.1:8000/shop/", params=data)

    shopEmbed = discord.Embed(
        color=discord.Colour.blue(),
        title="Items in shop :",
        type="rich",
    )
    shopEmbed.set_footer(text="saharaBOT your best economy bot! ⚱️")

    try:
        if response.status_code == 200:
            json_response = response.json()
            for item in json_response:
                name = item["name"]
                shopEmbed.add_field(name="Item Name:", value=f"**{name}**", inline=True)

                cost = item['cost']
                shopEmbed.add_field(name="Cost:", value=f"**{cost} $**", inline=True)

                desc = item["description"]
                shopEmbed.add_field(name="Destcription:", value=f"{desc} ", inline=True)
            await interaction.response.send_message(embed=shopEmbed)

    except Exception as e:
        await interaction.response.send_message(content=f"A error occured: {response.json()}, Exception: {e}")