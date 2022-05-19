from django.contrib import admin

from .models import Repository, ViewRepository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(ViewRepository)
class ViewRepositoryAdmin(admin.ModelAdmin):
    list_display = ('id',)
