import discord
from client import tree

accounts = set()
bal = set()

async def ifWalletCreated(interaction: discord.Interaction, user_id):
    return user_id in accounts


@tree.command(
    name="bal",
    description="Check your balance"
)
async def bal(interaction: discord.Interaction):
    user_id = interaction.user.id
    if await ifWalletCreated(interaction, user_id):
        balEmbed = discord.Embed(
            color=discord.Colour.green(),
            title="Your balance:",
            description="Money:\nTo check your crypto wallet type `/cball`",
            type="rich",
        )
        balEmbed.set_footer(text="backend ❇️ your best economy bot!")
        await interaction.response.send_message(embed=balEmbed)
    else:
        await interaction.response.send_message(content="You don't have a wallet! To create one, use `/createwallet`.")


@tree.command(
    name="createwallet",
    description="Create a wallet to start making big money"
)
async def createwallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    if await ifWalletCreated(interaction, user_id):
        await interaction.response.send_message(content="**You already have a wallet 🛑**")
    else:
        accounts.add(user_id)
        await interaction.response.send_message(content="Created wallet! **Your start balance is 1000 💰**")


@tree.command(
    name="deletewallet",
    description="Delete a wallet. Yeah, I also don’t know why someone would do that."
)
async def deletewallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    if await ifWalletCreated(interaction, user_id):
        accounts.discard(user_id)
        await interaction.response.send_message(content="Successfully deleted your wallet!")
    else:
        await interaction.response.send_message(content="**You don’t have a wallet 🛑**")
