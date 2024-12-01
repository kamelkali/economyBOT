from sys import exec_prefix

from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from colorama import Fore
from django.core.exceptions import ObjectDoesNotExist

@api_view(["GET"])
def get_user_wallet(request, user_id)->Response:
    print(Fore.RED)
    try:
        user = discord_users.objects.get(id=user_id)
        serialized_user = Discord_user_serializers(user,context={'request': request})
        return Response(serialized_user.data)
    except ObjectDoesNotExist:
        print("GW: User wallet dont exist")
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(["POST"])
def create_wallet(request)->Response:
    serialized_user = Discord_user_serializers(request.data)
    if serialized_user.is_valid():
        serialized_user.save()
        return Response(serialized_user.data)
    else:
        return Response({'detail':'unable to create user'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def delete_wallet(request)->Response:
    id = request.data.get('id')
    user = discord_users.objects.get(id=id)
    if user is not None:
        user.delete()
        return Response({'detail':'user deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"detail": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )