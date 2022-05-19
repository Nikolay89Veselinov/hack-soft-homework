import json
import requests
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from repositories.models import Repository, ViewRepository
from users.models import User


class Command(BaseCommand):
    help = 'Update repositories view'

    def handle(self, *args, **options):
      repositories = Repository.objects.all()
      for repository in repositories:
        user = repository.user
        headers={'Content-Type':'application/json', 'Authorization':f'Token {user.token}'}
        response = requests.get(f'{repository.url}/traffic/views', headers=headers)
        if response.status_code == 200:
          view = ViewRepository.objects.filter(repository=repository)
          if view.count() == 1:
            view.update(repository=repository, the_json=response.content)
          else:
            ViewRepository.objects.create(repository=repository, the_json=response.content)