from django.urls import path
from . import views

urlpatterns = [
    path('', views.LabelListView.as_view(), name='labels'),
    path('create/', views.LabelCreateView.as_view(), name='create_label'),
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='update_label'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='delete_label'),
]
