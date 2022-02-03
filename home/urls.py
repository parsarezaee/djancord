from unicodedata import name
from django.urls import path
from . import views 

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.CreateRoom.as_view(), name='create-room'),
    path('update-room/<str:pk>', views.UpdateRoom.as_view(), name='update-room'),
    path('delete-room/<str:pk>', views.DeleteRoom.as_view(), name='delete-room') 

]
