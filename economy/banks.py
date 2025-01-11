import discord
from django.core.exceptions import ObjectDoesNotExist
import requests

from client import tree, client
from backend.models import DiscordUsers
from asgiref.sync import sync_to_async

