from django.urls import path
from . import views

app_name = 'citizen'

urlpatterns = [
    path('lists', views.CitizenListView.as_view(), name='lists'),
    # path('menu/<int:pk>/show', views.MenuDetailView.as_view(), name='menu-detail'),
    # path('menu/create', views.MenuCreateView.as_view(), name='create-menu'),

    # path('sub-menu/<str:menu_id>', views.get_sub_menu_lists, name='sub-menu'), 

    # path('menu-links', views.MenuLinkListView.as_view(), name='menu-links'),

    
]