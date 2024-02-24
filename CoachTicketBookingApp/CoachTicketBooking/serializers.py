from .models import *
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar', 'email', 'image_url', 'role', 'phone',
                  'date_of_birth', 'gender', 'address']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_image_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user



class RouteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'create_date', 'depart', 'dest']
        # fields = '__all__'


class TicketPriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = TicketPrice
        fields = ['price']


class TripSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    route = RouteSerializers()
    price = TicketPriceSerializers()
    seat_numbers_list = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ['id', 'route', 'departure_date', 'start_time', 'end_time', 'driver', 'pickup_location',
                  'dropoff_location', 'price', 'image_url', 'seat_numbers_list']
        # fields = '__all__'

    def get_image_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    def get_seat_numbers_list(self, obj):
        if hasattr(obj, 'seat_numbers'):
            return obj.seat_numbers
        return []


class DriverSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Driver
        fields = ['id', 'license_number', 'user']
        # fields = '__all__'


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'seat_number', 'trip']


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TicketsSellerSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    ticket = TicketSerializers()

    class Meta:
        model = TicketSeller
        fields = ['id', 'license_number', 'user', 'ticket']
