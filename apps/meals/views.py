from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import MealSerializer, RatingSerializer
from .models import Meal, Rating
from .permissions import ObjectOwnerPermission
# Create your views here.

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', "description"]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        elif self.action == 'list':
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [ObjectOwnerPermission()]
        return super().get_permissions()

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'list':
            return [AllowAny()]
        elif self.action in ['update', 'destroy']:
            return [ObjectOwnerPermission()]
        return super().get_permissions()

