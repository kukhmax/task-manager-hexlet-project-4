from django.urls import path

from .views import (
    HomePageView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    LoginUserView,
    LogoutUserView,
) 

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]