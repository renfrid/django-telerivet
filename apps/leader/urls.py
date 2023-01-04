from django.urls import path
from . import views

app_name = 'leaders'

urlpatterns = [
    path('lists', views.LeaderListView.as_view(), name='lists'),
    # path('menu/<int:pk>/show', views.MenuDetailView.as_view(), name='menu-detail'),
    path('create', views.LeaderCreateView.as_view(), name='create'),

    # path('sub-menu/<str:menu_id>', views.get_sub_menu_lists, name='sub-menu'), 

    # path('menu-links', views.MenuLinkListView.as_view(), name='menu-links'),

    
]