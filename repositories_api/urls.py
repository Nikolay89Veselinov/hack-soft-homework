from django.urls import path

from .views import ReposotoryListApiView, ReposotoryDeleteApiView,\
                ReposotoryCreateApiView, ReposotoryDetailApiView, UserCreateApiView


urlpatterns = [
    path('repos/', ReposotoryListApiView.as_view(), name='repository_list'),
    path('repos/<int:pk>/delete/', ReposotoryDeleteApiView.as_view(), name='repository_delete'),
    path('repos/create/', ReposotoryCreateApiView.as_view(), name='repository_create'),
    path('repos/<int:pk>/', ReposotoryDetailApiView.as_view(), name='repository_detail'),
    path('users/create/', UserCreateApiView.as_view(), name='user_create'),
]