from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from rest_framework.views import APIView
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from .serializers import UserSerializer, TokenSerializer


class ConfirmationCode(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        try:
            send_mail(
                'Confirmation code',
                'code: ' + default_token_generator.make_token(user=user),
                'yamdb.local',
                [user.email]
            )
        except BadHeaderError:
            Response(
                {'error': 'failed to send message.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class Token(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, username=serializer.validated_data.get('username'))
        if default_token_generator.check_token(user, serializer.validated_data.get('confirmation_code')):
            token = RefreshToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=True, permission_classes=[IsAuthenticated], methods=['get', 'patch'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

