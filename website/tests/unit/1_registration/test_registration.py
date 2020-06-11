import pytest
from django.test import RequestFactory
from rest_framework import status
from api.views import RegistrationView
from api.models import User, Wallet, Transfer, Currency


registration_view = RegistrationView.as_view()


@pytest.mark.django_db
def test_registrationView_validEmail_successResponse():
    currency = Currency(usd_ratio=1, name='usd')
    currency.save()
    data = {
        "email": 'test_registration_attempt@mail.ru',
        "password": "qazwsxedc123",
        "currency": "usd",
        "balance": 100,
    }
    register_url = 'http://0.0.0.0:8000/api/register/'

    request = RequestFactory().post(register_url, data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['user']['email'] == data['email']

    user = User.objects.filter(email=data['email']).first()
    assert user
    assert user.wallet

    assert user.wallet.balance == data['balance']

    request = RequestFactory().post(register_url, data)
    response = registration_view(request)

    assert response.status_code != status.HTTP_200_OK

    data = {
        "email": 'test_registration_attempt2@mail.ru',
        "password": "qazwsxedc123",
        "currency": "USD",
        "balance": 100
    }

    request = RequestFactory().post(register_url, data)
    response = registration_view(request)

    assert response.status_code == status.HTTP_200_OK
