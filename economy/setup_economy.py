import discord

import traceback

from django.core.exceptions import ObjectDoesNotExist
import requests
from urllib3 import request

from client import tree
from backend.models import discord_users
from asgiref.sync import sync_to_async


@sync_to_async
def create_wallet(interaction: discord.Interaction,user_id):
    user_exists = requests.get(f"http://127.0.0.1:8000/wallet/{user_id}")
    print("CW_S:", user_exists, "request type ", type(user_exists))
    if user_exists.status_code == 404:
        user = discord_users.objects.get_or_create(id=user_id, balance=1000)
        print("Created user wallet: ", user)
        return True

    else:
        print("User already have a wallet!")
        return False


@tree.command(
    name="createwallet",
    description="Create a wallet to start making big money"
)
async def createwallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    try:
        user_wallet = await create_wallet(interaction, user_id)
        print("CW: ", user_wallet)

        if user_wallet:
            await interaction.response.send_message(content="Created wallet! **Your start balance is 1000 :moneybag:**")

        else:
            await interaction.response.send_message(content="**You already have a wallet :octagonal_sign:**")

    except Exception as e:
        print("discord.py sucks")




@sync_to_async
def delete_wallet(interaction: discord.Interaction,user_id):
    try:
        user = requests.get(f"http://127.0.0.1:8000/wallet/{user_id}")
        print("CW_S:", user, "request type ", type(user))
        if user.status_code == 404:
            print("DW: User dont have a wallet")
            return False
        else:
            print(user)
            obj = {"id": user_id}
            response = requests.post(f"http://127.0.0.1:8000/delete-wallet/",json=obj)
            if response.status_code == 200:
                return True
            else:
                return False
            print("DW: Deleted user wallet with id: ",user_id)
        return True
    except ObjectDoesNotExist:
        return False

@tree.command(
    name="deletewallet",
    description="Delete a wallet. Yeah, I also don’t know why someone would do that."
)
async def deletewallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    try:
        user_wallet = await delete_wallet(interaction, user_id)
        if user_wallet:
            await interaction.response.send_message(content="Successfully deleted your wallet!")
        else:
            await interaction.response.send_message(content="**You don’t have a wallet :octagonal_sign:**")
    except Exception as e:
        print("discord.py sucks")

@sync_to_async
def bal_fun(user_id):
    try:
        user = requests.get(f"http://127.0.0.1:8000/wallet/{user_id}")
        print(user)
        print(user.json())
        if user.status_code == 404:
            print("BL: User don`t have a wallet")
            return False
        elif user.status_code == 200:
            return user

    except ObjectDoesNotExist:
        print("BL: Wallet does not exist")
        return False


@tree.command(
    name="bal",
    description="Check your balance"
)
async def bal(interaction: discord.Interaction):
    user_id = interaction.user.id
    user = await bal_fun(user_id)
    print("BL: ",user)
    if user is False:
        await interaction.response.send_message(content="You don't have a wallet! To create one, use `/createwallet`.")
    else:
        balance = user.json()["balance"]
        balEmbed = discord.Embed(
            color=discord.Colour.green(),
            title="Your balance:",
            description=f"**Money: {balance}\n**To check your crypto wallet type `/cbal`",
            type="rich",
        )
        balEmbed.set_footer(text="saharaBOT your best economy bot! ⚱️")
        await interaction.response.send_message(embed=balEmbed)
