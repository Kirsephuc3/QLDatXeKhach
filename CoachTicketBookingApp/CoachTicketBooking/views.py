from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from .serializers import *
from .pagination import *
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser


# Create your views here.


class RouteViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializers


class TripViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers
    pagination_class = TripPagnigation

    def list(self, request, *args, **kwargs):
        return Response(TripSerializers(self.queryset, context={"request": request}, many=True).data,
                        status=status.HTTP_200_OK)


class DriverViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers


class CustomerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class TicketSellerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TicketSeller.objects.all()
    serializer_class = TicketsSellerSerializers


class TicketViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializers


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser, ]
