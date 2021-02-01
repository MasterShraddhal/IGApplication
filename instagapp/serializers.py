from .models import *
from rest_framework.serializers import ModelSerializer,ValidationError

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name','username','password','age','profile']
        read_only_fields = ['id','status'] 
        write_only_fields = ['password'] 

    def create(self,validated_data):
        user_obj=User.objects.create_user(**validated_data)
        return user_obj


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','username','profile','status']


class ListFollowingSerializers(ModelSerializer):
    following=UserSerializer()
    class Meta:
        model=FollowerInfo
        fields=['id','following_id','following']



class FollowerSerializer(ModelSerializer):
    class Meta:
        model=FollowerInfo
        fields=['following','status','id']
        read_only_fields = ['status','id'] 

    def create(self,validated_data):
        print(validated_data)
        Following=validated_data['following']
        user=validated_data['user']
        if Following.id==user.id:
            raise ValidationError("Cannot follow yourself")
        else:
            if Following.status=="Public":
                fobj=FollowerInfo(follower=user,following=Following,status="Accepted")
                fobj.save()
            else:
                fobj=FollowerInfo(follower=user,following=Following,status="Pending")
                fobj.save()
        return fobj


