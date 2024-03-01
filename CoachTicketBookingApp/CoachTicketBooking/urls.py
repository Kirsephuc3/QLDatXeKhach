from django.urls import path, include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
routers.register('routes', views.RouteViewSet, basename="routes")
routers.register('trips', views.TripViewSet, basename="trips")
routers.register('drivers', views.DriverViewSet, basename="drivers")
routers.register('customers', views.CustomerViewSet, basename="customers")
routers.register('sellers', views.TicketSellerViewSet, basename="sellers")
routers.register('ticket', views.TicketViewSet, basename="ticket")
routers.register('users', views.UserViewSet, basename="users")
routers.register('get-users-token', views.GetUserByToken, basename='get-users-token')
routers.register('feedbacks', views.FeedbacksViewSet, basename='feedbacks')
urlpatterns = [
    path('', include(routers.urls))
]
