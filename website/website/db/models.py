from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from .managers import SoftDeletableManager, TrackableSoftDeletableManager

User = get_user_model()


class TrackableUpdateCreateModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class OwnerModel(models.Model):

    owner = models.ForeignKey(User, related_name='%(class)s_owner', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OwnersModel(models.Model):

    owners = models.ManyToManyField(User,
                                    verbose_name='Owners',
                                    blank=True,
                                    related_name='%(class)s_owners')

    class Meta:
        abstract = True


# From https://github.com/jazzband/django-model-utils/blob/master/model_utils/models.py
class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a ``is_removed`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-removed entries.
    """
    is_removed = models.BooleanField(default=False, blank=True, db_index=True)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
            print('DELETE', self.is_removed)
        else:
            return super(SoftDeletableModel, self).delete(using=using, *args, **kwargs)


class TrackableSoftDeletableModel(SoftDeletableModel):

    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = TrackableSoftDeletableManager()

    def delete(self, *args, **kwargs):
        soft = kwargs.get('soft', True)
        if soft:
            self.removed_at = now()
        return super(TrackableSoftDeletableModel, self).delete(*args, **kwargs)


class SoftTrackableModel(TrackableUpdateCreateModel, TrackableSoftDeletableModel):

    class Meta:
        abstract = True


class SoftTrackableOwnerModel(OwnerModel, TrackableUpdateCreateModel, TrackableSoftDeletableModel):

    class Meta:
        abstract = True
