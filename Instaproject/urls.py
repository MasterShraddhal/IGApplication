"""Instaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from instagapp.views import RegUser,RetrieveUser,CustomAuthToken,FollowUsers,Unfollowuser,ListFollowingUsers,ListFollowersInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createuser/',RegUser.as_view()),
    path('getsingle/<int:pk>/',RetrieveUser.as_view()),
    path('createtoken/',CustomAuthToken.as_view()),
    path('followuser/',FollowUsers.as_view()),
    path('unfollowuser/<int:pk>/',Unfollowuser.as_view()),
    path('listfollowingusers/',ListFollowingUsers.as_view()),
    path('listfollowersusers/',ListFollowersInfo.as_view()),
]
