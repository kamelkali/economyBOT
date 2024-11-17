import discord
import datetime
import os
import threading
import subprocess
from manage import main

import setup_economy
import work
import help

from dotenv import load_dotenv
from client import client, tree

load_dotenv()
token = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.messages = True

def run_bot():
    @client.event
    async def on_ready():
        try:
            await client.wait_until_ready()
            await tree.sync()
            print("Tree sync")

        except Exception as e:
            print(f"Error syncing tree: {e}")
        print('------------------------------')
        print('Launched bot!:')
        print("Bot name:", client.user.name)
        print("Bot ID:", client.user.id)
        print("Launched", datetime.datetime.now())
        print('------------------------------')
    client.run(token)


