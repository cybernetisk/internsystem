from django.db import models

class RåvareManager(models.Manager):
    def get_query_set(self):
        return super(RåvareManager, self).get_query_set().select_related('innkjopskonto')
