from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('create/', views.create_group, name='create_group'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/join/', views.join_group, name='join_group'),
    path('<int:pk>/complete/<int:day_num>/', views.complete_day, name='complete_day'),
]
