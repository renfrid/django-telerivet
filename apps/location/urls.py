from django.urls import path
from .views import get_districts, get_wards, get_villages, get_neighborhood

app_name = 'location'

urlpatterns = [
    path('get_districts/<str:region_id>', get_districts, name='get_districts'), 
    path('get_wards/<str:district_id>', get_wards, name='get_wards'), 
    path('get_villages/<str:ward_id>', get_villages, name='get_villages'), 
    path('get_neighborhood/<str:village_id>', get_neighborhood, name='get_neighborhood'), 
]