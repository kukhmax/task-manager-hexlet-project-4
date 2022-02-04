from django.urls import path, include
from home.views import index
from users.views import LoginUserView, logout_user

urlpatterns = [
    path('', index, name='index'),
    path('users/', include('users.urls')),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
