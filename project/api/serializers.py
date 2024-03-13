from rest_framework.serializers import ModelSerializer, ValidationError

from .models import ReferalCode, ReferalHistory, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # Не возвращаем шифр пароля
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ReferalCodeSerializer(ModelSerializer):
    class Meta:
        model = ReferalCode
        fields = ['name', 'expiration_date']


class ReferalHistorySerializer(ModelSerializer):
    class Meta:
        model = ReferalHistory
        fields = ('id', 'ref_creator', 'ref_user', 'created_at')
