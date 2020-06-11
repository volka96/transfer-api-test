from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from website.db.models import TrackableUpdateCreateModel

User = get_user_model()


class Currency(models.Model):
    usd_ratio = models.PositiveIntegerField(_('USD ratio'), default=1)
    name = models.CharField(_('Currency short name'), max_length=3)


class Wallet(TrackableUpdateCreateModel):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='wallet',
                                on_delete=models.CASCADE, db_index=True)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), on_delete=models.SET_NULL, null=True)
    balance = models.PositiveIntegerField(_('Balance'), default=0)


class Transfer(TrackableUpdateCreateModel):
    user_from = models.ForeignKey(User,
                                  verbose_name=_('User from'),
                                  related_name='outgoing_transfers',
                                  related_query_name='outgoing_transfer',
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True)
    user_to = models.ForeignKey(User,
                                verbose_name=_('User to'),
                                related_name='incoming_transfers',
                                related_query_name='incoming_transfer',
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True)

    amount = models.PositiveIntegerField(_('Balance'), null=True, blank=False)
    currency = models.ForeignKey(Currency, verbose_name=_('Currency'), on_delete=models.SET_NULL, null=True)
