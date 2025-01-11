from django.contrib import admin

from .models import DiscordUsers, Work, Transaction, RegularShopItem, TierShopItem

admin.site.register(DiscordUsers)
admin.site.register(Work)
admin.site.register(Transaction)
admin.site.register(RegularShopItem)
admin.site.register(TierShopItem)