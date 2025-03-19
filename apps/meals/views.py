from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import MealSerializer, RatingSerializer
from .models import Meal, Rating
from .permissions import ObjectOwnerPermission
from customers.models import CustomUser
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
    
    @action(detail=True, methods=['post','put'])
    def rate_meal(self, request, uuid=None, ):
        if 'stars' in request.data:
            meal = Meal.objects.get(uuid=uuid)
            username = request.data['username']
            stars = request.data['stars']
            user = CustomUser.objects.get(username=username)
            try:
                rating = Rating.objects.get(user=user.id, meal=meal.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                return Response({'message': 'meal rate updated successfully', 'result': serializer.data}, status=status.HTTP_200_OK)
            except:
                   rating = Rating.objects.create(user=user, meal=meal, stars=request.data)
                   serializer = RatingSerializer(rating)
                   return Response({'message': 'rate created','result': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'stars not provided'},status=status.HTTP_400_BAD_REQUEST)

    

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

