from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_route, name='add_route'),

    path('airport/', views.add_airport, name='add_airport'),

    path('nth/', views.nth_node_view, name='nth_node'),

    path('longest/', views.longest_route_view, name='longest_route'),

    path('shortest/', views.shortest_path_view, name='shortest_path'),
]
