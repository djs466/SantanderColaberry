from django.urls import path, re_path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', views.apiOverview, name = 'api-overview'),
    path('weather/', views.weatherRawData.as_view({'get': 'list'}), name='weather-raw'),
    re_path('weather/stats/', views.weatherStats.as_view({'get': 'list'}), name='weather-stats'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('weather/slowerUI/', views.weatherRawDataSimplified.as_view({'get': 'list'}), name='weather-raw-fast'),
]