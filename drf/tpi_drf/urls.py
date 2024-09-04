from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('chats/', views.user_chat_list, name='chat_list'),
    path('chat/<uuid:chat_uuid>/', views.chat_detail, name='chat_detail'),
    path('staff/chats/', views.staff_chat_list, name='staff_chat_list'),
    path('staff/chat/<uuid:chat_uuid>/', views.staff_chat_detail, name='staff_chat_detail'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('chat/<uuid:chat_uuid>/close/', views.close_chat, name='close_chat'),
    path('update_status/<str:status>/', views.update_status, name='update_status'),
]
