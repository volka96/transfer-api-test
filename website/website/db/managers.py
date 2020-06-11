from django.db import models
from django.utils.timezone import now
from django.db.models.query import QuerySet


# From https://github.com/jazzband/django-model-utils/blob/master/model_utils/managers.py
class SoftDeletableQuerySetMixin(object):
    """
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``is_removed`` field to True.
    """

    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        self.update(is_removed=True)


class SoftDeletableQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    pass


class SoftDeletableManagerMixin(object):
    """
    Manager that limits the queryset by default to show only not removed
    instances of model.
    """
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(is_removed=False)


class SoftDeletableManager(SoftDeletableManagerMixin, models.Manager):
    pass


class TrackableSoftDeletableQuerySet(SoftDeletableQuerySet):

    def delete(self):
        self.update(removed_at=now())
        super().delete()


class TrackableSoftDeletableManager(SoftDeletableManager):

    _queryset_class = TrackableSoftDeletableQuerySet


class ActiveManager(models.Manager):

    def __init__(self, activity_fields=None, *args, **kwargs):
        if not activity_fields:
            activity_fields = ['is_active']
        self.activity_filter = {}
        for activity_field in activity_fields:
            self.activity_filter[activity_field] = True
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(**self.activity_filter)
