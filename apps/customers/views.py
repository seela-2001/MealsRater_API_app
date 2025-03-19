from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import UserSerializer
from .models import CustomUser
from .permissions import UserPermission
# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        if self.action == 'list':
            return [IsAdminUser()]
        if self.action == 'update':
            return [UserPermission()]
        if self.action == 'destroy':
            return [IsAdminUser(), UserPermission()]
        return super().get_permissions()
