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
def delete_wallet(request)->Response:
    try:
        user_id = request.data.get('id')
        user = DiscordUsers.objects.get(id=user_id)
        user.delete()
        return Response({'detail':'user deleted successfully'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def work(request)->Response:
    try:
        user_id:int = request.data.get('id')
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
        print("Request data:", request.data)
        payer_id:int = request.data.get('payer_id')
        payee_id:int = request.data.get('payee_id')

        payer = DiscordUsers.objects.get(id=payer_id)
        payee = DiscordUsers.objects.get(id=payee_id)
        balance = request.data.get('balance')


        if payee == payer:
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

