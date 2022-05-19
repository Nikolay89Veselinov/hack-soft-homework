from django.db import models
from uuid import uuid4


class User(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    token = models.CharField(max_length=200, unique=True, default=uuid4)

    def __str__(self):
        return self.email