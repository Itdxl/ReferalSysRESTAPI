from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.db import IntegrityError


from .serializers import (
    ReferalCodeSerializer,
    UserSerializer,
    ReferalHistorySerializer
)
from .models import ReferalCode, ReferalHistory, User

from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterAPIView(APIView):
    """ Регистрация и проверка реферального кода, создание записи в истории реф.кодов."""
    def post(self, request):
        referal_code = request.data.get('referal_code')
        if referal_code:
            try:
                referal = ReferalCode.objects.get(name=referal_code)
                ref_creator = referal.owner
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    ReferalHistory.objects.create(ref_creator=ref_creator, ref_user=user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ReferalCode.DoesNotExist:
                return Response({'error': 'Invalid referal code'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainView(APIView):
    """Получение токена"""
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

        return Response({'detail': 'Unable to log in with provided credentials.'}, status=status.HTTP_400_BAD_REQUEST)


class CodeViewSet(ModelViewSet):
    queryset = ReferalCode.objects.all()
    serializer_class = ReferalCodeSerializer


class ReferalByIdAPIView(generics.ListAPIView):
    """Получение информация о рефералах по id реферера"""
    serializer_class = ReferalHistorySerializer

    def get_queryset(self):
        referer_id = self.kwargs['pk']
        return ReferalHistory.objects.filter(ref_creator_id=referer_id)


class ReferalCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """Получние, создание, удаление кода для аутентифицированного пользователя."""
    def get(self, request):
        referal_code = ReferalCode.objects.filter(owner=request.user).first()
        serializer = ReferalCodeSerializer(referal_code)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = ReferalCodeSerializer(data=request.data)
            if serializer.is_valid():
                referal_code = serializer.save(owner=request.user)
                return Response(ReferalCodeSerializer(referal_code).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Делаем текстовый респонс на ошибку UNIQUE constraint failed
        except IntegrityError:
            return Response({'error': 'You already have a referal code'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        referal_code = ReferalCode.objects.filter(owner=request.user).first()
        if referal_code:
            referal_code.delete()
            return Response({'response': 'Referal code deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Referal code does not exist'}, status=status.HTTP_404_NOT_FOUND)


class ReferalByMail(APIView):
    def get(self, request):
            email = request.data.get('email')
            try:
                user = User.objects.get(email=email)
                referal_code = ReferalCode.objects.get(owner=user)
                serializer = ReferalCodeSerializer(referal_code)
                return Response(serializer.data)
            except ReferalCode.DoesNotExist:
                return Response({'error': 'This user has no referal code'}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({'error': 'User with this email not found'}, status=status.HTTP_404_NOT_FOUND)

