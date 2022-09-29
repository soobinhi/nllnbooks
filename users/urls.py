import imp
from django.urls import path
from .views import RegisterView, LoginView, UserListView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('list/',UserListView.as_view()),
]