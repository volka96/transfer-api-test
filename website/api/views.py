from django.contrib.auth import login, get_user_model
from django.contrib.auth.signals import user_logged_in
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Transfer
from .serializers import RegisterSerializer, WalletSerializer, LoginSerializer, TransferSerializer
from .utils import generate_token
from .renderers import APIRenderer
from .models import Currency

User = get_user_model()


def _user_to_json(user: User) -> dict:
    return {
        'id': user.id,
        'email': user.email,
    }


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [APIRenderer]

    def post(self, request: Request):
        data = request.POST.copy()
        data['username'] = data['email']

        user_serializer = RegisterSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()
        currency = Currency.objects.get(name=data['currency'].lower())
        if not currency:
            Response({
                'Error': 'This currency is not supported',
            })

        data['user'] = user.pk
        data['currency'] = currency.pk

        wallet_serializer = WalletSerializer(data=data)
        wallet_serializer.is_valid(raise_exception=True)
        wallet = wallet_serializer.save()

        user.wallet = wallet
        user.save()

        return Response({
            'user': _user_to_json(user),
        })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [APIRenderer]

    def post(self, request: Request, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)

        data = generate_token(user)
        data.update({
            'user': _user_to_json(user),
        })
        return Response(data)


class TransferView(APIView):
    renderer_classes = [APIRenderer]

    def post(self, request: Request, **kwargs):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request: Request, **kwargs):
        user = request.user
        transfers = Transfer.objects.filter(user_from=user).values()
        return Response({
            'transfers': transfers,
        })
