from django.urls import path, include
from .views import *
from .charts import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  
    path('ward-chart', WardChartView.as_view()), 
]