from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat),
    path('message/new', views.add_message),
    path('<int:conversation_id>', views.chat)

]