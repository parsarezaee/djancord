from unicodedata import name
from django.urls import path
from . import views 

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.SignupView, name='signup'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.CreateRoom, name='create-room'),
    path('update-room/<str:pk>', views.UpdateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.DeleteRoom, name='delete-room') 

]
