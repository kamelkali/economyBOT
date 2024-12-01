from django.contrib import admin
from django.urls import path

from economy.setup_economy import create_wallet
from .views import get_user_wallet, delete_wallet;

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wallet/<int:user_id>/', get_user_wallet),
    path("create-wallet/",create_wallet),
    path('delete-wallet/',delete_wallet)
]
