import discord
import requests

from datetime import datetime
from backend.models import Transaction
from asgiref.sync import sync_to_async
from client import tree, client

@sync_to_async
def fun_pay(payer_id, payee_id, balance):
    data = {
        "payer_id": payer_id,
        "payee_id": payee_id,
        "balance": balance,
     }
    response = requests.post(f"http://127.0.0.1:8000/pay/", json=data)
    transaction = Transaction.objects.create(payer_id=payer_id, payee_id=payee_id, balance=balance)
    print("Responce:", response)
    return response.status_code

@tree.command(
    name = "pay",
    description="Pay money to someone!"
)
async def pay(interaction: discord.Interaction, member: discord.Member,balance: float):
    payee_id = member.id
    payer_id = interaction.user.id
    pay_response = await fun_pay(payer_id, payee_id,balance)

    if pay_response == 406:
        await interaction.response.send_message(content="**You don't have enought money !**")
    elif pay_response == 404:
        await interaction.response.send_message(content=f"**User don't have wallet !** To create one use `/create-wallet`")
    elif pay_response == 400:
        await interaction.response.send_message(content=f"A Error has occured !")
    elif pay_response == 200:
        await interaction.response.send_message(content=f"*Sucessfully paid !*")
    elif pay_response == 409:
        await interaction.response.send_message(content="bruh.")
    elif pay_response == 405:
        await interaction.response.send_message(content=f"**You are in jail!** ⛔ For more info type `/jail` ")



@sync_to_async
def get_transaction(payer_id):
    request = requests.get(f"http://127.0.0.1:8000/transaction/{payer_id}/")
    if request.status_code != 200:
        return False
    return request.json()

@tree.command(
    name="transactions",
    description="Check your transactions"
)
async def transactions(interaction: discord.Interaction):
        payer_id = interaction.user.id
        transactions = await get_transaction(payer_id)
        if transactions is False:
            await interaction.response.send_message(content="Couldn't get transactions")
            return
        lbTrans = discord.Embed(color=discord.Color.fuchsia(), title="Your transactions: ")
        member = interaction.user
        user_avatar = member.avatar.url
        lbTrans.set_footer(text="saharaBOT your best economy bot! ⚱️")
        lbTrans.set_author(name=member.name, icon_url=user_avatar)
        for user in transactions:

            payee_id = user["payee_id"]
            lbTrans.add_field(name="User:", value=f"<@{payee_id}>", inline=True)

            date = user['date']
            date_strp = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            lbTrans.add_field(name="Date:", value=f"<t:{int(date_strp.timestamp())}:R>", inline=True)

            balance = user["balance"]
            lbTrans.add_field(name="Balance:", value=f"**{balance} $**", inline=True)

        lbTrans.add_field(name=" ", value="This show only 5 last transactions. To see more visit our site !", inline=False)
        await interaction.response.send_message(embed=lbTrans)
