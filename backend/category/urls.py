from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list_categories'),
    path('upload/', views.upload_categories, name='upload_categories'),
]
