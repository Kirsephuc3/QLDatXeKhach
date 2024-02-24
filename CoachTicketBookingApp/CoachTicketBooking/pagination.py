from rest_framework.pagination import PageNumberPagination


class TripPagnigation(PageNumberPagination):
    page_size = 2