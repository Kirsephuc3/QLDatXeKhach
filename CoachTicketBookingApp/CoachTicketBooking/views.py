from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .perms import *
from .serializers import *
from .pagination import TripPagnigation
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FileUploadParser
from . import dao
from drf_yasg import openapi


# Create your views here.


class RouteViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializers


class TripViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers
    pagination_class = TripPagnigation

    def filter_queryset(self, queryset):
        return dao.load_trip(self.request.query_params)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('depart', openapi.IN_QUERY, description="Lọc theo điểm khởi hành",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('dest', openapi.IN_QUERY, description="Lọc theo điểm đến",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('departure_date', openapi.IN_QUERY, description="Lọc theo ngày khởi hành",
                          type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DriverViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers


class CustomerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class TicketSellerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TicketSeller.objects.all()
    serializer_class = TicketsSellerSerializers

    def filter_queryset(self, queryset):
        return dao.load_seller(self.request.query_params)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('depart', openapi.IN_QUERY, description="Lọc theo điểm khởi hành",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('dest', openapi.IN_QUERY, description="Lọc theo điểm đến",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('departure_date', openapi.IN_QUERY, description="Lọc theo ngày khởi hành",
                          type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializers


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser, ]

    def get_queryset(self):
        queries = self.queryset
        name = self.request.query_params.get('name')

        if name:
            names = name.split()
            for name in names:
                queries = queries.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        return queries

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(UserSerializers(request.user).data, status=status.HTTP_200_OK)


class GetUserViewSet(viewsets.ReadOnlyModelViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def filter_queryset(self, queryset):
        return dao.load_user(self.request.query_params)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY, description="Lọc theo tên",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('username', openapi.IN_QUERY, description="Lọc theo username",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('role', openapi.IN_QUERY, description="Lọc theo role  ",
                          type=openapi.TYPE_STRING),
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UpdateUserViewSet(viewsets.GenericViewSet, generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]


class GetUserByToken(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({'data': serializer.data},
                        status=status.HTTP_200_OK)


# class AddTripViewSet(viewsets.ViewSet, generics.CreateAPIView):
#     queryset = Trip.objects.all()
#     serializer_class = AddTripSerializers
#
#     def create(self, request, *args, **kwargs):
#         route = request.data.get('route')
#         departure_date = request.data.get('departure_date')
#
#         if route and departure_date:
#             duplicate_entry = Trip.objects.filter(route=route, departure_date=departure_date).exists()
#             if duplicate_entry:
#                 return Response({'error': 'Đã tồn tại bản ghi với Route và Departure date này'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         # Gọi phương thức create của lớp cơ sở
#         return super().create(request, *args, **kwargs)
