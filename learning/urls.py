from django.urls import path
from . import views

urlpatterns = [
    path('', views.path_list, name='learning_paths'),
    path('<int:pk>/', views.path_detail, name='path_detail'),
    path('api/complete/<int:resource_id>/', views.complete_resource, name='complete_resource'),
]
