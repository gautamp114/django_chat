from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('id_for_chatId/',views.ajaxify, name="ajaxify"),
    path('<str:room_name>/', views.room, name='room'),
]
