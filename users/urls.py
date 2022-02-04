from django.urls import path
from . import views

urlpatterns = [
    # path('', views.get_users, name='users'),
    path('', views.UserListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
    # path('', views.LoginUserView.as_view(), name='login'),
    # path('', views.logout_user, name='logout'),
]
