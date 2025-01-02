from django.contrib import admin

from .models import DiscordUsers, Work, Transaction

admin.site.register(DiscordUsers)
admin.site.register(Work)
admin.site.register(Transaction)