
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wallet/<int:user_id>/', get_user_wallet),
    path("create-wallet/",create_wallet),
    path('work/',work),
    path('leaderboard/', leaderboard),
    path('pay/',pay),
    path('transaction/<int:payer_id>/',get_transaction),
    path('shop/',shop_items)
]
