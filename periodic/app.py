#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sanic import Sanic
import sys
import os
import requests
import asyncio

import django

RD = '/var/www/project/website'

HOST = '0.0.0.0'
PORT = 8017

sys.path.append(RD)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
print(sys.path)

from django.conf import settings

settings.configure()
django.setup()

from api.models import Currency

app = Sanic()


async def update_prices():
    currencies = Currency.objects.all()
    response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
    if response.status_code == 200:
        data = response.json()['rates']
        for currency in currencies:
            ratio = data.get(currency.name.upper(), None)
            if ratio:
                currency.usd_ratio = ratio
                currency.save()
    else:
        print('Got non 200 status code ', response.status_code)

    await asyncio.sleep(3 * 60)


app.add_task(update_prices)

app.run(host=HOST, port=PORT, debug=True, workers=1)

