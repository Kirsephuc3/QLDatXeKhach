from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from .perms import IsSeller, IsAdmin, IsCustomer, OwnerAuthenticated, IsDriver
from .serializers import DriverSerializers, TripSerializers, RouteSerializers, CustomerSerializers, UserSerializers, \
    AddTripSerializers, TicketSerializers, TicketsSellerSerializers, FeedbackSerializer, DriverForTripSerializers, \
    TicketsSellerDetailsSerializers
from .pagination import TripPagnigation
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser
from . import dao
from drf_yasg import openapi
from .models import Trip, Ticket, TicketSeller, Route, Customer, User, Driver, Feedback


# Create your views here.


class RouteViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView,
                   generics.DestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializers

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsSeller() and IsAdmin()]

        return [permissions.AllowAny()]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Route đã được tạo thành công '}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            route = self.get_object()
            serializer = self.serializer_class(route, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Route cập nhật thành công'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Route.DoesNotExist:
            return Response({'message': 'Route khum tìm thây'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            route = self.get_object()
            route.delete()
            return Response({'message': 'Route xóa thành công'}, status=status.HTTP_204_NO_CONTENT)
        except Route.DoesNotExist:
            return Response({'message': 'Route  khum tìm thây'}, status=status.HTTP_404_NOT_FOUND)


class TripViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers
    pagination_class = TripPagnigation
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['add_feedback']:
            return [IsCustomer()]
        if self.action in ['update']:
            return [IsAdmin()]

        return [permissions.AllowAny()]

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

    @action(methods=['POST'], detail=False, url_path='add_trip')
    def add_trip(self, request):
        try:
            with transaction.atomic():
                route = request.data.get('route')
                departure_date = request.data.get('departure_date')
                start_time = request.data.get('start_time')
                end_time = request.data.get('end_time')
                driver = request.data.get('driver')
                pickup_location = request.data.get('pickup_location')
                dropoff_location = request.data.get('dropoff_location')
                avatar = request.data.get('avatar')
                price = request.data.get('price')

                if route and departure_date:
                    duplicate_entry = Trip.objects.filter(route=route, departure_date=departure_date).exists()
                    if duplicate_entry:
                        return Response({'error': 'Đã tồn tại bản ghi với Route và Departure date này'},
                                        status=status.HTTP_400_BAD_REQUEST)

                    trip = Trip.objects.create(
                        route=route,
                        departure_date=departure_date,
                        start_time=start_time,
                        end_time=end_time,
                        driver=driver,
                        pickup_location=pickup_location,
                        dropoff_location=dropoff_location,
                        avatar=avatar,
                        price=price
                    )

                    serializer = AddTripSerializers(trip)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response({'error': 'Route và Departure date là bắt buộc'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = str(e)
            return Response({'error_message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], url_path='feedbacks', detail=True)
    def add_feedback(self, request, pk):
        trip = self.get_object()
        user = request.user
        content = request.data.get('content')
        rating = request.data.get('rating')
        if user is None:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        customer_instance, _ = Customer.objects.get_or_create(user=user)
        feedback = Feedback.objects.create(customer=customer_instance, trip=trip, content=content, rating=rating)
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FeedbacksViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permissions_class = [OwnerAuthenticated]


class DriverViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers

    def get_permissions(self):
        if self.action in ['trip_info']:
            return [IsDriver()]
        if self.action in ['update']:
            return [IsAdmin()]

        return [permissions.AllowAny()]

    @action(methods=['GET'], detail=True, url_path='trip_info')
    def trip_info(self, request, pk=None):
        try:
            # Đảm bảo chỉ tài xế hiện tại mới có thể xem trip của mình
            driver = self.get_object()
            if self.request.user.driver != driver:
                return Response({'message': 'Bạn không có quyền xem thông tin chuyến đi của tài xế này.'},
                                status=status.HTTP_403_FORBIDDEN)

            # Lấy danh sách các chuyến đi của tài xế
            trips = driver.trips.all()
            serializer = DriverForTripSerializers(trips, many=True)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response({'message': 'Tài xế không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers

    def get_permissions(self):
        if self.action in ['delete']:
            return [IsCustomer()]
        if self.action in ['update']:
            return [IsAdmin()]

        return [permissions.AllowAny()]

    @action(methods=['DELETE'], detail=True)
    def cancel_ticket(self, request, pk=None):
        try:
            customer = self.get_object()
            if customer.user == request.user:  # Kiểm tra xem user có phải là chủ nhân của vé không
                ticket = customer.ticket_info
                if ticket:  # Nếu khách hàng có vé
                    ticket.status = True
                    ticket.save()
                    return Response({'message': 'Vé được hủy thành công.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Không có vé nào thuộc về khách hàng.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Bạn không có quyền truy cập hủy vé.'},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True)
    def update_ticket(self, request, pk=None):
        try:
            customer = self.get_object()
            if customer.user == request.user:
                ticket_data = request.data.get('ticket_info')
                ticket = customer.ticket_info
                if ticket:
                    serializer = TicketSerializers(ticket, data=ticket_data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Không có vé nào thuộc khách hàng.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Bạn không có quyền truy cập.'},
                                status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TicketSellerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = TicketSeller.objects.all()
    serializer_class = TicketsSellerSerializers

    def get_permissions(self):
        if self.action in ['update_status']:
            return [IsSeller()]

        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='status', detail=True)
    def update_status(self, request, pk=None):
        try:
            ticket_seller = self.get_object()
            ticket = ticket_seller.ticket

            ticket.status = not ticket.status
            ticket.save()

            return Response(TicketsSellerDetailsSerializers(ticket_seller, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        except TicketSeller.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TicketViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializers

    def get_permissions(self):
        if self.action in ['add_ticket']:
            return [IsCustomer()]

        return [permissions.AllowAny()]

    @action(detail=False, methods=['POST'])
    def add_ticket(self, request):
        seat_number = request.data.get('seat_number')
        trip_id = request.data.get('trip')

        ticket = Ticket.objects.create(seat_number=seat_number, trip_id=trip_id)

        serializer = TicketSerializers(ticket)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveUpdateAPIView):
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
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update']:
            return [IsAdmin()]

        return [permissions.AllowAny()]

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
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(UserSerializers(request.user).data, status=status.HTTP_200_OK)


class GetUserByToken(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({'data': serializer.data},
                        status=status.HTTP_200_OK)
