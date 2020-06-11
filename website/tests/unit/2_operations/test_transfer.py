import pytest
from django.test import RequestFactory
from rest_framework import status
from api.views import RegistrationView, TransferView, LoginView
from api.models import User, Wallet, Transfer, Currency


registration_view = RegistrationView.as_view()
transfer_view = TransferView.as_view()
login_view = LoginView.as_view()


# @pytest.mark.django_db
# def test_registrationView_validEmail_successResponse():
#     currency = Currency(usd_ratio=1, name='usd')
#     currency.save()
#
#     register_data_1 = {
#         "email": 'test_registration_attempt1@mail.ru',
#         "password": "qazwsxedc123",
#         "currency": "usd",
#         "balance": 100,
#     }
#
#     register_data_2 = {
#         "email": 'test_registration_attempt2@mail.ru',
#         "password": "qazwsxedc123",
#         "currency": "usd",
#         "balance": 100,
#     }
#
#     register_url = 'http://http://0.0.0.0:8000/api/register/'
#
#     request = RequestFactory().post(register_url, register_data_1)
#     response = registration_view(request)
#
#     request = RequestFactory().post(register_url, register_data_2)
#     response = registration_view(request)
#
#     login_url = 'http://http://0.0.0.0:8000/api/login/'
#
#     request = RequestFactory().post(login_url, register_data_1)
#     response = login_view(request)
#     token = response.json()['token']
#
#     data = {
#         "user_from": '1',
#         "user_to": "2",
#         "amount": 50,
#     }
#
#     transfer_url = 'http://http://0.0.0.0:8000/api/transfer/'
#     headers = {"Authorization": "Bearer {0}".format(token)}
#
#     request = RequestFactory().post(transfer_url, data, headers)
#     response = transfer_view(request)
#
#     assert response.status_code == status.HTTP_200_OK
