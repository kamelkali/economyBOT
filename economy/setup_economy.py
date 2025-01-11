import discord
from django.core.exceptions import ObjectDoesNotExist
import requests

from client import tree, client
from backend.models import DiscordUsers
from asgiref.sync import sync_to_async


@sync_to_async
def create_wallet(interaction: discord.Interaction,user_id, discordName):
    user_exists = requests.get(f"http://127.0.0.1:8000/wallet/{user_id}")
    if user_exists.status_code == 404:
        user = DiscordUsers.objects.get_or_create(id=user_id, balance=1000,discord_name = discordName)
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
    user_discordName = interaction.user.name
    try:
        user_wallet = await create_wallet(interaction, user_id, user_discordName)
        print("CW: ", user_wallet)

        if user_wallet:
            await interaction.response.send_message(content="Created wallet! **Your start balance is 1000 :moneybag:**")

        else:
            await interaction.response.send_message(content="**You already have a wallet :octagonal_sign:**")

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
        tier = user.json()["tier"]
        balEmbed = discord.Embed(
            color=discord.Colour.green(),
            title="Your balance:",
            type="rich",
        )
        balEmbed.set_footer(text="saharaBOT your best economy bot! ⚱️")
        balEmbed.add_field(name="**Money stats**", value=f"Balance: {balance} $ \n Tier: {tier}",inline = True)
        member = interaction.user
        user_avatar = member.avatar.url
        balEmbed.set_author(name=member.name, icon_url=user_avatar)
        await interaction.response.send_message(embed=balEmbed)


@sync_to_async
def leaderboard_fun():
    response = requests.get("http://127.0.0.1:8000/leaderboard/")
    if response.status_code == 200:
        return response

@tree.command(
    name="leaderboard",
    description="Top 20 biggest wallets"
)
async def leaderboard(interaction: discord.Interaction):
    leaderboard = await leaderboard_fun()
    json_lb = leaderboard.json()


    lbEmbed = discord.Embed(color=discord.Color.blurple(), title="🏦 Top 20 biggest wallets:")
    lbEmbed.set_footer(text="saharaBOT your best economy bot! ⚱️")
    i = 0
    for user in json_lb:
        i+=1
        lbEmbed.add_field(name="Place",value=f"#{i}", inline=True)
        discord_name = user["discord_name"]
        lbEmbed.add_field(name="User",value=discord_name,inline=True)
        balance = user["balance"]
        lbEmbed.add_field(name="Balance",value=balance,inline=True)

    await interaction.response.send_message(embed=lbEmbed)
