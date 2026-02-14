from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('history/', views.test_history, name='test_history'),
    path('generate/<int:group_id>/', views.generate_test, name='generate_test'),
    path('take/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('result/<int:exam_id>/', views.exam_result, name='exam_result'),
]
