from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from drf_yasg import openapi

from rest_framework.routers import DefaultRouter

from .views import (
    CodeViewSet,
    UserRegisterAPIView,
    ReferalByIdAPIView,
    CustomTokenObtainView,
    ReferalCodeAPIView,
    ReferalByMail
)

schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('auth/register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('auth/get-token/', CustomTokenObtainView.as_view(), name='get-token'),
    path('referals/<int:pk>/', ReferalByIdAPIView.as_view(), name='referals'),
    path('referal-code/', ReferalCodeAPIView.as_view(), name='referal-code'),
    path('referal-mail/', ReferalByMail.as_view(), name='referal-mail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

]
