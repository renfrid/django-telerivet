from django.urls import path
from . import views

app_name = 'setup'

urlpatterns = [
    path('menu', views.MenuListView.as_view(), name='menu'),
    path('menu/<int:pk>/detail', views.MenuDetailView.as_view(), name='detail-menu'),
    path('menu/create', views.MenuCreateView.as_view(), name='create-menu'),
    path('menu/<int:pk>/edit', views.MenuUpdateView.as_view(), name='edit-menu'),
    path('menu/<int:pk>/delete', views.MenuDeleteView.as_view(), name='delete-menu'),

    path('menu/<int:pk>/delete-sub', views.SubMenuDeleteView.as_view(), name='delete-sub-menu'),

    #menu and sub menu
    path('menu-lists/<str:keyword_id>', views.get_menu_lists, name='menu-lists'), 
    path('sub-menu-lists/<str:menu_id>', views.get_sub_menu_lists, name='sub-menu-lists'), 
    

    #menu links
    path('menu-links', views.MenuLinkListView.as_view(), name='menu-links'),
    path('menu-links/<int:pk>/delete', views.MenuLinkDeleteView.as_view(), name='delete-menu-link'),

    
]