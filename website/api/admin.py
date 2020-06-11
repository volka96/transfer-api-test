from django.contrib import admin

from .models import Currency, Wallet, Transfer

admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(Transfer)
