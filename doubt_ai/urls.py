from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='doubt_ai_chat'),
    path('ask/', views.ask_ai, name='ask_ai'),
    path('clear/', views.clear_history, name='clear_doubt_history'),
]
