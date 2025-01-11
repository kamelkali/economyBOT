from PyQt5.pylupdate import merge
from django.template.defaultfilters import random
from rest_framework import status
from rest_framework.response import Response

from .notHttpFunctions import get_cooldown_date
from .serializers import *
from rest_framework.decorators import api_view
from colorama import Fore
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.utils import timezone

def check_user_in_jail(request,user_id):
    try:
        jail_user = Jail.objects.get(id=user_id)
        return True
    except ObjectDoesNotExist:
        return False

@api_view(["GET"])
def get_user_wallet(request, user_id)->Response:
    print(Fore.RED)
    try:
        user = DiscordUsers.objects.get(id=user_id)
        serialized_user = DiscordUsersSerialisers(user, context={'request': request})
        return Response(serialized_user.data)
    except ObjectDoesNotExist:
        print("GW: User wallet dont exist")
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(["POST"])
def create_wallet(request)->Response:
    serialized_user = DiscordUsersSerialisers(request.data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data)
    else:
        return Response({'detail':'unable to create user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def work(request)->Response:
    try:
        user_id:int = request.data.get('id')
        in_jail = check_user_in_jail(request,user_id)
        if in_jail:
            return Response({'detail':'user in jail'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = DiscordUsers.objects.get(id=user_id)
        print(user)
        query = Work.objects.raw(
            "SELECT * FROM backend_work  ORDER BY random() LIMIT 1"
        )
        random_event = query[0]
        current_date = timezone.now()
        print(current_date)
        if current_date < user.work_cooldown:
            return  Response(
                {'detail':'cooldown did not pass','cooldown':user.work_cooldown},
                status = status.HTTP_406_NOT_ACCEPTABLE
            )
        user.work_cooldown = get_cooldown_date()
        user.balance+= random_event.balance
        user.save()
        serialized_event = WorkSerializer(random_event, context={'request': request})
        return Response(serialized_event.data)

    except ObjectDoesNotExist:
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def leaderboard(request) -> Response:
    query = DiscordUsers.objects.all().order_by('-balance')[:10]
    serializedLeaderBoard = DiscordUsersSerialisers(query, many=True, context={'request': request})
    return Response(serializedLeaderBoard.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def pay(request) -> Response:
    try:
        payer_id:int = request.data.get('payer_id')
        in_jail = check_user_in_jail(request, payer_id)
        if in_jail:
            return Response({'detail': 'payer in jail'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        payee_id:int = request.data.get('payee_id')

        payer = DiscordUsers.objects.get(id=payer_id)
        payee = DiscordUsers.objects.get(id=payee_id)
        balance = request.data.get('balance')


        if payee == payer or balance <= 0:
            return Response({'detail':'bruh.'},status=status.HTTP_409_CONFLICT)

        if payer.balance < balance:
            return Response({'detail:'"Payer dont have that money !"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        payer.balance -= balance
        payee.balance += balance

        payer.save()
        payee.save()

        return Response({'detail':'payer paid successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'detail':'user dont have a wallet!'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail':f"Something wrong. Error: {e}"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_transaction(request, payer_id) -> Response:
    try:

        transactions = Transaction.objects.all().filter(payer_id=payer_id).order_by('-date')[:5]
        serialized_transactions = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serialized_transactions.data, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'detail':'transaction dont exist'},status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def shop_items(request) -> Response:
    item_list = RegularShopItem.objects.all()
    serialized_items = RegularItemsSerializer(item_list, many=True, context={'request': request}).data
    merged_items = []
    try:
        wallet_id = request.query_params.get('id')

        wallet = DiscordUsers.objects.get(id=wallet_id)
        wallet_tier = wallet.tier

        if wallet_tier == "IV" or not wallet_id:
            return Response(serialized_items, status=status.HTTP_200_OK)

        item_tier = str(wallet_tier) + "I"

        tier_item = TierShopItem.objects.get(tier=item_tier)

        serialized_tier = TierItemsSerializer(tier_item, many=False, context={'request': request}).data

        merged_items = serialized_items + [serialized_tier]

        if not merged_items:
            return Response(serialized_items, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'ERROR: detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except TierShopItem.DoesNotExist:
        return Response({'error': 'Tier item not found'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(merged_items, status=status.HTTP_200_OK)
