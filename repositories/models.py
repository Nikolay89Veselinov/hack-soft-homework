from datetime import datetime

from django.db import models
from jsonfield import JSONField

from users.models import User


class Repository(models.Model):
    url = models.URLField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        verbose_name = 'Repository'
        verbose_name_plural = 'Repositories'

    def __str__(self):
        return self.url


class ViewRepository(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    the_json = JSONField()
