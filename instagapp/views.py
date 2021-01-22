from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework.generics import GenericAPIView,CreateAPIView,ListAPIView
from rest_framework.permissions import AllowAny,BasePermission
from rest_framework.authentication import TokenAuthentication
from .permission import CustomUserPermission
# Create your views here.


class RegUser(CreateAPIView,ListAPIView,GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[CustomUserPermission,]
    
    



