from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('create/', views.create_note, name='create_note'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
]
