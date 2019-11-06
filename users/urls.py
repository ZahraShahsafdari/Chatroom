from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('list', views.user_list),
    path('login', views.login_view)
]