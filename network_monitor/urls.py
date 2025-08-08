# network_monitor/urls.py
from django.urls import path
from . import views

app_name = 'network_monitor'

urlpatterns = [
    # Main page
    path('', views.index, name='index'),

    # API endpoints
    path('api/ping/', views.ping_host_api, name='ping_api'),
    path('api/hosts/', views.get_monitored_hosts_api, name='get_hosts_api'),
    path('api/add_target/', views.add_monitor_target_api, name='add_target_api'),
    path('api/update_frequency/', views.update_ping_frequency_api, name='update_frequency_api'),
    path('api/delete_target/', views.delete_monitor_target_api, name='delete_target_api'),
    path('host/<int:host_id>/', views.host_detail_view_api, name='host_detail'),
    path('api/delete_host_data/', views.delete_host_data_api, name='api_delete_host_data'),
    path('api/update_status/', views.update_status_api, name='api_update_host_data'),
]