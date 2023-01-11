from django.urls import path
from . import views

app_name = 'citizens'

urlpatterns = [
    path('lists', views.CitizenListView.as_view(), name='lists'),
    path('<int:pk>/show', views.CitizenDetailView.as_view(), name='show'),
    path('create', views.CitizenCreateView.as_view(), name='create'),
    path('<int:pk>/edit', views.CitizenUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.CitizenDeleteView.as_view(), name='delete'),

    
]