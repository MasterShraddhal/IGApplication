from django.shortcuts import render
from .serializers import UserSerializer, UpdateUserSerializer, FollowerSerializer, ListFollowingSerializers,ListFollowersSerializers
from .models import User, FollowerInfo
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permission import CustomUserPermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
# Create your views here.


class ListFollowingUsers(ListAPIView, GenericAPIView):
    serializer_class = ListFollowingSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        param=self.request.query_params
        user = self.request.user
        id=param.get('id',None)
        if id==None:
            qs = FollowerInfo.objects.filter(follower_id=user)
        else:
            if int(id)==user.id:
                qs = FollowerInfo.objects.filter(follower_id=user)
            else:
                fobjs=FollowerInfo.objects.filter(following_id=int(id)).filter(follower_id=user.id).filter(status="Accepted").first()
                if fobjs:
                    qs=FollowerInfo.objects.filter(follower_id=int(id)).filter(status="Accepted")
                else:
                    raise Exception("you do not have permission to access data of this user!!!")
        return qs

class ListFollowersInfo(ListAPIView,GenericAPIView):
    serializer_class=ListFollowersSerializers
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        param=self.request.query_params
        user=self.request.user
        status=param.get('status',None)
        id=param.get('id',None)
        if id==None:
            if status!=None:
                qs=FollowerInfo.objects.filter(following_id=user.id).filter(status=status)
            elif status==None:
                qs=FollowerInfo.objects.filter(following_id=user.id)
        else:
            if int(id)==user.id:
                qs=FollowerInfo.objects.filter(following_id=user.id)
            else:
                uobj=FollowerInfo.objects.filter(following_id=int(id)).filter(follower_id=user.id).filter(status="Accepted").first()
                if uobj:
                    qs=FollowerInfo.objects.filter(following_id=int(id)).filter(status="Accepted")
                else:
                    raise Exception("you do not have permission to access data of this user!!!")
        return qs


class FollowUsers(CreateAPIView, GenericAPIView):
    queryset = FollowerInfo.objects.all()
    serializer_class = FollowerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Unfollowuser(DestroyAPIView, RetrieveAPIView, GenericAPIView):
    queryset = FollowerInfo.objects.all()
    serializer_class = FollowerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        data = instance.__dict__
        fid = data['follower_id']
        if self.request.user.id == fid:
            instance.delete()
        else:
            raise Exception("User not authorized to perform this action")


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        print(created)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RegUser(CreateAPIView, ListAPIView, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomUserPermission, ]


class RetrieveUser(DestroyAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView):
    queryset = User.objects.all()
    # serializer_class=UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomUserPermission]

    def retrieve(self,request,*args,**kwargs):
        user=self.get_object()
        followers=user.following.count()
        followings=user.followers.count()
        ser_class=self.get_serializer_class()
        ser_data=ser_class(user)
        data=ser_data.data
        data['followers']=followers
        data['followings']=followings
        return Response(data=data)
        

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return UpdateUserSerializer
        else:
            return UserSerializer
