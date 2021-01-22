from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quate import views


router = DefaultRouter()
router.register('quates', views.QuateViewSet)

app_name = 'quate'

urlpatterns = [
    path('', include(router.urls)),
]
