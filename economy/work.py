from datetime import datetime
from time import strptime

import discord
import requests
from IPython.core.release import author

from client import tree, client
import requests

@tree.command(
    name = "work",
    description="Earn money in legal way"
)
async def work(interaction: discord.Interaction):
    try:
        user_id = interaction.user.id
        user = requests.get(f"http://127.0.0.1:8000/wallet/{user_id}")
        if user.status_code == 404:
            await interaction.response.send_message(content="You need a wallet to start. To create one, use `/createwallet`.")
        elif user.status_code == 200:
            data = {"id": user_id}
            api_response = requests.post("http://127.0.0.1:8000/work/", data = data)
            print(api_response.status_code)
            response_data = api_response.json()
            if api_response.status_code == 200:
                description = response_data['description']
                print(description)
                balance = response_data['balance']
                work_embed = discord.Embed(
                    color = discord.Color.green(),
                    description = description + " **" + str(balance) + "$**",
                    type = "rich",
                )
                member = interaction.user
                user_avatar = member.avatar.url
                work_embed.set_footer(text="saharaBOT your best economy bot! ⚱️")
                work_embed.set_author(name = member.name, icon_url = user_avatar)
                await interaction.response.send_message(embed=work_embed)
            if api_response.status_code == 406:
                u_cooldown = response_data.get("cooldown")
                print(u_cooldown)
                ts_cooldown = datetime.strptime(u_cooldown, "%Y-%m-%dT%H:%M:%SZ");
                await interaction.response.send_message(content=f"Your cooldown will end <t:{int(ts_cooldown.timestamp())}:R>")
            elif api_response.status_code == 405:
                await interaction.response.send_message(content=f"**You are in jail!** ⛔ For more info type `/jail` ")
    except Exception as e:
        print("Discord error: " + str(e))