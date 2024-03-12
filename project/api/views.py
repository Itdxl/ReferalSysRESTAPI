from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .serializers import ReferralCodeSerializer, CustomUserSerializer
from .models import ReferalCode, ReferalHistory, CustomUser

from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterAPIView(APIView):
    def post(self, request):
        referal_code = request.data.get('referal_code')
        data = request.data.copy()
        if referal_code:
            try:
                referrer = CustomUser.objects.get(referal_code=referal_code)
                data['referrer'] = referrer.id
            except CustomUser.DoesNotExist:
                pass
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # Создание JWT токена
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            # Добавление JWT токена к ответу
            response_data = serializer.data
            response_data.update(tokens)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeViewSet(ModelViewSet):
    queryset = ReferalCode.objects.all()
    serializer_class = ReferralCodeSerializer
