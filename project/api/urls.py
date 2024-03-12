from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CodeViewSet, UserRegisterAPIView

router_v1 = DefaultRouter()


router_v1.register(r'codes', CodeViewSet, basename='codes')
# router_v1.register(r'payments', PaymentViewSet, basename='payments')
# # router_v1.register(r'investors', PaymentViewSet, basename='payments')


urlpatterns = [
    path('', include((router_v1.urls))),
    path('auth/register/', UserRegisterAPIView.as_view(), name='user-register'),

]
