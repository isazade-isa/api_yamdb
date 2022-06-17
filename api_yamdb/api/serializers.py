from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Don't create user with username 'me'")
        return data

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = CustomUser
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}


class TokenSerializer(serializers.Serializer):
    username =  serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
