from django.urls import path
from  . import views


urlpatterns = [

    path('Login/',views.loginPage, name='Login'),
    path('Logout/',views.LogoutUser, name='Logout'),
    path('register/', views.RegisterPage, name='register'),

    path('', views.home, name='home'), 
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteROOM, name='delete-room'),

    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),


    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    

]