from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImovelViewSet

router = DefaultRouter()
router.register(r'', ImovelViewSet, basename='imovel')

urlpatterns = [
    path('', include(router.urls)),
]
