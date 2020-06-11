from api.models import Wallet, Transfer

try:
    from hmac import compare_digest
except ImportError:
    def compare_digest(a, b):
        return a == b


from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


def get_email_field(validators=None):
    return serializers.EmailField(
        required=True,
        validators=validators,
        error_messages={
            'invalid': _('Указан некорректный e-mail.'),
            'blank': _('Email не может быть пустым.'),
            'required': _('Значение должно быть указано.'),
        }
    )


def get_password_field():
    return serializers.CharField(
        min_length=6,
        max_length=100,
        write_only=True,
        required=True,
        trim_whitespace=False,
        error_messages={
            'invalid': _('Значение не корректно.'),
            'blank': _('Пароль не может быть пустым.'),
            'required': _('Значение должно быть указано.'),
            'max_length': _('Пароль должен содержать менее {max_length} символов.'),
            'min_length': _('Пароль должен содержать как минимум {min_length} символов.'),
        }
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = get_email_field(validators=[UniqueValidator(queryset=User.objects.all(),
                                                        message='Введенный email уже используется.')])

    password = get_password_field()

    def create(self, validated_data: dict) -> User:
        user = User(email=validated_data['email'], username=validated_data['email'], is_active=True)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password')


class WalletSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict) -> Wallet:
        wallet = Wallet(user=validated_data['user'], currency=validated_data['currency'],
                        balance=int(validated_data['balance']))
        wallet.save()
        return wallet

    class Meta:
        model = Wallet
        fields = ('user', 'currency', 'balance')


class LoginSerializer(serializers.Serializer):
    email = get_email_field()
    password = get_password_field()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get('email')).first()
        if not user:
            raise serializers.ValidationError(detail={
                'email': True,
                'password': True,
                'common': 'Введенная пара email-пароль не найдена!'
            })

        username = user.username
        password = attrs['password']
        user = authenticate(request=self.context.get('request'),
                            username=username,
                            password=password)

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            raise serializers.ValidationError(detail={
                'email': True,
                'password': True,
                'common': 'Введенная пара email-пароль не найдена!'
            })

        attrs['user'] = user
        return attrs


class TransferSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        wallet = attrs['user_from'].wallet
        if attrs['amount'] > wallet.balance:
            raise serializers.ValidationError(detail={
                'wallet': 'Недостаточно средств!'
            })

        return attrs

    def create(self, validated_data: dict) -> Transfer:
        user_from = validated_data['user_from']
        user_to = validated_data['user_to']

        wallet_from = user_from.wallet
        wallet_to = user_to.wallet
        amount = validated_data['amount']

        wallet_from.balance = wallet_from.balance - amount

        currency_from = wallet_from.currency
        currency_to = wallet_to.currency

        if currency_from != currency_to:
            amount = amount * 100 * currency_from.usd_ratio / 100 * currency_to.usd_ratio

        wallet_to.balance = wallet_to.balance + amount

        wallet_from.save()
        wallet_to.save()

        transfer = Transfer(user_from=validated_data['user_from'], user_to=validated_data['user_to'],
                            amount=int(validated_data['amount']), currency=currency_from)
        transfer.save()
        return transfer

    class Meta:
        model = Transfer
        fields = ('user_from', 'user_to', 'amount')
