from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from Instaproject.settings import MEDIA_ROOT
from .managers import CustomManager
import os

# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField('email',unique=True)
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField()
    username=models.CharField(max_length=100,unique=True)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    superuser=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    profile=models.ImageField(upload_to='profile/',default=os.path.join(MEDIA_ROOT,'sample.jpg'))
    status=models.CharField(max_length=20,default="Public")

    objects=CustomManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name','email','age']

    def __str__(self):
        return self.email


    def get_full_name(self):
        name="{},{}".format(self.first_name,self.last_name)
        return name
    
    def get_email(self):
        return "{}".format(self.email)

    @property
    def is_active(self):
        return self.active
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_superuser(self):
        return self.superuser


class Posts(models.Model):
    img = models.ImageField()
    caption = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')

    class Meta:
        db_table = 'Posts'


class FollowerInfo(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followed_on=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20)

    class Meta:
        unique_together = [['follower', 'following']]
        db_table = 'FollowerInfo'


class Likes(models.Model):
    like = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    postliked = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='likes')
    liked_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['like', 'postliked']]
        db_table = 'Likes'


class Commemts(models.Model):
    userid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    postid = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    commented_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        db_table = 'Tag'


class PostTag(models.Model):
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='post_tag')
    tagid = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='post_tag')

    class Meta:
        unique_together = [['post', 'tagid']]
        db_table = 'PostTag'
