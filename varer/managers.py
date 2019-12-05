from django.db import models


class RåvareManager(models.Manager):
    def get_queryset(self):
        return super(RåvareManager, self).get_queryset().select_related("innkjopskonto")
