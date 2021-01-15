from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pet import views


router = DefaultRouter()
router.register('pets', views.PetViewSet)

app_name = 'pet'

urlpatterns = [
    path('', include(router.urls)),
]
