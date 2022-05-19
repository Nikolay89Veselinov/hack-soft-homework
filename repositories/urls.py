from django.urls import path

from .views import repo_detail, repos_list

app_name = 'repos'

urlpatterns = [
    path('users/<str:user_token>/repos/', repos_list, name='repos_list'),
    path('users/<user_token>/repos/<repository_id>/', repo_detail, name='repo_detail'),
]