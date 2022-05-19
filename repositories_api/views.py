from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from repositories.models import Repository
from .serializers import RepositorySerializer, UserSerializer
from users.models import User


class ReposotoryListApiView(generics.ListAPIView):

    def list(self, request):
        user = User.objects.get(token=request.headers['X-API-Token'])
        repos = Repository.objects.filter(user=user)
        serializer = RepositorySerializer(repos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReposotoryDeleteApiView(generics.DestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        if user.token == request.headers['X-API-Token']:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReposotoryCreateApiView(generics.CreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(token=request.headers['X-API-Token'])
        Repository.objects.filter(url=request.data['url']).update(user=user)
        content = {
            'token': request.headers['X-API-Token'],
        }
        return Response(content, status=status.HTTP_200_OK)


class ReposotoryDetailApiView(APIView):

    def get(self, request, pk):
        repository = get_object_or_404(Repository, pk=pk)
        serializer_class = RepositorySerializer(repository)
        view_repository = repository.viewrepository_set.first()
        return Response({
            'data': serializer_class.data,
            'view': view_repository.the_json
        })


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])
        content = {
            'token': request.headers['X-API-Token'],
        }
        return Response(content, status=status.HTTP_200_OK)
