from django.urls import path, re_path, include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
routers.register('get-routes', views.RouteViewSet, basename="get-routes")
routers.register('get-trips', views.TripViewSet, basename="get-trips")
routers.register('get-drivers', views.DriverViewSet, basename="get-drivers")
routers.register('get-customers', views.CustomerViewSet, basename="get-customers")
routers.register('get-sellers', views.TicketSellerViewSet, basename="get-sellers")
routers.register('get-ticket', views.TicketViewSet, basename="get-ticket")
routers.register('users', views.UserViewSet, basename="users")
routers.register('get-users', views.GetUserViewSet, basename='get-users')
routers.register('get-users-token', views.GetUserByToken, basename='get-users-token')
routers.register('upd-users', views.UpdateUserViewSet, basename='upd-users')
# routers.register('add-trips', views.AddTripViewSet, basename='add-trips')
urlpatterns = [
    path('', include(routers.urls))
]
