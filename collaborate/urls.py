from django.urls import path
from . import views

urlpatterns = [
    path('', views.collaborate_home, name='collaborate_home'),
    path('room/<int:group_id>/', views.room_view, name='collaborate_room'),
    path('api/messages/<int:room_id>/', views.get_messages, name='get_messages'),
    path('api/send/<int:room_id>/', views.send_message, name='send_message'),
    path('api/video/toggle/<int:room_id>/', views.toggle_video, name='toggle_video'),
    path('api/screen/toggle/<int:room_id>/', views.toggle_screen, name='toggle_screen'),
]
