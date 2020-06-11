from django.conf.urls import url
from knox import views as knox_views
from .apps import ApiConfig

from .views import LoginView, RegistrationView, TransferView

app_name = ApiConfig.name

urlpatterns = [
    # auth API (DFR knox + my own)
    # https://github.com/James1345/django-rest-knox

    url(r'login/', LoginView.as_view()),
    url(r'logout/', knox_views.LogoutView.as_view()),
    url(r'logoutall/', knox_views.LogoutAllView.as_view()),

    # Registration
    url(r'register/', RegistrationView.as_view()),

    url(r'transfers/', TransferView.as_view()),
]
