from django.urls import path
from . import views

urlpatterns = [
    path('', views.getresults,name='getresults'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
]
