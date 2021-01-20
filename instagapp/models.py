from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField('email',unique=True)
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField()
    username=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    profile=models.ImageField()











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
