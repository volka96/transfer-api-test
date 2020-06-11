from django.contrib import admin

from .models import Wallet, Transfer, Currency

admin.site.register(Wallet)
admin.site.register(Currency)
admin.site.register(Transfer)
