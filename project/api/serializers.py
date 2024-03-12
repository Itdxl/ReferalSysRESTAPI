from rest_framework.serializers import ModelSerializer

from .models import ReferalCode, ReferalHistory, CustomUser


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'referal_code']  # Включите ваши поля, которые вы хотите сериализовать
        extra_kwargs = {
            'password': {'write_only': False},  # Пароль должен возвращаться в ответе
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ReferralCodeSerializer(ModelSerializer):
    class Meta:
        model = ReferalCode
        fields = '__all__'


class ReferralSerializer(ModelSerializer):
    class Meta:
        model = ReferalHistory
        fields = '__all__'