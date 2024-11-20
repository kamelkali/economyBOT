import discord
import django

from colorama import Fore
from django.core.exceptions import ObjectDoesNotExist

from client import tree, client
from backend.models import discord_users
from asgiref.sync import sync_to_async

@sync_to_async
def ifWalletCreated(user_id):
    print(Fore.WHITE + "[DEBUG ONLY] " + "User ID:", user_id)
    print(Fore.RED)
    try:
        user = discord_users.objects.get(id=user_id)
        print(user)
        print("User exists")
        print("USER ID:", user)
        return user
    except ObjectDoesNotExist:
        print("User dont exist")
        return False

@sync_to_async
def create_wallet(interaction: discord.Interaction,user_id):
    print(Fore.WHITE + "[DEBUG ONLY] " + "User ID:", user_id)
    if not ifWalletCreated(user_id):
        return False
    else:
        user = discord_users(id=user_id, balance=1000)
        discord_users.save(user)
        return True
@sync_to_async
def delete_wallet(interaction: discord.Interaction,user_id):
    print(Fore.WHITE + "[DEBUG ONLY] " + "User ID:", user_id)
    if ifWalletCreated(user_id):
        return False
    else:
        user = discord_users(id=user_id)
        discord_users.delete(user)
        print("Deleted user with id: ",user_id)
        return True


@tree.command(
    name="bal",
    description="Check your balance"
)
async def bal(interaction: discord.Interaction):
    user_id = interaction.user.id
    print(Fore.WHITE + "[DEBUG ONLY]  " + "User ID:", user_id)
    user = await ifWalletCreated(user_id)
    print(user)
    if user is not None:
        balance = user.balance
        balEmbed = discord.Embed(
            color=discord.Colour.green(),
            title="Your balance:",
            description=f"**Money: {balance}\n**To check your crypto wallet type `/cbal`",
            type="rich",
        )
        balEmbed.set_footer(text="saharaBOT your best economy bot! ⚱️")
        await interaction.response.send_message(embed=balEmbed)
    else:
        await interaction.response.send_message(content="You don't have a wallet! To create one, use `/createwallet`.")


@tree.command(
    name="createwallet",
    description="Create a wallet to start making big money"
)
async def createwallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_exists = await ifWalletCreated(user_id)
    if user_exists:
        await interaction.response.send_message(content="Created wallet! **Your start balance is 1000 :moneybag:**")

    else:
        await interaction.response.send_message(content="**You already have a wallet :octagonal_sign:**")


@tree.command(
    name="deletewallet",
    description="Delete a wallet. Yeah, I also don’t know why someone would do that."
)
async def deletewallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    print(Fore.WHITE + "[DEBUG ONLY] " + "User ID:", user_id)
    user_exists = await  ifWalletCreated(user_id)
    if not user_exists:
        await interaction.response.send_message(content="**You don’t have a wallet :octagonal_sign:**")
    else:
        await interaction.response.send_message(content="Successfully deleted your wallet!")

@tree.command(
    name="checkuser",
    description="debug shit",
)
async def checkuser(interaction: discord.Interaction, member: discord.User):
    user_id = member.id
    user_exists = await  ifWalletCreated(user_id)
    if user_exists:
        await interaction.response.send_message(content=f"User exists, User balance: {user_exists.balance}")
    else:
        await interaction.response.send_message(content="User doesn't exits")