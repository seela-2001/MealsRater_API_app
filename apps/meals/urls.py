from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'meals'

router = DefaultRouter()
router.register(r'meals',MealViewSet,basename='meal')
router.register(r'ratings',RatingViewSet,basename='rating')

urlpatterns = [
    path('',include(router.urls)),
]
