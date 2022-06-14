from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from users.models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        return CustomUser.objects.filter(user=self.request.user)